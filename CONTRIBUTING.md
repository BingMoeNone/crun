# Contributing to crun

[中文](CONTRIBUTING_zh.md)

Thanks for your interest in contributing!

## Development Setup

```bash
git clone git@github.com:BingMoeNone/crun.git
cd crun

# Install uv if needed: curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --all-groups
uv pip install -e .
```

## Running Tests

```bash
uv run pytest tests/ -v
uv run pytest tests/ -v --cov=src/claude_run --cov-report=term-missing
```

## Code Style

- Python 3.12+
- Follow existing patterns in the codebase
- No AI-generated comments explaining what code does — well-named identifiers speak for themselves
- Keep commits focused and atomic

## Pull Request Guidelines

1. Fork the repo and create a feature branch from `main`
2. Make your changes, including tests if applicable
3. Ensure all tests pass: `uv run pytest tests/ -v`
4. If you modify `scripts/install.sh` or `scripts/install.ps1`, you MUST update the other to match — this is a hard requirement (see CLAUDE.md)
5. Submit a PR against `main` with a clear description

## Adding New Flags

New Claude Code CLI flags can be added to `data/flags_default.json`. Each flag needs:

```json
{
  "flag": "--new-flag",
  "description": { "zh": "中文描述", "en": "English description" },
  "required_args": [],
  "type": "multi",
  "group": "<group-name>"
}
```

## Architecture

See [CLAUDE.md](CLAUDE.md) for a detailed walkthrough of the codebase.
