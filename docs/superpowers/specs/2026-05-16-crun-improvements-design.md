# crun 8 项改进设计文档

> 日期: 2026-05-16
> 状态: 已确认

---

## 概述

本文档描述 crun 的 8 项功能改进的详细设计，覆盖搜索增强、用户体验优化、工程基础设施三个方面。

### 改进清单

| # | 改进项 | 类别 | 复杂度 |
|---|--------|------|--------|
| 1 | 命令历史（最近 9 次） | UX | 中 |
| 2 | 搜索字符级高亮 | UX | 中 |
| 3 | 参数预设 | UX | 高 |
| 4 | 参数使用提示 | UX | 中 |
| 5 | 拼音搜索 | 搜索增强 | 低 |
| 6 | 自定义快捷键 | UX | 中 |
| 7 | 集成测试 | 工程 | 中 |
| 8 | 覆盖率报告 | 工程 | 低 |

### 实施顺序

1→2→4→3→5→6→7→8（覆盖率可与 1 同步进行）

---

## 1. 命令历史

### 需求

- 保存最近 9 次执行记录（替代当前仅保存上次的 last_config）
- 未勾选参数就点执行时，展示历史列表
- 用户输入数字选择第 N 条，不输入则默认上次（第 1 条）
- 根据终端剩余空间自适应展示方案

### 数据模型

```python
# config.py

HISTORY_MAX = 9
HISTORY_PATH = CONFIG_DIR / "history.json"

# history.json 结构
{
  "version": 1,
  "entries": [
    {
      "id": 1,
      "saved_at": "2026-05-16T14:30:00+00:00",
      "preview": "claude --model sonnet --bare --debug",
      "selected": [
        {"flag": "--model", "type": "single", "value": "sonnet"},
        {"flag": "--bare", "type": "multi", "value": true}
      ]
    },
    // ... 最多 9 条，id 递增
  ],
  "next_id": 2
}
```

### 后端 API

```python
# config.py 新增函数

def load_history() -> list[dict]:
    """加载历史记录，损坏或不存在返回 []"""

def save_history_entry(selected_snapshot: list[dict], preview: str) -> None:
    """在历史头部插入新条目，超过 9 条则移除最旧的"""

def load_history_entry(entry: dict, flags: list[Flag]) -> tuple[list[SelectedFlag], int]:
    """清洗单条历史记录，返回 (结果, 丢弃数)。复用 _sanitize_last_config 的逻辑"""
```

### 向前兼容

`load_last_config()` 保留不删。`run_app()` 中当 history 为空时，尝试读取 last_config 作为首次迁移：

```python
history = load_history()
if not history:
    last = load_last_config()
    if last:
        # 迁移旧数据到历史
        history = [{"id": 1, "saved_at": last["saved_at"], ...}]
        # 迁移完成后删除旧文件，避免重复迁移
        LAST_CONFIG_PATH.unlink(missing_ok=True)
```

### 自适应展示

```
用户偏好检查:
  preferences.history_mode == "A" → 始终方案 A
  preferences.history_mode == "B" → 始终方案 B
  未设置 → 自动检测

自动检测逻辑:
  term_lines = os.get_terminal_size().lines
  used_lines = 标题行(1) + 分隔线(1) + 状态栏(2) + 后续交互预留(3) = 7
  available = term_lines - used_lines
  9条历史需要 9 行 → available >= 9*1.1 ≈ 10 行 → 方案 A
  available < 10 行 → 方案 B
```

**方案 A（直接列表）**：

```text
最近 9 次配置：

1  claude --model sonnet --bare --debug api           05-16 14:30
2  claude --model opus --permission-mode auto          05-16 09:15
3  claude -p --output-format json                      05-15 18:00
...

输入数字选择 (回车默认 1=上次): █
```

**方案 B（精简预览）**：

```text
当前未选择参数。

上次配置 (05-16 14:30):
  claude --model sonnet --bare --debug api

▶ 使用上次 (Enter)
▸ 查看更多历史 (数字键 1-9)...
✗ 重新选择
```

方案 B 下输入数字键 → 展开选中历史的完整预览 → 回车确认。

### questionary 集成（方案 A）

方案 A 需要更复杂的交互——用户输入数字。questionary 的 `select` 不支持数字快捷键，改用 questionary 的 `text` 并自定义验证：

```python
answer = questionary.text(
    "输入数字选择 (回车默认 1=上次):",
    default="1",
    validate=lambda text: text == "" or (text.isdigit() and 1 <= int(text) <= len(history)),
    style=_Q_STYLE,
).ask()
```

---

## 2. 搜索字符级高亮

### 需求

搜索匹配后，匹配的字符用高亮颜色标记。需要拆分每行为多个 `(style, text)` 片段。

### 核心算法

```python
# search.py 新增

def highlight_line(
    line: str,
    query: str,
    base_style: str,
    match_style: str,
) -> list[tuple[str, str]]:
    """
    将 line 拆分为带样式的片段列表。
    在 line 中标记所有 query 的匹配字符。

    返回: [(style, text), ...]，相邻同 style 片段已合并
    """
    if not query:
        return [(base_style, line)]

    qi = 0
    # 标记每个字符是否匹配
    chars: list[tuple[str, bool]] = []
    for ch in line:
        matched = False
        if qi < len(query) and ch.lower() == query[qi].lower():
            matched = True
            qi += 1
        chars.append((ch, matched))

    # 合并相邻同 style 字符为片段
    fragments: list[tuple[str, str]] = []
    buf = ""
    for ch, matched in chars:
        style = match_style if matched else base_style
        if fragments and fragments[-1][0] == style:
            # 追加到上一个片段
            fragments[-1] = (style, fragments[-1][1] + ch)
        else:
            fragments.append((style, ch))

    return fragments
```

注意：`highlight_line` 使用子序列匹配方式标记，与 `fuzzy_match` 的匹配语义一致——query 的字符在 line 中按序出现即匹配。这样能正确高亮搜索结果中已匹配的行。

### 渲染改造

`_render()` 中原来每行是单个 `(style, line)` 元组。改为：

```python
# 原来:
line = f" {mark} {f.flag}  {f.label(lang)}{suffix}\n"
lines.append((style, line))

# 改为:
base_line = f" {mark} {f.flag}  {f.label(lang)}{suffix}\n"
if ctx["in_search"] and ctx["search"]:
    fragments = highlight_line(
        base_line, ctx["search"],
        base_style=style, match_style="class:search-match"
    )
    lines.extend(fragments)
else:
    lines.append((style, base_line))
```

### 高亮维度

需要匹配的字段（与 search_flags 的 5 个维度一致）：

1. `f.flag` — 参数名（如 `--model`）
2. `f.label(lang)` — 当前语言描述
3. `f.label(alt_lang)` — 另一语言描述
4. Choice 的 `value` 和 `label` — 子选项（在 suffix 或单独行中）
5. 拼音（见改进 5）

高亮在已过滤的结果列表中对每行独立执行，不改变过滤逻辑，仅改变渲染。

### 新增样式

```python
_PT_STYLE = PTStyle.from_dict({
    ...
    "search-match": "fg:ansiyellow bold",  # 新增
})
```

### 技术难点

`f.label()` 是一个完整的描述字符串。query 可能在 f.flag、f.label、suffix 中的任意位置匹配。`highlight_line()` 需要接受整行文本，在其中标记所有匹配位置——不区分匹配来源，统一处理。

suffix 包含已选择的值（如 `=sonnet`），也需要高亮：

```
搜索: sonn▌ (1 项)
 ○ --model  当前会话使用的模型  =sonnet
             ^^^^^匹配^^^^^      ^^^^^匹配^^^^^
```

这简化了实现——不关心匹配来源，只标记整行中出现的匹配字符。

---

## 3. 参数预设

### 需求

- 用户可将当前选择保存为预设（命名）
- 从预设列表加载，替换当前选择
- 支持覆盖确认和删除
- 主菜单添加「保存为预设」「从预设加载」选项

### 数据模型

```python
# config.py

PRESETS_PATH = CONFIG_DIR / "presets.json"

# presets.json 结构
{
  "version": 1,
  "presets": {
    "开发模式": {
      "created_at": "2026-05-16T10:00:00+00:00",
      "updated_at": "2026-05-16T10:00:00+00:00",
      "selected": [
        {"flag": "--model", "type": "single", "value": "sonnet"},
        {"flag": "--bare", "type": "multi", "value": true}
      ]
    },
    ...
  }
}
```

### API

```python
def load_presets() -> dict[str, dict]:
    """返回 {name: preset_data}，损坏返回 {}"""

def save_preset(name: str, snapshot: list[dict]) -> None:
    """保存预设，同名则更新 updated_at"""

def delete_preset(name: str) -> None:
    """删除预设"""

def load_preset_into_selection(
    name: str, flags: list[Flag]
) -> tuple[set[str], dict[str, str], list[str]]:
    """
    加载预设并清洗。
    返回: (checked_set, value_state, warnings)
    warnings 列出被丢弃的无效项
    """
```

### UI 流程

**保存**：

```
主菜单 → 「💾 保存为预设...」
  → questionary.text("预设名称:", validate=非空)
    → 名称已存在:
      → questionary.confirm(f"「{name}」已存在，覆盖?")
        → Yes: save_preset() → 提示「已保存」
        → No: 返回主菜单
    → 名称不存在: save_preset() → 提示「已保存」
```

**加载**：

```
主菜单 → 「📂 从预设加载...」
  → questionary.select("选择预设:",
      choices=[
        Choice("开发模式", value="开发模式"),
        Choice("审查模式", value="审查模式"),
        ...
        Choice("──", disabled=True),
        Choice("🗑 删除预设...", value="__delete__"),
      ])
    → 选中预设:
      → load_preset_into_selection()
      → 展示加载结果（选中数 + 警告数）
      → 回到主选择器（checked + value_state 已更新）
    → 删除:
      → questionary.select("选择要删除的预设:",
          choices=[Choice(name, value=name) for name in presets])
      → questionary.confirm("确认删除「{name}」?")
        → Yes: delete_preset() → 提示「已删除」→ 回到预设列表
        → No: 回到预设列表
```

### 与命令历史的关系

预设是用户主动保存的，历史是自动记录的。两者独立存储，但数据格式兼容（都复用 `{"selected": [...]}` 快照格式）。

---

## 4. 参数使用提示

### 需求

光标停留在参数上时，底部信息栏显示该参数的详细说明。

- JSON 有 `tip` 字段 → 使用 tip
- JSON 无 tip → 自动从元数据生成

### JSON tip 字段（可选）

```json
{
  "flag": "--model",
  "description": {"zh": "...", "en": "..."},
  "tip": {
    "zh": "支持别名(sonnet/opus/haiku)或完整模型名。\n默认使用当前设置中的模型。",
    "en": "Supports aliases or full model names.\nDefault: current settings model."
  }
}
```

### 自动生成逻辑

```python
def _auto_tip(f: Flag, lang: str) -> str:
    parts = []
    if lang == "zh":
        type_map = {"multi": "开关", "single": "单选", "value": "文本输入"}
        parts.append(f"类型: {type_map[f.type]}")
    else:
        type_map = {"multi": "Toggle", "single": "Choice", "value": "Input"}
        parts.append(f"Type: {type_map[f.type]}")

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
            parts.append(f"参数: {arg_label}" if lang == "zh" else f"Arg: {arg_label}")
            ph = a.placeholder_str(lang)
            if ph:
                parts[-1] += f" ({'例' if lang == 'zh' else 'e.g.'}: {ph})"

    return " | ".join(parts)
```

### 渲染改造

`_render()` 底部新增提示行，位于状态栏上方：

```python
def _render():
    ...
    # 状态栏前插入提示行
    fl = ctx["filtered"]
    if fl and 0 <= ctx["cursor"] < len(fl):
        f = fl[ctx["cursor"]]
        tip = f.tip(lang) if hasattr(f, 'tip') else _auto_tip(f, lang)
        if tip:
            lines.append(("class:tip", f"  {tip[:80]}\n"))

    n_chk = len(checked)
    lines.append(("class:status", f"  已选 {n_chk} 项"))
    return lines
```

### Flag 数据模型扩展

```python
@dataclass
class Flag:
    ...
    tip: dict[str, str] | None = None  # 新增可选字段

    def tip_str(self, lang: str) -> str:
        if self.tip:
            return self.tip.get(lang, "")
        return ""
```

### 新增样式

```python
_PT_STYLE = PTStyle.from_dict({
    ...
    "tip": "fg:ansibrightblack italic",  # 新增，灰底斜体
})
```

---

## 5. 拼音搜索

### 需求

- 输入拼音（如 "moxing"）可匹配中文描述（"模型"）
- 仅支持全拼，不支持首字母缩写
- 在搜索时额外生成拼音索引

### 实现

```python
# search.py

def _get_pinyin(text: str) -> str:
    """返回中文文本的拼音串（空格分隔）"""
    import pypinyin
    segs = pypinyin.lazy_pinyin(text, style=pypinyin.Style.NORMAL)
    return "".join(segs)
```

在 `search_flags()` 中为中文描述扩展搜索维度：

```python
def search_flags(flags, query, lang="zh"):
    ...
    for flag in flags:
        scores = [
            fuzzy_match(query, flag.flag),
            fuzzy_match(query, flag.label(lang)),
            fuzzy_match(query, flag.label(alt_lang)),
        ]

        # 拼音维度：仅对中文描述生成拼音
        if lang == "zh":
            pinyin_desc = _get_pinyin(flag.label("zh"))
            scores.append(fuzzy_match(query, pinyin_desc))
            ...

        score = max(scores)
        ...
```

### 性能考量

71 个参数的中文描述，每次搜索调用 `_get_pinyin()` 71 次。pypinyin 的 `lazy_pinyin` 对短文本（平均 15 字）性能约 0.1ms/次，总开销 < 10ms。可考虑缓存：

```python
_pinyin_cache: dict[str, str] = {}

def _get_pinyin_cached(text: str) -> str:
    if text not in _pinyin_cache:
        _pinyin_cache[text] = _get_pinyin(text)
    return _pinyin_cache[text]
```

### 依赖

`pyproject.toml` 添加 `pypinyin>=0.51.0`。

---

## 6. 自定义快捷键

### 需求

- 默认（箭头键+空格+回车）和 Vim（hjkl）两套方案同时生效
- 用户可在 preferences.json 中完全自定义键位
- 自定义前提示风险，自定义后做冲突检测

### 预设方案

```python
# app.py

DEFAULT_KEYMAP = {
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

VIM_KEYMAP = {
    "up":        ["up", "k"],
    "down":      ["down", "j"],
    "toggle":    ["space", "l"],  # Vim 风格额外绑定
    "search":    ["/"],
    "confirm":   ["enter"],
    "quit":      ["escape"],
    "cancel":    ["c-c"],
    "page_up":   ["pageup", "ctrl+u"],
    "page_down": ["pagedown", "ctrl+d"],
}
```

默认行为：DEFAULT_KEYMAP 和 VIM_KEYMAP 的每个操作合并键位列表，所有键同时注册。

### 用户自定义

```json
// preferences.json
{
  "keybindings": {
    "up":        "k, up",
    "down":      "j, down",
    "toggle":    "space",
    "search":    "/",
    "confirm":   "enter",
    "quit":      "q",
    "cancel":    "c-c",
    "page_up":   "ctrl+b",
    "page_down": "ctrl+f"
  }
}
```

### 冲突检测

```python
def _validate_keybindings(kb: dict) -> list[str]:
    """检测键位冲突，返回警告列表。"""
    warnings = []
    reverse: dict[str, list[str]] = {}
    for action, key_string in kb.items():
        keys = [k.strip() for k in key_string.split(",")]
        for k in keys:
            reverse.setdefault(k, []).append(action)
    for key, actions in reverse.items():
        if len(actions) > 1:
            warnings.append(
                f"键位冲突: '{key}' 同时绑定到 {', '.join(actions)}"
            )
    return warnings
```

### 用户提示

当用户首次在 preferences.json 中设置 `keybindings` 时，启动时展示：

```text
⚠ 检测到自定义快捷键配置。

注意：
- 自定义快捷键可能与其他功能冲突
- 确保每个操作有唯一键位
- 如果遇到问题，删除 keybindings 字段恢复默认

检测到以下冲突: (若有)
  键位冲突: 'q' 同时绑定到 quit, search

继续使用自定义快捷键? (Y/n): █
```

### 实现方式

prompt_toolkit 的 KeyBindings 在 `Application` 构建时注册，不支持运行时重映射。因此采用「启动时选择方案」策略：

```python
def _build_keybindings(prefs) -> KeyBindings:
    kb = KeyBindings()

    if prefs.keybindings:
        # 用户自定义，验证后使用
        warnings = _validate_keybindings(prefs.keybindings)
        keymap = _parse_keybindings(prefs.keybindings)
    else:
        # 默认合并 DEFAULT + VIM
        keymap = _merge_keymaps(DEFAULT_KEYMAP, VIM_KEYMAP)

    # 注册所有键位
    for action, keys in keymap.items():
        _register_action(kb, action, keys)
    return kb
```

每个 action 的处理器统一路由，键位只是注册入口。

---

## 7. 集成测试

### 需求

- 用 pexpect 模拟终端交互
- 覆盖搜索、勾选、互斥、确认等核心路径

### 工具

`pyproject.toml` 添加 `pexpect>=4.9` 到 dev 依赖。

### 测试结构

```
tests/
├── test_integration.py     # pexpect 集成测试
├── test_search.py           # 保留
├── ...
```

### 测试用例

```python
import pexpect
import sys

def test_full_flow_search_toggle_run():
    """完整流程：搜索 → 勾选 → 确认 → 检查 argv"""
    child = pexpect.spawn("crun", encoding="utf-8")
    child.expect("crun")           # 等待界面加载
    child.send("/")                # 进入搜索
    child.send("model")            # 输入搜索词
    child.expect("--model")        # 确认搜索结果
    child.send("\x1b")             # Esc 退出搜索
    child.send(" ")                # 空格勾选 --model
    child.send("\r")               # 回车确认
    child.expect("下一步")          # 主菜单
    child.send("\r")               # 选择执行
    child.expect("确认执行")        # 确认提示
    child.send("y")
    child.expect("claude")         # 验证构建了正确的命令
    child.terminate()

def test_mutual_exclusion():
    """互斥测试：勾选 --chrome 应取消 --no-chrome"""
    child = pexpect.spawn("crun", encoding="utf-8")
    child.expect("crun")
    child.send("/")
    child.send("no-chrome")
    child.expect("--no-chrome")
    child.send("\x1b")
    child.send(" ")                # 勾选 --no-chrome
    child.send("/")
    child.send("chrome")
    child.expect("--chrome")
    child.send("\x1b")
    child.send(" ")                # 勾选 --chrome，应取消 --no-chrome
    child.send("\r")
    child.expect("当前已选")
    child.expect("--chrome")
    assert "--no-chrome" not in child.before
    child.terminate()

def test_command_history_shown():
    """无参数执行时展示历史"""
    child = pexpect.spawn("crun", encoding="utf-8")
    child.expect("crun")
    child.send("\r")               # 直接回车
    child.expect("上次配置|最近.*次配置")  # 应显示历史
    child.send("\x03")             # Ctrl+C 退出
    child.terminate()
```

### 注意事项

- pexpect 依赖 `pty`，CI 环境（GitHub Actions）支持 pty
- 测试中 crun 需要在 PATH 中，或使用 `uv run crun`
- prompt_toolkit 在 pty 下的渲染与真实终端一致

---

## 8. 覆盖率报告

### 需求

接入 pytest-cov，生成覆盖率报告。

### 实现

```toml
# pyproject.toml
[dependency-groups]
dev = [
    "pyinstaller>=6.16.0",
    "pytest>=9.0.3",
    "pytest-cov>=6.0.0",    # 新增
    "pexpect>=4.9",          # 新增
]
```

```bash
# 运行测试并生成覆盖率
uv run pytest --cov=src/claude_run tests/ --cov-report=term-missing

# 生成 HTML 报告
uv run pytest --cov=src/claude_run tests/ --cov-report=html
```

### CLAUDE.md 更新

```bash
# 运行测试（含覆盖率）
uv run pytest tests/ -v --cov=src/claude_run --cov-report=term-missing
```

---

## 数据流汇总

```
启动 → load_preferences()
      ├─ 检查 keybindings 冲突 → 警告/确认
      ├─ 加载 history.json → 9 条历史
      └─ 加载 presets.json → 预设列表
    → run_app()
      ├─ _run_selector() 渲染:
      │   ├─ _render() 高亮片段 (_highlight_line)
      │   ├─ _render() 提示行 (_auto_tip)
      │   └─ KeyBindings 双方案合并
      ├─ 未选参数 → 历史展示:
      │   ├─ 自适应 A/B 检测
      │   ├─ 数字选择 → _sanitize_history_entry()
      │   └─ 默认回车 → 上次配置
      ├─ 保存/加载预设:
      │   ├─ 主菜单 → 预设子菜单
      │   └─ load_preset_into_selection()
      └─ 确认执行:
          ├─ build_argv() → validate_argv()
          ├─ save_history_entry()  # 替代 save_last_config
          └─ execute_claude()
```

---

## 文件变更范围

| 文件 | 变更类型 | 内容 |
|------|---------|------|
| `src/claude_run/search.py` | 修改 | +highlight_line, +_get_pinyin_cached, +拼音维度 |
| `src/claude_run/app.py` | 重改 | _render 高亮化+提示行, KeyBindings 双方案, 历史交互, 预设菜单 |
| `src/claude_run/config.py` | 修改 | +history CRUD, +presets CRUD, +迁移向前兼容 |
| `src/claude_run/flags.py` | 修改 | Flag.tip 字段, _auto_tip |
| `src/claude_run/__main__.py` | 修改 | 启动时快捷键冲突警告 |
| `data/flags_default.json` | 可选 | 为关键参数添加 tip 字段 |
| `pyproject.toml` | 修改 | +pypinyin, +pytest-cov, +pexpect |
| `tests/test_integration.py` | 新增 | pexpect 集成测试 |
| `scripts/install.sh` | 不变 | — |
| `.github/workflows/release-linux.yml` | 不变 | — |
