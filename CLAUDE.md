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

# 运行测试（含覆盖率）
uv run pytest tests/ -v --cov=src/claude_run --cov-report=term-missing

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

## Windows 开发 / Windows Development

```bash
# Windows 上直接运行 (需 Python 3.12+)
uv pip install -e .
uv run crun

# 运行测试 (Windows runner)
uv run pytest tests/ -v -m "not integration"

# Windows 本地打包 (分隔符为 ; 非 :)
uv sync --all-groups
uv run pyinstaller --onefile --name crun --paths src --add-data "data/flags_default.json;data" --console src/claude_run/__main__.py
# 输出: dist/crun.exe
```

## 技术栈 / Tech Stack

- **Python 3.12+** with **uv** for environment management
- **prompt_toolkit** (main selector TUI) + **questionary** (sub-prompts, confirmations, wizard)
- **pypinyin** for Chinese pinyin fuzzy search
- **pytest-cov** for test coverage, **pexpect** for integration testing
- **PyInstaller** for binary distribution
- **Hatchling** as the build backend

## 代码架构 / Code Architecture

```
src/claude_run/
├── __main__.py      # CLI 入口点，print_logo() + 主流程 + 退出码约定 + 快捷键冲突检测
├── config.py        # Preferences dataclass + preferences/history/presets 读写 + keybindings 验证
├── flags.py         # Flag/Choice/RequiredArg 数据结构 + load_flags() + auto_tip() 提示生成
├── search.py        # fuzzy_match() + search_flags()（拼音维度）+ highlight_line() 字符高亮
├── runner.py        # SelectedFlag + build_argv() + execute_claude()（os.execvp）
├── wizard.py        # 首次运行引导界面（questionary，选语言+搜索模式）
└── app.py           # 主交互逻辑（prompt_toolkit 选择器 + questionary 子选项 / 主菜单 / 历史 / 预设）
```

**数据流：**
```
__main__.main()
  └── is_first_run() → wizard (questionary) → save_preferences()
  └── load_preferences() → run_app()
        ├── load_flags() → Flag list (default + custom merge)
        ├── _run_selector() (prompt_toolkit) → 用户勾选参数
        │     ├── _render() 渲染参数列表 + 搜索高亮 + 光标提示行
        │     └── KeyBindings（默认+Vim 双方案合并 + 用户自定义）
        ├── _prompt_flag_value() (questionary) → single/value 子选项追问
        ├── 主菜单（执行 / 继续选择 / 修改 / 保存预设 / 加载预设 / 清空 / 退出）
        ├── 未选参数时 → load_history() → A/B 自适应历史展示 → 数字选择复用
        └── build_argv() → validate_argv() → execute_claude() (os.execvp)
```

## TUI 双层架构 / Dual-Layer TUI Architecture

主选择器用 **prompt_toolkit** 直接构建（`app.py:_run_selector()`），不使用任何上层框架：
- `FormattedTextControl` + 自定义 `_render()` 函数渲染参数列表
- 搜索模式下 `highlight_line()` 对匹配字符渲染 `search-match` 样式（黄色加粗）
- 非搜索模式下光标所在参数底部显示提示行（JSON tip 优先，自动生成兜底）
- 自定义 `KeyBindings`（默认+Vim 双方案合并 + 用户自定义键位冲突警告）
- 分组标签（`_GROUP_LABELS`）仅在非搜索模式显示

子交互用 **questionary**：
- `_prompt_flag_value()`：single/value 类型的子选项追问或文本输入
- 主菜单 "下一步" 选择（执行/继续选择/修改/保存预设/加载预设/清空/退出）
- 命令历史复用（A/B 自适应方案，数字选择，最多 9 条）
- 预设管理（保存当前选择为预设/从预设加载/删除预设）
- 首次运行向导（`wizard.py`）

样式定义在 `app.py` 顶部：`_Q_STYLE`（questionary）和 `_PT_STYLE`（prompt_toolkit）。新增样式类：`search-match`（搜索高亮）、`tip`（参数提示行）。

## 退出码 / Exit Codes

定义在 `__main__.py:main()`：

| 退出码 | 含义 |
|--------|------|
| 0 | 成功执行 claude（进程被替换，实际不会返回） |
| 1 | 用户取消 / 正常退出 |
| 2 | 配置错误（无法读写 ~/.config/crun/） |
| 3 | 参数加载错误（flags_default.json 损坏或缺失） |
| 4 | 执行错误（claude 命令未找到或权限不足） |
| 5 | 其他未知错误 |

## 配置目录 / Config Directory

```
~/.config/crun/
├── preferences.json    # 用户偏好（search_mode, language, first_run, history_mode, keybindings）
├── flags_custom.json   # 用户自定义参数（覆盖 default）
├── flags_default.json  # 默认参数（内置，只读，打包时嵌入）
├── history.json        # 最近 9 次执行记录（环形缓冲，自动保存/读取）
└── presets.json        # 用户保存的参数预设方案
```

## 参数 JSON 结构 / Flag JSON Structure

`data/flags_default.json`（71 个 flag）+ 用户可选 `~/.config/crun/flags_custom.json`。

每个参数定义：
```json
{
  "flag": "--model",
  "description": { "zh": "描述", "en": "Description" },
  "required_args": [{ "name": "arg", "label": {...}, "placeholder": {...} }],
  "type": "single | multi | value",
  "group": "分组名",
  "choices": [{ "value": "val", "label": {...} }],
  "conflicts_with": ["--other-flag"],
  "tip": { "zh": "使用提示（可选）", "en": "Usage tip (optional)" }
}
```

`conflicts_with` 为可选字段，列出互斥的 flag 名称。目前互斥对：
- `--chrome` ↔ `--no-chrome`
- `--system-prompt` ↔ `--system-prompt-file`

互斥逻辑在 3 处执行：
1. **TUI toggle**（`app.py:_toggle()`）：勾选时自动取消冲突项
2. **TUI value_state 清理**（`app.py:run_app()`）：取消勾选时一并清理其 value_state
3. **历史配置清洗**（`app.py:_sanitize_last_config()`）：恢复历史配置时防御性去重

## 预设分组 / Preset Groups

| 组名 | 说明 | type |
|------|------|------|
| `model` | 模型选择 | single / value |
| `permission` | 权限模式 | single / multi / value |
| `output` | 输出模式 | single / multi / value |
| `session` | 会话管理 | multi / value |
| `tools` | 工具范围 | single / value |
| `system` | 系统提示 | value |
| `dev` | 开发模式 | multi / value |
| `mcp` | MCP/插件 | value |
| `debug` | 调试选项 | multi / value |
| `agent` | Agent | single / multi / value |
| `ide` | IDE/浏览器 | multi |
| `remote` | 远程 | multi / value |
| `hook` | Hooks | multi |
| `limit` | 限制 | value |
| `config` | 配置 | value |

## 配置迁移 / Config Migration

`config.py` 模块加载时自动执行 `_migrate_old_config()`：
- 旧路径 `~/.config/claude-run/` 存在且新路径 `~/.config/crun/` 不存在 → `Path.rename()` 迁移
- 两者都存在 → 使用新路径，旧路径保留不删
- 仅新路径存在 → 正常使用
- 迁移失败（权限等）→ 静默 warning，不影响后续运行

## questionary 注意事项

`questionary.select()` 的 `default` 参数必须传 **value 字符串**（如 `"A"`），不能传 `questionary.Choice` 对象。后者会触发 `ValueError: Invalid initial_choice value passed`。

## 重要笔记 / Important Notes

- `execute_claude()` 使用 `os.execvp()` 替换当前进程，不返回
- `flags_custom.json` 中的同名 flag 会覆盖 `flags_default.json`
- **PyInstaller 打包**：`flags.py:_default_flags_path()` 通过 `sys._MEIPASS` 检测是否在打包环境中，打包后 `flags_default.json` 嵌入在 bundle 的 `data/` 目录中，`--add-data` 参数必须匹配
- 首次运行会触发引导界面（wizard），用户选择后写入 `preferences.json`
- `search.py` 的 `fuzzy_match` 支持中文、英文和拼音模糊匹配（`_get_pinyin()` 通过 pypinyin 将中文转为拼音后匹配）
- `search.py` 的 `highlight_line()` 在搜索模式下对匹配字符逐字高亮（`search-match` 样式），仅在全部 query 字符都匹配时才显示高亮
- **命令历史**：执行成功后 `save_history_entry()` 保存到 `history.json` 环形缓冲（最多 9 条）；下次未勾选参数时就执行时，自适应展示 A/B 方案（大终端显示编号列表，小终端显示精简预览），支持数字选择
- **参数预设**：主菜单可保存当前选择为命名预设（`save_preset()` → `presets.json`），从预设加载或删除预设，加载时自动清洗失效参数
- **参数提示**：非搜索模式下光标所在参数底部显示提示行（优先 JSON `tip` 字段，回退到 `auto_tip()` 元数据自动生成），中英双语
- 设置 `DEBUG` 环境变量可启用调试日志（`logging.DEBUG`）
- CI 通过 `.github/workflows/release-linux.yml` 自动发布 Linux amd64/arm64 二进制
- `scripts/install.sh`：curl 安装脚本，环境变量 `CRUN_REPO` / `CRUN_VERSION` / `CRUN_INSTALL_DIR`
- 设计文档：`docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
- 实现计划：`docs/superpowers/plans/YYYY-MM-DD-<topic>.md`
- 变更项目名或二进制名时，需同步更新：`CLAUDE.md`、`README.md`、`pyproject.toml`、`scripts/install.sh`、`.github/workflows/release-linux.yml`、`src/claude_run/config.py`
