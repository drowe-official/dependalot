"""PR actions shared by the CLI commands and the review TUI."""

from __future__ import annotations

from dataclasses import dataclass

from dependalot.github import GitHubClient
from dependalot.models import DependabotPR, evaluate


class MergeRefused(Exception):
    """The PR no longer meets the conditions for merging."""


@dataclass(frozen=True)
class MergeOutcome:
    pr: DependabotPR
    approved: bool


def approve_and_merge(client: GitHubClient, pr: DependabotPR, method: str) -> MergeOutcome:
    """Re-check a PR and, if still mergeable, approve (if needed) and merge it.

    Raises MergeRefused if the PR can't be merged, or GitHubError if GitHub rejects a call.
    The merge is pinned to the head commit that was checked.
    """
    owner, name = pr.repo.split("/", 1)
    fresh = client.get_pr(owner, name, pr.number)
    check = evaluate(fresh, method)
    if not check.can_merge:
        raise MergeRefused(check.summary)
    if check.needs_approval:
        client.approve(fresh.repo, fresh.number)
    client.merge(fresh.repo, fresh.number, fresh.head_sha, method)
    return MergeOutcome(pr=fresh, approved=check.needs_approval)
