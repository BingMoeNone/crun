# claude-run

<!-- Badges -->
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-blue?style=flat-square&logo=linux&logoColor=white)](https://github.com/BingMoeNone/claude-run)

<!-- Chinese section -->
---

## 中文介绍

> [!TIP]
> **欢迎关注与贡献！** 这是一个完全开源的项目，你可以通过自定义配置文件来扩展任何你想要的功能。

`claude-run` 是一个专为 Linux 系统设计的 CLI 工具，通过优雅的 TUI 交互界面，帮助用户选择 Claude Code 的启动参数，然后一键启动带有自定义参数的 Claude。

### 核心特性

<p align="center">
  <img src="https://img.shields.io/badge/-交互式TUI界面-2E86AB?style=for-the-badge&logo=terminal&logoColor=white" alt="TUI" />
  <img src="https://img.shields.io/badge/-模糊搜索-7B68EE?style=for-the-badge&logo=magnifyingglass&logoColor=white" alt="Search" />
  <img src="https://img.shields.io/badge/-完全开源-FF6B6B?style=for-the-badge&logo=open-source&logoColor=white" alt="Open Source" />
  <img src="https://img.shields.io/badge/-高可定制化-4ECDC4?style=for-the-badge&logo=puzzle&logoColor=white" alt="Customizable" />
  <img src="https://img.shields.io/badge/-多语言支持-FFD93D?style=for-the-badge&logo=globe&logoColor=white" alt="i18n" />
</p>

- **交互式 TUI** — 简洁美观的终端界面，上手即用
- **多种搜索模式** — 支持模糊搜索（模式 A）和统一搜索（模式 B），按 `/` 或 `Ctrl+S` 激活
- **参数分组** — 8 大预设分组：模型、权限模式、输出模式、会话、工具、开发模式、MCP、调试
- **完全可扩展** — 用户可通过 `flags_custom.json` 添加任意自定义参数
- **多语言界面** — 支持中文和英文，可在首次引导中切换

### 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/BingMoeNone/claude-run.git
cd claude-run

# 使用 uv 安装
uv sync
uv pip install -e .
```

#### 使用

```bash
# 启动 claude-run
claude-run

# 或者使用 uv 运行
uv run claude-run
```

#### 交互说明

| 按键 | 功能 |
|------|------|
| `↑ / ↓` | 在预设组之间导航 |
| `空格` | 勾选 / 取消选项 |
| `回车` | 确认选择并启动 Claude |
| `/` 或 `Ctrl+S` | 激活模糊搜索模式 |
| `Ctrl+U` | 激活统一搜索模式 |
| `Escape` | 退出搜索模式 |
| `q` | 退出程序 |

### 目录结构

```
claude-run/
├── src/claude_run/          # 源代码
│   ├── app.py               # TUI 主界面
│   ├── wizard.py            # 首次运行引导
│   ├── config.py            # 用户偏好管理
│   ├── flags.py             # 参数定义与加载
│   ├── search.py            # 模糊搜索引擎
│   └── runner.py            # 命令组装与执行
├── data/
│   └── flags_default.json   # 默认参数集
├── tests/                   # 测试
└── docs/                    # 文档
```

### 自定义参数

项目支持完全自定义参数配置。在 `~/.config/claude-run/` 目录下创建 `flags_custom.json`，即可覆盖或扩展默认参数：

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

### 运行测试

```bash
uv run pytest tests/ -v
```

---

## English Introduction

> [!TIP]
> **Welcome to contribute!** This is a fully open source project with highly customizable flag configuration.

`claude-run` is a Linux-native CLI tool featuring an elegant TUI that helps you select Claude Code startup flags and launch Claude with one keystroke.

### Key Features

<p align="center">
  <img src="https://img.shields.io/badge/-Interactive_TUI-2E86AB?style=for-the-badge&logo=terminal&logoColor=white" alt="TUI" />
  <img src="https://img.shields.io/badge/-Fuzzy_Search-7B68EE?style=for-the-badge&logo=magnifyingglass&logoColor=white" alt="Search" />
  <img src="https://img.shields.io/badge/-Fully_Open_Source-FF6B6B?style=for-the-badge&logo=open-source&logoColor=white" alt="Open Source" />
  <img src="https://img.shields.io/badge/-Fully_Customizable-4ECDC4?style=for-the-badge&logo=puzzle&logoColor=white" alt="Customizable" />
  <img src="https://img.shields.io/badge/-i18n_Support-FFD93D?style=for-the-badge&logo=globe&logoColor=white" alt="i18n" />
</p>

- **Interactive TUI** — Clean and elegant terminal interface
- **Multiple Search Modes** — Fuzzy search (Mode A) and unified search (Mode B), activate with `/` or `Ctrl+S`
- **Flag Groups** — 8 preset groups: Model, Permission, Output, Session, Tools, Dev, MCP, Debug
- **Fully Extensible** — Add custom flags via `flags_custom.json`
- **Multilingual** — Chinese and English UI, switchable on first run

### Quick Start

#### Install

```bash
# Clone the repo
git clone https://github.com/BingMoeNone/claude-run.git
cd claude-run

# Install with uv
uv sync
uv pip install -e .
```

#### Usage

```bash
# Run claude-run
claude-run

# Or with uv
uv run claude-run
```

#### Keybindings

| Key | Action |
|-----|--------|
| `↑ / ↓` | Navigate between preset groups |
| `Space` | Toggle selection |
| `Enter` | Confirm and launch Claude |
| `/` or `Ctrl+S` | Activate fuzzy search mode |
| `Ctrl+U` | Activate unified search mode |
| `Escape` | Exit search mode |
| `q` | Quit program |

### Project Structure

```
claude-run/
├── src/claude_run/          # Source code
│   ├── app.py               # Main TUI app
│   ├── wizard.py            # First-run wizard
│   ├── config.py            # User preferences
│   ├── flags.py             # Flag definitions & loading
│   ├── search.py            # Fuzzy search engine
│   └── runner.py            # Command builder & executor
├── data/
│   └── flags_default.json   # Default flag definitions
├── tests/                   # Test suite
└── docs/                    # Documentation
```

### Custom Flags

The tool supports fully custom flag configuration. Create `flags_custom.json` in `~/.config/claude-run/` to override or extend the default flags:

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

### Run Tests

```bash
uv run pytest tests/ -v
```

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

本项目基于 MIT 许可证开源。

This project is open source under the MIT License.
