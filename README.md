# crun

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-blue?style=flat-square&logo=windows&logoColor=white)](https://github.com/BingMoeNone/crun)

`crun` 是一个 Linux CLI 工具，通过 TUI 交互界面选择 Claude Code 的 71 个启动参数（15 个分组），然后执行 `claude <flags>`。支持拼音模糊搜索、搜索字符高亮、参数互斥、9 条命令历史（A/B 自适应方案）、参数预设、参数使用提示和自定义快捷键。

`crun` is a Linux CLI TUI tool for selecting from 71 Claude Code startup flags (15 groups) and launching `claude <flags>`. Supports pinyin fuzzy search, search match highlighting, flag mutual exclusion, 9-entry command history (A/B adaptive), parameter presets, tooltips, and custom keybindings.

---

## 中文说明

### 功能特性

- **全量参数选择界面**：71 个 Claude Code CLI 参数，15 个分组
- **`/` 即时搜索**：在选择界面输入 `/` 进入搜索模式，`Esc` 退出搜索
- **拼音模糊搜索**：输入拼音（如 `moxing`）即可匹配中文描述（如「模型」），支持全拼和部分拼音
- **搜索字符高亮**：搜索结果中匹配的字符以黄色加粗高亮，帮助理解匹配原因
- **中英双语搜索**：可通过 flag 名、中文描述、英文描述、子选项（choices）的值/标签搜索
- **参数互斥**：自动处理互斥 flag（如 `--chrome` ↔ `--no-chrome`），勾选一方自动取消另一方
- **子参数即时追问**：勾选 `single` / `value` 参数后立即弹出子菜单或输入框
- **参数使用提示**：光标停留时底部显示参数详细说明（优先 JSON 自定义提示，自动生成兜底）
- **命令历史**：保存最近 9 次执行记录（环形缓冲），大终端显示编号列表，小终端显示精简预览，支持数字一键复用
- **参数预设**：支持将当前选择保存为命名预设方案，一键加载切换不同使用场景（如「开发模式」「审查模式」）
- **自定义快捷键**：支持在 `preferences.json` 中自定义键位映射，启动时自动冲突检测并警告
- **可自定义参数**：支持 `~/.config/crun/flags_custom.json` 覆盖或扩展默认参数
- **多语言界面**：首次运行向导支持中文/English

### 快速安装（二进制）

支持 Linux `amd64` / `arm64`。

```bash
curl -fsSL https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.sh | bash
```

指定版本安装：

```bash
CRUN_VERSION=v0.2.0 curl -fsSL https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.sh | bash
```

可选环境变量：

- `CRUN_REPO`：默认 `BingMoeNone/crun`
- `CRUN_VERSION`：默认 `latest`
- `CRUN_INSTALL_DIR`：安装目录（默认优先 `/usr/local/bin`，无权限时回退 `~/.local/bin`）

> 注意：`crun` 会调用系统中的 `claude` 命令，请先确保 Claude Code CLI 已安装并在 PATH 中。

### Windows 安装

支持 Windows 10+ `amd64`。推荐使用 [Windows Terminal](https://aka.ms/terminal)。

```powershell
# 一键安装
irm https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.ps1 | iex
```

指定版本安装：

```powershell
$env:CRUN_VERSION="v0.5.0"
irm https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.ps1 | iex
```

可选环境变量：

- `CRUN_REPO`：默认 `BingMoeNone/crun`
- `CRUN_VERSION`：默认 `latest`
- `CRUN_INSTALL_DIR`：安装目录（默认 `%LOCALAPPDATA%\Programs\crun`）
- `$env:DEBUG=$true`：启用调试输出

> 注意：`crun` 会调用系统中的 `claude` 命令，请先安装 Claude Code CLI 并确保在 PATH 中。首次运行可能需执行 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` 允许 PowerShell 脚本。

### 源码安装

```bash
git clone git@github.com:BingMoeNone/crun.git
cd claude-run

uv sync
uv pip install -e .
```

### 使用

```bash
crun
# 或
uv run crun
```

### 交互按键

| 按键 | 功能 |
|---|---|
| `↑ / ↓` 或 `j / k` | 上下移动 |
| `Space` | 勾选/取消当前参数 |
| `Enter` | 确认当前选择 |
| `/` | 进入搜索模式 |
| `Backspace` | 删除搜索字符（搜索模式） |
| `Esc` | 退出搜索模式；非搜索模式下退出选择器 |
| `Ctrl+C` | 取消退出 |
| `Ctrl+D` / `Ctrl+U` | 上下翻页（Vim 方案附加） |

> 支持在 `preferences.json` 的 `keybindings` 字段中自定义键位映射。启动时如有冲突会自动警告。

### 参数互斥机制

部分 flag 互斥（如 `--chrome` 与 `--no-chrome`、`--system-prompt` 与 `--system-prompt-file`）。在 TUI 中勾选互斥 flag 时，自动取消对方，避免无效组合传入 `claude`。

历史配置复用和最终命令行构建阶段也有相应的互斥防御。

### 命令历史

执行成功后会保存到环形缓冲（最近 9 次）中：

- `~/.config/crun/history.json`

当你在选择界面没有勾选任何参数就选择执行时，程序自动展示历史记录，根据终端大小自适应选择展示方案：

**方案 A（大终端 — 剩余空间 ≥ 10 行）：** 显示带编号的完整列表，输入数字选择第 N 条（默认回车选 1 = 上次），输入 `q` 取消。

**方案 B（小终端 — 剩余空间 < 10 行）：** 显示精简预览（仅最新一条），提供菜单：
- 使用上次（Enter）— 快速复用
- 更多历史 — 展开完整编号列表
- 重新选择 — 回到参数选择界面

用户可在 `preferences.json` 中设置 `history_mode: "A"` 或 `"B"` 固定展示方案。

如果历史配置中包含已失效参数（如已删除 flag 或子选项变更），会自动忽略失效项。

### 参数预设

主菜单提供保存/加载预设功能：

- **保存预设**：将当前选中的参数组合保存为命名预设 → `~/.config/crun/presets.json`
- **加载预设**：从预设列表中选择加载，自动清洗失效参数，恢复勾选状态。同时支持删除预设（需二次确认）。
- **覆盖保护**：保存时如同名预设已存在，会提示确认覆盖。

### 配置文件

配置目录：`~/.config/crun/`

> Windows 配置目录：`%LOCALAPPDATA%\crun\`（通常为 `C:\Users\<用户名>\AppData\Local\crun\`）

- `preferences.json`：用户偏好（language, search_mode, history_mode, keybindings 等）
- `flags_custom.json`：自定义参数定义（覆盖/扩展默认参数）
- `history.json`：最近 9 次执行记录（环形缓冲，自动保存/读取）
- `presets.json`：用户保存的参数预设方案
- `flags_default.json`：默认参数（内置，只读，打包时嵌入）

### 自定义参数示例

```json
{
  "version": 1,
  "flags": [
    {
      "flag": "--my-custom-flag",
      "description": {
        "zh": "我的自定义参数",
        "en": "My custom flag"
      },
      "required_args": [],
      "type": "multi",
      "group": "custom"
    }
  ]
}
```

### 开发与测试

```bash
# 开发模式
uv pip install -e .

# 运行测试
uv run pytest tests/ -v
```

### 本地打包二进制

```bash
uv sync --all-groups
uv run pyinstaller --onefile --name crun --paths src --add-data "data/flags_default.json:data" --copy-metadata crun src/claude_run/__main__.py
```

输出文件：`dist/crun`

---

## English

### Features

- **71 CLI flags** across 15 groups, matching the full Claude Code CLI reference
- **`/` live search** in selector, `Esc` to leave search
- **Pinyin fuzzy search**: type pinyin (e.g. "moxing") to match Chinese descriptions (e.g. "模型"), supports full and partial pinyin
- **Search character highlighting**: matched characters are highlighted in yellow bold, aiding match comprehension
- **Bilingual matching** across flag name, Chinese/English description, and choice labels/values
- **Mutual exclusion** for conflicting flags (e.g. `--chrome` ↔ `--no-chrome`), auto-deselected in TUI
- **Immediate sub-argument prompts** for `single` and `value` flags
- **Parameter tooltips**: cursor-focused flag shows detailed usage tip at screen bottom (JSON-defined tip first, auto-generated from metadata)
- **Command history**: 9-entry ring buffer, adaptive A/B display (numbered list on large terminals, compact preview on small), number selection for instant reuse
- **Parameter presets**: save current selection as named preset, one-click load for different scenarios (e.g. "dev mode", "review mode")
- **Custom keybindings**: configurable keymap in `preferences.json`, automatic conflict detection and warning at startup
- **Custom flag extension** via `~/.config/crun/flags_custom.json`
- **Bilingual UI** with first-run wizard (Chinese / English)

### Quick Install (binary)

Linux `amd64` / `arm64` are supported.

```bash
curl -fsSL https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.sh | bash
```

Install a specific version:

```bash
CRUN_VERSION=v0.2.0 curl -fsSL https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.sh | bash
```

Optional environment variables:

- `CRUN_REPO` (default: `BingMoeNone/crun`)
- `CRUN_VERSION` (default: `latest`)
- `CRUN_INSTALL_DIR` (install dir; default prefers `/usr/local/bin`, falls back to `~/.local/bin`)

> Note: `crun` calls the `claude` command on your system. Make sure Claude Code CLI is installed and available in PATH.

### Windows Install

Windows 10+ `amd64`. [Windows Terminal](https://aka.ms/terminal) recommended.

```powershell
irm https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.ps1 | iex
```

Specify version:

```powershell
$env:CRUN_VERSION="v0.5.0"
irm https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.ps1 | iex
```

Optional environment variables:

- `CRUN_REPO` (default: `BingMoeNone/crun`)
- `CRUN_VERSION` (default: `latest`)
- `CRUN_INSTALL_DIR` (default: `%LOCALAPPDATA%\Programs\crun`)
- `$env:DEBUG=$true` for verbose output

> Note: `crun` calls the `claude` command. Make sure Claude Code CLI is installed and in PATH. You may need `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` first.

### Install from source

```bash
git clone git@github.com:BingMoeNone/crun.git
cd claude-run

uv sync
uv pip install -e .
```

### Usage

```bash
crun
# or
uv run crun
```

### Keybindings

| Key | Action |
|---|---|
| `↑ / ↓` or `j / k` | Move cursor |
| `Space` | Toggle current flag |
| `Enter` | Confirm selection |
| `/` | Enter search mode |
| `Backspace` | Delete search char (in search mode) |
| `Esc` | Exit search mode; quit selector when not searching |
| `Ctrl+C` | Cancel |
| `Ctrl+D` / `Ctrl+U` | Page up/down (Vim scheme) |

> Custom keybindings can be configured via `keybindings` field in `preferences.json`. Conflicts are detected and warned at startup.

### Flag Mutual Exclusion

Some flags conflict with each other (e.g. `--chrome` vs `--no-chrome`, `--system-prompt` vs `--system-prompt-file`). The TUI auto-deselects conflicting flags when you toggle one on. This defense also applies during history reuse and final CLI construction.

### Command History

After a confirmed run, the selection is saved to a 9-entry ring buffer:

- `~/.config/crun/history.json`

If you attempt to run with no current selection, `crun` automatically displays history with adaptive layout:

**Mode A (large terminal — ≥10 free lines):** Full numbered list with timestamps, enter number to select (default Enter = 1 = last), `q` to cancel.

**Mode B (small terminal — <10 free lines):** Compact preview (latest only) with menu:
- Use last (Enter) — quick reuse
- More history — expands to full numbered list
- Reselect — return to flag selector

Set `history_mode: "A"` or `"B"` in `preferences.json` to lock a specific mode.

Stale entries (deleted flags, changed choices) are automatically filtered out on load.

### Parameter Presets

Main menu provides save/load preset functionality:

- **Save Preset**: save current flag selection as a named preset → `~/.config/crun/presets.json`
- **Load Preset**: select from preset list, auto-cleanse stale items, restore checked state. Delete with confirmation.
- **Overwrite protection**: prompts for confirmation if preset name already exists.

### Configuration Files

Directory: `~/.config/crun/`

> Windows: `%LOCALAPPDATA%\crun\` (usually `C:\Users\<username>\AppData\Local\crun\`)

- `preferences.json` — user preferences (language, search_mode, history_mode, keybindings, etc.)
- `flags_custom.json` — custom/override flag definitions
- `history.json` — 9 most recent runs (ring buffer, auto-saved)
- `presets.json` — user-saved parameter presets
- `flags_default.json` — built-in default flags (read-only, embedded in binary)

### Development & Test

```bash
uv pip install -e .
uv run pytest tests/ -v
```

### Build binary locally

```bash
uv sync --all-groups
uv run pyinstaller --onefile --name crun --paths src --add-data "data/flags_default.json:data" --copy-metadata crun src/claude_run/__main__.py
```

Output binary: `dist/crun`

---

## License

MIT License.
