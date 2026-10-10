import json

import httpx
import pytest
import respx

from dependalot.github import GitHubClient, GitHubError
from tests.conftest import make_node

API = "https://api.github.com"


@pytest.fixture
def client():
    with GitHubClient("t") as c:
        yield c


@respx.mock
def test_list_paginates_and_builds_query(client):
    route = respx.post(f"{API}/graphql").mock(
        side_effect=[
            httpx.Response(
                200,
                json={
                    "data": {
                        "search": {
                            "pageInfo": {"hasNextPage": True, "endCursor": "c1"},
                            "nodes": [make_node(number=2), {}],
                        }
                    }
                },
            ),
            httpx.Response(
                200,
                json={
                    "data": {
                        "search": {
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                            "nodes": [make_node(number=1)],
                        }
                    }
                },
            ),
        ]
    )
    prs = client.list_dependabot_prs("Dependalot", repo="app")
    assert [p.number for p in prs] == [1, 2]
    first = json.loads(route.calls[0].request.content)
    assert first["variables"]["q"] == (
        "is:pr is:open archived:false author:app/dependabot repo:Dependalot/app"
    )
    assert json.loads(route.calls[1].request.content)["variables"]["after"] == "c1"
    assert route.calls[0].request.headers["Authorization"] == "Bearer t"


@respx.mock
def test_get_pr_retries_while_mergeability_unknown(client):
    respx.post(f"{API}/graphql").mock(
        side_effect=[
            httpx.Response(
                200, json={"data": {"repository": {"pullRequest": make_node(mergeable="UNKNOWN")}}}
            ),
            httpx.Response(200, json={"data": {"repository": {"pullRequest": make_node()}}}),
        ]
    )
    pr = client.get_pr("Dependalot", "app", 7, delay=0)
    assert pr.mergeable == "MERGEABLE"


@respx.mock
def test_graphql_errors_raise(client):
    respx.post(f"{API}/graphql").mock(
        return_value=httpx.Response(200, json={"errors": [{"message": "boom"}]})
    )
    with pytest.raises(GitHubError, match="boom"):
        client.list_dependabot_prs("Dependalot")


@respx.mock
def test_approve_payload(client):
    route = respx.post(f"{API}/repos/Dependalot/app/pulls/7/reviews").mock(
        return_value=httpx.Response(200, json={"id": 1})
    )
    client.approve("Dependalot/app", 7)
    assert json.loads(route.calls[0].request.content) == {"event": "APPROVE"}


@respx.mock
def test_merge_pins_sha(client):
    route = respx.put(f"{API}/repos/Dependalot/app/pulls/7/merge").mock(
        return_value=httpx.Response(200, json={"merged": True})
    )
    client.merge("Dependalot/app", 7, "abc123", "rebase")
    assert json.loads(route.calls[0].request.content) == {
        "merge_method": "rebase",
        "sha": "abc123",
    }


@respx.mock
def test_merge_error_is_readable(client):
    respx.put(f"{API}/repos/Dependalot/app/pulls/7/merge").mock(
        return_value=httpx.Response(405, json={"message": "Pull Request is not mergeable"})
    )
    with pytest.raises(GitHubError, match="405 not mergeable: Pull Request is not mergeable"):
        client.merge("Dependalot/app", 7, "abc123", "rebase")
