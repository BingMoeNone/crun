"""配置管理：用户偏好读写，带回退默认值。"""
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import logging

log = logging.getLogger(__name__)

CONFIG_DIR = Path.home() / ".config" / "claude-run"
PREFERENCES_PATH = CONFIG_DIR / "preferences.json"
FLAGS_CUSTOM_PATH = CONFIG_DIR / "flags_custom.json"


class ConfigError(Exception):
    """配置相关错误，可被上层捕获并友好显示。"""
    pass


@dataclass
class Preferences:
    """用户偏好设置。"""
    search_mode: str = "A"      # "A" / "B" / "both"
    language: str = "zh"        # "zh" / "en"
    first_run: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Preferences":
        # 只取有效字段，忽略多余字段
        valid_keys = {"search_mode", "language", "first_run"}
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
        with open(path, "w", encoding="utf-8") as f:
            json.dump(prefs.to_dict(), f, indent=2, ensure_ascii=False)
    except PermissionError as e:
        raise ConfigError(f"无法写入配置文件 {path}: 权限不足") from e
    except OSError as e:
        raise ConfigError(f"无法写入配置文件 {path}: {e}") from e


def load_preferences(path: Path | None = None) -> Preferences:
    """加载用户偏好，损坏或不存在时返回默认值。"""
    path = path or PREFERENCES_PATH
    if not path.exists():
        return Preferences()

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
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