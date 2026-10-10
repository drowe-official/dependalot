"""Full-screen review UI: PR list on the left, release notes on the right (collapsible)."""

from __future__ import annotations

import asyncio
from collections import Counter
from dataclasses import dataclass

from rich.text import Text
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Collapsible, DataTable, Footer, Header, Label, Markdown, Static

from dependalot.actions import MergeRefused, approve_and_merge
from dependalot.browser import open_url
from dependalot.github import GitHubClient, GitHubError
from dependalot.models import DependabotPR, MergeCheck, evaluate
from dependalot.render import (
    body_sections,
    describe_update,
    header_panel,
    short_repo,
    update_cells,
)


@dataclass
class Item:
    pr: DependabotPR
    check: MergeCheck
    outcome: str | None = None  # merged | approved | skipped | failed


class ConfirmScreen(ModalScreen[bool]):
    """A yes/no dialog; dismisses with True on confirm."""

    DEFAULT_CSS = """
    ConfirmScreen {
        align: center middle;
    }
    ConfirmScreen > Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: auto 3;
        padding: 1 2;
        width: 70;
        height: auto;
        border: thick $warning;
        background: $surface;
    }
    ConfirmScreen #question {
        column-span: 2;
        width: 100%;
    }
    ConfirmScreen Button {
        width: 100%;
    }
    """

    BINDINGS = [
        Binding("y", "confirm", "Yes"),
        Binding("n", "cancel", "No"),
        Binding("escape", "cancel", "Cancel", show=False),
    ]

    def __init__(self, question: str, confirm_label: str = "Yes"):
        super().__init__()
        self.question = question
        self.confirm_label = confirm_label

    def compose(self) -> ComposeResult:
        with Grid():
            yield Label(Text(self.question), id="question")  # titles may contain [brackets]
            yield Button(f"{self.confirm_label} (y)", variant="warning", id="yes")
            yield Button("Cancel (n)", variant="primary", id="no")

    def on_mount(self) -> None:
        self.query_one("#no", Button).focus()  # Enter on its own shouldn't merge

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "yes")

    def action_confirm(self) -> None:
        self.dismiss(True)

    def action_cancel(self) -> None:
        self.dismiss(False)


class DetailTab(Static):
    """The thin strip left in place of the detail pane while it's collapsed."""

    async def on_click(self) -> None:
        await self.app.run_action("toggle_detail")


class LazySection(Collapsible):
    """A collapsible section whose Markdown is only built when it's first expanded.

    Textual's Markdown makes a widget per paragraph and list item, so building every
    section of a large grouped update up front takes over a second, mostly for sections
    that start collapsed and may never be opened.
    """

    def __init__(self, markdown: str, *, title: str, collapsed: bool):
        super().__init__(title=title, collapsed=collapsed)
        self.markdown = markdown
        self.loaded = False

    def on_mount(self) -> None:
        if not self.collapsed:
            self._load()

    def watch_collapsed(self, collapsed: bool) -> None:
        if not collapsed and self.is_mounted:
            self._load()

    def _load(self) -> None:
        if not self.loaded:
            self.loaded = True
            self.query_one(Collapsible.Contents).mount(Markdown(self.markdown or "_Empty_"))


# Sections Dependabot adds when a release may be a supply-chain risk: always expanded.
WARNING_SECTIONS = {"Maintainer changes", "Install script changes"}


class ReviewApp(App[Counter[str]]):
    """Step through Dependabot PRs and approve/merge them with single keypresses."""

    TITLE = "dependalot review"

    CSS = """
    #prs {
        width: 55%;
        height: 1fr;
        border-right: solid $panel-lighten-2;
    }
    #detail {
        width: 1fr;
        height: 1fr;
        padding: 0 1;
    }
    #detail-tab {
        display: none;
        width: 3;
        height: 1fr;
        content-align: center middle;
        color: $text-muted;
        background: $panel;
    }
    #detail-tab:hover {
        color: $text;
    }
    .detail-collapsed #prs {
        width: 1fr;
    }
    .detail-collapsed #detail {
        display: none;
    }
    .detail-collapsed #detail-tab {
        display: block;
    }
    #intro {
        margin: 1 0 0 0;
    }
    #sections {
        height: auto;  /* Vertical defaults to 1fr, which clips instead of scrolling */
    }
    #sections Collapsible {
        margin: 0;
    }
    """

    BINDINGS = [
        Binding("m", "merge", "Merge"),
        Binding("a", "approve", "Approve"),
        Binding("o", "open", "Open in browser"),
        Binding("s", "skip", "Skip"),
        Binding("r", "refresh", "Refresh"),
        Binding("q", "quit", "Quit"),
        # Priority so they win over the PR list's own PgUp/PgDn while it has focus.
        Binding("space", "detail_page(1)", "Scroll ↓", priority=True),
        Binding("b", "detail_page(-1)", "Scroll ↑", priority=True),
        Binding("pagedown", "detail_page(1)", show=False, priority=True),
        Binding("pageup", "detail_page(-1)", show=False, priority=True),
        Binding("e", "toggle_sections", "Expand/collapse"),
        Binding("d", "toggle_detail", "Hide/show details"),
    ]

    REVIEW_ACTIONS = {
        "merge",
        "approve",
        "open",
        "skip",
        "refresh",
        "quit",
        "detail_page",
        "toggle_sections",
        "toggle_detail",
    }

    # Actions that act on the detail pane, so are disabled while it's collapsed.
    DETAIL_ACTIONS = {"detail_page", "toggle_sections"}

    def __init__(
        self,
        client: GitHubClient,
        org: str,
        method: str,
        prs: list[DependabotPR],
        repo: str | None = None,
        include_all: bool = False,
    ):
        super().__init__()
        self.client = client
        self.org = org
        self.method = method
        self.repo = repo
        self.include_all = include_all
        self.items = self._items_for(prs)
        self.detail_collapsed = False
        self.sub_title = f"{org} · {method}"

    # --- layout -------------------------------------------------------------

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main"):
            yield DataTable(id="prs", cursor_type="row", zebra_stripes=True)
            with VerticalScroll(id="detail"):
                yield Static(id="summary")
                yield Markdown(id="intro")
                yield Vertical(id="sections")
            yield DetailTab("◀\n\nd", id="detail-tab")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#prs", DataTable)
        table.add_column("Type", key="type")
        table.add_column("PR", key="pr")
        table.add_column("Package", key="package")
        table.add_column("Update", key="update")
        table.add_column("Status", key="status")
        self._fill_table()
        table.focus()

    def _items_for(self, prs: list[DependabotPR]) -> list[Item]:
        items = [Item(pr, evaluate(pr, self.method)) for pr in prs]
        return [i for i in items if i.check.can_merge or self.include_all]

    def _fill_table(self) -> None:
        table = self.query_one("#prs", DataTable)
        table.clear()
        for idx, item in enumerate(self.items):
            package, update = update_cells(item.pr)
            table.add_row(
                Text(item.pr.ecosystem or "?", style="magenta"),
                f"{short_repo(item.pr.repo)}#{item.pr.number}",
                package,
                update,
                self._status_cell(item),
                key=str(idx),
            )
        if self.items:
            self.call_after_refresh(self.show_detail, 0)
        else:
            self.query_one("#summary", Static).update(
                Text("Nothing to review. Press r to refresh or q to quit.", style="dim")
            )

    @staticmethod
    def _status_cell(item: Item) -> Text:
        styles = {"merged": "bold green", "approved": "cyan", "skipped": "dim", "failed": "red"}
        if item.outcome:
            return Text(item.outcome, style=styles[item.outcome])
        if item.check.can_merge:
            return Text("✓ ready", style="green")
        return Text(f"✗ {item.check.summary}", style="red")

    # --- detail pane --------------------------------------------------------

    async def show_detail(self, idx: int) -> None:
        if not 0 <= idx < len(self.items):
            return
        item = self.items[idx]
        self.query_one("#summary", Static).update(header_panel(item.pr, item.check, self.method))
        intro, sections = body_sections(item.pr.body)
        await self.query_one("#intro", Markdown).update(intro or "_No description_")
        container = self.query_one("#sections", Vertical)
        await container.remove_children()
        await container.mount_all(
            LazySection(
                s.markdown,
                title=f"⚠ {s.title}" if s.kind in WARNING_SECTIONS else s.title,
                collapsed=n > 0 and s.kind not in WARNING_SECTIONS,
            )
            for n, s in enumerate(sections)
        )
        self.query_one("#detail", VerticalScroll).scroll_home(animate=False)

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        self._show_detail_worker(event.cursor_row)

    @work(exclusive=True, group="detail")
    async def _show_detail_worker(self, idx: int) -> None:
        # Exclusive: moving on cancels the previous PR's render, and the short pause lets
        # a held arrow key skip the PRs in between instead of rendering each one.
        await asyncio.sleep(0.05)
        await self.show_detail(idx)

    def on_markdown_link_clicked(self, event: Markdown.LinkClicked) -> None:
        if not open_url(event.href):
            self.notify(f"Couldn't open {event.href}", severity="warning")

    # --- actions ------------------------------------------------------------

    def _current(self) -> tuple[int, Item] | None:
        table = self.query_one("#prs", DataTable)
        if not self.items or table.cursor_row is None:
            return None
        return table.cursor_row, self.items[table.cursor_row]

    def _set_outcome(self, idx: int, outcome: str, advance: bool = True) -> None:
        self.items[idx].outcome = outcome
        table = self.query_one("#prs", DataTable)
        table.update_cell(str(idx), "status", self._status_cell(self.items[idx]))
        if advance and idx + 1 < len(self.items):
            table.move_cursor(row=idx + 1)

    def action_merge(self) -> None:
        current = self._current()
        if current is None:
            return
        idx, item = current
        if item.outcome == "merged":
            self.notify("Already merged.")
        elif not item.check.can_merge:
            self.notify(f"Can't merge: {item.check.summary}", severity="error")
        else:
            action = "Approve and merge" if item.check.needs_approval else "Merge"
            what = describe_update(item.pr)
            question = f"{action} {item.pr.ref}?\n\n{what}\nvia {self.method}"

            def on_answer(confirmed: bool | None) -> None:
                if confirmed:
                    self.notify(f"Merging {item.pr.ref}…")
                    self._merge_worker(idx)

            self.push_screen(ConfirmScreen(question, confirm_label=action), on_answer)

    @work(thread=True, group="github")
    def _merge_worker(self, idx: int) -> None:
        item = self.items[idx]
        try:
            outcome = approve_and_merge(self.client, item.pr, self.method)
        except (MergeRefused, GitHubError) as e:
            self.call_from_thread(self.notify, f"{item.pr.ref}: {e}", severity="error")
            self.call_from_thread(self._set_outcome, idx, "failed", False)
            return
        approved = "approved + " if outcome.approved else ""
        self.call_from_thread(self.notify, f"✓ {approved}merged {item.pr.ref} ({self.method})")
        self.call_from_thread(self._set_outcome, idx, "merged")

    def action_approve(self) -> None:
        current = self._current()
        if current is None:
            return
        idx, item = current
        if item.outcome in ("merged", "approved"):
            self.notify(f"Already {item.outcome}.")
            return
        self._approve_worker(idx)

    @work(thread=True, group="github")
    def _approve_worker(self, idx: int) -> None:
        item = self.items[idx]
        try:
            self.client.approve(item.pr.repo, item.pr.number)
        except GitHubError as e:
            self.call_from_thread(self.notify, f"{item.pr.ref}: {e}", severity="error")
            return
        self.call_from_thread(self.notify, f"✓ approved {item.pr.ref}")
        self.call_from_thread(self._set_outcome, idx, "approved")

    def action_open(self) -> None:
        current = self._current()
        if current is None:
            return
        url = current[1].pr.url
        if open_url(url):
            self.notify(f"Opened {url}")
        else:
            self.notify(f"Couldn't open a browser: {url}", severity="warning")

    def action_skip(self) -> None:
        current = self._current()
        if current is None:
            return
        idx, item = current
        self._set_outcome(idx, item.outcome or "skipped")

    def action_refresh(self) -> None:
        self.notify("Refreshing…")
        self._refresh_worker()

    @work(thread=True, exclusive=True, group="refresh")
    def _refresh_worker(self) -> None:
        try:
            prs = self.client.list_dependabot_prs(self.org, self.repo)
        except GitHubError as e:
            self.call_from_thread(self.notify, f"Refresh failed: {e}", severity="error")
            return
        self.call_from_thread(self._apply_refresh, prs)

    def _apply_refresh(self, prs: list[DependabotPR]) -> None:
        self.items = self._items_for(prs)
        self._fill_table()
        self.notify(f"{len(self.items)} PR(s) to review.")

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        # While a dialog is open, keys belong to it, not to the review screen behind it.
        if action in self.REVIEW_ACTIONS and isinstance(self.screen, ModalScreen):
            return False
        if action in self.DETAIL_ACTIONS and self.detail_collapsed:
            return None  # shown greyed out in the footer
        return True

    def action_toggle_detail(self) -> None:
        self.detail_collapsed = not self.detail_collapsed
        self.query_one("#main").set_class(self.detail_collapsed, "detail-collapsed")
        self.refresh_bindings()

    def action_detail_page(self, direction: int) -> None:
        detail = self.query_one("#detail", VerticalScroll)
        if direction > 0:
            detail.scroll_page_down(animate=False)
        else:
            detail.scroll_page_up(animate=False)

    def action_toggle_sections(self) -> None:
        sections = list(self.query("#sections Collapsible").results(Collapsible))
        expand = any(c.collapsed for c in sections)
        for c in sections:
            c.collapsed = not expand

    def action_quit(self) -> None:
        self.exit(Counter(i.outcome for i in self.items if i.outcome))
