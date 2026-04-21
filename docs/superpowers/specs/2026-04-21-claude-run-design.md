# claude-run 设计规格

## 概述

`claude-run` 是一个 Linux CLI 工具，通过 TUI 交互界面帮助用户选择 Claude CLI 的启动参数，然后组装并执行 `claude` 命令。

## 核心流程

```
claude-run [命令]
├── 首次运行 → 引导设置 → preferences.json → 主界面
└── 后续运行 → 读取 preferences.json → 主界面
```

## 交互模式

### 快速选择模式（默认）
- 上下键（↑/↓）在预设组之间导航
- 空格键勾选/取消选项
- 回车键确认并执行 `claude + 选中参数`
- 左/右键在组内选项之间切换（如在 Model 组内选 Opus/Sonnet/Haiku）

### 模糊搜索模式（A）
- 按 `/` 或 `Ctrl+S` 激活
- 光标跳到搜索框，输入即实时过滤
- 支持拼音、英文、中文模糊匹配
- 再次按 `/` 或 `Escape` 返回快速选择模式

### 统一搜索模式（B）
- 按 `Ctrl+U` 激活
- 搜索框常驻，实时过滤所有参数
- 上下键选择结果，回车确认

### 搜索匹配规则
| 输入 | 匹配目标 |
|---|---|
| `mcp` | `--mcp-config`（flag 原文） |
| `调试` | Debug 模式相关参数 |
| `model` | `--model`（英文原文） |
| `模型` | `--model`（中文描述） |

## 参数数据结构（JSON）

```json
{
  "version": 1,
  "flags": [
    {
      "flag": "--model",
      "description": {
        "zh": "当前会话使用的模型",
        "en": "Model for the current session"
      },
      "required_args": [],
      "type": "single",
      "group": "model",
      "choices": [
        { "value": "opus", "label": { "zh": "Opus", "en": "Opus" } },
        { "value": "sonnet", "label": { "zh": "Sonnet", "en": "Sonnet" } },
        { "value": "haiku", "label": { "zh": "Haiku", "en": "Haiku" } }
      ]
    },
    {
      "flag": "--mcp-config",
      "description": {
        "zh": "从 JSON 文件加载 MCP 服务器配置",
        "en": "Load MCP servers from JSON files"
      },
      "required_args": [
        {
          "name": "config_path",
          "label": { "zh": "配置文件路径", "en": "Config file path" },
          "placeholder": { "zh": "例: /path/to/mcp.json", "en": "e.g. /path/to/mcp.json" }
        }
      ],
      "type": "value",
      "group": "mcp"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `flag` | string | 参数原文，如 `--model` |
| `description` | object | 多语言功能描述，key 为语言码 |
| `required_args` | array | 触发该参数时用户必须输入的子参数 |
| `type` | enum | `single`（单选）/ `multi`（多选）/ `value`（需填值）|
| `group` | string | 所属预设组 |
| `choices` | array | type=single 时可选值列表 |
| `required_args[].name` | string | 子参数名 |
| `required_args[].label` | object | 子参数的多语言标签 |
| `required_args[].placeholder` | object | 子参数的输入提示 |

## 预设分组

| 组名 | 中文名 | 包含的参数 | 选择方式 |
|---|---|---|---|
| `model` | 模型 | `--model` | 单选 |
| `permission` | 权限模式 | `--permission-mode` | 单选 |
| `output` | 输出模式 | `-p`, `--output-format`, `--json-schema` | 多选 |
| `session` | 会话 | `-c/--continue`, `-r/--resume`, `--fork-session`, `--session-id` | 多选 |
| `tools` | 工具 | `--tools` | 单选 |
| `dev` | 开发模式 | `--bare`, `--disable-slash-commands`, `--strict-mcp-config` | 多选 |
| `debug` | 调试 | `-d`, `--debug-file`, `--mcp-debug` | 多选 |

## 配置文件布局

```
~/.config/claude-run/
├── preferences.json   # 用户偏好（首次运行生成）
├── flags_default.json # 默认参数集（内置，data/ 下）
└── flags_custom.json  # 用户自定义参数（可选，Merge 覆盖默认）
```

### preferences.json 结构

```json
{
  "search_mode": "A",          // "A" / "B" / "both"
  "language": "zh",             // "zh" / "en"
  "first_run": false
}
```

## 首次运行引导流程

```
1. 欢迎语 + 简介
2. 选择搜索模式：
   └─ A（模糊搜索） / B（统一搜索） / both（两者都显示）
3. 选择界面语言：
   └─ 中文 / English
4. 确认 → 写入 preferences.json → 进入主界面
```

## 目录结构

```
claude-run/
├── pyproject.toml
├── src/claude_run/
│   ├── __init__.py
│   ├── __main__.py      # 入口点：claude-run 命令
│   ├── app.py            # Textual TUI 主应用
│   ├── wizard.py         # 首次运行引导界面
│   ├── flags.py          # 参数定义、解析、Merge
│   ├── search.py         # 搜索匹配引擎
│   ├── runner.py         # 组装并执行 claude 命令
│   └── config.py         # 配置加载和偏好读写
├── data/
│   └── flags_default.json
└── tests/
```

## 技术选型

- **Python 3.10+**，**uv** 管理虚拟环境
- **Textual** 做 TUI（纯 Python，无额外 C 依赖）
- **fuzzywuzzy** 或自实现模糊匹配（纯 Python）

## 关键行为

1. **参数冲突处理**：同组参数互斥，后选中的覆盖先选中的
2. **自定义参数优先级**：`flags_custom.json` > `flags_default.json`
3. **子参数输入**：type=value 的参数被选中时，弹出子参数输入框
4. **空选择**：用户直接回车表示不传额外参数，执行 `claude`（原生行为）
5. **退出**：`Ctrl+C` 或 `q` 键退出程序，不执行 claude
