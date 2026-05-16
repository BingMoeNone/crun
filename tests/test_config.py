# tests/test_config.py
import json
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
        path.write_text('{"version":999,"selected":[]}', encoding="utf-8")
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


# ── History API tests ─────────────────────────────────────────────────────────

from claude_run.config import (
    load_history, save_history_entry, HISTORY_PATH, history_mode_for_terminal,
)

def test_save_and_load_history(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "history.json"
        monkeypatch.setattr("claude_run.config.HISTORY_PATH", path)

        save_history_entry(
            [{"flag": "--model", "type": "single", "value": "sonnet"}],
            "claude --model sonnet",
            config_path=path,
        )
        entries = load_history(path)
        assert len(entries) == 1
        assert entries[0]["preview"] == "claude --model sonnet"
        assert entries[0]["id"] == 1


def test_history_max_9():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "history.json"
        for i in range(12):
            save_history_entry(
                [{"flag": f"--flag{i}", "type": "multi", "value": True}],
                f"claude --flag{i}",
                config_path=path,
            )
        entries = load_history(path)
        assert len(entries) == 9
        # newest first (highest id)
        assert entries[0]["preview"] == "claude --flag11"


def test_load_history_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "nonexistent.json"
        assert load_history(path) == []


def test_lost_config_migration(monkeypatch):
    """old last_config.json → history.json migration"""
    with tempfile.TemporaryDirectory() as tmpdir:
        last_path = Path(tmpdir) / "last_config.json"
        hist_path = Path(tmpdir) / "history.json"
        last_data = {
            "version": 1,
            "saved_at": "2026-05-16T00:00:00Z",
            "selected": [{"flag": "--bare", "type": "multi", "value": True}],
        }
        import json
        last_path.write_text(json.dumps(last_data))
        from claude_run.config import _migrate_last_config_to_history
        _migrate_last_config_to_history(last_path, hist_path)
        assert not last_path.exists()  # old file deleted
        entries = load_history(hist_path)
        assert len(entries) == 1
        assert entries[0]["selected"][0]["flag"] == "--bare"


def test_history_mode_adaptive():
    # large terminal → A
    assert history_mode_for_terminal(None, 40) == "A"
    # small terminal → B (less than 10% space remaining)
    assert history_mode_for_terminal(None, 14) == "B"
    # user setting takes priority
    assert history_mode_for_terminal("B", 40) == "B"
    assert history_mode_for_terminal("A", 14) == "A"


# ── Presets API tests ──────────────────────────────────────────────────────────

from claude_run.config import load_presets, save_preset, delete_preset, PRESETS_PATH


def test_save_and_load_presets():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "presets.json"

        save_preset("开发模式", [{"flag": "--bare", "type": "multi", "value": True}], path)
        presets = load_presets(path)
        assert "开发模式" in presets
        assert presets["开发模式"]["selected"][0]["flag"] == "--bare"


def test_preset_overwrite():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "presets.json"
        save_preset("test", [{"flag": "--a", "type": "multi", "value": True}], path)
        save_preset("test", [{"flag": "--b", "type": "multi", "value": True}], path)
        presets = load_presets(path)
        assert presets["test"]["selected"][0]["flag"] == "--b"


def test_delete_preset():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "presets.json"
        save_preset("test", [{"flag": "--bare", "type": "multi", "value": True}], path)
        delete_preset("test", path)
        presets = load_presets(path)
        assert "test" not in presets


def test_load_presets_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "nonexistent.json"
        assert load_presets(path) == {}


# ── Keybindings tests ───────────────────────────────────────────────────────────

from claude_run.config import _validate_keybindings, _parse_keybindings


def test_parse_keybindings():
    kb = {"up": "k, up", "down": "j, down", "toggle": "space"}
    result = _parse_keybindings(kb)
    assert result["up"] == ["k", "up"]
    assert result["down"] == ["j", "down"]
    assert result["toggle"] == ["space"]


def test_keybindings_validation_no_conflict():
    kb = {"up": "k, up", "down": "j, down", "toggle": "space"}
    warnings = _validate_keybindings(kb)
    assert len(warnings) == 0


def test_keybindings_validation_conflict():
    kb = {"up": "k", "down": "k, j"}
    warnings = _validate_keybindings(kb)
    assert len(warnings) >= 1
    assert "k" in warnings[0]


def test_keybindings_validation_strips_whitespace():
    kb = {"up": " k , up ", "down": " j , down "}
    warnings = _validate_keybindings(kb)
    assert len(warnings) == 0


# ── Config version migration tests ──────────────────────────────────────────────

from claude_run.config import CONFIG_VERSION, _migrate_config_versions


def test_save_preferences_includes_version():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "preferences.json"
        prefs = Preferences(search_mode="A", language="zh", first_run=False)
        save_preferences(prefs, path)
        import json
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["version"] == CONFIG_VERSION
        assert data["search_mode"] == "A"


def test_load_preferences_without_version_field():
    """v0 config (no version field) should load as version-0 compat."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "preferences.json"
        path.write_text(
            '{"search_mode":"B","language":"en","first_run":false}',
            encoding="utf-8",
        )
        loaded = load_preferences(path)
        assert loaded.search_mode == "B"
        assert loaded.language == "en"
        assert loaded.first_run == False


def test_load_preferences_forward_compat():
    """Config with future version should still load known fields."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "preferences.json"
        path.write_text(
            '{"version":999,"search_mode":"both","language":"zh",'
            '"first_run":false,"future_field":"should_be_ignored"}',
            encoding="utf-8",
        )
        loaded = load_preferences(path)
        assert loaded.search_mode == "both"
        assert loaded.language == "zh"


def test_migrate_config_versions_adds_version_to_prefs():
    """Old prefs without version get version field added on migration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "preferences.json"
        path.write_text(
            '{"search_mode":"B","language":"en","first_run":false}',
            encoding="utf-8",
        )
        # Setup: override PREFERENCES_PATH and CONFIG_VERSION
        import claude_run.config as cfg
        orig = cfg.PREFERENCES_PATH
        try:
            cfg.PREFERENCES_PATH = path
            _migrate_config_versions()
            data = json.loads(path.read_text(encoding="utf-8"))
            assert data["version"] == CONFIG_VERSION
        finally:
            cfg.PREFERENCES_PATH = orig


def test_load_history_forward_compat():
    """History with slightly higher version should still load."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "history.json"
        future_ver = CONFIG_VERSION + 1
        path.write_text(
            json.dumps({
                "version": future_ver,
                "entries": [{
                    "id": 1, "preview": "test",
                    "selected": [{"flag": "--bare", "type": "multi", "value": True}],
                    "saved_at": "2026-05-17T00:00:00Z",
                }],
                "next_id": 2,
            }),
            encoding="utf-8",
        )
        entries = load_history(path)
        assert len(entries) == 1
        assert entries[0]["preview"] == "test"


def test_load_presets_forward_compat():
    """Presets with slightly higher version should still load."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "presets.json"
        future_ver = CONFIG_VERSION + 1
        path.write_text(
            json.dumps({
                "version": future_ver,
                "presets": {
                    "test": {
                        "created_at": "2026-05-17T00:00:00Z",
                        "updated_at": "2026-05-17T00:00:00Z",
                        "selected": [{"flag": "--bare", "type": "multi", "value": True}],
                    }
                },
            }),
            encoding="utf-8",
        )
        presets = load_presets(path)
        assert "test" in presets
        assert presets["test"]["selected"][0]["flag"] == "--bare"


def test_load_history_way_too_new_returns_empty():
    """History version too far ahead → empty (unsafe to load)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "history.json"
        path.write_text(
            json.dumps({"version": 999, "entries": [], "next_id": 1}),
            encoding="utf-8",
        )
        entries = load_history(path)
        assert entries == []
