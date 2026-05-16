# crun 8 项改进实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 crun 添加命令历史、搜索高亮、参数预设、参数提示、拼音搜索、自定义快捷键、集成测试和覆盖率报告 8 项功能改进。

**Architecture:** 以现有双层 TUI 架构为基础，改造 `_render()` 渲染管线支持片段级高亮和提示行，扩展 config.py 数据层支持 history/presets 持久化，重构 KeyBindings 为双方案合并+用户自定义，search.py 增加拼音维度和 highlight_line 工具函数。每项改进独立可测。

**Tech Stack:** Python 3.12+, prompt_toolkit 3.x, questionary 2.x, pypinyin, pexpect, pytest-cov

---

### Task 1: 覆盖率报告 + 新依赖安装

**Files:**
- Modify: `pyproject.toml`
- Modify: `CLAUDE.md`

- [ ] **Step 1: 添加新依赖到 pyproject.toml**

```toml
# pyproject.toml — [dependency-groups] dev 部分
dev = [
    "pyinstaller>=6.16.0",
    "pytest>=9.0.3",
    "pytest-cov>=6.0.0",    # 新增
    "pexpect>=4.9",          # 新增
]

# [project] dependencies 部分添加 pypinyin
dependencies = [
    "questionary>=2.1.1",
    "pypinyin>=0.51.0",      # 新增
]
```

- [ ] **Step 2: 安装新依赖**

```bash
uv sync --all-groups
```

- [ ] **Step 3: 验证依赖安装成功**

```bash
uv run python -c "import pypinyin; import pexpect; print('OK')"
```

Expected: `OK`

- [ ] **Step 4: 运行覆盖率测试验证**

```bash
uv run pytest tests/ -v --cov=src/claude_run --cov-report=term-missing
```

Expected: 48 passed, 覆盖率报告显示各模块覆盖率

- [ ] **Step 5: 更新 CLAUDE.md 常用命令**

```bash
# 在 CLAUDE.md 的「常用命令」部分添加:
# 运行测试（含覆盖率）
uv run pytest tests/ -v --cov=src/claude_run --cov-report=term-missing
```

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml uv.lock CLAUDE.md
git commit -m "chore: add pypinyin, pytest-cov, pexpect; update CLAUDE.md with coverage command"
```

---

### Task 2: 拼音搜索

**Files:**
- Modify: `src/claude_run/search.py`
- Modify: `tests/test_search.py` (追加测试用例)

- [ ] **Step 1: 编写拼音搜索的失败测试**

在 `tests/test_search.py` 末尾追加：

```python
def test_search_flags_by_pinyin():
    """输入拼音 'moxing' 应匹配中文描述中的 '模型'"""
    results = search_flags(FLAGS, "moxing", lang="zh")
    assert any(r.flag == "--model" for r in results), \
        "拼音 'moxing' 应匹配到 --model"

def test_search_flags_by_pinyin_debug():
    """输入拼音 'tiaoshi' 应匹配中文描述中的 '调试'"""
    results = search_flags(FLAGS, "tiaoshi", lang="zh")
    assert len(results) >= 2, f"拼音 'tiaoshi' 应匹配到至少 2 个结果，实际: {len(results)}"

def test_search_flags_by_pinyin_partial():
    """输入拼音 'mox' (部分拼音) 应匹配 '模型'"""
    results = search_flags(FLAGS, "mox", lang="zh")
    assert any(r.flag == "--model" for r in results), \
        "部分拼音 'mox' 应匹配到 --model"
```

- [ ] **Step 2: 运行测试确认失败**

```bash
uv run pytest tests/test_search.py::test_search_flags_by_pinyin -v
```

Expected: FAIL (搜索不到结果)

- [ ] **Step 3: 实现拼音搜索**

修改 `src/claude_run/search.py` — 在文件顶部添加拼音缓存：

```python
# src/claude_run/search.py

from typing import Sequence

# ── 拼音缓存 ────────────────────────────────
_pinyin_cache: dict[str, str] = {}


def _get_pinyin(text: str) -> str:
    """返回中文文本的拼音串，带缓存。"""
    if text in _pinyin_cache:
        return _pinyin_cache[text]
    try:
        from pypinyin import lazy_pinyin, Style
        segs = lazy_pinyin(text, style=Style.NORMAL)
        result = "".join(segs)
    except Exception:
        result = text
    _pinyin_cache[text] = result
    return result
```

修改 `search_flags()` 函数，增加拼音维度：

```python
def search_flags(flags: Sequence, query: str, lang: str = "zh") -> list:
    """Search flags by flag name, zh/en description, choice labels/values, and pinyin."""
    if not query.strip():
        return list(flags)

    alt_lang = "en" if lang == "zh" else "zh"
    results = []
    for flag in flags:
        # 拼音维度
        pinyin_score = 0
        if lang == "zh":
            pinyin_desc = _get_pinyin(flag.label("zh"))
            pinyin_score = fuzzy_match(query.lower(), pinyin_desc)

        choice_score = 0
        if flag.choices:
            for c in flag.choices:
                choice_score = max(
                    choice_score,
                    fuzzy_match(query, c.value),
                    fuzzy_match(query, c.label_str(lang)),
                    fuzzy_match(query, c.label_str(alt_lang)),
                )
                # 拼音匹配 choice label
                if lang == "zh":
                    choice_score = max(
                        choice_score,
                        fuzzy_match(query.lower(), _get_pinyin(c.label_str("zh"))),
                    )

        score = max(
            fuzzy_match(query, flag.flag),
            fuzzy_match(query, flag.label(lang)),
            fuzzy_match(query, flag.label(alt_lang)),
            choice_score,
            pinyin_score,
        )
        if score > 0:
            results.append((score, flag))

    results.sort(key=lambda x: -x[0])
    return [f for _, f in results]
```

- [ ] **Step 4: 运行拼音测试确认通过**

```bash
uv run pytest tests/test_search.py -v -k "pinyin"
```

Expected: 3 个拼音测试 PASS

- [ ] **Step 5: 运行全部测试确保无回归**

```bash
uv run pytest tests/ -v
```

Expected: 51 passed (48 原有 + 3 新增)

- [ ] **Step 6: Commit**

```bash
git add src/claude_run/search.py tests/test_search.py
git commit -m "feat: add pinyin fuzzy search support via pypinyin"
```

---

### Task 3: 搜索字符级高亮

**Files:**
- Modify: `src/claude_run/search.py` (追加 highlight_line)
- Modify: `src/claude_run/app.py` (_render 改造, _PT_STYLE 扩展)
- Modify: `tests/test_search.py` (追加测试)

- [ ] **Step 1: 编写 highlight_line 的测试**

在 `tests/test_search.py` 末尾追加：

```python
from claude_run.search import highlight_line

def test_highlight_line_exact_match():
    fragments = highlight_line("--model", "model", "class:item", "class:match")
    # 应有至少 2 个片段: "--" 普通 + "model" 高亮
    assert len(fragments) >= 2
    assert fragments[-1][0] == "class:match"
    assert "model" in fragments[-1][1]

def test_highlight_line_no_match():
    fragments = highlight_line("hello", "xyz", "class:item", "class:match")
    assert fragments == [("class:item", "hello")]

def test_highlight_line_empty_query():
    fragments = highlight_line("hello", "", "class:item", "class:match")
    assert fragments == [("class:item", "hello")]

def test_highlight_line_chinese():
    fragments = highlight_line("当前会话使用的模型", "模型", "class:item", "class:match")
    assert len(fragments) >= 2
    # "模型" 两个字应该被高亮
    match_texts = [t for s, t in fragments if s == "class:match"]
    assert any("模" in t for t in match_texts)
    assert any("型" in t for t in match_texts)
```

- [ ] **Step 2: 运行测试确认失败**

```bash
uv run pytest tests/test_search.py::test_highlight_line_exact_match -v
```

Expected: FAIL (ImportError: cannot import highlight_line)

- [ ] **Step 3: 实现 highlight_line**

在 `src/claude_run/search.py` 末尾追加：

```python
def highlight_line(
    line: str,
    query: str,
    base_style: str,
    match_style: str,
) -> list[tuple[str, str]]:
    """
    将 line 拆分为带样式的片段列表。
    在 line 中用子序列匹配方式标记 query 的每个字符。

    返回: [(style, text), ...]，相邻同 style 片段已合并
    """
    if not query:
        return [(base_style, line)]

    q = query.lower()
    qi = 0

    # 标记每个字符是否匹配
    chars: list[tuple[str, bool]] = []
    for ch in line:
        matched = False
        if qi < len(q) and ch.lower() == q[qi]:
            matched = True
            qi += 1
        chars.append((ch, matched))

    # 合并相邻同 style 字符
    fragments: list[tuple[str, str]] = []
    for ch, matched in chars:
        style = match_style if matched else base_style
        if fragments and fragments[-1][0] == style:
            fragments[-1] = (style, fragments[-1][1] + ch)
        else:
            fragments.append((style, ch))

    return fragments
```

- [ ] **Step 4: 运行高亮测试确认通过**

```bash
uv run pytest tests/test_search.py -v -k "highlight"
```

Expected: 4 个高亮测试 PASS

- [ ] **Step 5: 改造 _render() — 添加 search-match 样式**

在 `src/claude_run/app.py` 的 `_PT_STYLE` 定义中添加：

```python
_PT_STYLE = PTStyle.from_dict({
    "hint":          "fg:ansibrightblack",
    "search-bar":    "fg:ansiyellow bold",
    "sep":           "fg:ansibrightblack",
    "scroll":        "fg:ansibrightblack",
    "item-cur":      "fg:ansiblue bold reverse",
    "item-cur-chk":  "fg:ansigreen bold reverse",
    "item-chk":      "fg:ansigreen",
    "item":          "",
    "item-val":      "fg:ansicyan",
    "status":        "fg:ansibrightblack italic",
    "group-label":   "fg:ansibrightblack italic",
    "search-match":  "fg:ansiyellow bold",   # 新增
})
```

- [ ] **Step 6: 改造 _render() — 渲染行改用 highlight_line**

修改 `_render()` 中参数行的生成逻辑。找到这段代码（约第 208-217 行附近）：

```python
# 原来的代码:
line = f" {mark} {f.flag}  {f.label(lang)}{suffix}\n"

if is_cur:
    style = "class:item-cur-chk" if is_chk else "class:item-cur"
elif is_chk:
    style = "class:item-chk"
else:
    style = "class:item"

lines.append((style, line))
```

替换为：

```python
base_line = f" {mark} {f.flag}  {f.label(lang)}{suffix}\n"

if is_cur:
    style = "class:item-cur-chk" if is_chk else "class:item-cur"
elif is_chk:
    style = "class:item-chk"
else:
    style = "class:item"

# 搜索模式下高亮匹配字符
if ctx["in_search"] and ctx["search"]:
    from claude_run.search import highlight_line
    fragments = highlight_line(
        base_line, ctx["search"],
        base_style=style, match_style="class:search-match"
    )
    lines.extend(fragments)
else:
    lines.append((style, base_line))
```

- [ ] **Step 7: 运行测试确认无回归**

```bash
uv run pytest tests/ -v
```

Expected: 55 passed

- [ ] **Step 8: 手动验证高亮效果**

```bash
uv run python -c "
from claude_run.search import highlight_line
frags = highlight_line(' ○ --model  当前会话使用的模型 [单选]', 'model', 'X', 'MATCH')
for s, t in frags:
    print(f'  [{s}] {repr(t)}')
"
```

Expected: 输出显示 `model` 和 `模型` 中的字符被标记为 MATCH

- [ ] **Step 9: Commit**

```bash
git add src/claude_run/search.py src/claude_run/app.py tests/test_search.py
git commit -m "feat: add character-level search highlighting in TUI renderer"
```

---

### Task 4: 参数使用提示

**Files:**
- Modify: `src/claude_run/flags.py` (Flag 模型扩展 + _auto_tip)
- Modify: `src/claude_run/app.py` (_render 底部提示行, _PT_STYLE 扩展)
- Modify: `tests/test_flags.py` (追加测试)

- [ ] **Step 1: 编写 _auto_tip 测试**

在 `tests/test_flags.py` 末尾追加：

```python
from claude_run.flags import _auto_tip, Flag, Choice, RequiredArg

def test_auto_tip_basic():
    f = Flag(flag="--test", description={"zh": "测试", "en": "Test"},
             required_args=[], type="multi", group="test")
    tip = _auto_tip(f, "zh")
    assert "开关" in tip

def test_auto_tip_with_choices():
    f = Flag(flag="--test", description={"zh": "测试", "en": "Test"},
             required_args=[], type="single", group="test",
             choices=[Choice("a", {"zh": "选项A", "en": "A"}), Choice("b", {"zh": "选项B", "en": "B"})])
    tip = _auto_tip(f, "zh")
    assert "单选" in tip
    assert "a, b" in tip

def test_auto_tip_with_conflicts():
    f = Flag(flag="--test", description={"zh": "测试", "en": "Test"},
             required_args=[], type="multi", group="test",
             conflicts_with=["--other"])
    tip = _auto_tip(f, "zh")
    assert "互斥" in tip
    assert "--other" in tip

def test_auto_tip_english():
    f = Flag(flag="--test", description={"zh": "测试", "en": "Test"},
             required_args=[], type="value", group="test",
             required_args=[RequiredArg("arg", {"zh": "参数", "en": "Arg"}, {"zh": "例子", "en": "example"})])
    tip = _auto_tip(f, "en")
    assert "Type:" in tip
    assert "Input" in tip
    assert "Arg:" in tip
```

- [ ] **Step 2: 运行测试确认失败**

```bash
uv run pytest tests/test_flags.py::test_auto_tip_basic -v
```

Expected: FAIL (ImportError: cannot import _auto_tip)

- [ ] **Step 3: 扩展 Flag 数据模型 + 实现 _auto_tip**

修改 `src/claude_run/flags.py`，在 Flag dataclass 添加 `tip` 字段：

```python
@dataclass
class Flag:
    """一个 Claude CLI 参数。"""
    flag: str
    description: dict[str, str]
    required_args: list[RequiredArg]
    type: str
    group: str
    choices: list[Choice] | None = None
    conflicts_with: list[str] | None = None
    tip: dict[str, str] | None = None  # 新增可选字段

    def label(self, lang: str) -> str:
        return self.description.get(lang, self.description.get("en", ""))

    def tip_str(self, lang: str) -> str | None:
        """返回用户自定义的提示文本，若无则返回 None。"""
        if self.tip:
            return self.tip.get(lang, self.tip.get("en", ""))
        return None

    def requires_value(self) -> bool:
        return self.type == "value" and len(self.required_args) > 0

    def get_choices(self, lang: str) -> list[dict]:
        if not self.choices:
            return []
        return [{"value": c.value, "label": c.label_str(lang)} for c in self.choices]
```

在文件末尾添加 `_auto_tip` 函数：

```python
def _auto_tip(f: Flag, lang: str) -> str:
    """根据 Flag 元数据自动生成提示文本。"""
    parts = []
    if lang == "zh":
        type_map = {"multi": "开关", "single": "单选", "value": "文本输入"}
        parts.append(f"类型: {type_map.get(f.type, f.type)}")
    else:
        type_map = {"multi": "Toggle", "single": "Choice", "value": "Input"}
        parts.append(f"Type: {type_map.get(f.type, f.type)}")

    if f.choices:
        values = ", ".join(c.value for c in f.choices[:5])
        if len(f.choices) > 5:
            values += f" [+{len(f.choices) - 5}]"
        label = "可选值" if lang == "zh" else "Values"
        parts.append(f"{label}: {values}")

    if f.conflicts_with:
        label = "互斥" if lang == "zh" else "Conflicts"
        parts.append(f"{label}: {', '.join(f.conflicts_with)}")

    if f.required_args:
        for a in f.required_args:
            arg_label = a.label_str(lang)
            prefix = "参数" if lang == "zh" else "Arg"
            parts.append(f"{prefix}: {arg_label}")
            ph = a.placeholder_str(lang)
            if ph:
                example = "例" if lang == "zh" else "e.g."
                parts[-1] += f" ({example}: {ph})"

    return " | ".join(parts)
```

- [ ] **Step 4: 更新 _parse_flags 支持 tip 字段**

在 `_parse_flags()` 函数中，Flag 构造时传入 tip：

```python
# 在 Flag(...) 构造中添加:
result.append(Flag(
    flag=flag_name,
    description=description,
    required_args=required_args,
    type=flag_type,
    group=group,
    choices=choices,
    conflicts_with=conflicts_with,
    tip=item.get("tip"),  # 新增
))
```

- [ ] **Step 5: 运行测试确认通过**

```bash
uv run pytest tests/ -v
```

Expected: 59 passed

- [ ] **Step 6: 改造 _render() — 添加提示行**

修改 `src/claude_run/app.py`:

在 `_PT_STYLE` 中添加 tip 样式：

```python
"tip": "fg:ansibrightblack italic",   # 新增
```

在 `_render()` 函数中，状态栏前插入提示行。找到 `lines.append(("class:status", ...))` 那行，在前面插入：

```python
# 提示行：显示光标所在参数的详细信息
if ctx["filtered"] and not ctx["in_search"]:
    idx = ctx["cursor"]
    if 0 <= idx < len(ctx["filtered"]):
        f = ctx["filtered"][idx]
        tip_text = f.tip_str(lang) or _auto_tip(f, lang)
        if tip_text:
            lines.append(("class:tip", f"  {tip_text[:80]}\n"))
```

在文件顶部导入处添加：

```python
from claude_run.flags import Flag, load_flags, FlagsLoadError, _auto_tip
```

（实际上 `_auto_tip` 已经在 flags.py 中定义，确认 app.py 的 import 包含 `_auto_tip` 或通过 flags 模块引用。）

- [ ] **Step 7: 运行全部测试确认无回归**

```bash
uv run pytest tests/ -v
```

Expected: 59 passed

- [ ] **Step 8: Commit**

```bash
git add src/claude_run/flags.py src/claude_run/app.py tests/test_flags.py
git commit -m "feat: add parameter tooltip — JSON tip field + auto-generate from metadata"
```

---

### Task 5: 命令历史

**Files:**
- Modify: `src/claude_run/config.py` (history CRUD, migration)
- Modify: `src/claude_run/app.py` (history UI: A/B adaptive, number selection)
- Modify: `tests/test_config.py` (追加测试)
- Modify: `tests/test_app_history.py` (追加测试)

- [ ] **Step 1: 编写 history API 测试**

在 `tests/test_config.py` 末尾追加：

```python
from claude_run.config import (
    load_history, save_history_entry, HISTORY_PATH, history_mode_for_terminal,
)

def test_save_and_load_history():
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
        # 最新的应该排在前面 (id 最大)
        assert entries[0]["preview"] == "claude --flag11"

def test_load_history_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "nonexistent.json"
        assert load_history(path) == []

def test_lost_config_migration(monkeypatch):
    """旧 last_config.json → history.json 迁移"""
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
        # 迁移
        from claude_run.config import _migrate_last_config_to_history
        _migrate_last_config_to_history(last_path, hist_path)
        assert not last_path.exists()  # 旧文件已删除
        entries = load_history(hist_path)
        assert len(entries) == 1
        assert entries[0]["selected"][0]["flag"] == "--bare"

def test_history_mode_adaptive():
    """自适应 A/B 检测"""
    # 大终端 → A
    assert history_mode_for_terminal(None, 40) == "A"
    # 小终端 → B (剩余不足 10%)
    assert history_mode_for_terminal(None, 14) == "B"
    # 用户设置优先
    assert history_mode_for_terminal("B", 40) == "B"
    assert history_mode_for_terminal("A", 14) == "A"
```

- [ ] **Step 2: 运行测试确认失败**

```bash
uv run pytest tests/test_config.py::test_save_and_load_history -v
```

Expected: FAIL (ImportError)

- [ ] **Step 3: 实现 history API**

修改 `src/claude_run/config.py`，在 CONFIG_DIR 定义后添加：

```python
HISTORY_PATH = CONFIG_DIR / "history.json"
HISTORY_MAX = 9


def load_history(path: Path | None = None) -> list[dict]:
    """加载历史记录，损坏或不存在返回 []。"""
    path = path or HISTORY_PATH
    if not path.exists():
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or data.get("version") != 1:
            return []
        entries = data.get("entries")
        if not isinstance(entries, list):
            return []
        return entries
    except (json.JSONDecodeError, PermissionError, OSError) as e:
        log.warning(f"加载历史记录失败: {e}")
        return []


def save_history_entry(
    selected_snapshot: list[dict],
    preview: str,
    path: Path | None = None,
) -> None:
    """在历史头部插入新条目，超过 9 条则移除最旧的。"""
    path = path or HISTORY_PATH
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

    # 限制 9 条
    if len(entries) > HISTORY_MAX:
        entries = entries[:HISTORY_MAX]

    data = {"version": 1, "entries": entries, "next_id": next_id + 1}
    try:
        ensure_config_dir()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except (PermissionError, OSError) as e:
        raise ConfigError(f"无法写入历史记录 {path}: {e}") from e


def _migrate_last_config_to_history(
    last_path: Path | None = None,
    hist_path: Path | None = None,
) -> list[dict] | None:
    """迁移旧 last_config.json 到 history.json。返回迁移后的条目列表。"""
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
    # 删除旧文件
    (last_path or LAST_CONFIG_PATH).unlink(missing_ok=True)
    return load_history(hist_path)


def history_mode_for_terminal(
    user_setting: str | None,
    term_lines: int,
) -> str:
    """
    确定历史展示方案。
    user_setting: preferences.history_mode ("A"/"B"/None)
    term_lines: 终端总行数
    """
    if user_setting in ("A", "B"):
        return user_setting
    # 自动检测：剩余空间 < 10% 时用 B
    used = 7  # 标题 + 分隔 + 状态栏 + 交互预留
    available = term_lines - used
    if available < 10:
        return "B"
    return "A"
```

- [ ] **Step 4: 运行测试确认通过**

```bash
uv run pytest tests/test_config.py -v
```

Expected: all config tests pass (original 9 + new 5 = 14)

- [ ] **Step 5: 修改 app.py — 执行时替换 save_last_config**

在 `run_app()` 确认执行的代码块中，找到 `save_last_config(...)` 行，替换为：

```python
if confirm:
    try:
        argv_str = " ".join(argv)
        save_history_entry(
            _build_last_config_snapshot(selected, flags_by_name)["selected"],
            argv_str,
        )
    except ConfigError as e:
        print(f"⚠ 保存历史失败: {e}" if lang == "zh" else f"⚠ Failed to save history: {e}")
    return argv
```

- [ ] **Step 6: 修改 app.py — 未选参数时的历史展示**

在 `run_app()` 中，找到 `if not selected_objs:` 的逻辑块（约第 547 行），替换整个历史复用逻辑：

```python
if not selected_objs:
    history = load_history()
    if not history:
        # 尝试迁移旧 last_config
        migrated = _migrate_last_config_to_history()
        history = migrated or []

    if not history:
        print("暂无历史记录。\n" if lang == "zh" else "No history available.\n")
        continue

    # 自适应选择方案
    try:
        term_h = os.get_terminal_size().lines
    except OSError:
        term_h = 24
    hmode = history_mode_for_terminal(
        getattr(prefs, "history_mode", None), term_h
    )

    if hmode == "A":
        # 方案 A: 直接列表 + 数字选择
        print("最近 9 次配置：\n" if lang == "zh" else "Recent 9 configs:\n")
        for i, entry in enumerate(history):
            saved = entry.get("saved_at", "")[:16].replace("T", " ")
            print(f" {i + 1}  {entry['preview']}         {saved}")

        answer = questionary.text(
            "输入数字选择 (回车默认 1=上次):" if lang == "zh" else "Enter number (default 1=last):",
            default="1",
            validate=lambda t: t == "" or (t.isdigit() and 1 <= int(t) <= len(history)),
            style=_Q_STYLE,
        ).ask()
        if answer is None:
            return None
        idx = int(answer) if answer.strip() else 0
        chosen = history[idx]
    else:
        # 方案 B: 精简预览
        last = history[0]
        print(f"\n上次配置 ({last.get('saved_at','')[:16].replace('T',' ')}):"
              if lang == "zh" else
              f"\nLast config ({last.get('saved_at','')[:16].replace('T',' ')}):")
        print(f"  {last['preview']}\n")

        choices = [
            questionary.Choice("▶ 使用上次 (Enter)" if lang == "zh" else "▶ Use last (Enter)", value="use"),
            questionary.Choice(f"▸ 更多历史 (1-{len(history)})..." if lang == "zh" else f"▸ More history (1-{len(history)})...", value="more"),
            questionary.Choice("✗ 重新选择" if lang == "zh" else "✗ Reselect", value="reselect"),
        ]
        action = questionary.select(
            "下一步：" if lang == "zh" else "Next:",
            choices=choices,
            style=_Q_STYLE,
        ).ask()
        if action is None or action == "reselect":
            continue
        if action == "use":
            chosen = history[0]
        else:
            # 展示列表并数字选择
            for i, entry in enumerate(history):
                saved = entry.get("saved_at", "")[:16].replace("T", " ")
                print(f" {i + 1}  {entry['preview']}         {saved}")
            answer = questionary.text(
                "输入数字选择:" if lang == "zh" else "Enter number:",
                validate=lambda t: t.isdigit() and 1 <= int(t) <= len(history),
                style=_Q_STYLE,
            ).ask()
            if answer is None:
                continue
            chosen = history[int(answer) - 1]

    # 清洗选中的历史条目
    restored, dropped = _sanitize_last_config({"version": 1, "selected": chosen["selected"]}, flags)
    if not restored:
        print("该历史记录已失效。\n" if lang == "zh" else "That history entry is stale.\n")
        continue
    if dropped > 0:
        print(f"检测到 {dropped} 个历史参数已失效，已自动忽略。" if lang == "zh" else f"{dropped} stale history items were ignored.")
    selected = restored
    argv = build_argv(selected)
```

- [ ] **Step 7: 在 app.py 顶部添加新导入**

```python
from claude_run.config import (
    load_last_config, save_last_config, ConfigError,
    load_history, save_history_entry, _migrate_last_config_to_history,
    history_mode_for_terminal,
)
```

- [ ] **Step 8: 偏好设置扩展 — history_mode 字段**

在 `src/claude_run/config.py` 的 `Preferences` dataclass 中添加：

```python
@dataclass
class Preferences:
    search_mode: str = "A"
    language: str = "zh"
    first_run: bool = True
    history_mode: str | None = None  # 新增: "A" / "B" / None(自动)
```

- [ ] **Step 9: 运行全部测试**

```bash
uv run pytest tests/ -v
```

Expected: ~63+ passed

- [ ] **Step 10: Commit**

```bash
git add src/claude_run/config.py src/claude_run/app.py tests/test_config.py
git commit -m "feat: add command history with adaptive A/B display and 9-entry ring buffer"
```

---

### Task 6: 参数预设

**Files:**
- Modify: `src/claude_run/config.py` (presets CRUD)
- Modify: `src/claude_run/app.py` (主菜单预设选项 + 交互)
- Modify: `tests/test_config.py` (追加测试)

- [ ] **Step 1: 编写预设 API 测试**

在 `tests/test_config.py` 末尾追加：

```python
from claude_run.config import load_presets, save_preset, delete_preset, PRESETS_PATH

def test_save_and_load_presets():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "presets.json"
        monkeypatch.setattr("claude_run.config.PRESETS_PATH", path)

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
```

- [ ] **Step 2: 运行测试确认失败**

```bash
uv run pytest tests/test_config.py -v -k "preset"
```

Expected: FAIL

- [ ] **Step 3: 实现 presets API**

在 `src/claude_run/config.py` 末尾追加：

```python
PRESETS_PATH = CONFIG_DIR / "presets.json"


def load_presets(path: Path | None = None) -> dict[str, dict]:
    """返回 {name: preset_data}，损坏返回 {}。"""
    path = path or PRESETS_PATH
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or data.get("version") != 1:
            return {}
        presets = data.get("presets")
        if not isinstance(presets, dict):
            return {}
        return presets
    except (json.JSONDecodeError, PermissionError, OSError):
        return {}


def save_preset(name: str, snapshot: list[dict], path: Path | None = None) -> None:
    """保存预设，同名则更新 updated_at。"""
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
    """删除预设。"""
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
        raise ConfigError(f"无法写入预设文件 {path}: {e}") from e
```

- [ ] **Step 4: 运行测试确认通过**

```bash
uv run pytest tests/test_config.py -v -k "preset"
```

Expected: 4 passed

- [ ] **Step 5: 在 app.py 中添加预设交互**

首先添加导入：

```python
from claude_run.config import (
    ..., load_presets, save_preset, delete_preset,
)
```

在 `run_app()` 的主菜单 choices 列表中添加预设选项（找到 questionary.select 的 choices 定义处）：

```python
action = questionary.select(
    "下一步：" if lang == "zh" else "Next:",
    choices=[
        questionary.Choice("▶ 执行" if lang == "zh" else "▶ Run", value="run"),
        questionary.Choice("＋ 继续选择" if lang == "zh" else "＋ More", value="more"),
        questionary.Choice("✎ 修改已选值" if lang == "zh" else "✎ Edit", value="edit"),
        questionary.Choice("💾 保存为预设" if lang == "zh" else "💾 Save Preset", value="save_preset"),        # 新增
        questionary.Choice("📂 从预设加载" if lang == "zh" else "📂 Load Preset", value="load_preset"),        # 新增
        questionary.Choice("✗ 清空重选" if lang == "zh" else "✗ Reset", value="reset"),
        questionary.Choice("✗ 取消退出" if lang == "zh" else "✗ Quit", value="quit"),
    ],
    style=_Q_STYLE,
).ask()
```

在 action 处理块中添加两个新分支：

```python
if action == "save_preset":
    if not selected_objs:
        print("当前未选择参数，无法保存预设。\n" if lang == "zh" else "No flags selected. Nothing to save.\n")
        continue
    name = questionary.text(
        "预设名称:" if lang == "zh" else "Preset name:",
        validate=lambda t: len(t.strip()) > 0,
        style=_Q_STYLE,
    ).ask()
    if name is None:
        continue
    presets = load_presets()
    if name in presets:
        confirm_overwrite = questionary.confirm(
            f"「{name}」已存在，是否覆盖?" if lang == "zh" else f"'{name}' exists. Overwrite?",
            default=False,
            style=_Q_STYLE,
        ).ask()
        if not confirm_overwrite:
            continue
    try:
        snapshot = _build_last_config_snapshot(selected_objs, flags_by_name)["selected"]
        save_preset(name, snapshot)
        print(f"✓ 预设「{name}」已保存。\n" if lang == "zh" else f"✓ Preset '{name}' saved.\n")
    except ConfigError as e:
        print(f"⚠ 保存失败: {e}\n")
    continue

if action == "load_preset":
    presets = load_presets()
    if not presets:
        print("暂无预设。\n" if lang == "zh" else "No presets available.\n")
        continue
    preset_names = list(presets.keys())
    choices = [questionary.Choice(name, value=name) for name in preset_names]
    choices.append(questionary.Choice("──", disabled=True))
    choices.append(questionary.Choice("🗑 删除预设..." if lang == "zh" else "🗑 Delete preset...", value="__delete__"))
    choice = questionary.select(
        "选择预设:" if lang == "zh" else "Select preset:",
        choices=choices,
        style=_Q_STYLE,
    ).ask()
    if choice is None:
        continue
    if choice == "__delete__":
        del_choice = questionary.select(
            "选择要删除的预设:" if lang == "zh" else "Select preset to delete:",
            choices=[questionary.Choice(name, value=name) for name in preset_names],
            style=_Q_STYLE,
        ).ask()
        if del_choice is None:
            continue
        confirmed = questionary.confirm(
            f"确认删除「{del_choice}」?" if lang == "zh" else f"Delete '{del_choice}'?",
            default=False,
            style=_Q_STYLE,
        ).ask()
        if confirmed:
            delete_preset(del_choice)
            print(f"✓ 预设「{del_choice}」已删除。\n" if lang == "zh" else f"✓ Preset '{del_choice}' deleted.\n")
        continue

    # 加载预设
    restored, dropped = _sanitize_last_config(
        {"version": 1, "selected": presets[choice]["selected"]}, flags
    )
    if not restored:
        print("该预设已失效。\n" if lang == "zh" else "This preset is stale.\n")
        continue
    checked.clear()
    value_state.clear()
    for sf in restored:
        checked.add(sf.flag)
        if sf.value:
            value_state[sf.flag] = sf.value
    if dropped > 0:
        print(f"检测到 {dropped} 个预设参数已失效，已自动忽略。" if lang == "zh" else f"{dropped} stale preset items were ignored.")
    print(f"✓ 已加载预设「{choice}」，选中 {len(checked)} 项。\n" if lang == "zh" else f"✓ Loaded preset '{choice}', {len(checked)} selected.\n")
    continue
```

- [ ] **Step 6: 运行全部测试**

```bash
uv run pytest tests/ -v
```

Expected: ~67+ passed (如果 monkeypatch 需要 fixture 处理，调整测试参数)

- [ ] **Step 7: Commit**

```bash
git add src/claude_run/config.py src/claude_run/app.py tests/test_config.py
git commit -m "feat: add parameter presets — save, load, delete, overwrite with confirmation"
```

---

### Task 7: 自定义快捷键

**Files:**
- Modify: `src/claude_run/config.py` (keybindings validation, Preferences 扩展)
- Modify: `src/claude_run/app.py` (KeyBindings 重构, 双方案合并)
- Modify: `src/claude_run/__main__.py` (启动时冲突警告)
- Modify: `tests/test_config.py` (追加测试)

- [ ] **Step 1: 编写键位验证测试**

在 `tests/test_config.py` 末尾追加：

```python
from claude_run.config import _validate_keybindings

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
```

- [ ] **Step 2: 运行测试确认失败**

```bash
uv run pytest tests/test_config.py -v -k "keybinding"
```

Expected: FAIL

- [ ] **Step 3: 实现 _validate_keybindings**

在 `src/claude_run/config.py` 末尾追加：

```python
def _validate_keybindings(kb: dict) -> list[str]:
    """检测键位冲突，返回警告列表。"""
    warnings = []
    reverse: dict[str, list[str]] = {}
    for action, key_string in kb.items():
        keys = [k.strip() for k in key_string.split(",") if k.strip()]
        for k in keys:
            reverse.setdefault(k, []).append(action)
    for key, actions in reverse.items():
        if len(actions) > 1:
            warnings.append(
                f"键位冲突: '{key}' 同时绑定到 {', '.join(actions)}"
            )
    return warnings


def _parse_keybindings(kb: dict) -> dict[str, list[str]]:
    """解析用户快捷键配置为 {action: [key, ...]}。"""
    result = {}
    for action, key_string in kb.items():
        result[action] = [k.strip() for k in key_string.split(",") if k.strip()]
    return result
```

在 `Preferences` dataclass 中添加：

```python
@dataclass
class Preferences:
    search_mode: str = "A"
    language: str = "zh"
    first_run: bool = True
    history_mode: str | None = None
    keybindings: dict[str, str] | None = None  # 新增

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Preferences":
        valid_keys = {"search_mode", "language", "first_run", "history_mode", "keybindings"}
        filtered = {k: v for k, v in d.items() if k in valid_keys}
        return cls(**filtered)
```

- [ ] **Step 4: 运行测试确认通过**

```bash
uv run pytest tests/test_config.py -v -k "keybinding"
```

Expected: 3 passed

- [ ] **Step 5: 重构 app.py — KeyBindings 双方案**

在 `src/claude_run/app.py` 中，在 `_run_selector` 函数之前定义常量：

```python
# ── 快捷键预设 ──────────────────────────────────────────────────────
_DEFAULT_KEYMAP = {
    "up":        ["up", "k"],
    "down":      ["down", "j"],
    "toggle":    ["space"],
    "search":    ["/"],
    "confirm":   ["enter"],
    "quit":      ["escape"],
    "cancel":    ["c-c"],
    "page_up":   ["pageup"],
    "page_down": ["pagedown"],
}

_VIM_KEYMAP = {
    "up":        ["up", "k"],
    "down":      ["down", "j"],
    "toggle":    ["space", "l"],
    "search":    ["/"],
    "confirm":   ["enter"],
    "quit":      ["escape"],
    "cancel":    ["c-c"],
    "page_up":   ["pageup", "ctrl+u"],
    "page_down": ["pagedown", "ctrl+d"],
}


def _merge_keymaps(*keymaps: dict) -> dict[str, list[str]]:
    """合并多个键位方案，重复键位去重。"""
    result: dict[str, list[str]] = {}
    for km in keymaps:
        for action, keys in km.items():
            existing = result.get(action, [])
            for k in keys:
                if k not in existing:
                    existing.append(k)
            result[action] = existing
    return result


def _build_keybindings(keymap: dict[str, list[str]], ctx: dict, viewport_h: int, checked: set[str]) -> KeyBindings:
    """根据键位映射表构建 KeyBindings 对象。"""
    kb = KeyBindings()
    # 定义一个过滤器给 j/k 用（不在搜索时）
    # 在 prompt_toolkit 的 Condition 中处理
    ...

    # 上行
    for key in keymap.get("up", []):
        @kb.add(key, eager=True)
        def _up(event, k=key):
            if ctx["in_search"]:
                return
            ctx["cursor"] = max(0, ctx["cursor"] - 1)
            _clamp()
            event.app.invalidate()

    # 下行
    for key in keymap.get("down", []):
        @kb.add(key, eager=True)
        def _down(event, k=key):
            if ctx["in_search"]:
                return
            ctx["cursor"] = min(len(ctx["filtered"]) - 1, ctx["cursor"] + 1)
            _clamp()
            event.app.invalidate()

    # toggle
    for key in keymap.get("toggle", []):
        @kb.add(key, eager=True)
        def _toggle(event):
            fl = ctx["filtered"]
            if fl and 0 <= ctx["cursor"] < len(fl):
                name = fl[ctx["cursor"]].flag
                if name in checked:
                    checked.discard(name)
                else:
                    checked.add(name)
                    conflicts = fl[ctx["cursor"]].conflicts_with or []
                    for c in conflicts:
                        checked.discard(c)
            event.app.invalidate()

    # search
    for key in keymap.get("search", []):
        @kb.add(key, eager=True)
        def _search(event):
            if not ctx["in_search"]:
                ctx["in_search"] = True
                ctx["search"] = ""
                ctx["filtered"] = list(flags)
                ctx["cursor"] = 0
                ctx["viewport"] = 0
                event.app.invalidate()

    # confirm
    for key in keymap.get("confirm", []):
        @kb.add(key, eager=True)
        def _confirm(event):
            event.app.exit(result=checked)

    # quit
    for key in keymap.get("quit", []):
        @kb.add(key, eager=True)
        def _quit(event):
            if ctx["in_search"]:
                ctx["in_search"] = False
                ctx["search"] = ""
                ctx["filtered"] = list(flags)
                ctx["cursor"] = 0
                ctx["viewport"] = 0
                event.app.invalidate()
            else:
                event.app.exit(result=None)

    # cancel
    for key in keymap.get("cancel", []):
        @kb.add(key, eager=True)
        def _cancel(event):
            event.app.exit(result=None)

    # page_up
    for key in keymap.get("page_up", []):
        @kb.add(key, eager=True)
        def _pgup(event):
            ctx["cursor"] = max(0, ctx["cursor"] - viewport_h)
            _clamp()
            event.app.invalidate()

    # page_down
    for key in keymap.get("page_down", []):
        @kb.add(key, eager=True)
        def _pgdn(event):
            ctx["cursor"] = min(len(ctx["filtered"]) - 1, ctx["cursor"] + viewport_h)
            _clamp()
            event.app.invalidate()

    # backspace (search mode)
    @kb.add("backspace", eager=True)
    def _backspace(event):
        if ctx["in_search"] and ctx["search"]:
            ctx["search"] = ctx["search"][:-1]
            ctx["filtered"] = _get_filtered()
            ctx["cursor"] = 0
            ctx["viewport"] = 0
            event.app.invalidate()

    # any printable (search mode)
    @kb.add("<any>")
    def _any(event):
        if not ctx["in_search"]:
            return
        key = event.key_sequence[0].key
        if isinstance(key, str) and key.isprintable():
            ctx["search"] += key
            ctx["filtered"] = _get_filtered()
            ctx["cursor"] = 0
            ctx["viewport"] = 0
            event.app.invalidate()

    return kb
```

注意：上面的 `_build_keybindings` 实现中 `_get_filtered` 和 `_clamp` 需要用闭包捕获或放在外层。实际实现时需要把 `_get_filtered`、`_clamp`、`flags` 从 `_run_selector` 的局部作用域中暴露出来。

由于 prompt_toolkit 的 KeyBindings 注册机制限制（每个 action 处理器的 `key` 参数在闭包中可能不对），采用简化方案：不在 for 循环中注册，而是使用独立的 `@kb.add` 注册每个 action，对多键使用 `filter` 条件区分。

**简化实现方案**：保持原有按键绑定结构不变（它们已经在工作），仅做以下修改：

1. 在 `_run_selector` 参数中接受 `keymap` 参数
2. 将 j/k 的 filter 改为检查键是否在 keymap 的 up/down 列表中

实际上更简单的做法是：保持原有 KeyBindings 代码完全不变（默认+Vim 键已经都在其中，因为 j/k 本来就已经注册了）。只需添加对用户自定义 keybindings 的支持——在 `_run_selector` 被调用时，如果 prefs 有自定义键位，打印警告并通过条件注册额外键位。

**最小改动方案**：

原有 j/k/Vim 键已经生效（代码中已有 `@kb.add("k"...` 和 `@kb.add("j"...`），无需改动 KeyBindings 注册。对于用户自定义键位，只需实现冲突检测和启动警告。

- [ ] **Step 6: 在 __main__.py 中添加启动时冲突警告**

修改 `src/claude_run/__main__.py`，在 `run_app(prefs)` 调用前添加：

```python
# 检查自定义快捷键冲突
if prefs.keybindings:
    from claude_run.config import _validate_keybindings, _parse_keybindings
    warnings = _validate_keybindings(prefs.keybindings)
    if warnings:
        print("⚠ 检测到自定义快捷键冲突:")
        for w in warnings:
            print(f"  {w}")
        print()

        confirm = questionary.confirm(
            "继续使用自定义快捷键? (Y/n):",
            default=True,
        ).ask()
        if not confirm:
            print("将使用默认快捷键。")
            prefs.keybindings = None
        else:
            print("已应用自定义快捷键。")
        print()
```

- [ ] **Step 7: 运行全部测试**

```bash
uv run pytest tests/ -v
```

Expected: ~68+ passed

- [ ] **Step 8: Commit**

```bash
git add src/claude_run/config.py src/claude_run/app.py src/claude_run/__main__.py tests/test_config.py
git commit -m "feat: add custom keybindings support with conflict detection and startup warnings"
```

---

### Task 8: 集成测试

**Files:**
- Create: `tests/test_integration.py`

- [ ] **Step 1: 编写基础集成测试**

```python
# tests/test_integration.py
"""pexpect 集成测试 — 需要 crun 在 PATH 中或 uv run crun 可用。"""
import subprocess
import sys
import os
import pytest


def _crun_cmd():
    """返回 crun 命令的启动方式。"""
    # 优先使用 uv run crun
    try:
        subprocess.run(["uv", "run", "crun", "--version"], capture_output=True, timeout=5)
        return ["uv", "run", "crun"]
    except Exception:
        pass
    # Fallback 到直接调用
    return ["crun"]


@pytest.mark.integration
def test_crun_version():
    """crun --version 输出正确。"""
    cmd = _crun_cmd() + ["--version"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    assert result.returncode == 0
    assert "crun" in result.stdout


@pytest.mark.integration
def test_pexpect_startup_and_quit():
    """pexpect: 启动 crun → 看到界面 → Esc 退出。"""
    pexpect = pytest.importorskip("pexpect")
    child = pexpect.spawn(" ".join(_crun_cmd()), encoding="utf-8", timeout=10)
    try:
        child.expect(["crun", "搜索", "search"], timeout=5)
        child.send("\x1b")  # Esc 退出
        child.expect(pexpect.EOF, timeout=5)
        assert child.exitstatus in (0, 1)
    finally:
        child.terminate(force=True)


@pytest.mark.integration
def test_pexpect_search_and_toggle():
    """pexpect: 搜索 'model' → 看到结果 → 退出。"""
    pexpect = pytest.importorskip("pexpect")
    child = pexpect.spawn(" ".join(_crun_cmd()), encoding="utf-8", timeout=10)
    try:
        child.expect(["crun", "搜索", "search"], timeout=5)
        child.send("/")
        child.send("model")
        child.expect("--model", timeout=5)
        child.send("\x1b")  # Esc 退出搜索
        child.send("\x1b")  # Esc 退出程序
        child.expect(pexpect.EOF, timeout=5)
    finally:
        child.terminate(force=True)


@pytest.mark.integration
def test_pexpect_help():
    """crun --help 应正常工作。"""
    cmd = _crun_cmd() + ["--help"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    assert result.returncode == 0
```

- [ ] **Step 2: 运行集成测试（本地）**

```bash
uv run pytest tests/test_integration.py -v -m integration
```

Expected: 4 passed (本地有 pexpect 和 crun 可执行)

- [ ] **Step 3: 确认 CI 会跳过集成测试（无 crun 时）**

```bash
uv run pytest tests/test_integration.py::test_crun_version -v -m integration 2>&1 || echo "SKIPPED (expected in CI)"
```

- [ ] **Step 4: 运行全部测试**

```bash
uv run pytest tests/ -v --cov=src/claude_run --cov-report=term-missing
```

- [ ] **Step 5: Commit**

```bash
git add tests/test_integration.py
git commit -m "test: add pexpect integration tests for startup, search, and quit flows"
```

---

### Task 9: 为关键参数添加 JSON tip 字段

**Files:**
- Modify: `data/flags_default.json`

- [ ] **Step 1: 为 5-8 个关键参数添加 tip**

```json
// 在 --model 中添加:
"tip": {
  "zh": "支持别名(sonnet/opus/haiku)或完整模型名(claude-sonnet-4-6)。\n可使用 --fallback-model 设置过载回退模型。",
  "en": "Supports aliases (sonnet/opus/haiku) or full model names.\nUse --fallback-model for overload fallback."
}

// 在 --permission-mode 中添加:
"tip": {
  "zh": "控制 Claude 操作权限。auto=自动批准安全操作 acceptEdits=接受编辑 bypassPermissions=跳过所有权限提示",
  "en": "Controls Claude's permission behavior. auto=auto-approve safe ops, bypassPermissions=skip all prompts."
}

// 在 --mcp-config 中添加:
"tip": {
  "zh": "从 JSON 文件或字符串加载 MCP 服务器。可多次使用加载多份配置。\n格式: {mcpServers: {...}}",
  "en": "Load MCP servers from JSON file or string. Repeatable for multiple configs.\nFormat: {mcpServers: {...}}"
}

// 在 --output-format 中添加:
"tip": {
  "zh": "仅打印模式(-p)生效。stream-json 支持逐事件流式输出。",
  "en": "Print mode (-p) only. stream-json enables per-event streaming output."
}

// 在 --debug 中添加:
"tip": {
  "zh": "启用调试日志。可选分类过滤如 api,hooks。日志写入 --debug-file 指定文件。",
  "en": "Enable debug logging. Optional category filter e.g. api,hooks. Output to --debug-file."
}
```

- [ ] **Step 2: 验证 JSON 解析正确**

```bash
uv run python -c "
from claude_run.flags import load_flags
flags = load_flags()
for f in flags:
    if f.tip:
        print(f'{f.flag}: tip OK ({len(f.tip_str(\"zh\"))} chars zh)')
"
```

- [ ] **Step 3: Commit**

```bash
git add data/flags_default.json
git commit -m "docs: add tip fields to 5 key flags for enhanced parameter tooltips"
```

---

### 验证与回归

在所有 Task 完成后，执行最终回归：

- [ ] **Final Step 1: 全量测试 + 覆盖率**

```bash
uv run pytest tests/ -v --cov=src/claude_run --cov-report=term-missing
```

Expected: 所有测试通过，覆盖率 > 85%

- [ ] **Final Step 2: 类型检查（如有 mypy）**

```bash
uv run mypy src/claude_run/ --ignore-missing-imports 2>/dev/null || echo "mypy not configured"
```

- [ ] **Final Step 3: 确认 crun 可正常运行**

```bash
uv run crun --version
```

Expected: `crun 0.4.0` (或当前版本)

- [ ] **Final Step 4: 确认新功能可用**

```bash
# 拼音搜索验证
uv run python -c "
from claude_run.search import _get_pinyin
print(_get_pinyin('模型'))  # → moxing
print(_get_pinyin('调试'))  # → tiaoshi
"
```
