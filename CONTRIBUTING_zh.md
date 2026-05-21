# 参与贡献 crun

[English](CONTRIBUTING.md)

感谢你对贡献 crun 的关注！

## 开发环境搭建

```bash
git clone git@github.com:BingMoeNone/crun.git
cd crun

# 需安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --all-groups
uv pip install -e .
```

## 运行测试

```bash
uv run pytest tests/ -v
uv run pytest tests/ -v --cov=src/claude_run --cov-report=term-missing
```

## 代码风格

- Python 3.12+
- 遵循项目现有代码模式
- 禁止 AI 生成的解释性注释 — 良好的命名即文档
- 保持提交专注且原子化

## Pull Request 指南

1. Fork 本仓库并从 `main` 创建功能分支
2. 进行修改，适当时包含测试
3. 确保所有测试通过：`uv run pytest tests/ -v`
4. 如果修改了 `scripts/install.sh` 或 `scripts/install.ps1`，**必须**同步修改另一个 — 这是硬性要求（参见 CLAUDE.md）
5. 向 `main` 提交 PR，附上清晰的描述

## 新增参数

新的 Claude Code CLI 参数可添加到 `data/flags_default.json`。每个参数需要：

```json
{
  "flag": "--new-flag",
  "description": { "zh": "中文描述", "en": "English description" },
  "required_args": [],
  "type": "multi",
  "group": "<group-name>"
}
```

## 架构

详见 [CLAUDE.md](CLAUDE.md) 获取代码库的详细说明。
