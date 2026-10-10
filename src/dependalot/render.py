"""Terminal rendering: PR tables and detail views."""

from __future__ import annotations

import html
import os
import re
from datetime import UTC, datetime
from typing import NamedTuple

from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from dependalot.models import DependabotPR, MergeCheck

CHECK_ICONS = {
    None: ("–", "dim"),
    "SUCCESS": ("✓", "green"),
    "PENDING": ("…", "yellow"),
    "EXPECTED": ("…", "yellow"),
    "FAILURE": ("✗", "red"),
    "ERROR": ("✗", "red"),
}


def age(created_at: datetime, now: datetime | None = None) -> str:
    delta = (now or datetime.now(UTC)) - created_at
    if delta.days >= 1:
        return f"{delta.days}d"
    hours = delta.seconds // 3600
    return f"{hours}h" if hours else f"{delta.seconds // 60}m"


def short_repo(repo: str) -> str:
    return repo.split("/", 1)[-1]


def update_cells(pr: DependabotPR) -> tuple[str | Text, str]:
    """The (package, update) columns for a PR's row in a table."""
    if bump := pr.bump:
        return bump.package, f"{bump.old} → {bump.new}"
    if group := pr.group:
        updates = f"{group.updates} update{'s' if group.updates != 1 else ''}"
        return Text(f"{group.group} group", style="bold"), updates
    return Text(pr.title, style="italic"), ""


def describe_update(pr: DependabotPR) -> str:
    """One line saying what a PR updates, for confirmation prompts."""
    if bump := pr.bump:
        return f"{bump.package} {bump.old} → {bump.new}"
    return pr.title


def pr_link(url: str) -> Text:
    """A clickable "open ↗" terminal hyperlink (OSC 8) to the PR."""
    return Text("open ↗", style=f"link {url} underline blue")


def pr_table(prs: list[DependabotPR], checks: list[MergeCheck], hyperlinks: bool = True) -> Table:
    table = Table(header_style="bold", expand=False)
    table.add_column("PR", no_wrap=True)
    table.add_column("Type", style="magenta", no_wrap=True)
    table.add_column("Package")
    table.add_column("Update", no_wrap=True)
    table.add_column("Age", justify="right")
    table.add_column("Checks", justify="center")
    table.add_column("Status")
    # Only when output is a terminal: piped output can't be clicked.
    if hyperlinks:
        table.add_column("Link", no_wrap=True)
    for pr, check in zip(prs, checks, strict=True):
        package, update = update_cells(pr)
        icon, style = CHECK_ICONS.get(pr.checks_state, ("?", "dim"))
        status = (
            Text("✓ ready", style="green")
            if check.can_merge
            else Text(f"✗ {check.summary}", style="red")
        )
        cells = [
            f"{short_repo(pr.repo)}#{pr.number}",
            pr.ecosystem or "?",
            package,
            update,
            age(pr.created_at),
            Text(icon, style=style),
            status,
        ]
        if hyperlinks:
            cells.append(pr_link(pr.url))
        table.add_row(*cells)
    return table


def header_panel(pr: DependabotPR, check: MergeCheck, method: str) -> Panel:
    icon, style = CHECK_ICONS.get(pr.checks_state, ("?", "dim"))
    lines = Text()
    lines.append(f"{pr.repo}#{pr.number}", style="bold")
    lines.append(f"   [{pr.ecosystem or 'unknown'}]\n", style="magenta")
    lines.append(f"{pr.url}\n", style="link " + pr.url)
    lines.append("Checks: ")
    lines.append(f"{icon} {pr.checks_state or 'none'}", style=style)
    lines.append(f"   Review: {pr.review_decision or 'not required'}")
    lines.append(f"   Merge state: {pr.merge_state}\n")
    if check.can_merge:
        lines.append(f"Ready to {'approve + ' if check.needs_approval else ''}{method}", "green")
    else:
        lines.append(f"Cannot merge: {check.summary}", style="red")
    return Panel(lines, title=pr.title, title_align="left", border_style=style)


# --- Dependabot body cleanup -------------------------------------------------

_COMMANDS_BLOCK = re.compile(
    r"<details>\s*<summary>\s*Dependabot commands and options.*?</details>", re.S | re.I
)
_FENCE_SPLIT = re.compile(r"(```.*?```)", re.S)


def _convert_html(fragment: str) -> str:
    s = fragment
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"</?details[^>]*>", "\n", s, flags=re.I)
    s = re.sub(r"<summary[^>]*>(.*?)</summary>", r"\n\n### \1\n\n", s, flags=re.S | re.I)
    s = re.sub(
        r"<h([1-6])[^>]*>(.*?)</h\1>",
        lambda m: "\n\n" + "#" * min(int(m[1]) + 2, 6) + " " + m[2].strip() + "\n\n",
        s,
        flags=re.S | re.I,
    )
    s = re.sub(
        r"<pre[^>]*>(?:\s*<code[^>]*>)?(.*?)(?:</code>\s*)?</pre>",
        lambda m: "\n```\n" + html.unescape(m[1]).strip("\n") + "\n```\n",
        s,
        flags=re.S | re.I,
    )
    s = re.sub(r'<a [^>]*href="([^"]*)"[^>]*>(.*?)</a>', r"[\2](\1)", s, flags=re.S | re.I)
    s = re.sub(r"</?(?:strong|b)>", "**", s, flags=re.I)
    s = re.sub(r"</?(?:em|i)>", "*", s, flags=re.I)
    s = re.sub(r"</?code>", "`", s, flags=re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"<li[^>]*>", "\n- ", s, flags=re.I)
    s = re.sub(r"</(?:p|li|ul|ol|blockquote|div)>", "\n", s, flags=re.I)
    s = re.sub(r"<img[^>]*>", "", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)  # anything left over
    return html.unescape(s)


# A block GitHub's 65,535-character body limit cut off has no </details>: it runs to the end.
_DETAILS_BLOCK = re.compile(
    r"<details>\s*<summary>(?P<title>.*?)</summary>(?P<inner>.*?)(?P<end></details>|\Z)",
    re.S | re.I,
)
# In grouped updates, each package's sections follow a line like "Updates `flask` from 2 to 3".
_GROUP_PACKAGE_LINE = re.compile(r"^Updates `([^`]+)` from \S+ to \S+[ \t]*$", re.M)
_TRUNCATED_MARKER = "_Description has been truncated_"
TRUNCATED_NOTE = "_Dependabot truncated this description; open the PR for the rest._"


def _strip_boilerplate(body: str) -> str:
    body = body.replace("\r\n", "\n")
    body = _COMMANDS_BLOCK.sub("", body)
    body = re.sub(r"^\[//\]: # .*$", "", body, flags=re.M)
    return re.sub(r"\[!\[Dependabot compatibility score\].*?\)\]\(.*?\)", "", body)


class Section(NamedTuple):
    kind: str  # Dependabot's <summary> text, e.g. "Release notes"
    markdown: str
    package: str | None = None  # set in grouped updates
    truncated: bool = False

    @property
    def title(self) -> str:
        title = f"{self.package} · {self.kind}" if self.package else self.kind
        return f"{title} (truncated)" if self.truncated else title


def body_sections(body: str) -> tuple[str, list[Section]]:
    """Split a Dependabot body into its intro and its collapsible sections.

    Sections are Dependabot's <details> blocks such as "Release notes", "Changelog" and
    "Commits"; in a grouped update each package has its own, labelled with the package.
    """
    body = _strip_boilerplate(body)
    truncated = _TRUNCATED_MARKER in body
    body = body.replace(_TRUNCATED_MARKER, "")
    sections: list[Section] = []

    def take_from(package: str | None):
        def take(m: re.Match) -> str:
            kind = html.unescape(re.sub(r"<[^>]+>", "", m["title"])).strip()
            sections.append(Section(kind, clean_body(m["inner"]), package, not m["end"]))
            return ""

        return take

    # split() with a capture group gives [intro, package, chunk, package, chunk, ...].
    parts = _GROUP_PACKAGE_LINE.split(body)
    rest = [_DETAILS_BLOCK.sub(take_from(None), parts[0])]
    for package, chunk in zip(parts[1::2], parts[2::2], strict=True):
        rest.append(_DETAILS_BLOCK.sub(take_from(package), chunk))
    intro = clean_body("\n".join(rest))
    if truncated:
        intro = f"{intro}\n\n{TRUNCATED_NOTE}".strip()
    return intro, sections


def clean_body(body: str) -> str:
    """Turn Dependabot's mixed Markdown/HTML PR description into plain Markdown."""
    body = _strip_boilerplate(body)

    out = []
    for part in _FENCE_SPLIT.split(body):
        if part.startswith("```"):
            out.append(part)
            continue
        converted = _convert_html(part)
        # Leading indentation from the HTML would turn into Markdown code blocks.
        out.append("\n".join(line.strip() for line in converted.split("\n")))
    text = "".join(out)
    text = re.sub(r"\n---\s*$", "", text.strip())
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def show_pr(
    console: Console, pr: DependabotPR, check: MergeCheck, method: str, page: bool = True
) -> None:
    content = Group(header_panel(pr, check, method), Markdown(clean_body(pr.body) or "_No body_"))
    if page and console.is_terminal:
        with console.capture() as capture:
            console.print(content)
        if capture.get().count("\n") > console.height - 4:
            os.environ.setdefault("LESS", "-RFX")  # keep colours; exit if it fits
            with console.pager(styles=True):
                console.print(content)
            return
    console.print(content)
