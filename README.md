# dependalot

Manage Dependabot pull requests across a GitHub organization from the terminal:
list them, read the release notes/changelog/commits Dependabot attaches, and
approve + merge the ones whose checks have passed.

## Install

Requires [uv](https://docs.astral.sh/uv/)

```sh
 # puts `dependalot` on your PATH
uv tool install .
dependalot --help

# or, without installing:
uv run dependalot --help
```

If `dependalot` isn't found after installing, run `uv tool update-shell` and open a new
terminal.

## Authentication

To list, approve and merge PRs, export a **fine-grained** personal access token as
`GITHUB_TOKEN` (or `GH_TOKEN`). Classic PATs (`ghp_...`) are rejected. Create the token with
the org as resource owner, give it access to the repositories you want to manage, and grant
these repository permissions:

| Permission | Access | Used for |
|------------|--------|----------|
| *Pull requests* | read/write | Read: finding Dependabot PRs and reading their title, description, mergeability and review state (`list`, `show`, `review`). Write: approving a PR when branch protection requires a review. |
| *Contents* | read/write | Merging: the merge endpoint writes commits to the base branch, so GitHub checks it under Contents. |
| *Workflows* | read/write | Merging PRs that change files under `.github/workflows/`, such as Dependabot `github-actions` updates. Without it GitHub refuses these merges. |
| *Checks* | read | Seeing check runs (GitHub Actions and other Checks API apps) in the PR's CI status. |
| *Commit statuses* | read | Seeing commit statuses posted by external CI in the PR's CI status. |
| *Metadata* | read | Always included. Repository permissions and allowed merge methods. |

Checks and Commit statuses are both needed to see the PR's full CI result. If either is
missing, a PR with failing CI can show as ready.

```sh
export GITHUB_TOKEN=github_pat_...
```

This works the same in Linux, WSL and Git Bash. To keep it for new terminals, add the
line to `~/.bashrc`. `DEPENDALOT_ORG` is set the same way.

## Options

Settings are passed as command-line flags; there is no config file. The organization can
also be set with the `DEPENDALOT_ORG` environment variable (the flag wins if both are set),
and the token is read from the environment.

| Option | Commands | Meaning | Default |
|--------|----------|---------|---------|
| `--org` | all | GitHub organization (or set `DEPENDALOT_ORG`) | *(required)* |
| `--method`, `-m` | all | Merge method: `rebase`, `squash` or `merge`. Also decides which PRs count as ready, since a repo may disable some methods | `rebase` |
| `--repo`, `-r` | `list`, `review` | Only look at this repository in the org | all repos |
| `--mergeable-only` | `list` | Only show PRs that are ready to merge | off |
| `--all`, `-a` | `review` | Also include PRs that can't be merged yet | off |
| `--plain` | `review` | Line-by-line prompts instead of the full-screen UI | off |
| `--no-pager` | `show`, `review` | Print the PR description directly instead of through a pager (with `review`, only applies to `--plain`) | off |
| `--yes`, `-y` | `merge` | Merge without asking for confirmation | off |
| `--help` | all | Show the command's options | |

`show` and `merge` also take the PR to act on as an argument: `REPO#N` (in `--org`),
`OWNER/REPO#N`, or a GitHub PR URL.

## Usage

```sh
dependalot list --org my-org                  # all open Dependabot PRs in the org

dependalot show --org my-org my-repo#12       # release notes, changelog, commits

dependalot merge --org my-org my-repo#12
dependalot merge --org my-org my-repo#12 --yes --method squash

dependalot review --org my-org                # full-screen review of ready-to-merge PRs
dependalot review --org my-org --all          # ...including ones that can't merge yet
dependalot review --org my-org --plain        # line-by-line prompts instead of the full-screen UI
```

### Review screen

`dependalot review` opens a full-screen view: the PR list on the left, and the selected
PR's details on the right — status, then Dependabot's *Release notes*, *Changelog* and
*Commits* as collapsible sections. Supply-chain warnings (*Maintainer changes*,
*Install script changes*) are always expanded.

| Key | Action |
|-----|--------|
| `↑` / `↓` | Select PR |
| `space` / `PgDn` | Scroll the PR description down a page |
| `b` / `PgUp` | Scroll the PR description up a page |
| `e` | Expand / collapse all sections |
| `d` | Hide / show the details pane, widening the PR list |
| `m` | Approve (if needed) and merge — asks to confirm (`y` / `n`) |
| `a` | Approve only |
| `o` | Open PR in browser |
| `s` | Skip to the next PR |
| `r` | Refresh the list from GitHub (e.g. once pending checks finish) |
| `q` | Quit and print a summary |

The mouse wheel also scrolls the description; click a section title to expand or collapse
it, and click links to open them. While the details pane is hidden, a thin strip stays on
the right; click it (or press `d`) to bring the pane back. The full-screen UI needs an interactive terminal;
otherwise `review` falls back to `--plain`.

### When is a PR "ready"?

A PR is offered for merging only when all of these hold:

- you have write (or maintain/admin) access to the repository;
- the chosen merge method is enabled for the repository;
- GitHub reports it mergeable (no conflicts) and the branch isn't behind/draft;
- every status check has passed (PRs with no checks count as passing);
- it isn't blocked by branch protection — except for a missing approval, which
  `dependalot` supplies before merging.

The PR is re-fetched immediately before merging and the merge is pinned to the head
commit you reviewed, so a branch that changes underneath you won't be merged.

## Development

```sh
uv sync
uv run pytest
uv run ruff check
```
