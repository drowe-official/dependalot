import pytest

from dependalot.config import ConfigError, load_settings


def test_settings_come_from_arguments():
    settings = load_settings(org="my-org", method="SQUASH")
    assert (settings.org, settings.merge_method, settings.token) == (
        "my-org",
        "squash",
        "test-token",
    )
    assert load_settings(org="my-org").merge_method == "rebase"


def test_env_and_config_file_are_ignored(monkeypatch, tmp_path):
    monkeypatch.setenv("DEPENDALOT_MERGE_METHOD", "merge")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    (tmp_path / "dependalot").mkdir()
    (tmp_path / "dependalot" / "config.toml").write_text('merge_method = "squash"\n')
    assert load_settings(org="my-org").merge_method == "rebase"


def test_token_still_from_env(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN")
    monkeypatch.setenv("GH_TOKEN", "gh-token")
    assert load_settings(org="my-org").token == "gh-token"
    monkeypatch.delenv("GH_TOKEN")
    with pytest.raises(ConfigError, match="GITHUB_TOKEN"):
        load_settings(org="my-org")


def test_classic_pat_is_rejected(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_classic")
    with pytest.raises(ConfigError, match="Classic PATs"):
        load_settings(org="my-org")
