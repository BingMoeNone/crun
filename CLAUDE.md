# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述 / Project Overview

`crun` 是一个 Linux CLI 工具，通过 TUI 交互界面帮助用户选择 Claude Code 的启动参数，然后执行 `claude <flags>`。

`crun` is a Linux CLI tool with a TUI interface for selecting Claude Code startup flags and executing `claude <flags>`.

## 常用命令 / Common Commands

```bash
# 开发模式安装
uv pip install -e .

# 运行程序
crun
uv run crun

# 运行所有测试
uv run pytest tests/ -v

# 运行单个测试文件
uv run pytest tests/test_search.py -v

# 运行单个测试函数
uv run pytest tests/test_search.py::test_fuzzy_match_exact -v

# 添加新依赖
uv add <package>
uv add --dev <package>

# 本地打包二进制
uv sync --all-groups
uv run pyinstaller --onefile --name crun --paths src --add-data "data/flags_default.json:data" src/claude_run/__main__.py
# 输出: dist/crun

# 开启调试日志
DEBUG=1 uv run crun
```

## 技术栈 / Tech Stack

- **Python 3.12+** with **uv** for environment management
- **prompt_toolkit** (main selector TUI) + **questionary** (sub-prompts, confirmations, wizard)
- **PyInstaller** for binary distribution
- **Hatchling** as the build backend

## 代码架构 / Code Architecture

```
src/claude_run/
├── __main__.py      # CLI 入口点，print_logo() + 主流程 + 退出码约定
├── config.py        # Preferences dataclass + preferences.json / last_config.json 读写
├── flags.py         # Flag/Choice/RequiredArg 数据结构 + load_flags()（合并 default + custom）
├── search.py        # fuzzy_match() + search_flags() 模糊搜索引擎
├── runner.py        # SelectedFlag + build_argv() + execute_claude()（os.execvp）
├── wizard.py        # 首次运行引导界面（questionary，选语言+搜索模式）
└── app.py           # 主交互逻辑（prompt_toolkit 全量参数选择器 + questionary 子选项追问）
```

**数据流：**
```
__main__.main()
  └── is_first_run() → wizard (questionary) → save_preferences()
  └── load_preferences() → run_app()
        ├── load_flags() → Flag list (default + custom merge)
        ├── _run_selector() (prompt_toolkit) → 用户勾选参数
        ├── _prompt_flag_value() (questionary) → single/value 子选项追问
        ├── 未选参数时 → load_last_config() → _sanitize_last_config() → 历史复用提示
        └── build_argv() → validate_argv() → execute_claude() (os.execvp)
```

## TUI 双层架构 / Dual-Layer TUI Architecture

主选择器用 **prompt_toolkit** 直接构建（`app.py:_run_selector()`），不使用任何上层框架：
- `FormattedTextControl` + 自定义 `_render()` 函数渲染参数列表
- 自定义 `KeyBindings` 处理 `/` 搜索、空格勾选、方向键移动
- 分组标签（`_GROUP_LABELS`）仅在非搜索模式显示

子交互用 **questionary**：
- `_prompt_flag_value()`：single/value 类型的子选项追问或文本输入
- 主菜单的 "下一步" 选择（执行/继续选择/修改/清空/退出）
- 历史配置复用确认
- 首次运行向导（`wizard.py`）

样式定义在 `app.py` 顶部：`_Q_STYLE`（questionary）和 `_PT_STYLE`（prompt_toolkit）。

## 退出码 / Exit Codes

定义在 `__main__.py:main()`：

| 退出码 | 含义 |
|--------|------|
| 0 | 成功执行 claude（进程被替换，实际不会返回） |
| 1 | 用户取消 / 正常退出 |
| 2 | 配置错误（无法读写 ~/.config/claude-run/） |
| 3 | 参数加载错误（flags_default.json 损坏或缺失） |
| 4 | 执行错误（claude 命令未找到或权限不足） |
| 5 | 其他未知错误 |

## 配置目录 / Config Directory

```
~/.config/claude-run/
├── preferences.json    # 用户偏好（search_mode, language, first_run）
├── flags_custom.json   # 用户自定义参数（覆盖 default）
├── flags_default.json  # 默认参数（内置，只读，打包时嵌入）
└── last_config.json    # 最近一次执行配置（自动保存/读取）
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
- `flags_custom.json` 中的同名 flag 会覆盖 `flags_default.json`
- **PyInstaller 打包**：`flags.py:_default_flags_path()` 通过 `sys._MEIPASS` 检测是否在打包环境中，打包后 `flags_default.json` 嵌入在 bundle 的 `data/` 目录中，`--add-data` 参数必须匹配
- 首次运行会触发引导界面（wizard），用户选择后写入 `preferences.json`
- `search.py` 的 `fuzzy_match` 支持中文、英文模糊匹配（不包含拼音——tests 中无拼音相关测试）
- **历史复用**：执行成功后 `save_last_config()` 保存配置；下次未勾选任何参数时就执行时，`_sanitize_last_config()` 会清洗并提示复用历史配置（自动丢弃已失效的 flag/choice）
- 设置 `DEBUG` 环境变量可启用调试日志（`logging.DEBUG`）
- CI 通过 `.github/workflows/release-linux.yml` 自动发布 Linux amd64/arm64 二进制
