# crun · 中文文档

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-blue?style=flat-square&logo=windows&logoColor=white)](https://github.com/BingMoeNone/crun)
[![GitHub release](https://img.shields.io/github/v/release/BingMoeNone/crun?style=flat-square)](https://github.com/BingMoeNone/crun/releases)

**crun** 是一个跨平台 TUI 工具，通过交互界面选择 [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) 的 71 个启动参数（15 个分组），然后执行 `claude <flags>`。支持拼音模糊搜索、搜索高亮、参数互斥、命令历史、参数预设和自定义快捷键。

[English README](README.md)

## 快速安装

**Linux**（amd64 / arm64）：

```bash
curl -fsSL https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.sh | bash
```

**Windows**（amd64，推荐使用 Windows Terminal）：

```powershell
irm https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.ps1 | iex
```

指定版本：`CRUN_VERSION=v0.6.1`（Linux）或 `$env:CRUN_VERSION="v0.6.1"`（Windows）。所有版本见 [releases](https://github.com/BingMoeNone/crun/releases)。

> **前置条件：** 系统中需已安装 `claude` 命令并在 PATH 中。

## 功能特性

- **71 个启动参数，15 个分组** — 完整的 Claude Code CLI 参数，分类浏览
- **`/` 即时搜索** — 按 flag 名、中英文描述或子选项值搜索
- **拼音模糊搜索** — 输入 `moxing` 即可匹配「模型」，支持全拼和部分拼音
- **搜索字符高亮** — 匹配的字符以黄色加粗高亮，帮助理解匹配原因
- **参数互斥** — 冲突 flag（如 `--chrome` ↔ `--no-chrome`）自动取消对方
- **子参数追问** — `single` / `value` 类型参数勾选后立即弹出选择/输入界面
- **参数提示** — 光标停留时底部显示详细使用说明（优先 JSON 自定义，自动生成兜底）
- **命令历史** — 9 条环形缓冲记录，大终端编号列表 / 小终端精简预览，数字一键复用
- **参数预设** — 保存当前选择为命名预设，一键切换不同使用场景
- **自定义快捷键** — `preferences.json` 中配置键位映射，启动时自动冲突检测
- **可扩展参数** — 通过 `~/.config/crun/flags_custom.json` 覆盖或新增参数
- **双语界面** — 首次运行向导支持中文 / English

## 使用

```bash
crun
```

| 按键 | 功能 |
| --- | --- |
| `↑ / ↓` 或 `j / k` | 上下移动 |
| `Space` | 勾选/取消当前参数 |
| `Enter` | 确认选择 |
| `/` | 进入搜索模式 |
| `Backspace` | 删除搜索字符 |
| `Esc` | 退出搜索 / 退出选择器 |
| `Ctrl+C` | 取消 |
| `Ctrl+D` / `Ctrl+U` | 上下翻页（Vim） |

可在 `~/.config/crun/preferences.json` 的 `keybindings` 字段中自定义键位。

## 配置文件

```text
~/.config/crun/                        # Windows: %LOCALAPPDATA%\crun\
├── preferences.json                   # 语言、搜索模式、快捷键等
├── flags_custom.json                  # 自定义/覆盖参数定义
├── history.json                       # 最近 9 次执行记录（环形缓冲）
├── presets.json                       # 保存的参数预设方案
└── flags_default.json                 # 内置参数（只读，打包嵌入）
```

## 参数互斥机制

部分 flag 互斥（如 `--chrome` 与 `--no-chrome`、`--system-prompt` 与 `--system-prompt-file`）。TUI 中勾选互斥 flag 时自动取消对方，历史复用和命令行构建阶段也有相应的防御清洗。

## 命令历史

执行成功后会保存到环形缓冲（最近 9 次）：`~/.config/crun/history.json`

未勾选参数就执行时自动展示历史记录，根据终端大小自适应展示：

**方案 A（大终端 — 剩余空间 ≥ 10 行）：** 完整编号列表，输入数字选择第 N 条（回车 = 上次），`q` 取消。

**方案 B（小终端 — 剩余空间 < 10 行）：** 精简预览（最新一条），提供：
- 使用上次（Enter）— 快速复用
- 更多历史 — 展开完整列表
- 重新选择 — 回到选择界面

可在 `preferences.json` 中设置 `history_mode: "A"` 或 `"B"` 固定方案。

## 参数预设

主菜单提供保存/加载预设：

- **保存预设**：当前参数组合保存为命名预设 → `presets.json`
- **加载预设**：选择预设加载，自动清洗失效参数，支持删除（需二次确认）
- **覆盖保护**：同名预设会提示确认覆盖

## 自定义参数

`~/.config/crun/flags_custom.json`：

```json
{
  "version": 1,
  "flags": [
    {
      "flag": "--my-custom-flag",
      "description": { "zh": "我的自定义参数", "en": "My custom flag" },
      "required_args": [],
      "type": "multi",
      "group": "custom"
    }
  ]
}
```

## 源码安装

```bash
git clone git@github.com:BingMoeNone/crun.git
cd crun

# 需安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --all-groups
uv pip install -e .
```

## 开发

```bash
# 运行测试
uv run pytest tests/ -v

# 本地打包
uv run pyinstaller --onefile --name crun --paths src \
  --add-data "data/flags_default.json:data" \
  --add-data "pyproject.toml:." \
  --copy-metadata crun \
  src/claude_run/__main__.py
```

详见 [CONTRIBUTING.md](CONTRIBUTING.md)（PR 指南）和 [SECURITY.md](SECURITY.md)（安全漏洞报告）。

## License

[Apache 2.0](LICENSE)
