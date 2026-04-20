# src/claude_run/config.py
from dataclasses import dataclass, asdict
from pathlib import Path
import json

CONFIG_DIR = Path.home() / ".config" / "claude-run"
PREFERENCES_PATH = CONFIG_DIR / "preferences.json"
FLAGS_CUSTOM_PATH = CONFIG_DIR / "flags_custom.json"

@dataclass
class Preferences:
    search_mode: str = "A"      # "A" / "B" / "both"
    language: str = "zh"        # "zh" / "en"
    first_run: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Preferences":
        return cls(**d)

def ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def save_preferences(prefs: Preferences, path: Path | None = None):
    path = path or PREFERENCES_PATH
    ensure_config_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(prefs.to_dict(), f, indent=2, ensure_ascii=False)

def load_preferences(path: Path | None = None) -> Preferences:
    path = path or PREFERENCES_PATH
    if not path.exists():
        return Preferences()
    try:
        with open(path, encoding="utf-8") as f:
            return Preferences.from_dict(json.load(f))
    except (json.JSONDecodeError, ValueError):
        # Corrupted or invalid config - return defaults
        return Preferences()

def is_first_run() -> bool:
    prefs = load_preferences()
    return prefs.first_run

def mark_first_run_done(path: Path | None = None):
    prefs = load_preferences(path)
    prefs.first_run = False
    save_preferences(prefs, path)
