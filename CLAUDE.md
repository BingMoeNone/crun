# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述 / Project Overview

`claude-run` 是一个 Linux CLI 工具，通过 TUI 交互界面帮助用户选择 Claude Code 的启动参数，然后执行 `claude <flags>`。

`claude-run` is a Linux CLI tool with a TUI interface for selecting Claude Code startup flags and executing `claude <flags>`.

## 常用命令 / Common Commands

```bash
# 开发模式安装
uv pip install -e .

# 运行程序
claude-run
uv run claude-run

# 运行测试
uv run pytest tests/ -v

# 添加新依赖
uv add <package>
uv add --dev <package>
```

## 技术栈 / Tech Stack

- **Python 3.12+** with **uv** for environment management
- **Textual** for TUI (pure Python, no C dependencies)
- **Hatchling** as the build backend

## 代码架构 / Code Architecture

```
src/claude_run/
├── __main__.py      # CLI 入口点
├── config.py        # 用户偏好 + 配置文件读写（Preferences dataclass）
├── flags.py         # Flag/Choice/RequiredArg 数据结构 + load_flags()（合并 default + custom）
├── search.py        # fuzzy_match() + search_flags() 模糊搜索引擎
├── runner.py        # SelectedFlag + build_argv() + execute_claude()（os.execvp）
├── wizard.py        # 首次运行 Textual 引导界面（4步）
└── app.py           # 主 TUI 应用（FlagItem widget + MainApp）
```

**数据流：**
```
__main__.main()
  └── is_first_run() → wizard → save_preferences()
  └── load_preferences() → MainApp
        ├── load_flags() → Flag list
        ├── search_flags() → filtered flags
        └── build_argv() → execute_claude()
```

## 配置目录 / Config Directory

```
~/.config/claude-run/
├── preferences.json    # 用户偏好（search_mode, language, first_run）
├── flags_custom.json  # 用户自定义参数（覆盖 default）
└── flags_default.json # 默认参数（内置，只读）
```

## 参数 JSON 结构 / Flag JSON Structure

每个参数定义：
```json
{
  "flag": "--model",
  "description": { "zh": "描述", "en": "Description" },
  "required_args": [{ "name": "arg", "label": {...}, "placeholder": {...} }],
  "type": "single | multi | value",
  "group": "分组名",
  "choices": [{ "value": "val", "label": {...} }]
}
```

## 预设分组 / Preset Groups

| 组名 | 说明 | type |
|------|------|------|
| `model` | 模型选择 | single |
| `permission` | 权限模式 | single |
| `output` | 输出模式 | multi |
| `session` | 会话管理 | multi / value |
| `tools` | 工具范围 | single |
| `dev` | 开发模式 | multi |
| `mcp` | MCP 配置 | value |
| `debug` | 调试选项 | multi / value |

## 重要笔记 / Important Notes

- `execute_claude()` 使用 `os.execvp()` 替换当前进程，不返回
- `flags_custom.json` 中的同名参数会覆盖 `flags_default.json`
- 首次运行会触发引导界面（wizard），用户选择后写入 `preferences.json`
- `search.py` 的 `fuzzy_match` 支持中文、英文、拼音模糊匹配
