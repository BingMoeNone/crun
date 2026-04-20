# src/claude_run/flags.py
import json
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"
DEFAULT_FLAGS_PATH = DATA_DIR / "flags_default.json"
CUSTOM_FLAGS_PATH = Path.home() / ".config" / "claude-run" / "flags_custom.json"

@dataclass
class Choice:
    value: str
    label: dict[str, str]

    def label_str(self, lang: str) -> str:
        return self.label.get(lang, self.label.get("en", ""))

@dataclass
class RequiredArg:
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

def _parse_flags(data: dict) -> list[Flag]:
    result = []
    for item in data.get("flags", []):
        choices = None
        if "choices" in item:
            choices = [Choice(c["value"], c["label"]) for c in item["choices"]]
        required_args = [
            RequiredArg(a["name"], a["label"], a.get("placeholder"))
            for a in item.get("required_args", [])
        ]
        result.append(Flag(
            flag=item["flag"],
            description=item["description"],
            required_args=required_args,
            type=item["type"],
            group=item["group"],
            choices=choices,
        ))
    return result

def load_flags() -> list[Flag]:
    """Load and merge default + custom flags. Custom overrides default by flag name."""
    with open(DEFAULT_FLAGS_PATH, encoding="utf-8") as f:
        default_flags = _parse_flags(json.load(f))

    custom_flags = []
    if CUSTOM_FLAGS_PATH.exists():
        with open(CUSTOM_FLAGS_PATH, encoding="utf-8") as f:
            custom_flags = _parse_flags(json.load(f))

    default_map = {f.flag: f for f in default_flags}
    for cf in custom_flags:
        default_map[cf.flag] = cf

    return list(default_map.values())