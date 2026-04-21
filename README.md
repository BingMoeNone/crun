# claude-run

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-blue?style=flat-square&logo=linux&logoColor=white)](https://github.com/BingMoeNone/claude-run)

`claude-run` 是一个 Linux CLI 工具，用于在终端里快速选择 Claude Code 启动参数，并执行 `claude <flags>`。

`claude-run` is a Linux CLI tool for selecting Claude Code startup flags and launching `claude <flags>`.

---

## 中文说明

### 功能特性

- **全量参数选择界面**：启动后直接进入参数列表，不需要先选模式
- **`/` 即时搜索**：在选择界面输入 `/` 进入搜索模式，`Esc` 退出搜索
- **中英双语搜索**：可通过 flag 名、中文描述、英文描述、子选项（choices）的值/标签搜索
- **子参数即时追问**：勾选 `single` / `value` 参数后立即弹出子菜单或输入框
- **历史配置复用**：当本次未选择参数就执行时，会提示是否使用上次配置
- **可自定义参数**：支持 `~/.config/claude-run/flags_custom.json` 覆盖或扩展默认参数
- **多语言界面**：首次运行向导支持中文/English

### 快速安装（二进制）

支持 Linux `amd64` / `arm64`。

```bash
curl -fsSL https://raw.githubusercontent.com/BingMoeNone/claude-run/main/scripts/install.sh | bash
```

指定版本安装：

```bash
CLAUDE_RUN_VERSION=v0.2.0 curl -fsSL https://raw.githubusercontent.com/BingMoeNone/claude-run/main/scripts/install.sh | bash
```

可选环境变量：

- `CLAUDE_RUN_REPO`：默认 `BingMoeNone/claude-run`
- `CLAUDE_RUN_VERSION`：默认 `latest`
- `CLAUDE_RUN_INSTALL_DIR`：安装目录（默认优先 `/usr/local/bin`，无权限时回退 `~/.local/bin`）

> 注意：`claude-run` 会调用系统中的 `claude` 命令，请先确保 Claude Code CLI 已安装并在 PATH 中。

### 源码安装

```bash
git clone git@github.com:BingMoeNone/claude-run.git
cd claude-run

uv sync
uv pip install -e .
```

### 使用

```bash
claude-run
# 或
uv run claude-run
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

### 历史配置机制

执行成功后会保存最近一次配置到：

- `~/.config/claude-run/last_config.json`

当你在选择界面没有勾选任何参数就选择执行时：

1. 程序会读取上次配置
2. 展示可用的上次命令预览
3. 让你选择：
   - 使用上次配置
   - 重新选择
   - 取消退出

如果历史配置中包含已失效参数（如已删除 flag 或子选项变更），会自动忽略失效项。

### 配置文件

配置目录：`~/.config/claude-run/`

- `preferences.json`：界面语言、首次运行状态等偏好
- `flags_custom.json`：自定义参数定义（覆盖/扩展默认参数）
- `last_config.json`：最近一次执行配置（自动生成）

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
uv run pyinstaller --onefile --name claude-run --paths src --add-data "data/flags_default.json:data" src/claude_run/__main__.py
```

输出文件：`dist/claude-run`

---

## English

### Features

- **All-flags selector on startup** (no pre-mode screen)
- **`/` live search** in selector, `Esc` to leave search
- **Bilingual matching** across flag name, Chinese/English description, and choice labels/values
- **Immediate sub-argument prompts** for `single` and `value` flags
- **Last-config reuse** when running with no current selection
- **Custom flag extension** via `~/.config/claude-run/flags_custom.json`
- **Bilingual UI** with first-run wizard (Chinese / English)

### Quick Install (binary)

Linux `amd64` / `arm64` are supported.

```bash
curl -fsSL https://raw.githubusercontent.com/BingMoeNone/claude-run/main/scripts/install.sh | bash
```

Install a specific version:

```bash
CLAUDE_RUN_VERSION=v0.2.0 curl -fsSL https://raw.githubusercontent.com/BingMoeNone/claude-run/main/scripts/install.sh | bash
```

Optional environment variables:

- `CLAUDE_RUN_REPO` (default: `BingMoeNone/claude-run`)
- `CLAUDE_RUN_VERSION` (default: `latest`)
- `CLAUDE_RUN_INSTALL_DIR` (install dir; default prefers `/usr/local/bin`, falls back to `~/.local/bin`)

> Note: `claude-run` calls the `claude` command on your system. Make sure Claude Code CLI is installed and available in PATH.

### Install from source

```bash
git clone git@github.com:BingMoeNone/claude-run.git
cd claude-run

uv sync
uv pip install -e .
```

### Usage

```bash
claude-run
# or
uv run claude-run
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

### Last Configuration

After a confirmed run, the latest selection is saved to:

- `~/.config/claude-run/last_config.json`

If you attempt to run with no current selection, `claude-run` can:

1. Load last config
2. Show command preview
3. Let you choose to reuse / reselect / cancel

Stale entries in history are automatically filtered out.

### Configuration Files

Directory: `~/.config/claude-run/`

- `preferences.json` — user preferences
- `flags_custom.json` — custom/override flag definitions
- `last_config.json` — auto-saved latest configuration

### Development & Test

```bash
uv pip install -e .
uv run pytest tests/ -v
```

### Build binary locally

```bash
uv sync --all-groups
uv run pyinstaller --onefile --name claude-run --paths src --add-data "data/flags_default.json:data" src/claude_run/__main__.py
```

Output binary: `dist/claude-run`

---

## License

MIT License.