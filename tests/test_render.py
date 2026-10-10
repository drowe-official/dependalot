from pathlib import Path

from rich.style import Style

from dependalot.render import TRUNCATED_NOTE, body_sections, clean_body, pr_link

BODY = """Bumps [requests](https://github.com/psf/requests) from 2.31.0 to 2.32.3.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/psf/requests/releases">requests's releases</a>.</em></p>
<blockquote>
<h2>v2.32.3</h2>
<ul>
<li>Fixed <code>HTTPAdapter</code> &amp; friends</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/psf/requests/commit/0e322af"><code>0e322af</code></a> v2.32.3</li>
</ul>
</details>
<br />


[![Dependabot compatibility score](https://x/badges/score.svg)](https://docs.github.com/x)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
</details>
"""


def test_clean_body_converts_dependabot_html():
    out = clean_body(BODY)
    assert "### Release notes" in out
    assert "### Commits" in out
    assert "#### v2.32.3" in out
    assert "- Fixed `HTTPAdapter` & friends" in out
    assert "[`0e322af`](https://github.com/psf/requests/commit/0e322af) v2.32.3" in out
    assert "*Sourced from [requests's releases](https://github.com/psf/requests/releases).*" in out
    assert "<" not in out.replace("<!--", "")


def test_clean_body_drops_boilerplate():
    out = clean_body(BODY)
    assert "Dependabot commands and options" not in out
    assert "@dependabot rebase" not in out
    assert "compatibility score" not in out
    assert "[//]" not in out
    assert not out.endswith("---")


def test_clean_body_keeps_code_fences():
    body = "<p>Example:</p>\n```\n    <indented> code\n```\n"
    assert "```\n    <indented> code\n```" in clean_body(body)


def test_body_sections_splits_details_blocks():
    intro, sections = body_sections(BODY)
    assert intro.startswith("Bumps [requests]")
    assert "Release notes" not in intro
    assert [s.title for s in sections] == ["Release notes", "Commits"]
    assert "#### v2.32.3" in sections[0].markdown
    assert "0e322af" in sections[1].markdown
    assert all("Dependabot commands" not in s.markdown for s in sections)
    assert all(s.package is None and not s.truncated for s in sections)
    assert TRUNCATED_NOTE not in intro


# Real bodies of grouped-update PRs from Dependalot/grouped-sandbox.
FIXTURES = Path(__file__).parent / "fixtures"


def test_body_sections_grouped_update():
    intro, sections = body_sections((FIXTURES / "grouped_actions.md").read_text())
    assert intro.startswith("Bumps the actions group with 2 updates")
    assert "Updates `actions/checkout`" not in intro  # moved into the section titles
    assert "Dependabot will resolve any conflicts" in intro
    assert [s.title for s in sections] == [
        "actions/checkout · Release notes",
        "actions/checkout · Changelog",
        "actions/checkout · Commits",
        "actions/setup-python · Release notes",  # setup-python has no changelog
        "actions/setup-python · Commits",
    ]
    assert "#### v7.0.0" in sections[0].markdown
    assert "setup-python" in sections[4].markdown and "checkout/commit" not in sections[4].markdown
    assert "<details>" not in intro and all("<details>" not in s.markdown for s in sections)


def test_body_sections_grouped_update_truncated_by_github():
    body = (FIXTURES / "grouped_python_truncated.md").read_text()
    assert len(body) == 65535  # GitHub's limit: Dependabot cut it mid-changelog
    intro, sections = body_sections(body)
    assert "| [pytest](https://github.com/pytest-dev/pytest) | `7.4.0` | `9.1.1` |" in intro
    assert intro.endswith(TRUNCATED_NOTE)
    assert "_Description has been truncated_" not in intro
    packages = list(dict.fromkeys(s.package for s in sections))
    assert packages == ["flask", "werkzeug", "jinja2", "click", "requests", "urllib3"]
    assert sections[-1].title == "urllib3 · Changelog (truncated)"
    assert "2.8.0 (2026-09-15)" in sections[-1].markdown
    assert [s for s in sections if s.truncated] == [sections[-1]]
    assert "urllib3's changelog" not in intro  # the unclosed block doesn't leak into the intro


def test_pr_link_is_a_terminal_hyperlink():
    url = "https://github.com/Dependalot/app/pull/7"
    link = pr_link(url)
    assert link.plain == "open ↗"
    assert Style.parse(link.style).link == url
