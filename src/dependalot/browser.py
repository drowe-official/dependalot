"""Open URLs in the user's browser, including from WSL."""

from __future__ import annotations

import os
import shutil
import subprocess
import webbrowser
from pathlib import Path


def is_wsl() -> bool:
    if os.environ.get("WSL_DISTRO_NAME"):
        return True
    try:
        return "microsoft" in Path("/proc/version").read_text().lower()
    except OSError:
        return False


def open_url(url: str) -> bool:
    """Open a URL, handing off to Windows when running under WSL. Returns False on failure."""
    # An explicit $BROWSER wins; otherwise Python's default (gio/xdg-open) can't reach
    # the Windows browser from WSL.
    if is_wsl() and not os.environ.get("BROWSER"):
        for cmd in (["wslview", url], ["explorer.exe", url]):
            if shutil.which(cmd[0]):
                # explorer.exe exits non-zero even on success, so don't check the status.
                subprocess.run(
                    cmd,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return True
    return webbrowser.open(url)
