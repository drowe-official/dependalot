import json

import httpx
import pytest
import respx
from typer.testing import CliRunner

from dependalot.cli import app, parse_pr_ref
from tests.conftest import make_node

API = "https://api.github.com"
runner = CliRunner()


@pytest.mark.parametrize(
    ("ref", "expected"),
    [
        ("app#7", ("Dependalot", "app", 7)),
        ("other/app#7", ("other", "app", 7)),
        ("https://github.com/Dependalot/app/pull/7", ("Dependalot", "app", 7)),
        ("https://github.com/Dependalot/app/pull/7/files", ("Dependalot", "app", 7)),
    ],
)
def test_parse_pr_ref(ref, expected):
    assert parse_pr_ref(ref, "Dependalot") == expected


def test_missing_token(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN")
    result = runner.invoke(app, ["list", "--org", "Dependalot"])
    assert result.exit_code == 1
    assert "GITHUB_TOKEN" in result.output


def test_org_is_required():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 2
    assert "Missing option '--org'" in result.output


@respx.mock
def test_org_from_env(monkeypatch):
    route = respx.post(f"{API}/graphql").mock(return_value=_search(make_node()))
    monkeypatch.setenv("DEPENDALOT_ORG", "env-org")
    assert runner.invoke(app, ["list"]).exit_code == 0
    assert "org:env-org" in json.loads(route.calls[-1].request.content)["variables"]["q"]
    runner.invoke(app, ["list", "--org", "flag-org"])
    assert "org:flag-org" in json.loads(route.calls[-1].request.content)["variables"]["q"]


def test_invalid_method():
    result = runner.invoke(app, ["list", "--org", "Dependalot", "--method", "yolo"])
    assert result.exit_code == 1
    assert "Invalid merge method 'yolo'" in result.output


def _search(*nodes):
    return httpx.Response(
        200,
        json={
            "data": {
                "search": {
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                    "nodes": list(nodes),
                }
            }
        },
    )


def _pr(node):
    return httpx.Response(200, json={"data": {"repository": {"pullRequest": node}}})


@respx.mock
def test_list(monkeypatch):
    respx.post(f"{API}/graphql").mock(
        return_value=_search(
            make_node(),
            make_node(number=8, title="Bump flask from 2.0 to 3.0", mergeable="CONFLICTING"),
        )
    )
    result = runner.invoke(app, ["list", "--org", "Dependalot"])
    assert result.exit_code == 0, result.output
    assert "requests" in result.output and "2.31.0 → 2.32.3" in result.output
    assert "python" in result.output
    assert "Link" not in result.output  # not a terminal under CliRunner, so no links
    assert "conflicts" in result.output
    assert "2 PR(s), 1 ready to merge." in result.output


@respx.mock
def test_show():
    respx.post(f"{API}/graphql").mock(return_value=_pr(make_node()))
    result = runner.invoke(app, ["show", "--org", "Dependalot", "app#7"])
    assert result.exit_code == 0, result.output
    assert "Bumps requests from 2.31.0 to 2.32.3" in result.output


@respx.mock
def test_merge_approves_then_merges():
    respx.post(f"{API}/graphql").mock(return_value=_pr(make_node()))
    approve = respx.post(f"{API}/repos/Dependalot/app/pulls/7/reviews").mock(
        return_value=httpx.Response(200, json={})
    )
    merge = respx.put(f"{API}/repos/Dependalot/app/pulls/7/merge").mock(
        return_value=httpx.Response(200, json={"merged": True})
    )
    result = runner.invoke(app, ["merge", "--org", "Dependalot", "app#7", "--yes"])
    assert result.exit_code == 0, result.output
    assert approve.called
    assert json.loads(merge.calls[0].request.content)["merge_method"] == "rebase"


@respx.mock
def test_merge_refuses_when_checks_fail():
    respx.post(f"{API}/graphql").mock(
        return_value=_pr(
            make_node(commits={"nodes": [{"commit": {"statusCheckRollup": {"state": "FAILURE"}}}]})
        )
    )
    merge = respx.put(f"{API}/repos/Dependalot/app/pulls/7/merge")
    result = runner.invoke(app, ["merge", "--org", "Dependalot", "app#7", "--yes"])
    assert result.exit_code == 1
    assert "checks failing" in result.output
    assert not merge.called


@respx.mock
def test_review_merge_and_skip():
    respx.post(f"{API}/graphql").mock(
        side_effect=[
            _search(make_node(), make_node(number=8)),
            _pr(make_node()),  # re-check before merging #7
        ]
    )
    respx.post(f"{API}/repos/Dependalot/app/pulls/7/reviews").mock(
        return_value=httpx.Response(200, json={})
    )
    merge = respx.put(f"{API}/repos/Dependalot/app/pulls/7/merge").mock(
        return_value=httpx.Response(200, json={"merged": True})
    )
    result = runner.invoke(app, ["review", "--org", "Dependalot", "--no-pager"], input="m\ns\n")
    assert result.exit_code == 0, result.output
    assert merge.call_count == 1
    assert "1 merged, 1 skipped" in result.output


@respx.mock
def test_review_prompt_shows_key_hints():
    respx.post(f"{API}/graphql").mock(return_value=_search(make_node()))
    result = runner.invoke(app, ["review", "--org", "Dependalot", "--no-pager"], input="q\n")
    assert result.exit_code == 0, result.output
    for hint in ("[m]erge", "[a]pprove", "[o]pen", "[s]kip", "[q]uit"):
        assert hint in result.output
