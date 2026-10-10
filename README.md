# dependalot

Triage Dependabot pull requests across a whole GitHub organization from the terminal:
list them, read the release notes / changelog / commits Dependabot attaches, and
approve + merge the ones whose checks have passed — in a keypress.

## Install

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```sh
uv tool install .          # puts `dependalot` on your PATH
# or, from a checkout:
uv run dependalot --help
```

### Windows

Use [Windows Terminal](https://aka.ms/terminal) (the default on Windows 11). The
full-screen `review` UI needs a modern terminal, and the old console host doesn't render
it properly. In PowerShell:

1. Install uv (or use `winget install --id=astral-sh.uv -e`), then open a new terminal so
   `uv` is on your `PATH`:

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Install Python 3.13 if you don't have it. uv manages its own copy, so this doesn't
   affect any other Python on the machine:

   ```powershell
   uv python install 3.13
   ```

3. From a checkout of this repository, install dependalot and add uv's tool directory to
   your `PATH`, then open a new terminal:

   ```powershell
   uv tool install .
   uv tool update-shell
   ```

4. Set your token (see [Authentication](#authentication)) and check it works:

   ```powershell
   $env:GITHUB_TOKEN = "ghp_..."
   dependalot list --org my-org
   ```

If `show` or `review --plain` prints raw escape codes like `←[1m` through the pager, add
`--no-pager`.

Alternatively, run dependalot inside [WSL](https://learn.microsoft.com/windows/wsl/) and
follow the Linux steps. Opening PRs in the browser (`o` in the review screen) still opens
your Windows browser.

## Authentication

Export a GitHub token as `GITHUB_TOKEN` (or `GH_TOKEN`):

- **Classic PAT:** `repo` scope.
- **Fine-grained PAT** (resource owner: the org): *Pull requests* read/write,
  *Contents* read/write, *Checks* and *Commit statuses* read.

```sh
export GITHUB_TOKEN=ghp_...
```

On Windows, in PowerShell:

```powershell
$env:GITHUB_TOKEN = "ghp_..."        # this terminal only
setx GITHUB_TOKEN "ghp_..."          # saved for new terminals (not the current one)
```

In `cmd.exe`, use `set GITHUB_TOKEN=ghp_...`. `DEPENDALOT_ORG` is set the same way.

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
dependalot list --org my-org --repo my-repo --mergeable-only

dependalot show --org my-org my-repo#12       # release notes, changelog, commits
dependalot show --org my-org https://github.com/my-org/my-repo/pull/12

dependalot merge --org my-org my-repo#12      # approve (if needed) + merge, with confirmation
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

The scroll keys work while the PR list keeps focus, so `↑`/`↓` always move between PRs.
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
