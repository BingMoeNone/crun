from claude_run.app import _sanitize_last_config
from claude_run.flags import load_flags


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
