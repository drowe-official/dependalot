"""Dependabot PR model and mergeability rules."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime

WRITE_PERMISSIONS = {"WRITE", "MAINTAIN", "ADMIN"}

# "Bump requests from 2.31.0 to 2.32.3", optionally with a prefix such as
# "build(deps): " or "chore(deps-dev): ", and an optional " in /path" suffix.
_BUMP_RE = re.compile(
    r"^(?:[\w-]+(?:\([\w-]+\))?:\s*)?"
    r"[Bb]ump (?P<package>\S+) from (?P<old>\S+) to (?P<new>\S+)"
)

# Grouped updates: "Bump the pip group with 3 updates", optionally "across 2 directories"
# or "in /web" before "with". A group with a single update uses the plain bump title.
_GROUP_RE = re.compile(
    r"^(?:[\w-]+(?:\([\w-]+\))?:\s*)?"
    r"[Bb]ump the (?P<group>\S+) group\b.*? with (?P<updates>\d+) updates?\b"
)


# Dependabot's branch slug for each ecosystem -> the name we display.
ECOSYSTEMS = {
    "pip": "python",
    "uv": "uv",
    "conda": "conda",
    "npm_and_yarn": "npm",
    "bun": "bun",
    "github_actions": "actions",
    "bundler": "ruby",
    "cargo": "rust",
    "composer": "php",
    "go_modules": "go",
    "gradle": "gradle",
    "maven": "maven",
    "nuget": "nuget",
    "dotnet_sdk": "dotnet",
    "mix": "elixir",
    "pub": "dart",
    "swift": "swift",
    "elm": "elm",
    "docker": "docker",
    "docker_compose": "docker-compose",
    "helm": "helm",
    "terraform": "terraform",
    "gitsubmodule": "submodule",
    "devcontainers": "devcontainers",
    "pre_commit": "pre-commit",
}

# "dependabot/pip/requests-2.32.3"; the separator is configurable, so allow "-" too.
_BRANCH_RE = re.compile(r"^dependabot[/-](?P<slug>[a-z_]+)[/-]")


@dataclass(frozen=True)
class PackageBump:
    package: str
    old: str
    new: str


@dataclass(frozen=True)
class GroupBump:
    group: str
    updates: int


@dataclass
class DependabotPR:
    repo: str  # "owner/name"
    number: int
    title: str
    url: str
    body: str
    created_at: datetime
    head_sha: str
    head_ref: str
    mergeable: str  # MERGEABLE | CONFLICTING | UNKNOWN
    merge_state: str  # CLEAN | BLOCKED | BEHIND | DIRTY | DRAFT | HAS_HOOKS | UNSTABLE | UNKNOWN
    review_decision: str | None  # APPROVED | CHANGES_REQUESTED | REVIEW_REQUIRED | None
    checks_state: str | None  # SUCCESS | PENDING | FAILURE | ERROR | EXPECTED | None (no checks)
    viewer_permission: str | None
    allowed_methods: frozenset[str] = field(default_factory=frozenset)

    @property
    def ref(self) -> str:
        return f"{self.repo}#{self.number}"

    @property
    def bump(self) -> PackageBump | None:
        return parse_bump(self.title)

    @property
    def group(self) -> GroupBump | None:
        return parse_group(self.title)

    @property
    def ecosystem(self) -> str | None:
        return parse_ecosystem(self.head_ref)

    @classmethod
    def from_node(cls, node: dict) -> DependabotPR:
        repo = node["repository"]
        allowed = {
            method
            for method, key in (
                ("rebase", "rebaseMergeAllowed"),
                ("squash", "squashMergeAllowed"),
                ("merge", "mergeCommitAllowed"),
            )
            if repo.get(key)
        }
        commits = (node.get("commits") or {}).get("nodes") or []
        rollup = commits[0]["commit"].get("statusCheckRollup") if commits else None
        return cls(
            repo=repo["nameWithOwner"],
            number=node["number"],
            title=node["title"],
            url=node["url"],
            body=node.get("body") or "",
            created_at=datetime.fromisoformat(node["createdAt"].replace("Z", "+00:00")),
            head_sha=node["headRefOid"],
            head_ref=node["headRefName"],
            mergeable=node.get("mergeable") or "UNKNOWN",
            merge_state=node.get("mergeStateStatus") or "UNKNOWN",
            review_decision=node.get("reviewDecision"),
            checks_state=rollup["state"] if rollup else None,
            viewer_permission=repo.get("viewerPermission"),
            allowed_methods=frozenset(allowed),
        )


@dataclass(frozen=True)
class MergeCheck:
    can_merge: bool
    needs_approval: bool
    reasons: tuple[str, ...]

    @property
    def summary(self) -> str:
        return "; ".join(self.reasons) if self.reasons else "ready"


def parse_bump(title: str) -> PackageBump | None:
    m = _BUMP_RE.match(title)
    if not m:
        return None
    return PackageBump(m["package"], m["old"], m["new"])


def parse_group(title: str) -> GroupBump | None:
    m = _GROUP_RE.match(title)
    if not m:
        return None
    return GroupBump(m["group"], int(m["updates"]))


def parse_ecosystem(branch: str) -> str | None:
    m = _BRANCH_RE.match(branch)
    if not m:
        return None
    return ECOSYSTEMS.get(m["slug"], m["slug"].replace("_", "-"))


def evaluate(pr: DependabotPR, method: str) -> MergeCheck:
    reasons: list[str] = []

    if pr.viewer_permission not in WRITE_PERMISSIONS:
        reasons.append("you lack write access")

    if method not in pr.allowed_methods:
        reasons.append(f"{method} merges disabled in repo")

    if pr.mergeable == "CONFLICTING":
        reasons.append("conflicts")
    elif pr.mergeable != "MERGEABLE":
        reasons.append("mergeability unknown")

    if pr.checks_state == "PENDING" or pr.checks_state == "EXPECTED":
        reasons.append("checks pending")
    elif pr.checks_state not in (None, "SUCCESS"):
        reasons.append("checks failing")

    if pr.merge_state == "BEHIND":
        reasons.append("branch behind base")
    elif pr.merge_state == "DIRTY" and "conflicts" not in reasons:
        reasons.append("conflicts")
    elif pr.merge_state == "DRAFT":
        reasons.append("draft")
    elif pr.merge_state == "BLOCKED" and pr.review_decision != "REVIEW_REQUIRED":
        # A missing approval is something we fix ourselves; any other block is not.
        if pr.checks_state in (None, "SUCCESS"):
            reasons.append("blocked by branch protection")

    if pr.review_decision == "CHANGES_REQUESTED":
        reasons.append("changes requested")

    return MergeCheck(
        can_merge=not reasons,
        needs_approval=pr.review_decision != "APPROVED",
        reasons=tuple(reasons),
    )
