import pytest


def make_node(**overrides):
    node = {
        "number": 7,
        "title": "Bump requests from 2.31.0 to 2.32.3",
        "url": "https://github.com/Dependalot/app/pull/7",
        "body": "Bumps [requests](https://github.com/psf/requests) from 2.31.0 to 2.32.3.",
        "createdAt": "2026-10-01T12:00:00Z",
        "headRefOid": "abc123",
        "headRefName": "dependabot/pip/requests-2.32.3",
        "mergeable": "MERGEABLE",
        "mergeStateStatus": "CLEAN",
        "reviewDecision": None,
        "commits": {"nodes": [{"commit": {"statusCheckRollup": {"state": "SUCCESS"}}}]},
        "repository": {
            "nameWithOwner": "Dependalot/app",
            "viewerPermission": "ADMIN",
            "rebaseMergeAllowed": True,
            "squashMergeAllowed": True,
            "mergeCommitAllowed": True,
        },
    }
    repo_overrides = overrides.pop("repository", {})
    node.update(overrides)
    node["repository"] = {**node["repository"], **repo_overrides}
    return node


@pytest.fixture
def node():
    return make_node


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("DEPENDALOT_ORG", raising=False)
