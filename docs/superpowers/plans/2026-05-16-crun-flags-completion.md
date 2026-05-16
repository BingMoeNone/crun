# crun: Flag Completion & Project Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 补全 63 个 CLI flag 到 `flags_default.json`，添加互斥机制，项目重命名为 `crun`，配置路径迁移。

**Architecture:** 数据层（flags_default.json + Flag dataclass）→ 交互层（app.py TUI + 互斥逻辑）→ 配置层（config.py 迁移）。改动沿现有架构模式，最小化侵入。

**Tech Stack:** Python 3.12+, prompt_toolkit, questionary, pytest

---

### Task 1: Add `conflicts_with` to Flag dataclass and parsing

**Files:**
- Modify: `src/claude_run/flags.py:53-64` (Flag dataclass)
- Modify: `src/claude_run/flags.py:108-149` (_parse_flags)

- [ ] **Step 1: Add `conflicts_with` field to Flag dataclass**

```python
@dataclass
class Flag:
    """一个 Claude CLI 参数。"""
    flag: str
    description: dict[str, str]
    required_args: list[RequiredArg]
    type: str  # "single" | "multi" | "value"
    group: str
    choices: list[Choice] | None = None
    conflicts_with: list[str] | None = None  # 互斥 flag 名列表
```

- [ ] **Step 2: Parse `conflicts_with` in `_parse_flags()`**

In `_parse_flags()`, inside the try block, after parsing `choices`, add:

```python
conflicts_with = item.get("conflicts_with")
if isinstance(conflicts_with, list):
    conflicts_with = [str(c) for c in conflicts_with if isinstance(c, str)]
else:
    conflicts_with = None
```

Then pass it to the Flag constructor:

```python
result.append(Flag(
    flag=flag_name,
    description=description,
    required_args=required_args,
    type=flag_type,
    group=group,
    choices=choices,
    conflicts_with=conflicts_with,
))
```

- [ ] **Step 3: Run existing tests to ensure no regression**

```bash
uv run pytest tests/ -v
```

Expected: all 14 tests pass.

- [ ] **Step 4: Commit**

```bash
git add src/claude_run/flags.py
git commit -m "feat: add conflicts_with field to Flag dataclass"
```

---

### Task 2: Write complete `flags_default.json` with 63+ flags

**Files:**
- Modify: `data/flags_default.json`

- [ ] **Step 1: Write the complete flags JSON**

Replace the entire content of `data/flags_default.json`:

```json
{
  "version": 1,
  "flags": [
    {
      "flag": "--model",
      "description": { "zh": "当前会话使用的模型，支持别名或完整模型名", "en": "Model for the current session (alias or full name)" },
      "required_args": [],
      "type": "single",
      "group": "model",
      "choices": [
        { "value": "sonnet", "label": { "zh": "Sonnet (最新)", "en": "Sonnet (latest)" } },
        { "value": "opus", "label": { "zh": "Opus (最新)", "en": "Opus (latest)" } },
        { "value": "haiku", "label": { "zh": "Haiku (最新)", "en": "Haiku (latest)" } },
        { "value": "claude-sonnet-4-6", "label": { "zh": "Claude Sonnet 4.6", "en": "Claude Sonnet 4.6" } },
        { "value": "claude-opus-4-7", "label": { "zh": "Claude Opus 4.7", "en": "Claude Opus 4.7" } },
        { "value": "claude-opus-4-6", "label": { "zh": "Claude Opus 4.6", "en": "Claude Opus 4.6" } },
        { "value": "claude-haiku-4-5", "label": { "zh": "Claude Haiku 4.5", "en": "Claude Haiku 4.5" } }
      ]
    },
    {
      "flag": "--effort",
      "description": { "zh": "设置当前会话的工作量级别", "en": "Set effort level for the current session" },
      "required_args": [],
      "type": "single",
      "group": "model",
      "choices": [
        { "value": "low", "label": { "zh": "Low", "en": "Low" } },
        { "value": "medium", "label": { "zh": "Medium", "en": "Medium" } },
        { "value": "high", "label": { "zh": "High", "en": "High" } },
        { "value": "xhigh", "label": { "zh": "XHigh", "en": "XHigh" } },
        { "value": "max", "label": { "zh": "Max (仅当前会话)", "en": "Max (this session only)" } }
      ]
    },
    {
      "flag": "--fallback-model",
      "description": { "zh": "默认模型过载时自动回退到指定模型（仅打印模式）", "en": "Auto fallback model when default is overloaded (print mode only)" },
      "required_args": [{ "name": "model", "label": { "zh": "回退模型", "en": "Fallback model" }, "placeholder": { "zh": "例: sonnet", "en": "e.g. sonnet" } }],
      "type": "value",
      "group": "model"
    },
    {
      "flag": "--permission-mode",
      "description": { "zh": "当前会话的权限模式", "en": "Permission mode for the session" },
      "required_args": [],
      "type": "single",
      "group": "permission",
      "choices": [
        { "value": "acceptEdits", "label": { "zh": "Accept Edits", "en": "Accept Edits" } },
        { "value": "auto", "label": { "zh": "Auto", "en": "Auto" } },
        { "value": "bypassPermissions", "label": { "zh": "Bypass Permissions", "en": "Bypass Permissions" } },
        { "value": "default", "label": { "zh": "Default", "en": "Default" } },
        { "value": "dontAsk", "label": { "zh": "Don't Ask", "en": "Don't Ask" } },
        { "value": "plan", "label": { "zh": "Plan", "en": "Plan" } }
      ]
    },
    {
      "flag": "--dangerously-skip-permissions",
      "description": { "zh": "跳过权限提示（等同于 --permission-mode bypassPermissions）", "en": "Skip all permission prompts (same as --permission-mode bypassPermissions)" },
      "required_args": [],
      "type": "multi",
      "group": "permission"
    },
    {
      "flag": "--allow-dangerously-skip-permissions",
      "description": { "zh": "允许在 Shift+Tab 切换到 bypassPermissions 模式", "en": "Allow switching to bypassPermissions via Shift+Tab" },
      "required_args": [],
      "type": "multi",
      "group": "permission"
    },
    {
      "flag": "--allowedTools",
      "description": { "zh": "无需提示权限即可执行的工具列表", "en": "Tools allowed without permission prompts" },
      "required_args": [{ "name": "tools", "label": { "zh": "工具列表", "en": "Tool list" }, "placeholder": { "zh": "例: \"Bash(git *)\" \"Read\"", "en": "e.g. \"Bash(git *)\" \"Read\"" } }],
      "type": "value",
      "group": "permission"
    },
    {
      "flag": "--disallowedTools",
      "description": { "zh": "从模型上下文中移除的工具，不可使用", "en": "Tools removed from context, cannot be used" },
      "required_args": [{ "name": "tools", "label": { "zh": "工具列表", "en": "Tool list" }, "placeholder": { "zh": "例: \"Bash(git *)\" \"Edit\"", "en": "e.g. \"Bash(git *)\" \"Edit\"" } }],
      "type": "value",
      "group": "permission"
    },
    {
      "flag": "--permission-prompt-tool",
      "description": { "zh": "指定 MCP 工具以在非交互模式下处理权限提示", "en": "MCP tool to handle permission prompts in non-interactive mode" },
      "required_args": [{ "name": "tool", "label": { "zh": "MCP 工具名", "en": "MCP tool name" }, "placeholder": { "zh": "例: mcp_auth_tool", "en": "e.g. mcp_auth_tool" } }],
      "type": "value",
      "group": "permission"
    },
    {
      "flag": "-p",
      "description": { "zh": "打印输出后退出（非交互模式）", "en": "Print response and exit (non-interactive)" },
      "required_args": [],
      "type": "multi",
      "group": "output"
    },
    {
      "flag": "--print",
      "description": { "zh": "打印输出后退出（非交互模式，同 -p）", "en": "Print response and exit (same as -p)" },
      "required_args": [],
      "type": "multi",
      "group": "output"
    },
    {
      "flag": "--output-format",
      "description": { "zh": "输出格式（仅打印模式）", "en": "Output format for print mode" },
      "required_args": [],
      "type": "single",
      "group": "output",
      "choices": [
        { "value": "text", "label": { "zh": "Text", "en": "Text" } },
        { "value": "json", "label": { "zh": "JSON", "en": "JSON" } },
        { "value": "stream-json", "label": { "zh": "Stream JSON", "en": "Stream JSON" } }
      ]
    },
    {
      "flag": "--json-schema",
      "description": { "zh": "结构化输出的 JSON Schema 验证（仅打印模式）", "en": "JSON Schema for structured output validation (print mode)" },
      "required_args": [{ "name": "schema", "label": { "zh": "Schema", "en": "Schema" }, "placeholder": { "zh": "例: {\"type\":\"object\"}", "en": "e.g. {\"type\":\"object\"}" } }],
      "type": "value",
      "group": "output"
    },
    {
      "flag": "--input-format",
      "description": { "zh": "为打印模式指定输入格式", "en": "Specify input format for print mode" },
      "required_args": [],
      "type": "single",
      "group": "output",
      "choices": [
        { "value": "text", "label": { "zh": "Text", "en": "Text" } },
        { "value": "stream-json", "label": { "zh": "Stream JSON", "en": "Stream JSON" } }
      ]
    },
    {
      "flag": "--include-hook-events",
      "description": { "zh": "在输出流中包含所有 hook 生命周期事件（需 --output-format stream-json）", "en": "Include hook lifecycle events in output (needs --output-format stream-json)" },
      "required_args": [],
      "type": "multi",
      "group": "output"
    },
    {
      "flag": "--include-partial-messages",
      "description": { "zh": "在输出中包含部分流事件（需 -p 和 --output-format stream-json）", "en": "Include partial stream events in output (needs -p and stream-json)" },
      "required_args": [],
      "type": "multi",
      "group": "output"
    },
    {
      "flag": "--replay-user-messages",
      "description": { "zh": "从 stdin 重放用户消息到 stdout（需 stream-json 输入输出）", "en": "Re-emit user messages from stdin to stdout (needs stream-json I/O)" },
      "required_args": [],
      "type": "multi",
      "group": "output"
    },
    {
      "flag": "--exclude-dynamic-system-prompt-sections",
      "description": { "zh": "将机器相关部分从系统提示移到首条用户消息，改进跨机器缓存重用", "en": "Move machine-specific prompt sections to first user message for cache reuse" },
      "required_args": [],
      "type": "multi",
      "group": "output"
    },
    {
      "flag": "-c",
      "description": { "zh": "继续当前目录最近的会话", "en": "Continue the most recent conversation" },
      "required_args": [],
      "type": "multi",
      "group": "session"
    },
    {
      "flag": "--continue",
      "description": { "zh": "继续当前目录最近的会话（同 -c）", "en": "Continue the most recent conversation (same as -c)" },
      "required_args": [],
      "type": "multi",
      "group": "session"
    },
    {
      "flag": "-r",
      "description": { "zh": "通过会话 ID 或名称恢复会话，或打开交互选择器", "en": "Resume a session by ID or name, or open interactive selector" },
      "required_args": [{ "name": "session_id", "label": { "zh": "会话 ID/名称", "en": "Session ID/name" }, "placeholder": { "zh": "例: abc-123", "en": "e.g. abc-123" } }],
      "type": "value",
      "group": "session"
    },
    {
      "flag": "--resume",
      "description": { "zh": "恢复会话（同 -r）", "en": "Resume a conversation (same as -r)" },
      "required_args": [{ "name": "session_id", "label": { "zh": "会话 ID/名称", "en": "Session ID/name" }, "placeholder": { "zh": "例: auth-refactor", "en": "e.g. auth-refactor" } }],
      "type": "value",
      "group": "session"
    },
    {
      "flag": "--fork-session",
      "description": { "zh": "恢复时创建新的会话 ID", "en": "Create a new session ID when resuming" },
      "required_args": [],
      "type": "multi",
      "group": "session"
    },
    {
      "flag": "--session-id",
      "description": { "zh": "使用指定 UUID 的会话", "en": "Use a specific session UUID" },
      "required_args": [{ "name": "uuid", "label": { "zh": "UUID", "en": "UUID" }, "placeholder": { "zh": "例: 550e8400-e29b-41d4-a716-446655440000", "en": "e.g. 550e8400-e29b-41d4-a716-446655440000" } }],
      "type": "value",
      "group": "session"
    },
    {
      "flag": "-n",
      "description": { "zh": "为会话设置显示名称", "en": "Set a display name for the session" },
      "required_args": [{ "name": "name", "label": { "zh": "会话名称", "en": "Session name" }, "placeholder": { "zh": "例: my-feature-work", "en": "e.g. my-feature-work" } }],
      "type": "value",
      "group": "session"
    },
    {
      "flag": "--name",
      "description": { "zh": "为会话设置显示名称（同 -n）", "en": "Set a display name for the session (same as -n)" },
      "required_args": [{ "name": "name", "label": { "zh": "会话名称", "en": "Session name" }, "placeholder": { "zh": "例: my-feature-work", "en": "e.g. my-feature-work" } }],
      "type": "value",
      "group": "session"
    },
    {
      "flag": "--from-pr",
      "description": { "zh": "恢复链接到特定 PR 的会话（PR 号或 URL）", "en": "Resume session linked to a pull request (number or URL)" },
      "required_args": [{ "name": "pr", "label": { "zh": "PR 号/URL", "en": "PR number/URL" }, "placeholder": { "zh": "例: 123", "en": "e.g. 123" } }],
      "type": "value",
      "group": "session"
    },
    {
      "flag": "--no-session-persistence",
      "description": { "zh": "禁用会话持久化，会话不保存到磁盘（仅打印模式）", "en": "Disable session persistence (print mode only)" },
      "required_args": [],
      "type": "multi",
      "group": "session"
    },
    {
      "flag": "--tools",
      "description": { "zh": "限制可用的内置工具（\"\" 禁用所有，\"default\" 全部）", "en": "Limit available built-in tools (\"\" to disable all, \"default\" for all)" },
      "required_args": [],
      "type": "single",
      "group": "tools",
      "choices": [
        { "value": "default", "label": { "zh": "所有工具（默认）", "en": "All tools (default)" } },
        { "value": "", "label": { "zh": "禁用所有工具", "en": "Disable all tools" } },
        { "value": "Bash,Edit,Read", "label": { "zh": "仅 Bash/Edit/Read", "en": "Bash/Edit/Read only" } }
      ]
    },
    {
      "flag": "--add-dir",
      "description": { "zh": "添加额外的工作目录以读取和编辑文件", "en": "Add additional working directories for file access" },
      "required_args": [{ "name": "dir", "label": { "zh": "目录路径", "en": "Directory path" }, "placeholder": { "zh": "例: ../apps ../lib", "en": "e.g. ../apps ../lib" } }],
      "type": "value",
      "group": "tools"
    },
    {
      "flag": "--system-prompt",
      "description": { "zh": "用自定义文本替换整个系统提示", "en": "Replace the entire system prompt with custom text" },
      "required_args": [{ "name": "prompt", "label": { "zh": "系统提示", "en": "System prompt" }, "placeholder": { "zh": "例: You are a Python expert", "en": "e.g. You are a Python expert" } }],
      "type": "value",
      "group": "system",
      "conflicts_with": ["--system-prompt-file"]
    },
    {
      "flag": "--system-prompt-file",
      "description": { "zh": "从文件加载系统提示，替换默认提示", "en": "Load system prompt from file, replacing the default" },
      "required_args": [{ "name": "path", "label": { "zh": "文件路径", "en": "File path" }, "placeholder": { "zh": "例: ./custom-prompt.txt", "en": "e.g. ./custom-prompt.txt" } }],
      "type": "value",
      "group": "system",
      "conflicts_with": ["--system-prompt"]
    },
    {
      "flag": "--append-system-prompt",
      "description": { "zh": "将自定义文本附加到默认系统提示末尾", "en": "Append custom text to the end of the default system prompt" },
      "required_args": [{ "name": "text", "label": { "zh": "附加文本", "en": "Append text" }, "placeholder": { "zh": "例: Always use TypeScript", "en": "e.g. Always use TypeScript" } }],
      "type": "value",
      "group": "system"
    },
    {
      "flag": "--append-system-prompt-file",
      "description": { "zh": "从文件加载额外系统提示文本并附加到默认提示", "en": "Load additional system prompt text from file and append" },
      "required_args": [{ "name": "path", "label": { "zh": "文件路径", "en": "File path" }, "placeholder": { "zh": "例: ./extra-rules.txt", "en": "e.g. ./extra-rules.txt" } }],
      "type": "value",
      "group": "system"
    },
    {
      "flag": "--bare",
      "description": { "zh": "最小模式：跳过 hooks、skills、plugins、MCP 服务器、auto-memory 和 CLAUDE.md 自动发现", "en": "Minimal mode: skip hooks, skills, plugins, MCP servers, auto-memory, and CLAUDE.md auto-discovery" },
      "required_args": [],
      "type": "multi",
      "group": "dev"
    },
    {
      "flag": "--disable-slash-commands",
      "description": { "zh": "为此会话禁用所有 skills 和命令", "en": "Disable all slash command skills and commands for this session" },
      "required_args": [],
      "type": "multi",
      "group": "dev"
    },
    {
      "flag": "--strict-mcp-config",
      "description": { "zh": "仅使用 --mcp-config 指定的 MCP 服务器，忽略其他 MCP 配置", "en": "Only use MCP servers from --mcp-config, ignoring other MCP configurations" },
      "required_args": [],
      "type": "multi",
      "group": "dev"
    },
    {
      "flag": "--verbose",
      "description": { "zh": "启用详细日志记录，显示完整的逐轮输出", "en": "Enable verbose logging, showing full turn-by-turn output" },
      "required_args": [],
      "type": "multi",
      "group": "dev"
    },
    {
      "flag": "-v",
      "description": { "zh": "输出版本号", "en": "Output version number" },
      "required_args": [],
      "type": "multi",
      "group": "dev"
    },
    {
      "flag": "--version",
      "description": { "zh": "输出版本号（同 -v）", "en": "Output version number (same as -v)" },
      "required_args": [],
      "type": "multi",
      "group": "dev"
    },
    {
      "flag": "--betas",
      "description": { "zh": "要包含在 API 请求中的 Beta 标头（仅 API 密钥用户）", "en": "Beta headers to include in API requests (API key users only)" },
      "required_args": [{ "name": "betas", "label": { "zh": "Beta 标头", "en": "Beta headers" }, "placeholder": { "zh": "例: interleaved-thinking", "en": "e.g. interleaved-thinking" } }],
      "type": "value",
      "group": "dev"
    },
    {
      "flag": "--mcp-config",
      "description": { "zh": "从 JSON 文件或字符串加载 MCP 服务器配置", "en": "Load MCP servers from JSON files or strings" },
      "required_args": [{ "name": "config_path", "label": { "zh": "配置文件路径", "en": "Config file path" }, "placeholder": { "zh": "例: /path/to/mcp.json", "en": "e.g. /path/to/mcp.json" } }],
      "type": "value",
      "group": "mcp"
    },
    {
      "flag": "--plugin-dir",
      "description": { "zh": "从此目录或 .zip 加载插件（可重复使用以加载多个）", "en": "Load plugin from directory or .zip (repeatable for multiple)" },
      "required_args": [{ "name": "path", "label": { "zh": "插件路径", "en": "Plugin path" }, "placeholder": { "zh": "例: ./my-plugin", "en": "e.g. ./my-plugin" } }],
      "type": "value",
      "group": "mcp"
    },
    {
      "flag": "--plugin-url",
      "description": { "zh": "从 URL 获取插件 .zip 存档（可重复使用以加载多个）", "en": "Fetch plugin .zip from URL (repeatable for multiple)" },
      "required_args": [{ "name": "url", "label": { "zh": "插件 URL", "en": "Plugin URL" }, "placeholder": { "zh": "例: https://example.com/plugin.zip", "en": "e.g. https://example.com/plugin.zip" } }],
      "type": "value",
      "group": "mcp"
    },
    {
      "flag": "-d",
      "description": { "zh": "启用调试模式", "en": "Enable debug mode" },
      "required_args": [],
      "type": "multi",
      "group": "debug"
    },
    {
      "flag": "--debug",
      "description": { "zh": "启用调试模式（可指定分类过滤）", "en": "Enable debug mode with optional category filtering" },
      "required_args": [{ "name": "filter", "label": { "zh": "过滤分类", "en": "Filter category" }, "placeholder": { "zh": "例: api,hooks", "en": "e.g. api,hooks" } }],
      "type": "value",
      "group": "debug"
    },
    {
      "flag": "--debug-file",
      "description": { "zh": "将调试日志写入指定文件", "en": "Write debug logs to a specific file path" },
      "required_args": [{ "name": "path", "label": { "zh": "日志文件路径", "en": "Log file path" }, "placeholder": { "zh": "例: /tmp/claude-debug.log", "en": "e.g. /tmp/claude-debug.log" } }],
      "type": "value",
      "group": "debug"
    },
    {
      "flag": "--agent",
      "description": { "zh": "为当前会话指定代理（覆盖 agent 设置）", "en": "Specify agent for the current session" },
      "required_args": [{ "name": "agent", "label": { "zh": "代理名称", "en": "Agent name" }, "placeholder": { "zh": "例: my-custom-agent", "en": "e.g. my-custom-agent" } }],
      "type": "value",
      "group": "agent"
    },
    {
      "flag": "--agents",
      "description": { "zh": "通过 JSON 动态定义自定义 subagents", "en": "Dynamically define custom subagents via JSON" },
      "required_args": [{ "name": "json", "label": { "zh": "JSON 定义", "en": "JSON definition" }, "placeholder": { "zh": "例: {\"reviewer\":{\"description\":\"...\",\"prompt\":\"...\"}}", "en": "e.g. {\"reviewer\":{\"description\":\"...\",\"prompt\":\"...\"}}" } }],
      "type": "value",
      "group": "agent"
    },
    {
      "flag": "--bg",
      "description": { "zh": "启动会话作为后台代理并立即返回", "en": "Start session as background agent and return immediately" },
      "required_args": [],
      "type": "multi",
      "group": "agent"
    },
    {
      "flag": "--teammate-mode",
      "description": { "zh": "设置 agent team 队友的显示方式", "en": "Set how agent team teammates are displayed" },
      "required_args": [],
      "type": "single",
      "group": "agent",
      "choices": [
        { "value": "auto", "label": { "zh": "Auto（默认）", "en": "Auto (default)" } },
        { "value": "in-process", "label": { "zh": "In-Process", "en": "In-Process" } },
        { "value": "tmux", "label": { "zh": "Tmux", "en": "Tmux" } }
      ]
    },
    {
      "flag": "-w",
      "description": { "zh": "在隔离的 git worktree 中启动 Claude", "en": "Start Claude in an isolated git worktree" },
      "required_args": [{ "name": "name", "label": { "zh": "worktree 名称", "en": "Worktree name" }, "placeholder": { "zh": "例: feature-auth", "en": "e.g. feature-auth" } }],
      "type": "value",
      "group": "agent"
    },
    {
      "flag": "--worktree",
      "description": { "zh": "在隔离的 git worktree 中启动 Claude（同 -w）", "en": "Start Claude in an isolated git worktree (same as -w)" },
      "required_args": [{ "name": "name", "label": { "zh": "worktree 名称", "en": "Worktree name" }, "placeholder": { "zh": "例: feature-auth", "en": "e.g. feature-auth" } }],
      "type": "value",
      "group": "agent"
    },
    {
      "flag": "--tmux",
      "description": { "zh": "为 worktree 创建 tmux 会话（需 --worktree）", "en": "Create tmux session for worktree (needs --worktree)" },
      "required_args": [{ "name": "type", "label": { "zh": "tmux 类型", "en": "Tmux type" }, "placeholder": { "zh": "留空或 classic", "en": "empty or classic" } }],
      "type": "value",
      "group": "agent"
    },
    {
      "flag": "--ide",
      "description": { "zh": "启动时自动连接到可用的 IDE", "en": "Auto-connect to an available IDE at startup" },
      "required_args": [],
      "type": "multi",
      "group": "ide"
    },
    {
      "flag": "--chrome",
      "description": { "zh": "启用 Chrome 浏览器集成以进行网络自动化和测试", "en": "Enable Chrome browser integration for web automation and testing" },
      "required_args": [],
      "type": "multi",
      "group": "ide",
      "conflicts_with": ["--no-chrome"]
    },
    {
      "flag": "--no-chrome",
      "description": { "zh": "为此会话禁用 Chrome 浏览器集成", "en": "Disable Chrome browser integration for this session" },
      "required_args": [],
      "type": "multi",
      "group": "ide",
      "conflicts_with": ["--chrome"]
    },
    {
      "flag": "--remote",
      "description": { "zh": "在 claude.ai 上创建新的网络会话", "en": "Create a new web session on claude.ai" },
      "required_args": [],
      "type": "multi",
      "group": "remote"
    },
    {
      "flag": "--rc",
      "description": { "zh": "启动启用了 Remote Control 的交互式会话", "en": "Start interactive session with Remote Control enabled" },
      "required_args": [],
      "type": "multi",
      "group": "remote"
    },
    {
      "flag": "--remote-control",
      "description": { "zh": "启动启用了 Remote Control 的交互式会话（同 --rc）", "en": "Start interactive session with Remote Control enabled (same as --rc)" },
      "required_args": [],
      "type": "multi",
      "group": "remote"
    },
    {
      "flag": "--remote-control-session-name-prefix",
      "description": { "zh": "Remote Control 自动生成会话名称的前缀", "en": "Prefix for auto-generated Remote Control session names" },
      "required_args": [{ "name": "prefix", "label": { "zh": "名称前缀", "en": "Name prefix" }, "placeholder": { "zh": "例: dev-box", "en": "e.g. dev-box" } }],
      "type": "value",
      "group": "remote"
    },
    {
      "flag": "--teleport",
      "description": { "zh": "在本地终端中恢复网络会话", "en": "Resume a web session in the local terminal" },
      "required_args": [],
      "type": "multi",
      "group": "remote"
    },
    {
      "flag": "--channels",
      "description": { "zh": "MCP 服务器 channel 通知列表（研究预览）", "en": "MCP server channel notification list (research preview)" },
      "required_args": [{ "name": "channels", "label": { "zh": "Channel 列表", "en": "Channel list" }, "placeholder": { "zh": "例: plugin:my-notifier@my-marketplace", "en": "e.g. plugin:my-notifier@my-marketplace" } }],
      "type": "value",
      "group": "remote"
    },
    {
      "flag": "--dangerously-load-development-channels",
      "description": { "zh": "启用不在批准允许列表中的 channels（本地开发用）", "en": "Enable channels not on the approved allowlist (for local dev)" },
      "required_args": [{ "name": "channels", "label": { "zh": "Channel 条目", "en": "Channel entries" }, "placeholder": { "zh": "例: server:webhook", "en": "e.g. server:webhook" } }],
      "type": "value",
      "group": "remote"
    },
    {
      "flag": "--init",
      "description": { "zh": "在会话前运行 setup hooks（仅打印模式）", "en": "Run setup hooks before session (print mode only)" },
      "required_args": [],
      "type": "multi",
      "group": "hook"
    },
    {
      "flag": "--init-only",
      "description": { "zh": "运行 Setup 和 SessionStart hooks 后退出", "en": "Run Setup and SessionStart hooks then exit" },
      "required_args": [],
      "type": "multi",
      "group": "hook"
    },
    {
      "flag": "--maintenance",
      "description": { "zh": "在会话前运行 maintenance hooks（仅打印模式）", "en": "Run maintenance hooks before session (print mode only)" },
      "required_args": [],
      "type": "multi",
      "group": "hook"
    },
    {
      "flag": "--max-budget-usd",
      "description": { "zh": "API 调用前停止的最大美元金额（仅打印模式）", "en": "Max USD amount before stopping API calls (print mode)" },
      "required_args": [{ "name": "amount", "label": { "zh": "金额 (USD)", "en": "Amount (USD)" }, "placeholder": { "zh": "例: 5.00", "en": "e.g. 5.00" } }],
      "type": "value",
      "group": "limit"
    },
    {
      "flag": "--max-turns",
      "description": { "zh": "限制代理转数（仅打印模式），达到限制时以错误退出", "en": "Limit agent turns (print mode), exits with error when reached" },
      "required_args": [{ "name": "turns", "label": { "zh": "转数", "en": "Turns" }, "placeholder": { "zh": "例: 3", "en": "e.g. 3" } }],
      "type": "value",
      "group": "limit"
    },
    {
      "flag": "--settings",
      "description": { "zh": "设置 JSON 文件的路径或内联 JSON 字符串", "en": "Path to settings JSON file or inline JSON string" },
      "required_args": [{ "name": "settings", "label": { "zh": "设置路径/JSON", "en": "Settings path/JSON" }, "placeholder": { "zh": "例: ./settings.json", "en": "e.g. ./settings.json" } }],
      "type": "value",
      "group": "config"
    },
    {
      "flag": "--setting-sources",
      "description": { "zh": "逗号分隔的设置源列表（user, project, local）", "en": "Comma-separated list of setting sources (user, project, local)" },
      "required_args": [{ "name": "sources", "label": { "zh": "设置源", "en": "Setting sources" }, "placeholder": { "zh": "例: user,project", "en": "e.g. user,project" } }],
      "type": "value",
      "group": "config"
    }
  ]
}
```

- [ ] **Step 2: Run tests to verify JSON loads correctly**

```bash
uv run pytest tests/test_flags.py -v
```

Expected: some tests will fail because model choices count changed (3→7), group count changed (8→15). This is expected.

- [ ] **Step 3: Commit**

```bash
git add data/flags_default.json
git commit -m "feat: expand flags from 19 to 63+ aligned with official CLI reference"
```

---

### Task 3: Update `_GROUP_LABELS` in app.py for 15 groups

**Files:**
- Modify: `src/claude_run/app.py:55-64` (_GROUP_LABELS)

- [ ] **Step 1: Replace `_GROUP_LABELS` with full 15-group mapping**

Replace the existing `_GROUP_LABELS` dict:

```python
_GROUP_LABELS: dict[str, tuple[str, str]] = {
    "model":      ("模型",  "Model"),
    "permission": ("权限",  "Permission"),
    "output":     ("输出",  "Output"),
    "session":    ("会话",  "Session"),
    "tools":      ("工具",  "Tools"),
    "system":     ("系统提示", "System Prompt"),
    "dev":        ("开发",  "Dev"),
    "mcp":        ("MCP/插件", "MCP/Plugin"),
    "debug":      ("调试",  "Debug"),
    "agent":      ("Agent", "Agent"),
    "ide":        ("IDE/浏览器", "IDE/Browser"),
    "remote":     ("远程",  "Remote"),
    "hook":       ("Hooks", "Hooks"),
    "limit":      ("限制",  "Limits"),
    "config":     ("配置",  "Config"),
}
```

- [ ] **Step 2: Run tests to confirm app imports still work**

```bash
uv run python -c "from claude_run.app import _GROUP_LABELS; print(len(_GROUP_LABELS))"
```

Expected: `15`

- [ ] **Step 3: Commit**

```bash
git add src/claude_run/app.py
git commit -m "feat: add 7 new group labels for expanded flag coverage"
```

---

### Task 4: Mutual exclusion logic in app.py `_run_selector()`

**Files:**
- Modify: `src/claude_run/app.py:251-260` (_toggle handler in _run_selector)
- Modify: `src/claude_run/app.py:444-449` (newly_added handling in run_app)

- [ ] **Step 1: Add mutual exclusion in the space-toggle handler**

Replace the `_toggle` handler in `_run_selector()` (around line 252):

```python
@kb.add("space", eager=True)
def _toggle(event):
    fl = ctx["filtered"]
    if fl and 0 <= ctx["cursor"] < len(fl):
        name = fl[ctx["cursor"]].flag
        if name in checked:
            checked.discard(name)
        else:
            checked.add(name)
            # 互斥处理：取消冲突的已选项
            conflicts = fl[ctx["cursor"]].conflicts_with or []
            for c in conflicts:
                if c in checked:
                    checked.discard(c)
    event.app.invalidate()
```

- [ ] **Step 2: Also clean value_state for mutually excluded flags**

In `run_app()`, after the `for name in prev_checked - checked` block (around line 444), add cleanup for conflict values:

```python
for name in prev_checked - checked:
    value_state.pop(name, None)

# 清理互斥 flag 的 value_state
for f in flags:
    if f.flag in checked and f.conflicts_with:
        for c in f.conflicts_with:
            if c not in checked:
                value_state.pop(c, None)
```

- [ ] **Step 3: Run existing tests**

```bash
uv run pytest tests/ -v
```

Expected: all tests pass (some may need updates from test count changes).

- [ ] **Step 4: Commit**

```bash
git add src/claude_run/app.py
git commit -m "feat: add mutual exclusion logic for conflicting flags in TUI"
```

---

### Task 5: Config path migration (`~/.config/claude-run/` → `~/.config/crun/`)

**Files:**
- Modify: `src/claude_run/config.py:9-11` (CONFIG_DIR path)
- Modify: `src/claude_run/config.py` (add migration function)
- Modify: `src/claude_run/__main__.py:77` (error message path)

- [ ] **Step 1: Update CONFIG_DIR and add migration logic**

Replace `config.py` lines 9-11 and add migration:

```python
log = logging.getLogger(__name__)

CONFIG_DIR = Path.home() / ".config" / "crun"
OLD_CONFIG_DIR = Path.home() / ".config" / "claude-run"
PREFERENCES_PATH = CONFIG_DIR / "preferences.json"
LAST_CONFIG_PATH = CONFIG_DIR / "last_config.json"


def _migrate_old_config() -> None:
    """将旧配置目录迁移到新路径。"""
    if not OLD_CONFIG_DIR.exists():
        return
    if CONFIG_DIR.exists():
        log.info(f"新旧配置目录均存在，使用新路径 {CONFIG_DIR}，旧路径忽略")
        return
    try:
        OLD_CONFIG_DIR.rename(CONFIG_DIR)
        log.info(f"配置已从 {OLD_CONFIG_DIR} 迁移到 {CONFIG_DIR}")
    except OSError as e:
        log.warning(f"配置迁移失败: {e}")
```

- [ ] **Step 2: Call migration at module load time**

Add at the bottom of `config.py` (after all function definitions, before EOF):

```python
# 模块加载时自动迁移旧配置
_migrate_old_config()
```

- [ ] **Step 3: Update error message in `__main__.py` line 77**

Change:
```python
print("请检查 ~/.config/claude-run/ 目录权限。", file=sys.stderr)
```
To:
```python
print("请检查 ~/.config/crun/ 目录权限。", file=sys.stderr)
```

- [ ] **Step 4: Run config tests**

```bash
uv run pytest tests/test_config.py -v
```

Expected: all 10 tests pass (they use temp dirs, not affected by path change).

- [ ] **Step 5: Commit**

```bash
git add src/claude_run/config.py src/claude_run/__main__.py
git commit -m "feat: migrate config dir from ~/.config/claude-run/ to ~/.config/crun/"
```

---

### Task 6: Project rename (`claude-run` → `crun`)

**Files:**
- Modify: `pyproject.toml:2,12` (name + scripts)
- Modify: `src/claude_run/__main__.py:38` (print_logo)
- Modify: `CLAUDE.md` (command references)

- [ ] **Step 1: Update `pyproject.toml`**

Change `name` and `scripts`:
```toml
[project]
name = "crun"
...
[project.scripts]
crun = "claude_run.__main__:main"
```

- [ ] **Step 2: Update logo in `__main__.py`**

Replace `_LOGO` with new "crun" ASCII art and update `print_logo`:

```python
_LOGO = r"""
   ____  ____  _  _  ____
  / ___)|  _ \| || ||  _ \
 | |    | |_| | || || |_| |
 | |    |  _ (| || ||  _ <
 | |___ | |_| | \__/ | |_| |
  \____)|____/  \__/ |____/
""".strip("\n")


def print_logo() -> None:
    print(_LOGO)
    print("  by.BingMoe")
    print()
```

- [ ] **Step 3: Update `CLAUDE.md` command references**

Change all `claude-run` to `crun` in CLAUDE.md (the install/run commands).

- [ ] **Step 4: Reinstall the package**

```bash
uv pip install -e .
```

- [ ] **Step 5: Verify new entry point works**

```bash
which crun
crun --help 2>&1 || true  # Will exit because no claude, but should print logo
```

Expected: prints "crun" logo, then errors about missing claude (or enters wizard).

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml src/claude_run/__main__.py CLAUDE.md
git commit -m "feat: rename project from claude-run to crun"
```

---

### Task 7: Update tests for new flag counts and new features

**Files:**
- Modify: `tests/test_flags.py:73-78` (test_flag_get_display_choices)
- Modify: `tests/test_flags.py` (add schema + conflicts tests)
- Create: `tests/test_app_conflicts.py` (mutual exclusion tests)
- Modify: `tests/test_config.py` (add migration test)

- [ ] **Step 1: Update `test_flag_get_display_choices` for 7 model choices**

Change assertion from `len(choices) == 3` to `len(choices) == 7`:

```python
def test_flag_get_display_choices():
    flags = load_flags()
    model_flag = next(f for f in flags if f.flag == "--model")
    choices = model_flag.get_choices("zh")
    assert len(choices) == 7
    assert choices[0]["value"] == "sonnet"
```

- [ ] **Step 2: Update `test_load_flags_default` for 15 groups**

Change the group check:
```python
def test_load_flags_default():
    flags = load_flags()
    group_map = {f.group for f in flags}
    expected_groups = {"model", "permission", "session", "output", "tools",
                       "dev", "debug", "mcp", "system", "agent", "ide",
                       "remote", "hook", "limit", "config"}
    assert group_map == expected_groups
```

- [ ] **Step 3: Update `test_flag_structure` to accept `conflicts_with`**

No code change needed — the test already validates structure generically. But we should add a test for conflicts:

```python
def test_flag_conflicts_with():
    """conflicts_with 引用的 flag 必须存在。"""
    flags = load_flags()
    all_names = {f.flag for f in flags}
    for f in flags:
        if f.conflicts_with:
            for target in f.conflicts_with:
                assert target in all_names, \
                    f"{f.flag}.conflicts_with 引用不存在的 {target}"

def test_flag_conflicts_symmetric():
    """互斥关系应双向声明。"""
    flags = load_flags()
    for f in flags:
        if f.conflicts_with:
            for target in f.conflicts_with:
                target_flag = next(fl for fl in flags if fl.flag == target)
                assert target_flag.conflicts_with is not None, \
                    f"{f.flag} 声明与 {target} 互斥，但 {target} 未声明 conflicts_with"
                assert f.flag in target_flag.conflicts_with, \
                    f"{f.flag} 声明与 {target} 互斥，但 {target} 未反向声明"
```

- [ ] **Step 4: Create `tests/test_app_conflicts.py` for mutual exclusion logic**

```python
# tests/test_app_conflicts.py
"""测试 TUI 互斥逻辑。"""
from claude_run.flags import Flag, Choice


def make_flag(name: str, conflicts: list[str] | None = None, group: str = "test") -> Flag:
    return Flag(
        flag=name,
        description={"zh": name, "en": name},
        required_args=[],
        type="multi",
        group=group,
        choices=None,
        conflicts_with=conflicts,
    )


def test_toggle_adds_conflicting_removes_existing():
    """勾选互斥 flag 时，应取消已选的冲突 flag。"""
    chrome = make_flag("--chrome", conflicts_with=["--no-chrome"])
    no_chrome = make_flag("--no-chrome", conflicts_with=["--chrome"])

    checked = {"--no-chrome"}

    # 模拟 toggle：勾选 --chrome
    if "--chrome" not in checked:
        checked.add("--chrome")
        for c in (chrome.conflicts_with or []):
            checked.discard(c)

    assert "--chrome" in checked
    assert "--no-chrome" not in checked


def test_toggle_non_conflicting_preserves_existing():
    """勾选无冲突 flag 时，不影响已选项。"""
    bare = make_flag("--bare")
    verbose = make_flag("--verbose")

    checked = {"--verbose"}
    if "--bare" not in checked:
        checked.add("--bare")

    assert "--bare" in checked
    assert "--verbose" in checked


def test_toggle_uncheck_does_not_affect_others():
    """取消勾选时，不影响其他已选项。"""
    chrome = make_flag("--chrome", conflicts_with=["--no-chrome"])

    checked = {"--chrome", "--bare"}
    checked.discard("--chrome")

    assert "--chrome" not in checked
    assert "--bare" in checked


def test_system_prompt_mutual_exclusion():
    """--system-prompt 和 --system-prompt-file 互斥。"""
    sp = make_flag("--system-prompt", conflicts_with=["--system-prompt-file"])
    spf = make_flag("--system-prompt-file", conflicts_with=["--system-prompt"])

    checked = {"--system-prompt-file"}
    checked.add("--system-prompt")
    for c in (sp.conflicts_with or []):
        checked.discard(c)

    assert "--system-prompt" in checked
    assert "--system-prompt-file" not in checked


def test_no_conflicts_field_does_not_crash():
    """没有 conflicts_with 的 flag 正常 toggle。"""
    flag = make_flag("--verbose")
    checked: set[str] = set()
    checked.add("--verbose")
    for c in (flag.conflicts_with or []):
        checked.discard(c)
    assert "--verbose" in checked
```

- [ ] **Step 5: Add config migration test to `tests/test_config.py`**

```python
from claude_run.config import _migrate_old_config, CONFIG_DIR, OLD_CONFIG_DIR


def test_migration_renames_old_dir(tmp_path, monkeypatch):
    """旧目录存在、新目录不存在时，自动 rename 迁移。"""
    old = tmp_path / "old_config"
    new = tmp_path / "new_config"
    old.mkdir()
    (old / "preferences.json").write_text('{"search_mode":"A"}', encoding="utf-8")

    monkeypatch.setattr("claude_run.config.OLD_CONFIG_DIR", old)
    monkeypatch.setattr("claude_run.config.CONFIG_DIR", new)

    _migrate_old_config()

    assert new.exists()
    assert not old.exists()
    assert (new / "preferences.json").exists()


def test_migration_both_exist_keeps_new(tmp_path, monkeypatch):
    """新旧目录都存在时，保留新目录不动。"""
    old = tmp_path / "old_config"
    new = tmp_path / "new_config"
    old.mkdir()
    new.mkdir()
    (new / "existing.txt").write_text("keep me", encoding="utf-8")

    monkeypatch.setattr("claude_run.config.OLD_CONFIG_DIR", old)
    monkeypatch.setattr("claude_run.config.CONFIG_DIR", new)

    _migrate_old_config()

    assert old.exists()  # 旧目录不动
    assert new.exists()
    assert (new / "existing.txt").read_text() == "keep me"
```

- [ ] **Step 6: Run all tests**

```bash
uv run pytest tests/ -v
```

Expected: all tests pass (existing + new).

- [ ] **Step 7: Commit**

```bash
git add tests/
git commit -m "test: update tests for new flag counts, conflicts, and config migration"
```

---

### Task 8: Final integration test

- [ ] **Step 1: Run full test suite**

```bash
uv run pytest tests/ -v --tb=short
```

Expected: all tests pass, ~25+ tests total.

- [ ] **Step 2: Smoke test with DEBUG mode**

```bash
DEBUG=1 uv run crun 2>&1 || true
```

Expected: prints logo, wizard or fails gracefully (no claude installed in dev).

- [ ] **Step 3: Verify search covers new flags**

```bash
uv run python -c "
from claude_run.flags import load_flags
from claude_run.search import search_flags
flags = load_flags()
print(f'Total flags: {len(flags)}')
results = search_flags(flags, 'system', 'zh')
print(f'Search \"system\" hits: {len(results)}')
for f in results:
    print(f'  {f.flag}')
"
```

Expected: Total flags >= 63, search returns system-related flags.

- [ ] **Step 4: Commit if any cleanup needed**

```bash
git status
```

---

### Summary of Commits

1. `feat: add conflicts_with field to Flag dataclass`
2. `feat: expand flags from 19 to 63+ aligned with official CLI reference`
3. `feat: add 7 new group labels for expanded flag coverage`
4. `feat: add mutual exclusion logic for conflicting flags in TUI`
5. `feat: migrate config dir from ~/.config/claude-run/ to ~/.config/crun/`
6. `feat: rename project from claude-run to crun`
7. `test: update tests for new flag counts, conflicts, and config migration`
