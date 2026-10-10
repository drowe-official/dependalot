"""Thin GitHub API client: GraphQL for reads, REST for approve/merge."""

from __future__ import annotations

import time

import httpx

from dependalot.models import DependabotPR

API_URL = "https://api.github.com"

PR_FIELDS = """
  number
  title
  url
  body
  createdAt
  headRefOid
  headRefName
  mergeable
  mergeStateStatus
  reviewDecision
  commits(last: 1) { nodes { commit { statusCheckRollup { state } } } }
  repository {
    nameWithOwner
    viewerPermission
    rebaseMergeAllowed
    squashMergeAllowed
    mergeCommitAllowed
  }
"""

SEARCH_QUERY = f"""
query($q: String!, $after: String) {{
  search(query: $q, type: ISSUE, first: 50, after: $after) {{
    pageInfo {{ hasNextPage endCursor }}
    nodes {{ ... on PullRequest {{ {PR_FIELDS} }} }}
  }}
}}
"""

PR_QUERY = f"""
query($owner: String!, $name: String!, $number: Int!) {{
  repository(owner: $owner, name: $name) {{
    pullRequest(number: $number) {{ {PR_FIELDS} }}
  }}
}}
"""


class GitHubError(Exception):
    pass


def _rest_error(resp: httpx.Response) -> GitHubError:
    try:
        message = resp.json().get("message", resp.text)
    except ValueError:
        message = resp.text
    hints = {
        401: "bad or expired token",
        403: "insufficient permission",
        404: "not found (or token lacks access)",
        405: "not mergeable",
        409: "head branch was modified; refresh and retry",
        422: "rejected by GitHub",
    }
    hint = hints.get(resp.status_code)
    prefix = f"{resp.status_code} {hint}" if hint else str(resp.status_code)
    return GitHubError(f"{prefix}: {message}")


class GitHubClient:
    def __init__(self, token: str, base_url: str = API_URL, transport=None):
        self._http = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "dependalot",
            },
            timeout=30.0,
            transport=transport,
        )

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> GitHubClient:
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def _graphql(self, query: str, variables: dict) -> dict:
        try:
            resp = self._http.post("/graphql", json={"query": query, "variables": variables})
        except httpx.HTTPError as e:
            raise GitHubError(f"network error: {e}") from e
        if resp.status_code != 200:
            raise _rest_error(resp)
        payload = resp.json()
        if payload.get("errors"):
            raise GitHubError("; ".join(err.get("message", str(err)) for err in payload["errors"]))
        return payload["data"]

    def _rest(self, method: str, path: str, json: dict) -> dict:
        try:
            resp = self._http.request(method, path, json=json)
        except httpx.HTTPError as e:
            raise GitHubError(f"network error: {e}") from e
        if not resp.is_success:
            raise _rest_error(resp)
        return resp.json()

    def list_dependabot_prs(self, org: str, repo: str | None = None) -> list[DependabotPR]:
        # Search ORs org: and repo: together, so a repo filter must replace the org one.
        scope = f"repo:{org}/{repo}" if repo else f"org:{org}"
        q = f"is:pr is:open archived:false author:app/dependabot {scope}"
        prs: list[DependabotPR] = []
        after = None
        while True:
            data = self._graphql(SEARCH_QUERY, {"q": q, "after": after})["search"]
            prs.extend(DependabotPR.from_node(n) for n in data["nodes"] if n)
            if not data["pageInfo"]["hasNextPage"]:
                break
            after = data["pageInfo"]["endCursor"]
        prs.sort(key=lambda p: (p.repo.lower(), p.number))
        return prs

    def get_pr(
        self, owner: str, name: str, number: int, retries: int = 3, delay: float = 1.5
    ) -> DependabotPR:
        """Fetch one PR, re-polling while GitHub is still computing mergeability."""
        for attempt in range(retries + 1):
            data = self._graphql(PR_QUERY, {"owner": owner, "name": name, "number": number})
            node = (data.get("repository") or {}).get("pullRequest")
            if node is None:
                raise GitHubError(f"PR {owner}/{name}#{number} not found")
            pr = DependabotPR.from_node(node)
            if pr.mergeable != "UNKNOWN" or attempt == retries:
                return pr
            time.sleep(delay)
        raise AssertionError("unreachable")

    def approve(self, repo: str, number: int) -> None:
        self._rest("POST", f"/repos/{repo}/pulls/{number}/reviews", {"event": "APPROVE"})

    def merge(self, repo: str, number: int, sha: str, method: str) -> dict:
        return self._rest(
            "PUT",
            f"/repos/{repo}/pulls/{number}/merge",
            {"merge_method": method, "sha": sha},
        )
