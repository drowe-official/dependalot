"""Settings come from command-line flags (the org also from DEPENDALOT_ORG) and the token
from the environment."""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_METHOD = "rebase"
MERGE_METHODS = ("rebase", "squash", "merge")

TOKEN_HELP = (
    "No GitHub token found. Export GITHUB_TOKEN (or GH_TOKEN) with a token that has:\n"
    "  - classic PAT: the 'repo' scope, or\n"
    "  - fine-grained PAT: Pull requests (read/write), Contents (read/write),\n"
    "    Checks and Commit statuses (read) on the org's repositories."
)


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class Settings:
    org: str
    token: str
    merge_method: str


def load_settings(org: str, method: str = DEFAULT_METHOD) -> Settings:
    merge_method = method.lower()
    if merge_method not in MERGE_METHODS:
        raise ConfigError(
            f"Invalid merge method {method!r}; choose one of {', '.join(MERGE_METHODS)}"
        )

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise ConfigError(TOKEN_HELP)

    return Settings(org=org, token=token, merge_method=merge_method)
