"""参数定义与加载：支持默认 + 用户自定义合并。"""
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger(__name__)


def _default_flags_path() -> Path:
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return Path(meipass) / "data" / "flags_default.json"
    return Path(__file__).parent.parent.parent / "data" / "flags_default.json"


DEFAULT_FLAGS_PATH = _default_flags_path()
CUSTOM_FLAGS_PATH = Path.home() / ".config" / "claude-run" / "flags_custom.json"


class FlagsLoadError(Exception):
    """参数加载错误，可被上层捕获并友好显示。"""
    pass


@dataclass
class Choice:
    """单选项。"""
    value: str
    label: dict[str, str]

    def label_str(self, lang: str) -> str:
        return self.label.get(lang, self.label.get("en", ""))


@dataclass
class RequiredArg:
    """必填子参数。"""
    name: str
    label: dict[str, str]
    placeholder: dict[str, str] | None = None

    def label_str(self, lang: str) -> str:
        return self.label.get(lang, self.label.get("en", ""))

    def placeholder_str(self, lang: str) -> str:
        if self.placeholder:
            return self.placeholder.get(lang, self.placeholder.get("en", ""))
        return ""


@dataclass
class Flag:
    """一个 Claude CLI 参数。"""
    flag: str
    description: dict[str, str]
    required_args: list[RequiredArg]
    type: str  # "single" | "multi" | "value"
    group: str
    choices: list[Choice] | None = None

    def label(self, lang: str) -> str:
        return self.description.get(lang, self.description.get("en", ""))

    def requires_value(self) -> bool:
        return self.type == "value" and len(self.required_args) > 0

    def get_choices(self, lang: str) -> list[dict]:
        if not self.choices:
            return []
        return [{"value": c.value, "label": c.label_str(lang)} for c in self.choices]


@dataclass
class FlagGroup:
    """分组容器。"""
    name: str
    label_zh: str
    label_en: str
    flags: list["Flag"]

    def label(self, lang: str) -> str:
        return self.label_zh if lang == "zh" else self.label_en

    @staticmethod
    def group_by(flags: list["Flag"]) -> dict[str, list["Flag"]]:
        groups: dict[str, list["Flag"]] = {}
        for f in flags:
            groups.setdefault(f.group, []).append(f)
        return groups


def _parse_choice(item: dict) -> Choice | None:
    """解析单个 Choice，字段缺失时返回 None。"""
    if "value" not in item or "label" not in item:
        return None
    return Choice(item["value"], item.get("label", {"en": "", "zh": ""}))


def _parse_required_arg(item: dict) -> RequiredArg | None:
    """解析单个 RequiredArg，字段缺失时返回 None。"""
    if "name" not in item or "label" not in item:
        return None
    return RequiredArg(item["name"], item.get("label", {}), item.get("placeholder"))


def _parse_flags(data: dict) -> list[Flag]:
    """解析 flags 数组，跳过无效条目。"""
    result = []
    for item in data.get("flags", []):
        try:
            flag_name = item.get("flag", "")
            if not flag_name:
                log.warning("跳过无 flag 字段的条目")
                continue

            description = item.get("description", {"en": "", "zh": ""})
            if not isinstance(description, dict):
                description = {"en": str(description), "zh": str(description)}

            required_args = []
            for a in item.get("required_args", []):
                arg = _parse_required_arg(a)
                if arg:
                    required_args.append(arg)

            choices = None
            if "choices" in item:
                choices = [_parse_choice(c) for c in item["choices"] if _parse_choice(c)]

            flag_type = item.get("type", "multi")
            if flag_type not in ("single", "multi", "value"):
                flag_type = "multi"

            group = item.get("group", "uncategorized")

            result.append(Flag(
                flag=flag_name,
                description=description,
                required_args=required_args,
                type=flag_type,
                group=group,
                choices=choices,
            ))
        except Exception as e:
            log.warning(f"解析参数条目失败: {e}，跳过")
            continue
    return result


def load_flags() -> list[Flag]:
    """
    加载并合并默认 + 用户自定义参数。
    用户自定义同名参数覆盖默认。
    """
    # 加载默认参数（必须成功，否则抛错）
    if not DEFAULT_FLAGS_PATH.exists():
        raise FlagsLoadError(f"默认参数文件不存在: {DEFAULT_FLAGS_PATH}")

    try:
        with open(DEFAULT_FLAGS_PATH, encoding="utf-8") as f:
            default_data = json.load(f)
        default_flags = _parse_flags(default_data)
    except json.JSONDecodeError as e:
        raise FlagsLoadError(f"默认参数文件 JSON 损坏: {e}")
    except PermissionError as e:
        raise FlagsLoadError(f"无法读取默认参数文件: 权限不足")
    except OSError as e:
        raise FlagsLoadError(f"无法读取默认参数文件: {e}")

    # 加载用户自定义参数（可选，失败时静默忽略）
    custom_flags = []
    if CUSTOM_FLAGS_PATH.exists():
        try:
            with open(CUSTOM_FLAGS_PATH, encoding="utf-8") as f:
                custom_data = json.load(f)
            custom_flags = _parse_flags(custom_data)
        except json.JSONDecodeError as e:
            log.warning(f"用户自定义参数文件 JSON 损坏: {e}，忽略")
        except PermissionError:
            log.warning(f"无法读取用户自定义参数文件: 权限不足，忽略")
        except OSError as e:
            log.warning(f"无法读取用户自定义参数文件: {e}，忽略")

    # 合并：用户自定义覆盖默认
    default_map = {f.flag: f for f in default_flags}
    for cf in custom_flags:
        default_map[cf.flag] = cf

    return list(default_map.values())