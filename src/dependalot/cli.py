"""dependalot command-line interface."""

from __future__ import annotations

import re
import sys
from collections import Counter
from contextlib import contextmanager
from typing import Annotated

import typer
from rich.console import Console
from rich.markup import escape
from rich.prompt import Confirm, Prompt

from dependalot.actions import MergeRefused, approve_and_merge
from dependalot.browser import open_url
from dependalot.config import DEFAULT_METHOD, MERGE_METHODS, ConfigError, load_settings
from dependalot.github import GitHubClient, GitHubError
from dependalot.models import DependabotPR, evaluate
from dependalot.render import pr_table, show_pr

app = typer.Typer(
    help="Triage, approve and merge Dependabot PRs across a GitHub organization.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()
err_console = Console(stderr=True)

OrgOpt = Annotated[str, typer.Option("--org", envvar="DEPENDALOT_ORG", help="GitHub organization.")]
RepoOpt = Annotated[
    str | None, typer.Option("--repo", "-r", help="Limit to one repository in the org.")
]
MethodOpt = Annotated[
    str,
    typer.Option("--method", "-m", help=f"Merge method: {', '.join(MERGE_METHODS)}."),
]
PrArg = Annotated[
    str, typer.Argument(help="PR as REPO#N, OWNER/REPO#N, or a GitHub PR URL.", metavar="PR")
]

_URL_RE = re.compile(r"github\.com/(?P<owner>[^/]+)/(?P<name>[^/]+)/pull/(?P<number>\d+)")
_REF_RE = re.compile(r"^(?:(?P<owner>[\w.-]+)/)?(?P<name>[\w.-]+)#(?P<number>\d+)$")


class UsageError(Exception):
    pass


def parse_pr_ref(ref: str, default_owner: str) -> tuple[str, str, int]:
    m = _URL_RE.search(ref) or _REF_RE.match(ref.strip())
    if not m:
        raise UsageError(f"Can't parse PR reference {ref!r}; use REPO#N or a PR URL.")
    return m["owner"] or default_owner, m["name"], int(m["number"])


@contextmanager
def session(org: str, method: str):
    """Load settings, open a client, and turn known errors into clean exits."""
    try:
        settings = load_settings(org=org, method=method)
        with GitHubClient(settings.token) as client:
            yield settings, client
    except (ConfigError, GitHubError, UsageError) as e:
        err_console.print(f"[red]error:[/red] {escape(str(e))}")
        raise typer.Exit(1) from None


def _open_url(url: str) -> None:
    console.print(f"Opening {url}")
    if not open_url(url):
        console.print("[yellow]Couldn't launch a browser; open the link above manually.[/yellow]")


def _merge(client: GitHubClient, pr: DependabotPR, method: str) -> bool:
    """Approve (if needed) and merge, reporting the outcome on the console."""
    try:
        outcome = approve_and_merge(client, pr, method)
    except MergeRefused as e:
        console.print(f"[red]✗ {pr.ref} can't be merged:[/red] {escape(str(e))}")
        return False
    if outcome.approved:
        console.print(f"[green]✓ approved {pr.ref}[/green]")
    console.print(f"[green]✓ merged {pr.ref} ({method})[/green]")
    return True


def _print_tally(tally: Counter[str]) -> None:
    summary = ", ".join(
        f"{tally[k]} {k}" for k in ("merged", "approved", "skipped", "failed") if tally[k]
    )
    console.print(summary or "No actions taken.")


@app.command("list")
def list_cmd(
    org: OrgOpt,
    repo: RepoOpt = None,
    method: MethodOpt = DEFAULT_METHOD,
    mergeable_only: Annotated[
        bool, typer.Option("--mergeable-only", help="Only show PRs ready to merge.")
    ] = False,
) -> None:
    """List open Dependabot PRs in the organization."""
    with session(org, method) as (settings, client):
        with console.status(f"Searching {settings.org} for Dependabot PRs…"):
            prs = client.list_dependabot_prs(settings.org, repo)
        checks = [evaluate(pr, settings.merge_method) for pr in prs]
        if mergeable_only:
            pairs = [(p, c) for p, c in zip(prs, checks, strict=True) if c.can_merge]
            prs, checks = [p for p, _ in pairs], [c for _, c in pairs]
        if not prs:
            console.print("No open Dependabot PRs found.")
            return
        console.print(pr_table(prs, checks, hyperlinks=console.is_terminal))
        ready = sum(c.can_merge for c in checks)
        console.print(f"{len(prs)} PR(s), {ready} ready to merge.")


@app.command()
def show(
    pr_ref: PrArg,
    org: OrgOpt,
    method: MethodOpt = DEFAULT_METHOD,
    no_pager: Annotated[bool, typer.Option("--no-pager", help="Don't use a pager.")] = False,
) -> None:
    """Show a Dependabot PR's description: release notes, changelog and commits."""
    with session(org, method) as (settings, client):
        owner, name, number = parse_pr_ref(pr_ref, settings.org)
        pr = client.get_pr(owner, name, number)
        show_pr(
            console,
            pr,
            evaluate(pr, settings.merge_method),
            settings.merge_method,
            page=not no_pager,
        )


@app.command()
def merge(
    pr_ref: PrArg,
    org: OrgOpt,
    method: MethodOpt = DEFAULT_METHOD,
    yes: Annotated[bool, typer.Option("--yes", "-y", help="Don't ask for confirmation.")] = False,
) -> None:
    """Approve (if needed) and merge a PR, provided all checks have passed."""
    with session(org, method) as (settings, client):
        owner, name, number = parse_pr_ref(pr_ref, settings.org)
        pr = client.get_pr(owner, name, number)
        check = evaluate(pr, settings.merge_method)
        if not check.can_merge:
            err_console.print(f"[red]✗ {pr.ref} can't be merged:[/red] {check.summary}")
            raise typer.Exit(1)
        action = "Approve and merge" if check.needs_approval else "Merge"
        question = f"{action} {pr.ref} ({pr.title}) via {settings.merge_method}?"
        if not yes and not Confirm.ask(question):
            raise typer.Exit(0)
        if not _merge(client, pr, settings.merge_method):
            raise typer.Exit(1)


@app.command()
def review(
    org: OrgOpt,
    repo: RepoOpt = None,
    method: MethodOpt = DEFAULT_METHOD,
    include_all: Annotated[
        bool, typer.Option("--all", "-a", help="Include PRs that can't be merged yet.")
    ] = False,
    plain: Annotated[
        bool,
        typer.Option("--plain", help="Use line-by-line prompts instead of the full-screen UI."),
    ] = False,
    no_pager: Annotated[
        bool, typer.Option("--no-pager", help="With --plain: don't use a pager.")
    ] = False,
) -> None:
    """Review Dependabot PRs: read release notes, then approve, merge or skip each one."""
    with session(org, method) as (settings, client):
        with console.status(f"Searching {settings.org} for Dependabot PRs…"):
            prs = client.list_dependabot_prs(settings.org, repo)

        if not plain and sys.stdin.isatty() and sys.stdout.isatty():
            from dependalot.tui import ReviewApp

            tally = ReviewApp(
                client,
                org=settings.org,
                method=settings.merge_method,
                prs=prs,
                repo=repo,
                include_all=include_all,
            ).run()
            _print_tally(tally or Counter())
            return

        candidates = [
            (pr, check)
            for pr in prs
            if (check := evaluate(pr, settings.merge_method)).can_merge or include_all
        ]
        if not candidates:
            hidden = len(prs)
            hint = f" ({hidden} not mergeable; use --all to see them)" if hidden else ""
            console.print(f"Nothing to review{hint}.")
            return

        tally: Counter[str] = Counter()
        for i, (pr, check) in enumerate(candidates, 1):
            console.rule(f"[bold]{i}/{len(candidates)}[/bold]  {pr.ref}")
            show_pr(console, pr, check, settings.merge_method, page=not no_pager)

            choices = (["m"] if check.can_merge else []) + ["a", "o", "s", "q"]
            labels = {
                "m": "erge (approve + merge)",
                "a": "pprove only",
                "o": "pen in browser",
                "s": "kip",
                "q": "uit",
            }
            # Escape the "[x]" key hints so rich doesn't treat them as markup tags.
            prompt = "  ".join(f"[bold cyan]\\[{c}][/bold cyan]{labels[c]}" for c in choices)
            while True:
                choice = Prompt.ask(
                    prompt,
                    choices=choices,
                    show_choices=False,
                    default="m" if check.can_merge else "s",
                )
                if choice != "o":
                    break
                _open_url(pr.url)

            if choice == "q":
                break
            if choice == "s":
                tally["skipped"] += 1
                continue
            try:
                if choice == "a":
                    client.approve(pr.repo, pr.number)
                    console.print(f"[green]✓ approved {pr.ref}[/green]")
                    tally["approved"] += 1
                elif _merge(client, pr, settings.merge_method):
                    tally["merged"] += 1
                else:
                    tally["failed"] += 1
            except GitHubError as e:
                console.print(f"[red]✗ {pr.ref}: {escape(str(e))}[/red]")
                tally["failed"] += 1

        console.rule()
        _print_tally(tally)


if __name__ == "__main__":
    app()
