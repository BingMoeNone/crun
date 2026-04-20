# claude-run 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标：** 构建 `claude-run` CLI 工具，通过 TUI 交互选择 Claude CLI 参数后执行。

**架构概述：** Python 3.10+ 项目，使用 uv 管理环境，Textual 构建 TUI，配置文件 JSON 格式存储参数和用户偏好，三种交互模式（快速选择/模糊搜索/统一搜索）通过首次引导让用户选择。

**技术栈：** Python 3.10+ / uv / Textual / fuzzywuzzy（或自实现）/ JSON

---

## 文件结构

```
claude-run/
├── pyproject.toml
├── src/claude_run/
│   ├── __init__.py
│   ├── __main__.py        # 入口：python -m claude_run
│   ├── config.py           # 偏好加载 + 配置文件读写
│   ├── flags.py            # 参数定义 + custom/default Merge
│   ├── search.py           # 模糊搜索匹配引擎
│   ├── runner.py           # 组装并 exec claude 命令
│   ├── wizard.py            # 首次运行引导界面
│   └── app.py               # Textual TUI 主应用
├── data/
│   └── flags_default.json  # 默认参数集
└── tests/
    ├── test_config.py
    ├── test_flags.py
    ├── test_search.py
    └── test_runner.py
```

---

## Task 1: 项目脚手架

**Files:**
- Create: `pyproject.toml`
- Create: `src/claude_run/__init__.py`
- Create: `src/claude_run/__main__.py`

- [ ] **Step 1: 创建 pyproject.toml**

```toml
[project]
name = "claude-run"
version = "0.1.0"
description = "TUI tool for selecting Claude CLI flags"
requires-python = ">=3.10"
dependencies = ["textual>=0.50.0"]

[project.scripts]
claude-run = "claude_run.__main__:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Run: `uv init --name claude-run` 初始化项目，将自动生成 pyproject.toml 和基础结构。

- [ ] **Step 2: 创建目录结构**

```bash
mkdir -p src/claude_run data tests
touch src/claude_run/__init__.py
```

- [ ] **Step 3: 验证项目可运行**

Run: `uv run python -m claude_run --help`
Expected: 报错 `No module named 'claude_run'`（尚未安装模块）

- [ ] **Step 4: 提交**

```bash
git add pyproject.toml src/claude_run/__init__.py
git commit -m "chore: scaffold project with uv and textual"
```

---

## Task 2: 默认参数数据集 flags_default.json

**Files:**
- Create: `data/flags_default.json`
- Test: `tests/test_flags.py`

- [ ] **Step 1: 编写测试，验证 JSON 结构完整性**

```python
# tests/test_flags.py
import json
import os

def get_flags_path():
    return os.path.join(os.path.dirname(__file__), "..", "..", "data", "flags_default.json")

def test_flags_json_valid():
    path = get_flags_path()
    with open(path) as f:
        data = json.load(f)
    assert data["version"] == 1
    assert "flags" in data
    assert len(data["flags"]) > 0

def test_flag_structure():
    path = get_flags_path()
    with open(path) as f:
        data = json.load(f)
    for flag in data["flags"]:
        assert "flag" in flag
        assert "description" in flag
        assert "zh" in flag["description"]
        assert "en" in flag["description"]
        assert "type" in flag
        assert "group" in flag
        assert flag["type"] in ("single", "multi", "value")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_flags.py -v`
Expected: FAIL (flags_default.json 不存在)

- [ ] **Step 3: 创建 data/flags_default.json**

包含所有 Claude CLI 标志，按以下分组：

**model 组：**
```json
{
  "flag": "--model",
  "description": { "zh": "当前会话使用的模型", "en": "Model for the current session" },
  "required_args": [],
  "type": "single",
  "group": "model",
  "choices": [
    { "value": "opus", "label": { "zh": "Opus", "en": "Opus" } },
    { "value": "sonnet", "label": { "zh": "Sonnet", "en": "Sonnet" } },
    { "value": "haiku", "label": { "zh": "Haiku", "en": "Haiku" } }
  ]
}
```

**permission 组：**
```json
{
  "flag": "--permission-mode",
  "description": { "zh": "当前会话的权限模式", "en": "Permission mode for the session" },
  "required_args": [],
  "type": "single",
  "group": "permission",
  "choices": [
    { "value": "acceptEdits", "label": { "zh": "Accept Edits", "en": "Accept Edits" } },
    { "value": "auto", "label": { "zh": "Auto", "en": "Auto" } },
    { "value": "bypassPermissions", "label": { "zh": "Bypass Permissions", "en": "Bypass Permissions" } },
    { "value": "default", "label": { "zh": "Default", "en": "Default" } },
    { "value": "dontAsk", "label": { "zh": "Don't Ask", "en": "Don't Ask" } },
    { "value": "plan", "label": { "zh": "Plan", "en": "Plan" } }
  ]
}
```

**output 组（多选）：**
```json
{
  "flag": "-p",
  "description": { "zh": "打印输出后退出（非交互模式）", "en": "Print response and exit (non-interactive)" },
  "required_args": [],
  "type": "multi",
  "group": "output"
}
```
```json
{
  "flag": "--output-format",
  "description": { "zh": "输出格式", "en": "Output format for print mode" },
  "required_args": [],
  "type": "single",
  "group": "output",
  "choices": [
    { "value": "text", "label": { "zh": "Text", "en": "Text" } },
    { "value": "json", "label": { "zh": "JSON", "en": "JSON" } },
    { "value": "stream-json", "label": { "zh": "Stream JSON", "en": "Stream JSON" } }
  ]
}
```
```json
{
  "flag": "--json-schema",
  "description": { "zh": "结构化输出的 JSON Schema 验证", "en": "JSON Schema for structured output validation" },
  "required_args": [{ "name": "schema", "label": { "zh": "Schema", "en": "Schema" }, "placeholder": { "zh": "例: {\"type\":\"object\"}", "en": "e.g. {\"type\":\"object\"}" } }],
  "type": "value",
  "group": "output"
}
```

**session 组（多选）：**
```json
{
  "flag": "-c",
  "description": { "zh": "继续当前目录最近的会话", "en": "Continue the most recent conversation" },
  "required_args": [],
  "type": "multi",
  "group": "session"
}
```
```json
{
  "flag": "--continue",
  "description": { "zh": "继续当前目录最近的会话（同 -c）", "en": "Continue the most recent conversation" },
  "required_args": [],
  "type": "multi",
  "group": "session"
}
```
```json
{
  "flag": "-r",
  "description": { "zh": "通过会话 ID 恢复会话，或打开交互选择器", "en": "Resume a conversation by session ID" },
  "required_args": [{ "name": "session_id", "label": { "zh": "会话 ID", "en": "Session ID" }, "placeholder": { "zh": "例: abc-123", "en": "e.g. abc-123" } }],
  "type": "value",
  "group": "session"
}
```
```json
{
  "flag": "--resume",
  "description": { "zh": "恢复会话（同 -r）", "en": "Resume a conversation" },
  "required_args": [{ "name": "session_id", "label": { "zh": "会话 ID", "en": "Session ID" }, "placeholder": { "zh": "例: abc-123", "en": "e.g. abc-123" } }],
  "type": "value",
  "group": "session"
}
```
```json
{
  "flag": "--fork-session",
  "description": { "zh": "恢复时创建新的会话 ID", "en": "Create a new session ID when resuming" },
  "required_args": [],
  "type": "multi",
  "group": "session"
}
```
```json
{
  "flag": "--session-id",
  "description": { "zh": "使用指定 UUID 的会话", "en": "Use a specific session ID" },
  "required_args": [{ "name": "uuid", "label": { "zh": "UUID", "en": "UUID" }, "placeholder": { "zh": "例: 550e8400-e29b-41d4-a716-446655440000", "en": "e.g. 550e8400-e29b-41d4-a716-446655440000" } }],
  "type": "value",
  "group": "session"
}
```

**tools 组：**
```json
{
  "flag": "--tools",
  "description": { "zh": "指定可用的内置工具", "en": "Specify available built-in tools" },
  "required_args": [],
  "type": "single",
  "group": "tools",
  "choices": [
    { "value": "default", "label": { "zh": "所有工具（默认）", "en": "All tools (default)" } },
    { "value": "", "label": { "zh": "禁用所有工具", "en": "Disable all tools" } },
    { "value": "Bash,Edit,Read", "label": { "zh": "仅 Bash/Edit/Read", "en": "Bash/Edit/Read only" } }
  ]
}
```

**dev 组（多选）：**
```json
{
  "flag": "--bare",
  "description": { "zh": "最小化模式：跳过 hooks、LSP、插件同步、归属、auto-memory 等", "en": "Minimal mode: skip hooks, LSP, plugin sync, attribution, auto-memory" },
  "required_args": [],
  "type": "multi",
  "group": "dev"
}
```
```json
{
  "flag": "--disable-slash-commands",
  "description": { "zh": "禁用所有 skills", "en": "Disable all slash command skills" },
  "required_args": [],
  "type": "multi",
  "group": "dev"
}
```
```json
{
  "flag": "--strict-mcp-config",
  "description": { "zh": "仅使用 --mcp-config 指定的 MCP 服务器", "en": "Only use MCP servers from --mcp-config, ignoring other MCP configurations" },
  "required_args": [],
  "type": "multi",
  "group": "dev"
}
```

**mcp 组：**
```json
{
  "flag": "--mcp-config",
  "description": { "zh": "从 JSON 文件加载 MCP 服务器配置", "en": "Load MCP servers from JSON files" },
  "required_args": [{ "name": "config_path", "label": { "zh": "配置文件路径", "en": "Config file path" }, "placeholder": { "zh": "例: /path/to/mcp.json", "en": "e.g. /path/to/mcp.json" } }],
  "type": "value",
  "group": "mcp"
}
```

**debug 组（多选）：**
```json
{
  "flag": "-d",
  "description": { "zh": "启用调试模式", "en": "Enable debug mode" },
  "required_args": [],
  "type": "multi",
  "group": "debug"
}
```
```json
{
  "flag": "--debug",
  "description": { "zh": "启用调试模式（可指定分类过滤）", "en": "Enable debug mode with optional category filtering" },
  "required_args": [{ "name": "filter", "label": { "zh": "过滤分类", "en": "Filter category" }, "placeholder": { "zh": "例: api,hooks", "en": "e.g. api,hooks" } }],
  "type": "value",
  "group": "debug"
}
```
```json
{
  "flag": "--debug-file",
  "description": { "zh": "将调试日志写入指定文件", "en": "Write debug logs to a specific file path" },
  "required_args": [{ "name": "path", "label": { "zh": "日志文件路径", "en": "Log file path" }, "placeholder": { "zh": "例: /tmp/claude-debug.log", "en": "e.g. /tmp/claude-debug.log" } }],
  "type": "value",
  "group": "debug"
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_flags.py -v`
Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add data/flags_default.json tests/test_flags.py
git commit -m "data: add flags_default.json with all Claude CLI flags"
```

---

## Task 3: 配置管理 config.py

**Files:**
- Create: `src/claude_run/config.py`
- Test: `tests/test_config.py`

- [ ] **Step 1: 编写测试**

```python
# tests/test_config.py
import os
import json
import tempfile
from pathlib import Path
from claude_run.config import Preferences, load_preferences, save_preferences

def test_preferences_default():
    p = Preferences()
    assert p.search_mode == "A"  # default to A
    assert p.language == "zh"    # default to zh
    assert p.first_run == True

def test_preferences_merge():
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

def test_save_and_load_preferences():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "preferences.json"
        prefs = Preferences(search_mode="B", language="en", first_run=False)
        save_preferences(prefs, path)
        loaded = load_preferences(path)
        assert loaded.search_mode == "B"
        assert loaded.language == "en"
        assert loaded.first_run == False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_config.py -v`
Expected: FAIL (claude_run.config 不存在)

- [ ] **Step 3: 实现 config.py**

```python
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
    with open(path, encoding="utf-8") as f:
        return Preferences.from_dict(json.load(f))

def is_first_run() -> bool:
    prefs = load_preferences()
    return prefs.first_run

def mark_first_run_done(path: Path | None = None):
    prefs = load_preferences(path)
    prefs.first_run = False
    save_preferences(prefs, path)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_config.py -v`
Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add src/claude_run/config.py tests/test_config.py
git commit -m "feat: add preferences config management"
```

---

## Task 4: 参数合并与解析 flags.py

**Files:**
- Create: `src/claude_run/flags.py`
- Test: `tests/test_flags.py`（扩展）

- [ ] **Step 1: 编写测试**

```python
# tests/test_flags.py 新增以下测试
import json
import os
from claude_run.flags import Flag, FlagGroup, load_flags

def get_flags_path():
    return os.path.join(os.path.dirname(__file__), "..", "..", "data", "flags_default.json")

def test_load_flags_default():
    flags = load_flags()
    group_map = {f.group for f in flags}
    assert "model" in group_map
    assert "permission" in group_map
    assert "session" in group_map
    assert "output" in group_map
    assert "tools" in group_map
    assert "dev" in group_map
    assert "debug" in group_map
    assert "mcp" in group_map

def test_flag_has_label():
    flags = load_flags()
    model_flag = next(f for f in flags if f.flag == "--model")
    assert model_flag.label("zh") == "当前会话使用的模型"
    assert model_flag.label("en") == "Model for the current session"

def test_flag_get_display_choices():
    flags = load_flags()
    model_flag = next(f for f in flags if f.flag == "--model")
    choices = model_flag.get_choices("zh")
    assert len(choices) == 3
    assert choices[0]["value"] == "opus"

def test_flag_requires_value():
    flags = load_flags()
    mcp_flag = next(f for f in flags if f.flag == "--mcp-config")
    assert mcp_flag.requires_value() == True
    assert mcp_flag.required_args[0].label("zh") == "配置文件路径"

def test_group_flags():
    flags = load_flags()
    groups = FlagGroup.group_by(flags)
    assert "model" in groups
    assert all(f.group == "model" for f in groups["model"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_flags.py -v`
Expected: FAIL (claude_run.flags 不存在)

- [ ] **Step 3: 实现 flags.py**

```python
# src/claude_run/flags.py
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent.parent.parent / "data"
DEFAULT_FLAGS_PATH = DATA_DIR / "flags_default.json"
CUSTOM_FLAGS_PATH = Path.home() / ".config" / "claude-run" / "flags_custom.json"

@dataclass
class Choice:
    value: str
    label: dict[str, str]  # {"zh": "...", "en": "..."}

    def label(self, lang: str) -> str:
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
        return [{"value": c.value, "label": c.label(lang)} for c in self.choices]

@dataclass
class FlagGroup:
    name: str
    label_zh: str
    label_en: str
    flags: list[Flag]

    def label(self, lang: str) -> str:
        return self.label_zh if lang == "zh" else self.label_en

    @staticmethod
    def group_by(flags: list[Flag]) -> dict[str, list[Flag]]:
        groups: dict[str, list[Flag]] = {}
        for f in flags:
            groups.setdefault(f.group, []).append(f)
        return groups

def _parse_flags(data: dict) -> list[Flag]:
    result = []
    for item in data.get("flags", []):
        choices = None
        if "choices" in item:
            choices = [Choice(c["value"], c["label"]) for c in item["choices"]]
        required_args = [RequiredArg(a["name"], a["label"], a.get("placeholder")) for a in item.get("required_args", [])]
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
    """Load and merge default + custom flags. Custom overrides default."""
    with open(DEFAULT_FLAGS_PATH, encoding="utf-8") as f:
        default_flags = _parse_flags(json.load(f))

    custom_flags = []
    if CUSTOM_FLAGS_PATH.exists():
        with open(CUSTOM_FLAGS_PATH, encoding="utf-8") as f:
            custom_flags = _parse_flags(json.load(f))

    # Merge: custom overrides default by flag name
    default_map = {f.flag: f for f in default_flags}
    for cf in custom_flags:
        default_map[cf.flag] = cf

    return list(default_map.values())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_flags.py -v`
Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add src/claude_run/flags.py
git commit -m "feat: add flag definition, parsing and merge logic"
```

---

## Task 5: 搜索匹配引擎 search.py

**Files:**
- Create: `src/claude_run/search.py`
- Test: `tests/test_search.py`

- [ ] **Step 1: 编写测试**

```python
# tests/test_search.py
from claude_run.search import fuzzy_match, search_flags

# Mock flag data
class MockFlag:
    def __init__(self, flag, label_zh, label_en):
        self.flag = flag
        self._label_zh = label_zh
        self._label_en = label_en
        self.description = {"zh": label_zh, "en": label_en}

    def label(self, lang):
        return self._label_zh if lang == "zh" else self._label_en

FLAGS = [
    MockFlag("--model", "当前会话使用的模型", "Model for the current session"),
    MockFlag("--mcp-config", "从 JSON 文件加载 MCP 服务器配置", "Load MCP servers from JSON files"),
    MockFlag("-d", "启用调试模式", "Enable debug mode"),
    MockFlag("--debug-file", "将调试日志写入指定文件", "Write debug logs to a specific file path"),
]

def test_fuzzy_match_exact():
    assert fuzzy_match("model", "model") > 0
    assert fuzzy_match("mcp", "mcp-config") > 0
    assert fuzzy_match("debug", "debug") > 0

def test_fuzzy_match_zh():
    assert fuzzy_match("调试", "调试模式") > 0
    assert fuzzy_match("模型", "当前会话使用的模型") > 0

def test_fuzzy_match_no_match():
    assert fuzzy_match("xyz", "model") == 0

def test_search_flags_by_flag_name():
    results = search_flags(FLAGS, "mcp", lang="en")
    assert len(results) > 0
    assert any(r.flag == "--mcp-config" for r in results)

def test_search_flags_by_zh_description():
    results = search_flags(FLAGS, "调试", lang="zh")
    assert len(results) >= 2  # -d and --debug-file

def test_search_flags_by_en_description():
    results = search_flags(FLAGS, "debug", lang="en")
    assert len(results) >= 2

def test_search_flags_case_insensitive():
    results = search_flags(FLAGS, "MODEL", lang="en")
    assert any(r.flag == "--model" for r in results)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_search.py -v`
Expected: FAIL

- [ ] **Step 3: 实现 search.py**

```python
# src/claude_run/search.py
from typing import Sequence

def fuzzy_match(query: str, target: str) -> int:
    """
    Simple fuzzy matching returning a score > 0 if query matches target.
    Higher score = better match. 0 = no match.
    """
    query = query.lower()
    target = target.lower()

    if query == target:
        return 100
    if target.startswith(query):
        return 80
    if query in target:
        return 60

    # Subsequence match
    qi = 0
    score = 0
    consecutive = 0
    for ch in target:
        if qi < len(query) and ch == query[qi]:
            qi += 1
            consecutive += 1
            score += consecutive * 5
    if qi == len(query):
        return score + 20

    return 0

def search_flags(flags: Sequence, query: str, lang: str = "zh") -> list:
    """
    Search flags by flag name, zh description, or en description.
    Returns sorted list of (score, flag) tuples.
    """
    if not query.strip():
        return list(flags)

    results = []
    for flag in flags:
        score = max(
            fuzzy_match(query, flag.flag),
            fuzzy_match(query, flag.label(lang)),
            fuzzy_match(query, flag.label("en" if lang == "zh" else "zh")),
        )
        if score > 0:
            results.append((score, flag))

    results.sort(key=lambda x: -x[0])
    return [f for _, f in results]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_search.py -v`
Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add src/claude_run/search.py tests/test_search.py
git commit -m "feat: add fuzzy search engine for flag matching"
```

---

## Task 6: 命令执行器 runner.py

**Files:**
- Create: `src/claude_run/runner.py`
- Test: `tests/test_runner.py`

- [ ] **Step 1: 编写测试**

```python
# tests/test_runner.py
import subprocess
from unittest.mock import patch
from claude_run.runner import build_args, execute_claude

def test_build_argv_empty():
    args = build_argv([])
    assert args == ["claude"]

def test_build_argv_single_flag():
    args = build_argv([SelectedFlag("--model", "opus")])
    assert args == ["claude", "--model", "opus"]

def test_build_argv_no_value_flag():
    args = build_argv([SelectedFlag("--bare")])
    assert args == ["claude", "--bare"]

def test_build_argv_with_value():
    args = build_argv([SelectedFlag("--mcp-config", "/path/to/mcp.json")])
    assert args == ["claude", "--mcp-config", "/path/to/mcp.json"]

def test_execute_claude_dry_run():
    # 干跑测试：验证 argv 正确生成
    argv = build_argv([SelectedFlag("--model", "sonnet")])
    assert argv == ["claude", "--model", "sonnet"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_runner.py -v`
Expected: FAIL

- [ ] **Step 3: 实现 runner.py**

```python
# src/claude_run/runner.py
import os
import sys
from typing import Sequence

class SelectedFlag:
    def __init__(self, flag: str, value: str | None = None):
        self.flag = flag
        self.value = value

    def to_argv(self) -> list[str]:
        argv = [self.flag]
        if self.value is not None:
            argv.append(self.value)
        return argv

def build_argv(selected: Sequence[SelectedFlag]) -> list[str]:
    """Build the claude command argument list."""
    argv = ["claude"]
    for sel in selected:
        argv.extend(sel.to_argv())
    return argv

def execute_claude(argv: list[str]):
    """Execute claude with the given arguments using execvp."""
    os.execvp(argv[0], argv)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_runner.py -v`
Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add src/claude_run/runner.py tests/test_runner.py
git commit -m "feat: add command builder and executor"
```

---

## Task 7: 首次运行引导 wizard.py

**Files:**
- Create: `src/claude_run/wizard.py`
- Test: `tests/test_wizard.py`（可选，功能测试为主）

- [ ] **Step 1: 实现 wizard.py**

使用 Textual 构建引导流程，三个步骤：

1. **欢迎页** — 显示简介
2. **搜索模式选择** — Radio group: A / B / both
3. **语言选择** — Radio group: 中文 / English
4. **确认完成**

```python
# src/claude_run/wizard.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RadioButton, RadioSet, Button, Static
from textual.containers import Container, VerticalScroll
from claude_run.config import Preferences, save_preferences

class WizardApp(App):
    CSS = """
    Screen { align: center middle; }
    #title { text-style: bold; font-size: 2; }
    .step { margin-bottom: 2; }
    """

    BINDINGS = [("q", "quit", "退出")]

    def __init__(self, prefs: Preferences):
        super().__init__()
        self.prefs = prefs
        self.step = 0  # 0=Welcome, 1=SearchMode, 2=Language, 3=Done

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(id="content")
        yield Footer()

    def watch_step(self) -> None:
        self.query_one("#content").remove_children()
        if self.step == 0:
            self._render_welcome()
        elif self.step == 1:
            self._render_search_mode()
        elif self.step == 2:
            self._render_language()
        elif self.step == 3:
            self._render_done()

    def _render_welcome(self) -> None:
        container = self.query_one("#content")
        container.mount(Static("欢迎使用 claude-run", id="title"))
        container.mount(Static("claude-run 是一个 TUI 工具，帮助你选择 Claude CLI 的启动参数。"))
        container.mount(Button("开始设置", id="start", variant="primary"))

    def _render_search_mode(self) -> None:
        container = self.query_one("#content")
        container.mount(Static("选择搜索模式", id="title"))
        with container.mount(RadioSet(id="search_mode")):
            for label, value in [("模糊搜索（A 模式）", "A"), ("统一搜索（B 模式）", "B"), ("两者都显示", "both")]:
                container.mount(RadioButton(label, value=value))
        container.mount(Button("下一步", id="next", variant="primary"))

    def _render_language(self) -> None:
        container = self.query_one("#content")
        container.mount(Static("选择界面语言", id="title"))
        with container.mount(RadioSet(id="language")):
            container.mount(RadioButton("中文", value="zh"))
            container.mount(RadioButton("English", value="en"))
        container.mount(Button("下一步", id="next", variant="primary"))

    def _render_done(self) -> None:
        container = self.query_one("#content")
        container.mount(Static("设置完成！", id="title"))
        container.mount(Static("正在进入主界面..."))
        self.save_and_exit()

    def save_and_exit(self) -> None:
        rs = self.query_one("#search_mode", RadioSet)
        if rs.selected: self.prefs.search_mode = rs.selected
        lang = self.query_one("#language", RadioSet)
        if lang.selected: self.prefs.language = lang.selected
        self.prefs.first_run = False
        save_preferences(self.prefs)
        self.exit(self.prefs)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.step = 1
        elif event.button.id == "next":
            self.step += 1
        self.watch_step()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        pass  # just track state

def run_wizard(prefs: Preferences) -> Preferences:
    app = WizardApp(prefs)
    result = app.run()
    return result or prefs
```

- [ ] **Step 2: 验证可运行（手动）**

Run: `uv run python -m claude_run --wizard`
Expected: TUI wizard 界面出现

- [ ] **Step 3: 提交**

```bash
git add src/claude_run/wizard.py
git commit -m "feat: add first-run wizard with search mode and language selection"
```

---

## Task 8: TUI 主界面 app.py

**Files:**
- Create: `src/claude_run/app.py`
- Modify: `src/claude_run/__main__.py`

- [ ] **Step 1: 实现 app.py**

主要组件：
- **左侧**：预设组列表（Quick Select 模式）
- **右侧**：当前组内选项详情（勾选状态、子参数输入框）
- **底部**：搜索栏（搜索模式激活时显示）
- **状态栏**：显示已选参数摘要、Enter 执行提示

```python
# src/claude_run/app.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, RadioButton, Checkbox, Input, Button
from textual.containers import Container, Horizontal, VerticalScroll
from textual.binding import Binding
from claude_run.config import load_preferences
from claude_run.flags import Flag, FlagGroup, load_flags
from claude_run.search import search_flags
from claude_run.runner import build_argv, execute_claude, SelectedFlag

class FlagItem(VerticalScroll):
    def __init__(self, flag: Flag, lang: str):
        super().__init__()
        self.flag = flag
        self.lang = lang
        self.value_input: Input | None = None
        self._selected = False

    def compose(self) -> ComposeResult:
        label = self.flag.label(self.lang)
        yield Static(f"[b]{self.flag.flag}[/b] — {label}", classes="flag-desc")
        if self.flag.type == "single" and self.flag.choices:
            with Horizontal():
                for c in self.flag.choices:
                    yield RadioButton(c.label(self.lang), value=c.value, name=self.flag.flag)
        elif self.flag.type == "multi":
            yield Checkbox(self.flag.flag, value=False, name=self.flag.flag)
        elif self.flag.requires_value():
            yield Input(placeholder=self.flag.required_args[0].placeholder_str(self.lang), id=f"input-{self.flag.flag}")

    @property
    def selected(self) -> bool:
        if self.flag.type == "single":
            rb = self.query_one(RadioButton)
            return rb.value == "selected"
        elif self.flag.type == "multi":
            cb = self.query_one(Checkbox)
            return cb.value
        elif self.flag.requires_value():
            inp = self.query_one(Input)
            return bool(inp.value)
        return False

class MainApp(App):
    CSS = """
    #groups { width: 25%; border-right: solid green; }
    #detail { width: 75%; }
    #search-bar { height: 3; }
    .flag-item { margin-bottom: 1; padding: 1; border: solid green; }
    """

    BINDINGS = [
        Binding("q", "quit", "退出"),
        Binding("/", "activate_search", "搜索"),
        Binding("ctrl+s", "activate_search", "搜索"),
        Binding("ctrl+u", "unified_search", "统一搜索"),
        Binding("escape", "deactivate_search", "退出搜索"),
        Binding("enter", "execute", "执行"),
    ]

    def __init__(self, prefs):
        super().__init__()
        self.prefs = prefs
        self.lang = prefs.language
        self.flags = load_flags()
        self.groups = FlagGroup.group_by(self.flags)
        self.search_mode = prefs.search_mode
        self.search_active = False
        self.selected_flags: list[SelectedFlag] = []

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield VerticalScroll(Static("预设组", classes="section-title"), id="groups")
            yield VerticalScroll(id="detail")
        yield Container(Input(placeholder="输入搜索...", id="search-input"), id="search-bar")
        yield Footer()

    def on_mount(self) -> None:
        self._render_groups()

    def _render_groups(self) -> None:
        groups_container = self.query_one("#groups")
        groups_container.remove_children()
        for group_name, group_flags in self.groups.items():
            group_label = self._get_group_label(group_name)
            groups_container.mount(Button(group_label, id=f"group-{group_name}", variant="primary"))

    def _get_group_label(self, group_name: str) -> str:
        labels = {
            "model": ("模型", "Model"),
            "permission": ("权限模式", "Permission"),
            "output": ("输出模式", "Output"),
            "session": ("会话", "Session"),
            "tools": ("工具", "Tools"),
            "dev": ("开发模式", "Dev"),
            "debug": ("调试", "Debug"),
            "mcp": ("MCP", "MCP"),
        }
        zh, en = labels.get(group_name, (group_name, group_name))
        return zh if self.lang == "zh" else en

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id and event.button.id.startswith("group-"):
            group_name = event.button.id[len("group-"):]
            self._render_detail(group_name)

    def _render_detail(self, group_name: str) -> None:
        detail = self.query_one("#detail")
        detail.remove_children()
        group_flags = self.groups.get(group_name, [])
        for flag in group_flags:
            detail.mount(FlagItem(flag, self.lang))

    def action_activate_search(self) -> None:
        self.search_active = True
        search_bar = self.query_one("#search-bar")
        search_bar.scroll_visible()
        input_el = self.query_one("#search-input", Input)
        input_el.focus()

    def action_deactivate_search(self) -> None:
        self.search_active = False
        self._render_groups()

    def on_input_changed(self, event: Input.Changed) -> None:
        if self.search_active:
            query = event.value
            if query:
                results = search_flags(self.flags, query, self.lang)
                self._render_search_results(results)

    def _render_search_results(self, results: list[Flag]) -> None:
        detail = self.query_one("#detail")
        detail.remove_children()
        for flag in results:
            detail.mount(FlagItem(flag, self.lang))

    def action_execute(self) -> None:
        # Collect selected flags
        selected = []
        for fi in self.query(FlagItem):
            if fi.selected:
                value = None
                if fi.flag.requires_value():
                    value = fi.query_one(Input).value
                selected.append(SelectedFlag(fi.flag.flag, value))
        argv = build_argv(selected)
        self.exit()
        execute_claude(argv)
```

- [ ] **Step 2: 更新 __main__.py**

```python
# src/claude_run/__main__.py
import sys
from claude_run.config import load_preferences, is_first_run, Preferences
from claude_run.wizard import run_wizard
from claude_run.app import MainApp

def main():
    if is_first_run():
        prefs = run_wizard(Preferences())
    else:
        prefs = load_preferences()

    app = MainApp(prefs)
    app.run()

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 验证 CLI 入口**

Run: `uv run python -m claude_run --help`（预期：运行程序）
确保 `pyproject.toml` 中 `scripts.claude-run` 指向正确。

- [ ] **Step 4: 提交**

```bash
git add src/claude_run/app.py src/claude_run/__main__.py
git commit -m "feat: add main TUI app with quick-select, search, and runner integration"
```

---

## Task 9: 安装脚本和最终验证

**Files:**
- Create: `scripts/install.sh`（可选，将 claude-run 安装到 PATH）

- [ ] **Step 1: 通过 uv 安装本地包**

Run: `uv pip install -e .`
验证: `claude-run --help`

- [ ] **Step 2: 端到端手动测试**

1. 首次运行：出现引导界面，选择 A 模式 + 中文
2. 验证 preferences.json 生成
3. 主界面出现预设组列表
4. 选择 Model 组，选中 Sonnet
5. 按 `/` 激活搜索，输入 "mcp"，出现 `--mcp-config` 结果
6. 回车执行，验证 `claude --model sonnet` 被调用

- [ ] **Step 3: 提交**

```bash
git add scripts/install.sh
git commit -m "chore: add install script for local development"
```

---

## 依赖汇总

| 包 | 用途 | 安装命令 |
|---|---|---|
| textual | TUI 框架 | `uv add textual` |
| pytest | 测试 | `uv add --dev pytest` |

---

## 实施顺序

1. Task 1: 项目脚手架
2. Task 2: flags_default.json（定义所有参数）
3. Task 3: config.py（偏好管理）
4. Task 4: flags.py（参数加载+合并）
5. Task 5: search.py（搜索匹配）
6. Task 6: runner.py（命令执行）
7. Task 7: wizard.py（首次引导）
8. Task 8: app.py + __main__.py（主界面）
9. Task 9: 端到端验证
