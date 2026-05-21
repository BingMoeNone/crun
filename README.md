# crun

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-blue?style=flat-square&logo=windows&logoColor=white)](https://github.com/BingMoeNone/crun)
[![GitHub release](https://img.shields.io/github/v/release/BingMoeNone/crun?style=flat-square)](https://github.com/BingMoeNone/crun/releases)

**crun** is a cross-platform TUI tool for interactively selecting [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) startup flags. Browse 71 flags across 15 groups, search by name / description / pinyin, and launch `claude <flags>` — no more memorizing CLI arguments.

[中文文档](README_zh.md)

## Quick Install

**Linux** (amd64 / arm64):

```bash
curl -fsSL https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.sh | bash
```

**Windows** (amd64, Windows Terminal recommended):

```powershell
irm https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.ps1 | iex
```

Specify a version: `CRUN_VERSION=v0.6.1` (Linux) or `$env:CRUN_VERSION="v0.6.1"` (Windows). See [releases](https://github.com/BingMoeNone/crun/releases) for all versions.

> **Prerequisite:** The `claude` CLI must be installed and available in PATH.

## Features

- **71 flags, 15 groups** — full Claude Code CLI reference, organized and browsable
- **`/` instant search** — filter by flag name, Chinese/English description, or choice values
- **Pinyin fuzzy search** — type `moxing` to match `模型`, supports partial pinyin
- **Search highlighting** — matched characters highlighted in yellow bold
- **Mutual exclusion** — conflicting flags (`--chrome` ↔ `--no-chrome`) auto-deselected
- **Sub-argument prompts** — `single` / `value` flags prompt immediately on toggle
- **Inline tooltips** — cursor-focused flag shows usage tip at screen bottom
- **Command history** — 9-entry ring buffer, adaptive layout (A/B), number-to-reuse
- **Parameter presets** — save/load named flag combinations for different workflows
- **Custom keybindings** — configure in `preferences.json`, conflict detection at startup
- **Custom flags** — extend via `~/.config/crun/flags_custom.json`
- **Bilingual UI** — first-run wizard (Chinese / English)

## Usage

```bash
crun
```

| Key | Action |
| --- | --- |
| `↑ / ↓` or `j / k` | Move cursor |
| `Space` | Toggle flag |
| `Enter` | Confirm selection |
| `/` | Enter search mode |
| `Backspace` | Delete search char |
| `Esc` | Exit search / quit selector |
| `Ctrl+C` | Cancel |
| `Ctrl+D` / `Ctrl+U` | Page up/down (Vim) |

Customize keybindings via `keybindings` in `~/.config/crun/preferences.json`.

## Configuration

```text
~/.config/crun/                        # Windows: %LOCALAPPDATA%\crun\
├── preferences.json                   # language, search_mode, keybindings, etc.
├── flags_custom.json                  # custom/override flag definitions
├── history.json                       # 9 most recent runs (ring buffer)
├── presets.json                       # saved parameter presets
└── flags_default.json                 # built-in flags (read-only, embedded)
```

## Custom Flags

Add or override flags in `~/.config/crun/flags_custom.json`:

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

## Development

```bash
git clone git@github.com:BingMoeNone/crun.git
cd crun

# uv is required: curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --all-groups
uv pip install -e .

# Run tests
uv run pytest tests/ -v

# Build binary
uv run pyinstaller --onefile --name crun --paths src \
  --add-data "data/flags_default.json:data" \
  --add-data "pyproject.toml:." \
  --copy-metadata crun \
  src/claude_run/__main__.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for PR guidelines and [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

[Apache 2.0](LICENSE)
