"""配置管理：用户偏好读写，带回退默认值。"""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import logging
import os
import platform

log = logging.getLogger(__name__)

def _default_config_dir() -> Path:
    """Return the platform-appropriate config directory."""
    if platform.system() == "Windows":
        localappdata = os.environ.get("LOCALAPPDATA", "")
        if localappdata:
            return Path(localappdata) / "crun"
        return Path.home() / "AppData" / "Local" / "crun"
    return Path.home() / ".config" / "crun"


CONFIG_DIR = _default_config_dir()
OLD_CONFIG_DIR = Path.home() / ".config" / "claude-run"
PREFERENCES_PATH = CONFIG_DIR / "preferences.json"
LAST_CONFIG_PATH = CONFIG_DIR / "last_config.json"
HISTORY_PATH = CONFIG_DIR / "history.json"
HISTORY_MAX = 9
CONFIG_VERSION = 1  # current schema version for all config files


def _migrate_old_config() -> None:
    """将旧配置目录迁移到新路径。"""
    if not OLD_CONFIG_DIR.exists():
        return
    if CONFIG_DIR.exists():
        log.info(f"新旧配置目录均存在，使用新路径 {CONFIG_DIR}，旧路径忽略")
        return
    try:
        OLD_CONFIG_DIR.rename(CONFIG_DIR)
        log.info(f"配置已从 {OLD_CONFIG_DIR} 迁移到 {CONFIG_DIR}")
    except OSError as e:
        log.warning(f"配置迁移失败: {e}")


class ConfigError(Exception):
    """配置相关错误，可被上层捕获并友好显示。"""
    pass


@dataclass
class Preferences:
    """用户偏好设置。"""
    search_mode: str = "A"      # "A" / "B" / "both"
    language: str = "zh"        # "zh" / "en"
    first_run: bool = True
    history_mode: str | None = None  # "A" / "B" / None(auto)
    keybindings: dict[str, str] | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Preferences":
        # 只取有效字段，忽略多余字段
        valid_keys = {"search_mode", "language", "first_run", "history_mode", "keybindings"}
        filtered = {k: v for k, v in d.items() if k in valid_keys}
        return cls(**filtered)


def ensure_config_dir() -> None:
    """确保配置目录存在。"""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise ConfigError(f"无法创建配置目录 {CONFIG_DIR}: 权限不足") from e
    except OSError as e:
        raise ConfigError(f"无法创建配置目录 {CONFIG_DIR}: {e}") from e


def save_preferences(prefs: Preferences, path: Path | None = None) -> None:
    """保存用户偏好到 JSON 文件。"""
    path = path or PREFERENCES_PATH
    try:
        ensure_config_dir()
        data = prefs.to_dict()
        data["version"] = CONFIG_VERSION
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except PermissionError as e:
        raise ConfigError(f"无法写入配置文件 {path}: 权限不足") from e
    except OSError as e:
        raise ConfigError(f"无法写入配置文件 {path}: {e}") from e


def load_preferences(path: Path | None = None) -> Preferences:
    """加载用户偏好，损坏或不存在时返回默认值。

    Forward compatible: if file version > CONFIG_VERSION, new fields are
    silently ignored and the known subset is loaded.
    """
    path = path or PREFERENCES_PATH
    if not path.exists():
        return Preferences()

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        file_version = data.get("version", 0)
        if file_version > CONFIG_VERSION:
            log.info(
                f"配置文件 {path} 版本 {file_version} 高于当前支持版本 "
                f"{CONFIG_VERSION}，尝试兼容加载"
            )
        return Preferences.from_dict(data)
    except json.JSONDecodeError as e:
        log.warning(f"配置文件 {path} JSON 损坏: {e}，使用默认值")
        return Preferences()
    except PermissionError as e:
        log.warning(f"无法读取配置文件 {path}: 权限不足，使用默认值")
        return Preferences()
    except OSError as e:
        log.warning(f"无法读取配置文件 {path}: {e}，使用默认值")
        return Preferences()
    except Exception as e:
        log.warning(f"加载配置 {path} 失败: {e}，使用默认值")
        return Preferences()


def is_first_run() -> bool:
    """是否首次运行。"""
    prefs = load_preferences()
    return prefs.first_run


def mark_first_run_done(path: Path | None = None) -> None:
    """标记首次运行已完成。"""
    try:
        prefs = load_preferences(path)
        prefs.first_run = False
        save_preferences(prefs, path)
    except ConfigError:
        # 如果无法保存，静默忽略（不影响后续运行）
        pass


def save_last_config(data: dict, path: Path | None = None) -> None:
    """保存上次执行配置到 JSON 文件。"""
    path = path or LAST_CONFIG_PATH
    try:
        ensure_config_dir()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except PermissionError as e:
        raise ConfigError(f"无法写入配置文件 {path}: 权限不足") from e
    except OSError as e:
        raise ConfigError(f"无法写入配置文件 {path}: {e}") from e


def load_last_config(path: Path | None = None) -> dict | None:
    """加载上次执行配置，损坏或不存在时返回 None。"""
    path = path or LAST_CONFIG_PATH
    if not path.exists():
        return None

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return None
        file_version = data.get("version", 0)
        if file_version < 1 or file_version > CONFIG_VERSION + 1:
            return None  # too old or too new to safely load
        if not isinstance(data.get("selected"), list):
            return None
        return data
    except json.JSONDecodeError as e:
        log.warning(f"配置文件 {path} JSON 损坏: {e}，忽略上次配置")
        return None
    except PermissionError:
        log.warning(f"无法读取配置文件 {path}: 权限不足，忽略上次配置")
        return None
    except OSError as e:
        log.warning(f"无法读取配置文件 {path}: {e}，忽略上次配置")
        return None
    except Exception as e:
        log.warning(f"加载上次配置 {path} 失败: {e}，忽略")
        return None


def load_history(path: Path | None = None) -> list[dict]:
    """Load history entries, return [] if corrupt or missing."""
    path = path or HISTORY_PATH
    if not path.exists():
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return []
        file_version = data.get("version", 0)
        if file_version < 1 or file_version > CONFIG_VERSION + 1:
            return []
        entries = data.get("entries")
        if not isinstance(entries, list):
            return []
        return entries
    except (json.JSONDecodeError, PermissionError, OSError) as e:
        log.warning(f"Failed to load history: {e}")
        return []


def save_history_entry(
    selected_snapshot: list[dict],
    preview: str,
    config_path: Path | None = None,
) -> None:
    """Insert new entry at head, cap at HISTORY_MAX."""
    path = config_path or HISTORY_PATH
    entries = load_history(path)
    existing_data = {}
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                existing_data = json.load(f)
        except Exception:
            pass

    next_id = existing_data.get("next_id", 1)
    for entry in entries:
        if entry.get("id", 0) >= next_id:
            next_id = entry["id"] + 1

    new_entry = {
        "id": next_id,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "preview": preview,
        "selected": selected_snapshot,
    }
    entries.insert(0, new_entry)
    if len(entries) > HISTORY_MAX:
        entries = entries[:HISTORY_MAX]

    data = {"version": 1, "entries": entries, "next_id": next_id + 1}
    try:
        ensure_config_dir()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except (PermissionError, OSError) as e:
        raise ConfigError(f"Cannot write history {path}: {e}") from e


def _migrate_last_config_to_history(
    last_path: Path | None = None,
    hist_path: Path | None = None,
) -> list[dict] | None:
    """Migrate old last_config.json to history.json. Returns migrated entries."""
    last = load_last_config(last_path)
    if not last:
        return None
    preview_items = []
    for item in last.get("selected", []):
        f = item.get("flag", "")
        v = item.get("value")
        if v and v is not True:
            preview_items.append(f"{f} {v}")
        else:
            preview_items.append(f)
    preview = "claude " + " ".join(preview_items)
    save_history_entry(last["selected"], preview, hist_path)
    (last_path or LAST_CONFIG_PATH).unlink(missing_ok=True)
    return load_history(hist_path)


def history_mode_for_terminal(
    user_setting: str | None,
    term_lines: int,
) -> str:
    """Determine history display mode A/B."""
    if user_setting in ("A", "B"):
        return user_setting
    used = 7  # title + separator + status + interaction
    available = term_lines - used
    if available < 10:
        return "B"
    return "A"


PRESETS_PATH = CONFIG_DIR / "presets.json"


def load_presets(path: Path | None = None) -> dict[str, dict]:
    """Return {name: preset_data}, return {} if corrupt."""
    path = path or PRESETS_PATH
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        file_version = data.get("version", 0)
        if file_version < 1 or file_version > CONFIG_VERSION + 1:
            return {}
        presets = data.get("presets")
        if not isinstance(presets, dict):
            return {}
        return presets
    except (json.JSONDecodeError, PermissionError, OSError):
        return {}


def save_preset(name: str, snapshot: list[dict], path: Path | None = None) -> None:
    """Save preset, overwrite if name exists (updates updated_at)."""
    path = path or PRESETS_PATH
    presets = load_presets(path)
    now = datetime.now(timezone.utc).isoformat()
    if name in presets:
        presets[name]["updated_at"] = now
        presets[name]["selected"] = snapshot
    else:
        presets[name] = {
            "created_at": now,
            "updated_at": now,
            "selected": snapshot,
        }
    _write_presets(presets, path)


def delete_preset(name: str, path: Path | None = None) -> None:
    """Delete a preset by name."""
    path = path or PRESETS_PATH
    presets = load_presets(path)
    presets.pop(name, None)
    _write_presets(presets, path)


def _write_presets(presets: dict, path: Path) -> None:
    data = {"version": 1, "presets": presets}
    try:
        ensure_config_dir()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except (PermissionError, OSError) as e:
        raise ConfigError(f"Cannot write presets file {path}: {e}") from e


def _validate_keybindings(kb: dict) -> list[str]:
    """Detect keybinding conflicts, return list of warning messages."""
    warnings = []
    reverse: dict[str, list[str]] = {}
    for action, key_string in kb.items():
        keys = [k.strip() for k in key_string.split(",") if k.strip()]
        for k in keys:
            reverse.setdefault(k, []).append(action)
    for key, actions in reverse.items():
        if len(actions) > 1:
            warnings.append(
                f"Key conflict: '{key}' is bound to {', '.join(actions)}"
            )
    return warnings


def _parse_keybindings(kb: dict) -> dict[str, list[str]]:
    """Parse user keybinding config into {action: [key, ...]}."""
    result = {}
    for action, key_string in kb.items():
        result[action] = [k.strip() for k in key_string.split(",") if k.strip()]
    return result


def _migrate_config_versions() -> None:
    """Migrate all config files to current CONFIG_VERSION.

    Each config file carries its own "version" field. When the app bumps
    CONFIG_VERSION, migration functions here bring old files forward.

    Migration functions are keyed by (file_type, from_version) and return
    the migrated data dict (or None if no migration needed).
    """
    # Register migrations here as version increases.
    # Example for future v1 → v2:
    #   _MIGRATIONS[("preferences", 1)] = _migrate_prefs_v1_to_v2
    _MIGRATIONS: dict[tuple[str, int], callable] = {}

    configs = [
        ("preferences", PREFERENCES_PATH),
        ("history", HISTORY_PATH),
        ("presets", PRESETS_PATH),
    ]

    for cfg_type, cfg_path in configs:
        if not cfg_path.exists():
            continue
        try:
            with open(cfg_path, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, PermissionError, OSError):
            log.warning(f"无法读取 {cfg_path} 进行版本迁移，跳过")
            continue

        file_version = data.get("version", 0)
        if file_version >= CONFIG_VERSION:
            continue  # already current (or ahead — forward compatible)

        migrated = data
        changed = False
        for v in range(file_version, CONFIG_VERSION):
            migrator = _MIGRATIONS.get((cfg_type, v))
            if migrator:
                try:
                    migrated = migrator(migrated)
                    changed = True
                except Exception as e:
                    log.warning(f"迁移 {cfg_type} v{v} → v{v + 1} 失败: {e}，保留原文件")
                    migrated = None
                    break
            # No migrator: version bump is a no-op for data, but we still
            # write the updated version field below.

        if migrated is not None:
            migrated["version"] = CONFIG_VERSION
            try:
                ensure_config_dir()
                with open(cfg_path, "w", encoding="utf-8") as f:
                    json.dump(migrated, f, indent=2, ensure_ascii=False)
                log.info(f"已迁移 {cfg_type} 配置到版本 {CONFIG_VERSION}")
            except (PermissionError, OSError) as e:
                log.warning(f"无法写入迁移后的 {cfg_type} 配置: {e}")


# 模块加载时自动迁移旧配置
_migrate_old_config()
_migrate_config_versions()
