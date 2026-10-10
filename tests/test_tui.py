from collections import Counter

from textual.widgets import Collapsible, DataTable, Markdown

from dependalot.github import GitHubError
from dependalot.models import DependabotPR
from dependalot.tui import ReviewApp
from tests.conftest import make_node
from tests.test_render import BODY, FIXTURES


class FakeClient:
    def __init__(self, nodes, fail_merge=False):
        self.nodes = {n["number"]: n for n in nodes}
        self.fail_merge = fail_merge
        self.approved: list[int] = []
        self.merged: list[tuple[int, str, str]] = []

    def get_pr(self, owner, name, number):
        return DependabotPR.from_node(self.nodes[number])

    def approve(self, repo, number):
        self.approved.append(number)

    def merge(self, repo, number, sha, method):
        if self.fail_merge:
            raise GitHubError("405 not mergeable: nope")
        self.merged.append((number, sha, method))

    def list_dependabot_prs(self, org, repo=None):
        return [DependabotPR.from_node(n) for n in self.nodes.values()]


def make_app(nodes, **kw):
    client = FakeClient(nodes, **kw)
    prs = [DependabotPR.from_node(n) for n in nodes]
    return client, ReviewApp(client, org="Dependalot", method="rebase", prs=prs)


async def test_shows_prs_and_sections():
    _, app = make_app([make_node(body=BODY), make_node(number=8)])
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.pause()
        assert app.query_one("#prs", DataTable).row_count == 2
        titles = [c.title for c in app.query(Collapsible)]
        assert titles == ["Release notes", "Commits"]


async def test_merge_approves_merges_and_advances():
    client, app = make_app([make_node(), make_node(number=8)])
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.press("m", "y")
        await app.workers.wait_for_complete()
        await pilot.pause()
        assert client.approved == [7]
        assert client.merged == [(7, "abc123", "rebase")]
        assert app.items[0].outcome == "merged"
        assert app.query_one("#prs", DataTable).cursor_row == 1
        await pilot.press("s", "q")
    assert app.return_value == Counter({"merged": 1, "skipped": 1})


async def test_merge_failure_is_reported_not_crashing():
    client, app = make_app([make_node()], fail_merge=True)
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.press("m", "y")
        await app.workers.wait_for_complete()
        await pilot.pause()
        assert app.items[0].outcome == "failed"
        await pilot.press("q")
    assert app.return_value == Counter({"failed": 1})


async def test_hides_unmergeable_unless_all():
    failing = make_node(
        number=8, commits={"nodes": [{"commit": {"statusCheckRollup": {"state": "FAILURE"}}}]}
    )
    _, app = make_app([make_node(), failing])
    assert [i.pr.number for i in app.items] == [7]
    client = FakeClient([make_node(), failing])
    prs = [DependabotPR.from_node(n) for n in (make_node(), failing)]
    app_all = ReviewApp(client, org="Dependalot", method="rebase", prs=prs, include_all=True)
    assert [i.pr.number for i in app_all.items] == [7, 8]


async def test_merge_cancelled_does_nothing():
    client, app = make_app([make_node()])
    async with app.run_test(size=(140, 40)) as pilot:
        for keys in (("m", "n"), ("m", "escape"), ("m", "enter")):  # Enter hits Cancel
            await pilot.press(*keys)
            await pilot.pause()
            await app.workers.wait_for_complete()
        assert client.merged == []
        assert client.approved == []
        assert app.items[0].outcome is None


async def test_detail_scrolls_while_list_keeps_focus():
    long_body = "Intro\n\n" + "\n\n".join(f"Paragraph {i}" for i in range(200))
    _, app = make_app([make_node(body=long_body), make_node(number=8)])
    async with app.run_test(size=(140, 30)) as pilot:
        await pilot.pause()
        detail = app.query_one("#detail")
        table = app.query_one("#prs", DataTable)
        await pilot.press("space")
        await pilot.pause()
        after_space = detail.scroll_y
        assert after_space > 0
        await pilot.press("pagedown")
        await pilot.pause()
        assert detail.scroll_y > after_space
        await pilot.press("b", "pageup")
        await pilot.pause()
        assert detail.scroll_y == 0
        assert app.focused is table
        assert table.cursor_row == 0


async def test_grouped_update_sections_are_labelled_by_package():
    body = (FIXTURES / "grouped_actions.md").read_text()
    node = make_node(
        title="Bump the actions group with 2 updates",
        headRefName="dependabot/github_actions/actions-e91bde37dc",
        body=body,
    )
    _, app = make_app([node])
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.pause()
        table = app.query_one("#prs", DataTable)
        row = [str(cell) for cell in table.get_row_at(0)]
        assert row[2:4] == ["actions group", "2 updates"]
        titles = [c.title for c in app.query(Collapsible)]
        assert titles[0] == "actions/checkout · Release notes"
        assert titles[-1] == "actions/setup-python · Commits"


async def test_toggle_sections():
    _, app = make_app([make_node(body=BODY)])
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.pause()
        states = lambda: [c.collapsed for c in app.query(Collapsible)]  # noqa: E731
        assert states() == [False, True]
        await pilot.press("e")
        assert states() == [False, False]
        await pilot.press("e")
        assert states() == [True, True]


async def test_review_keys_ignored_while_dialog_open():
    client, app = make_app([make_node()])
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.press("m")
        await pilot.pause()
        await pilot.press("m", "q", "space", "e")
        await pilot.pause()
        assert len(app.screen_stack) == 2  # still just the one dialog, app not quit
        await pilot.press("n")
        await pilot.pause()
        assert len(app.screen_stack) == 1
        assert client.merged == []


async def test_long_sections_make_detail_scrollable():
    notes = "".join(f"<li>Change {i}</li>" for i in range(200))
    body = (
        "Bumps x from 1 to 2.\n<details>\n<summary>Release notes</summary>\n"
        f"<ul>{notes}</ul>\n</details>\n"
    )
    _, app = make_app([make_node(body=body)])
    async with app.run_test(size=(140, 30)) as pilot:
        await pilot.pause()
        detail = app.query_one("#detail")
        assert detail.max_scroll_y > 0
        await pilot.press("space")
        await pilot.pause()
        assert detail.scroll_y > 0


async def test_toggle_detail_pane_widens_list():
    _, app = make_app([make_node(body=BODY)])
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.pause()
        table = app.query_one("#prs", DataTable)
        detail, tab = app.query_one("#detail"), app.query_one("#detail-tab")
        narrow = table.size.width
        assert detail.display and not tab.display
        await pilot.press("d")
        await pilot.pause()
        assert not detail.display and tab.display
        assert tab.size.width == 3
        assert table.size.width > narrow
        await pilot.press("e")  # acts on the hidden pane: disabled
        assert [c.collapsed for c in app.query(Collapsible)] == [False, True]
        await pilot.click("#detail-tab")
        await pilot.pause()
        assert detail.display and not tab.display
        assert table.size.width == narrow
        assert app.focused is table


async def test_collapsed_sections_are_built_only_when_expanded():
    body = (FIXTURES / "grouped_actions.md").read_text()
    _, app = make_app([make_node(body=body)])
    async with app.run_test(size=(140, 40)) as pilot:
        await pilot.pause()
        sections = list(app.query(Collapsible))
        built = lambda: [bool(c.query(Markdown)) for c in sections]  # noqa: E731
        assert built() == [True, False, False, False, False]
        sections[2].collapsed = False
        await pilot.pause()
        assert built() == [True, False, True, False, False]
        assert "actions/checkout/commit" in sections[2].query_one(Markdown).source
