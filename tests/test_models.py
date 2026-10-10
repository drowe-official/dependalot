import pytest

from dependalot.models import (
    DependabotPR,
    GroupBump,
    PackageBump,
    evaluate,
    parse_bump,
    parse_ecosystem,
    parse_group,
)


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("Bump requests from 2.31.0 to 2.32.3", PackageBump("requests", "2.31.0", "2.32.3")),
        (
            "build(deps): bump lodash from 4.17.20 to 4.17.21",
            PackageBump("lodash", "4.17.20", "4.17.21"),
        ),
        (
            "chore(deps-dev): Bump @types/node from 20.1.0 to 20.2.0 in /web",
            PackageBump("@types/node", "20.1.0", "20.2.0"),
        ),
        ("Bump the pip group across 1 directory with 3 updates", None),
    ],
)
def test_parse_bump(title, expected):
    assert parse_bump(title) == expected


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("Bump the pip group with 3 updates", GroupBump("pip", 3)),
        ("Bump the pip group across 1 directory with 3 updates", GroupBump("pip", 3)),
        ("Bump the npm-deps group across 2 directories with 12 updates", GroupBump("npm-deps", 12)),
        ("chore(deps): bump the actions group in /ci with 1 update", GroupBump("actions", 1)),
        ("Bump requests from 2.31.0 to 2.32.3 in the pip group", None),
        ("Bump requests from 2.31.0 to 2.32.3", None),
    ],
)
def test_parse_group(title, expected):
    assert parse_group(title) == expected


def pr(node, **kw):
    return DependabotPR.from_node(node(**kw))


def test_clean_pr_is_mergeable(node):
    check = evaluate(pr(node), "rebase")
    assert check.can_merge
    assert check.needs_approval
    assert check.reasons == ()


def test_already_approved(node):
    assert not evaluate(pr(node, reviewDecision="APPROVED"), "rebase").needs_approval


def test_no_checks_counts_as_passing(node):
    assert evaluate(pr(node, commits={"nodes": []}), "rebase").can_merge


@pytest.mark.parametrize(
    ("overrides", "reason"),
    [
        ({"repository": {"viewerPermission": "READ"}}, "you lack write access"),
        ({"repository": {"rebaseMergeAllowed": False}}, "rebase merges disabled in repo"),
        ({"mergeable": "CONFLICTING", "mergeStateStatus": "DIRTY"}, "conflicts"),
        ({"mergeable": "UNKNOWN"}, "mergeability unknown"),
        (
            {"commits": {"nodes": [{"commit": {"statusCheckRollup": {"state": "FAILURE"}}}]}},
            "checks failing",
        ),
        (
            {"commits": {"nodes": [{"commit": {"statusCheckRollup": {"state": "PENDING"}}}]}},
            "checks pending",
        ),
        ({"mergeStateStatus": "BEHIND"}, "branch behind base"),
        ({"mergeStateStatus": "BLOCKED"}, "blocked by branch protection"),
        ({"reviewDecision": "CHANGES_REQUESTED"}, "changes requested"),
    ],
)
def test_blockers(node, overrides, reason):
    check = evaluate(pr(node, **overrides), "rebase")
    assert not check.can_merge
    assert reason in check.reasons


def test_conflicts_reported_once(node):
    check = evaluate(pr(node, mergeable="CONFLICTING", mergeStateStatus="DIRTY"), "rebase")
    assert check.reasons.count("conflicts") == 1


def test_blocked_only_on_missing_review_is_mergeable(node):
    check = evaluate(
        pr(node, mergeStateStatus="BLOCKED", reviewDecision="REVIEW_REQUIRED"), "rebase"
    )
    assert check.can_merge
    assert check.needs_approval


def test_method_specific(node):
    p = pr(node, repository={"rebaseMergeAllowed": False})
    assert evaluate(p, "squash").can_merge
    assert not evaluate(p, "rebase").can_merge


@pytest.mark.parametrize(
    ("branch", "expected"),
    [
        ("dependabot/pip/requests-2.32.3", "python"),
        ("dependabot/uv/httpx-0.28.0", "uv"),
        ("dependabot/npm_and_yarn/lodash-4.17.21", "npm"),
        ("dependabot/github_actions/actions/checkout-4", "actions"),
        ("dependabot-npm_and_yarn-lodash-4.17.21", "npm"),
        ("dependabot/some_new_thing/pkg-1.0", "some-new-thing"),
        ("feature/not-dependabot", None),
    ],
)
def test_parse_ecosystem(branch, expected):
    assert parse_ecosystem(branch) == expected
