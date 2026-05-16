# tests/test_config.py
import tempfile
from pathlib import Path
from claude_run.config import (
    Preferences,
    load_preferences,
    save_preferences,
    save_last_config,
    load_last_config,
    _migrate_old_config,
    CONFIG_DIR,
    OLD_CONFIG_DIR,
)


def test_preferences_default():
    p = Preferences()
    assert p.search_mode == "A"
    assert p.language == "zh"
    assert p.first_run == True


def test_preferences_custom():
    p = Preferences(search_mode="B", language="en", first_run=False)
    assert p.search_mode == "B"
    assert p.language == "en"
    assert p.first_run == False


def test_preferences_to_dict():
    p = Preferences(search_mode="both", language="zh", first_run=False)
    d = p.to_dict()
    assert d["search_mode"] == "both"
    assert d["language"] == "zh"
    assert d["first_run"] == False


def test_preferences_from_dict():
    d = {"search_mode": "B", "language": "en", "first_run": False}
    p = Preferences.from_dict(d)
    assert p.search_mode == "B"
    assert p.language == "en"
    assert p.first_run == False


def test_save_and_load_preferences():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "preferences.json"
        prefs = Preferences(search_mode="B", language="en", first_run=False)
        save_preferences(prefs, path)
        loaded = load_preferences(path)
        assert loaded.search_mode == "B"
        assert loaded.language == "en"
        assert loaded.first_run == False


def test_load_nonexistent_returns_default():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "nonexistent.json"
        loaded = load_preferences(path)
        assert loaded.search_mode == "A"
        assert loaded.language == "zh"
        assert loaded.first_run == True


def test_corrupted_json_returns_defaults():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "corrupted.json"
        path.write_text("{ invalid json }", encoding="utf-8")
        loaded = load_preferences(path)
        assert loaded.search_mode == "A"
        assert loaded.language == "zh"
        assert loaded.first_run == True


def test_save_and_load_last_config():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "last_config.json"
        data = {
            "version": 1,
            "saved_at": "2026-04-21T00:00:00+00:00",
            "selected": [
                {"flag": "--model", "type": "single", "value": "sonnet"},
                {"flag": "--bare", "type": "multi", "value": True},
            ],
        }
        save_last_config(data, path)
        loaded = load_last_config(path)
        assert loaded == data


def test_load_last_config_nonexistent_returns_none():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "missing_last_config.json"
        assert load_last_config(path) is None


def test_load_last_config_corrupted_returns_none():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "bad_last_config.json"
        path.write_text("{ invalid json }", encoding="utf-8")
        assert load_last_config(path) is None


def test_load_last_config_invalid_version_returns_none():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "bad_version.json"
        path.write_text('{"version":2,"selected":[]}', encoding="utf-8")
        assert load_last_config(path) is None


def test_migration_renames_old_dir(tmp_path, monkeypatch):
    """旧目录存在、新目录不存在时，自动 rename 迁移。"""
    old = tmp_path / "old_config"
    new = tmp_path / "new_config"
    old.mkdir()
    (old / "preferences.json").write_text('{"search_mode":"A"}', encoding="utf-8")

    monkeypatch.setattr("claude_run.config.OLD_CONFIG_DIR", old)
    monkeypatch.setattr("claude_run.config.CONFIG_DIR", new)

    _migrate_old_config()

    assert new.exists()
    assert not old.exists()
    assert (new / "preferences.json").exists()


def test_migration_both_exist_keeps_new(tmp_path, monkeypatch):
    """新旧目录都存在时，保留新目录不动。"""
    old = tmp_path / "old_config"
    new = tmp_path / "new_config"
    old.mkdir()
    new.mkdir()
    (new / "existing.txt").write_text("keep me", encoding="utf-8")

    monkeypatch.setattr("claude_run.config.OLD_CONFIG_DIR", old)
    monkeypatch.setattr("claude_run.config.CONFIG_DIR", new)

    _migrate_old_config()

    assert old.exists()  # 旧目录不动
    assert new.exists()
    assert (new / "existing.txt").read_text() == "keep me"
