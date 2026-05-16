from claude_run.app import _sanitize_last_config
from claude_run.flags import load_flags

import json
import tempfile
from pathlib import Path


def test_sanitize_last_config_keeps_valid_items():
    flags = load_flags()
    cfg = {
        "version": 1,
        "selected": [
            {"flag": "--permission-mode", "type": "single", "value": "auto"},
            {"flag": "--bare", "type": "multi", "value": True},
        ],
    }
    selected, dropped = _sanitize_last_config(cfg, flags)
    assert dropped == 0
    assert [s.flag for s in selected] == ["--permission-mode", "--bare"]


def test_sanitize_last_config_drops_unknown_flag():
    flags = load_flags()
    cfg = {
        "version": 1,
        "selected": [
            {"flag": "--not-exists", "type": "multi", "value": True},
            {"flag": "--bare", "type": "multi", "value": True},
        ],
    }
    selected, dropped = _sanitize_last_config(cfg, flags)
    assert dropped == 1
    assert [s.flag for s in selected] == ["--bare"]


def test_sanitize_last_config_drops_invalid_single_choice():
    flags = load_flags()
    cfg = {
        "version": 1,
        "selected": [
            {"flag": "--permission-mode", "type": "single", "value": "invalid-choice"},
        ],
    }
    selected, dropped = _sanitize_last_config(cfg, flags)
    assert dropped == 1
    assert selected == []


def test_validate_upgrade_configs_stale_history():
    """Stale history entries are detected but don't crash validation."""
    from claude_run.__main__ import _validate_upgrade_configs
    from claude_run.config import HISTORY_PATH, save_history_entry

    with tempfile.TemporaryDirectory() as tmpdir:
        hist_path = Path(tmpdir) / "history.json"
        save_history_entry(
            [{"flag": "--not-a-real-flag", "type": "multi", "value": True}],
            "claude --not-a-real-flag",
            config_path=hist_path,
        )
        # Patch HISTORY_PATH and run validation (should not raise)
        import claude_run.config as cfg
        orig = cfg.HISTORY_PATH
        try:
            cfg.HISTORY_PATH = hist_path
            _validate_upgrade_configs()  # just verifies no crash
        finally:
            cfg.HISTORY_PATH = orig


def test_validate_upgrade_configs_no_configs():
    """Validation with no config files should not crash."""
    from claude_run.__main__ import _validate_upgrade_configs
    _validate_upgrade_configs()  # just verifies no crash on empty state
