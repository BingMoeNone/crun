# crun: Flag Completion & Project Rename

## Summary

补全 CLI flag 定义使其与 Claude Code 官方文档对齐（19 → 63 个 flag），同时将项目重命名为 `crun`。

## Motivation

当前 `flags_default.json` 仅有 19 个 flag，而 Claude Code 官方 CLI 参考列出了 63 个。差距导致用户无法通过 TUI 选择大量有用的启动参数。同时 `claude-run` 名称较长，缩写 `crun` 更简洁。

## Design Decisions

| 决策 | 选择 |
|------|------|
| Scope | 63 个 flag 全部补全 |
| 分组 | 按官方文档页面分类，15 组 |
| Model choices | 别名 + 完整模型名 |
| 互斥 | TUI 自动互斥（`conflicts_with` 字段） |
| 项目名 | `claude-run` → `crun` |
| 配置迁移 | 自动检测旧路径 `~/.config/claude-run/`，存在则迁移到 `~/.config/crun/` |

## Architecture

```
data/flags_default.json          # 63 flag 定义（新增 conflicts_with）
src/claude_run/flags.py          # Flag dataclass + conflicts_with 解析
src/claude_run/app.py            # 15 组标签 + 互斥逻辑
src/claude_run/runner.py         # 不变
src/claude_run/search.py         # 不变
src/claude_run/config.py         # CONFIG_DIR 路径更新 + 旧配置迁移
src/claude_run/__main__.py       # entry point: crun
pyproject.toml                   # name + scripts 更新
CLAUDE.md                        # 命令引用更新
tests/                           # 新测试
```

## Flag Groups (15 groups, 63 flags)

完整 flag 列表见实现时编写的 `flags_default.json`。分组如下：

| 组 key | 中文标签 | 英文标签 | count |
|--------|---------|---------|-------|
| model | 模型 | Model | 3 |
| permission | 权限 | Permission | 6 |
| output | 输出 | Output | 8 |
| session | 会话 | Session | 9 |
| tools | 工具 | Tools | 2 |
| system | 系统提示 | System Prompt | 4 |
| dev | 开发 | Dev | 6 |
| mcp | MCP/插件 | MCP/Plugin | 3 |
| debug | 调试 | Debug | 3 |
| agent | Agent | Agent | 6 |
| ide | IDE/浏览器 | IDE/Browser | 3 |
| remote | 远程 | Remote | 6 |
| hook | Hooks | Hooks | 3 |
| limit | 限制 | Limits | 2 |
| config | 配置 | Config | 2 |

## New Flag Data Field: `conflicts_with`

```json
{
  "flag": "--chrome",
  "conflicts_with": ["--no-chrome"],
  ...
}
```

TUI 行为：勾选 flag 时，自动取消 `conflicts_with` 中所有已选项（及对应的 value_state）。

互斥对：
- `--chrome` ↔ `--no-chrome`
- `--system-prompt` ↔ `--system-prompt-file`

## Project Rename: `claude-run` → `crun`

- CLI 入口：`crun`（原 `claude-run`）
- Package 名保持 `claude_run`（Python import 路径不变）
- 配置目录：`~/.config/crun/`（自动从旧路径迁移）
- 更新文件：`pyproject.toml`、`CLAUDE.md`、`config.py`、`__main__.py`

### 配置迁移策略

`config.py` 启动时检测：
1. 旧路径 `~/.config/claude-run/` 存在且新路径 `~/.config/crun/` 不存在 → 自动 rename 迁移
2. 两者都存在 → 使用新路径，旧路径忽略（不删除，用户手动清理）
3. 仅新路径存在 → 正常使用

## Model Choices Update

```
sonnet, opus, haiku (别名)
+ claude-sonnet-4-6, claude-opus-4-7, claude-opus-4-6, claude-haiku-4-5 (完整名)
```

## Description Fixes

- `--bare`: 补充 "跳过 skills、MCP 服务器、CLAUDE.md 自动发现"
- `--disable-slash-commands`: 补充 "和命令"

## Testing

- `test_flags.py`: 全 flag JSON schema 校验（type 合法性、required_args 结构、conflicts_with 引用完整性）
- `test_app.py`: 互斥逻辑测试
- `test_config.py`: 配置迁移测试
- 现有测试全部保持通过
