import pytest

from dependalot import browser


def test_open_url_uses_explorer_on_wsl(monkeypatch):
    calls = []
    monkeypatch.setenv("WSL_DISTRO_NAME", "Ubuntu")
    monkeypatch.delenv("BROWSER", raising=False)
    monkeypatch.setattr(browser.shutil, "which", lambda name: name == "explorer.exe")
    monkeypatch.setattr(browser.subprocess, "run", lambda cmd, **kw: calls.append(cmd))
    monkeypatch.setattr(browser.webbrowser, "open", lambda url: pytest.fail("used webbrowser"))
    assert browser.open_url("https://github.com/Dependalot/app/pull/7")
    assert calls == [["explorer.exe", "https://github.com/Dependalot/app/pull/7"]]


def test_open_url_respects_browser_env_on_wsl(monkeypatch):
    opened = []
    monkeypatch.setenv("WSL_DISTRO_NAME", "Ubuntu")
    monkeypatch.setenv("BROWSER", "firefox")
    monkeypatch.setattr(browser.subprocess, "run", lambda *a, **kw: pytest.fail("ran explorer"))
    monkeypatch.setattr(browser.webbrowser, "open", lambda url: opened.append(url) or True)
    assert browser.open_url("https://example.com")
    assert opened == ["https://example.com"]


def test_open_url_uses_webbrowser_off_wsl(monkeypatch):
    opened = []
    monkeypatch.setattr(browser, "is_wsl", lambda: False)
    monkeypatch.setattr(browser.webbrowser, "open", lambda url: opened.append(url) or True)
    assert browser.open_url("https://example.com")
    assert opened == ["https://example.com"]
