> ## Documentation Index
>
> Fetch the complete documentation index at: <https://code.claude.com/docs/llms.txt>
> Use this file to discover all available pages before exploring further.

# CLI 参考

> Claude Code 命令行界面的完整参考，包括命令和标志。

## CLI 命令

您可以使用这些命令启动会话、管道内容、恢复对话和管理更新：

| 命令                              | 描述                                                                                                                                                                                                                                       | 示例                                                          |
| :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------- |
| `claude`                        | 启动交互式会话                                                                                                                                                                                                                                  | `claude`                                                    |
| `claude "query"`                | 使用初始提示启动交互式会话                                                                                                                                                                                                                            | `claude "explain this project"`                             |
| `claude -p "query"`             | 通过 SDK 查询，然后退出                                                                                                                                                                                                                           | `claude -p "explain this function"`                         |
| `cat file \| claude -p "query"` | 处理管道内容                                                                                                                                                                                                                                   | `cat logs.txt \| claude -p "explain"`                       |
| `claude -c`                     | 在当前目录中继续最近的对话                                                                                                                                                                                                                            | `claude -c`                                                 |
| `claude -c -p "query"`          | 通过 SDK 继续                                                                                                                                                                                                                                | `claude -c -p "Check for type errors"`                      |
| `claude -r "<session>" "query"` | 按 ID 或名称恢复会话                                                                                                                                                                                                                             | `claude -r "auth-refactor" "Finish this PR"`                |
| `claude update`                 | 更新到最新版本                                                                                                                                                                                                                                  | `claude update`                                             |
| `claude install [version]`      | 安装或重新安装本机二进制文件。接受版本号如 `2.1.118`、`stable` 或 `latest`。请参阅 [安装特定版本](/zh-CN/setup#install-a-specific-version)                                                                                                                                | `claude install stable`                                     |
| `claude auth login`             | 登录您的 Anthropic 账户。使用 `--email` 预填充您的电子邮件地址，使用 `--sso` 强制 SSO 身份验证，使用 `--console` 使用 Anthropic Console 登录以进行 API 使用计费而不是 Claude 订阅                                                                                                        | `claude auth login --console`                               |
| `claude auth logout`            | 从您的 Anthropic 账户登出                                                                                                                                                                                                                       | `claude auth logout`                                        |
| `claude auth status`            | 以 JSON 格式显示身份验证状态。使用 `--text` 获取人类可读的输出。如果已登录，则以代码 0 退出，如果未登录，则以代码 1 退出                                                                                                                                                                  | `claude auth status`                                        |
| `claude agents`                 | 打开 [agent view](/zh-CN/agent-view) 以监控和分派并行后台会话。使用 `--cwd <path>` 仅显示在该目录下启动的会话                                                                                                                                                          | `claude agents`                                             |
| `claude attach <id>`            | 在此终端中附加到 [background session](/zh-CN/agent-view#manage-sessions-from-the-shell)                                                                                                                                                          | `claude attach 7c5dcf5d`                                    |
| `claude auto-mode defaults`     | 以 JSON 格式打印内置 [auto mode](/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 分类器规则。使用 `claude auto-mode config` 查看应用了设置的有效配置                                                                                                      | `claude auto-mode defaults > rules.json`                    |
| `claude logs <id>`              | 从 [background session](/zh-CN/agent-view#manage-sessions-from-the-shell) 打印最近的输出                                                                                                                                                         | `claude logs 7c5dcf5d`                                      |
| `claude mcp`                    | 配置 Model Context Protocol (MCP) 服务器                                                                                                                                                                                                      | 请参阅 [Claude Code MCP 文档](/zh-CN/mcp)。                       |
| `claude plugin`                 | 管理 Claude Code [plugins](/zh-CN/plugins)。别名：`claude plugins`。请参阅 [plugin 参考](/zh-CN/plugins-reference#cli-commands-reference) 了解子命令                                                                                                      | `claude plugin install code-review@claude-plugins-official` |
| `claude project purge [path]`   | 删除项目的所有本地 Claude Code 状态：记录、任务列表、调试日志、文件编辑历史、提示历史行和项目在 `~/.claude.json` 中的条目。省略 `[path]` 以从交互式列表中选择。标志：`--dry-run` 预览，`-y`/`--yes` 跳过确认，`-i`/`--interactive` 确认每一项，`--all` 用于每个项目。请参阅 [清除本地数据](/zh-CN/claude-directory#clear-local-data) | `claude project purge ~/work/repo --dry-run`                |
| `claude remote-control`         | 启动 [Remote Control](/zh-CN/remote-control) 服务器以从 Claude.ai 或 Claude 应用控制 Claude Code。在服务器模式下运行（无本地交互式会话）。请参阅 [服务器模式标志](/zh-CN/remote-control#start-a-remote-control-session)                                                             | `claude remote-control --name "My Project"`                 |
| `claude respawn <id>`           | 重启已停止的 [background session](/zh-CN/agent-view#manage-sessions-from-the-shell)，保持其对话完整。使用 `--all` 重启每个已停止的会话                                                                                                                              | `claude respawn 7c5dcf5d`                                   |
| `claude rm <id>`                | 从列表中删除 [background session](/zh-CN/agent-view#manage-sessions-from-the-shell)                                                                                                                                                            | `claude rm 7c5dcf5d`                                        |
| `claude setup-token`            | 为 CI 和脚本生成长期 OAuth 令牌。将令牌打印到终端而不保存。需要 Claude 订阅。请参阅 [生成长期令牌](/zh-CN/authentication#generate-a-long-lived-token)                                                                                                                          | `claude setup-token`                                        |
| `claude stop <id>`              | 停止 [background session](/zh-CN/agent-view#manage-sessions-from-the-shell)。也接受 `claude kill`                                                                                                                                              | `claude stop 7c5dcf5d`                                      |
| `claude ultrareview [target]`   | 非交互式运行 [ultrareview](/zh-CN/ultrareview#run-ultrareview-non-interactively)。将发现结果打印到标准输出，成功时退出代码 0，失败时退出代码 1。使用 `--json` 获取原始有效负载，使用 `--timeout <minutes>` 覆盖 30 分钟的默认值                                                                   | `claude ultrareview 1234 --json`                            |

如果您输入错误的子命令，Claude Code 会建议最接近的匹配项并退出而不启动会话。例如，`claude udpate` 会打印 `Did you mean claude update?`。

## CLI 标志

使用这些命令行标志自定义 Claude Code 的行为。`claude --help` 不会列出每个标志，因此标志在 `--help` 中的缺失并不意味着它不可用。

| 标志                                              | 描述                                                                                                                                                                                                                                                              | 示例                                                                                                 |
| :---------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                                     | 为 Claude 添加额外的工作目录以读取和编辑文件。授予文件访问权限；大多数 `.claude/` 配置 [不会从这些目录中发现](/zh-CN/permissions#additional-directories-grant-file-access-not-configuration)。验证每个路径是否存在为目录。要在会话间持久化这些目录，请在设置中设置 [`permissions.additionalDirectories`](/zh-CN/settings#permission-settings) | `claude --add-dir ../apps ../lib`                                                                  |
| `--agent`                                       | 为当前会话指定代理（覆盖 `agent` 设置）                                                                                                                                                                                                                                        | `claude --agent my-custom-agent`                                                                   |
| `--agents`                                      | 通过 JSON 动态定义自定义 subagents。使用与 subagent [frontmatter](/zh-CN/sub-agents#supported-frontmatter-fields) 相同的字段名称，加上代理指令的 `prompt` 字段                                                                                                                                | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions`          | 将 `bypassPermissions` 添加到 `Shift+Tab` 模式循环中而不启动它。允许您以不同的模式（如 `plan`）开始，稍后切换到 `bypassPermissions`。请参阅 [权限模式](/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode)                                                                                | `claude --permission-mode plan --allow-dangerously-skip-permissions`                               |
| `--allowedTools`                                | 无需提示权限即可执行的工具。请参阅 [权限规则语法](/zh-CN/settings#permission-rule-syntax) 了解模式匹配。要限制哪些工具可用，请改用 `--tools`                                                                                                                                                               | `"Bash(git log *)" "Bash(git diff *)" "Read"`                                                      |
| `--append-system-prompt`                        | 将自定义文本附加到默认系统提示的末尾                                                                                                                                                                                                                                              | `claude --append-system-prompt "Always use TypeScript"`                                            |
| `--append-system-prompt-file`                   | 从文件加载额外的系统提示文本并附加到默认提示                                                                                                                                                                                                                                          | `claude --append-system-prompt-file ./extra-rules.txt`                                             |
| `--bare`                                        | 最小模式：跳过 hooks、skills、plugins、MCP 服务器、自动内存和 CLAUDE.md 的自动发现，以便脚本化调用启动更快。Claude 可以访问 Bash、文件读取和文件编辑工具。设置 [`CLAUDE_CODE_SIMPLE`](/zh-CN/env-vars)。请参阅 [bare mode](/zh-CN/headless#start-faster-with-bare-mode)                                                     | `claude --bare -p "query"`                                                                         |
| `--betas`                                       | 要包含在 API 请求中的 Beta 标头（仅限 API 密钥用户）                                                                                                                                                                                                                              | `claude --betas interleaved-thinking`                                                              |
| `--bg`                                          | 启动会话作为 [后台代理](/zh-CN/agent-view) 并立即返回。打印会话 ID 和管理命令。与 `--agent` 结合以运行特定的 subagent                                                                                                                                                                              | `claude --bg "investigate the flaky test"`                                                         |
| `--channels`                                    | （研究预览）MCP 服务器，其 [channel](/zh-CN/channels) 通知 Claude 应在此会话中侦听。以空格分隔的 `plugin:<name>@<marketplace>` 条目列表。需要 Claude.ai 身份验证                                                                                                                                       | `claude --channels plugin:my-notifier@my-marketplace`                                              |
| `--chrome`                                      | 启用 [Chrome 浏览器集成](/zh-CN/chrome) 以进行网络自动化和测试                                                                                                                                                                                                                    | `claude --chrome`                                                                                  |
| `--continue`, `-c`                              | 加载当前目录中最近的对话。包括使用 `/add-dir` 添加此目录的会话                                                                                                                                                                                                                           | `claude --continue`                                                                                |
| `--dangerously-load-development-channels`       | 启用不在批准的允许列表中的 [channels](/zh-CN/channels-reference#test-during-the-research-preview)，用于本地开发。接受 `plugin:<name>@<marketplace>` 和 `server:<name>` 条目。提示确认                                                                                                          | `claude --dangerously-load-development-channels server:webhook`                                    |
| `--dangerously-skip-permissions`                | 跳过权限提示。等同于 `--permission-mode bypassPermissions`。请参阅 [权限模式](/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode) 了解此操作跳过和不跳过的内容                                                                                                                 | `claude --dangerously-skip-permissions`                                                            |
| `--debug`                                       | 启用调试模式，可选类别过滤（例如，`"api,hooks"` 或 `"!statsig,!file"`）                                                                                                                                                                                                            | `claude --debug "api,mcp"`                                                                         |
| `--debug-file <path>`                           | 将调试日志写入特定文件路径。隐式启用调试模式。优先于 `CLAUDE_CODE_DEBUG_LOGS_DIR`                                                                                                                                                                                                         | `claude --debug-file /tmp/claude-debug.log`                                                        |
| `--disable-slash-commands`                      | 为此会话禁用所有 skills 和命令                                                                                                                                                                                                                                             | `claude --disable-slash-commands`                                                                  |
| `--disallowedTools`                             | 从模型的上下文中删除的工具，无法使用                                                                                                                                                                                                                                              | `"Bash(git log *)" "Bash(git diff *)" "Edit"`                                                      |
| `--effort`                                      | 为当前会话设置 [工作量级别](/zh-CN/model-config#adjust-effort-level)。选项：`low`、`medium`、`high`、`xhigh`、`max`；可用级别取决于模型。覆盖此会话的 [`effortLevel`](/zh-CN/settings#available-settings) 设置，不会持久化                                                                                   | `claude --effort high`                                                                             |
| `--enable-auto-mode`                            | {/*max-version: 2.1.110*/}在 v2.1.111 中移除。Auto mode 现在默认在 `Shift+Tab` 循环中；使用 `--permission-mode auto` 以它开始                                                                                                                                                     | `claude --permission-mode auto`                                                                    |
| `--exclude-dynamic-system-prompt-sections`      | 将每台机器的部分从系统提示（工作目录、环境信息、内存路径、git 状态）移到第一条用户消息中。改进在运行相同任务的不同用户和机器之间的提示缓存重用。仅适用于默认系统提示；当设置 `--system-prompt` 或 `--system-prompt-file` 时忽略。与 `-p` 一起用于脚本化的多用户工作负载                                                                                                  | `claude -p --exclude-dynamic-system-prompt-sections "query"`                                       |
| `--fallback-model`                              | 当默认模型过载时启用自动回退到指定模型（仅打印模式）                                                                                                                                                                                                                                      | `claude -p --fallback-model sonnet "query"`                                                        |
| `--fork-session`                                | 恢复时，创建新的会话 ID 而不是重用原始 ID（与 `--resume` 或 `--continue` 一起使用）                                                                                                                                                                                                      | `claude --resume abc123 --fork-session`                                                            |
| `--from-pr`                                     | 恢复链接到特定拉取请求的会话。接受 PR 号、GitHub 或 GitHub Enterprise PR URL、GitLab 合并请求 URL 或 Bitbucket 拉取请求 URL。当 Claude 创建拉取请求时会自动链接会话                                                                                                                                           | `claude --from-pr 123`                                                                             |
| `--ide`                                         | 如果恰好有一个有效的 IDE 可用，则在启动时自动连接到 IDE                                                                                                                                                                                                                                | `claude --ide`                                                                                     |
| `--init`                                        | 在会话前运行带有 `init` 匹配器的 [Setup hooks](/zh-CN/hooks#setup)（仅打印模式）                                                                                                                                                                                                   | `claude -p --init "query"`                                                                         |
| `--init-only`                                   | 运行 [Setup](/zh-CN/hooks#setup) 和 `SessionStart` hooks，然后退出而不启动对话                                                                                                                                                                                                | `claude --init-only`                                                                               |
| `--include-hook-events`                         | 在输出流中包含所有 hook 生命周期事件。需要 `--output-format stream-json`                                                                                                                                                                                                          | `claude -p --output-format stream-json --include-hook-events "query"`                              |
| `--include-partial-messages`                    | 在输出中包含部分流事件。需要 `--print` 和 `--output-format stream-json`                                                                                                                                                                                                        | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--input-format`                                | 为打印模式指定输入格式（选项：`text`、`stream-json`）                                                                                                                                                                                                                            | `claude -p --output-format json --input-format stream-json`                                        |
| `--json-schema`                                 | 在代理完成其工作流后获得与 JSON Schema 匹配的验证 JSON 输出（仅打印模式，请参阅 [结构化输出](/zh-CN/agent-sdk/structured-outputs)）                                                                                                                                                                 | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"`                           |
| `--maintenance`                                 | 在会话前运行带有 `maintenance` 匹配器的 [Setup hooks](/zh-CN/hooks#setup)（仅打印模式）                                                                                                                                                                                            | `claude -p --maintenance "query"`                                                                  |
| `--max-budget-usd`                              | API 调用前停止的最大美元金额（仅打印模式）                                                                                                                                                                                                                                         | `claude -p --max-budget-usd 5.00 "query"`                                                          |
| `--max-turns`                                   | 限制代理转数（仅打印模式）。达到限制时以错误退出。默认无限制                                                                                                                                                                                                                                  | `claude -p --max-turns 3 "query"`                                                                  |
| `--mcp-config`                                  | 从 JSON 文件或字符串加载 MCP 服务器（以空格分隔）                                                                                                                                                                                                                                  | `claude --mcp-config ./mcp.json`                                                                   |
| `--model`                                       | 为当前会话设置模型，使用最新模型的别名（`sonnet` 或 `opus`）或模型的完整名称。覆盖 [`model`](/zh-CN/settings#available-settings) 设置和 [`ANTHROPIC_MODEL`](/zh-CN/model-config#environment-variables)                                                                                              | `claude --model claude-sonnet-4-6`                                                                 |
| `--name`, `-n`                                  | 为会话设置显示名称，显示在 `/resume` 和终端标题中。您可以使用 `claude --resume <name>` 恢复命名会话。<br /><br />[`/rename`](/zh-CN/commands) 在会话中更改名称，也会在提示栏中显示                                                                                                                                | `claude -n "my-feature-work"`                                                                      |
| `--no-chrome`                                   | 为此会话禁用 [Chrome 浏览器集成](/zh-CN/chrome)                                                                                                                                                                                                                            | `claude --no-chrome`                                                                               |
| `--no-session-persistence`                      | 禁用会话持久化，以便会话不会保存到磁盘且无法恢复。仅打印模式。[`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/zh-CN/env-vars) 环境变量在任何模式下都做同样的事情                                                                                                                                                           | `claude -p --no-session-persistence "query"`                                                       |
| `--output-format`                               | 为打印模式指定输出格式（选项：`text`、`json`、`stream-json`）                                                                                                                                                                                                                     | `claude -p "query" --output-format json`                                                           |
| `--permission-mode`                             | 以指定的 [权限模式](/zh-CN/permission-modes) 开始。接受 `default`、`acceptEdits`、`plan`、`auto`、`dontAsk` 或 `bypassPermissions`。覆盖设置文件中的 `defaultMode`                                                                                                                         | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`                      | 指定 MCP 工具以在非交互模式下处理权限提示                                                                                                                                                                                                                                         | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--plugin-dir`                                  | 仅为此会话从目录或 `.zip` 存档加载插件。每个标志采用一个路径。重复该标志以获取多个插件：`--plugin-dir A --plugin-dir B.zip`                                                                                                                                                                             | `claude --plugin-dir ./my-plugin`                                                                  |
| `--plugin-url`                                  | 仅为此会话从 URL 获取插件 `.zip` 存档。重复该标志以获取多个插件，或在单个引用值中传递以空格分隔的 URL                                                                                                                                                                                                     | `claude --plugin-url https://example.com/plugin.zip`                                               |
| `--print`, `-p`                                 | 打印响应而不进入交互模式（请参阅 [Agent SDK 文档](/zh-CN/agent-sdk/overview) 了解编程使用详情）                                                                                                                                                                                            | `claude -p "query"`                                                                                |
| `--remote`                                      | 在 claude.ai 上创建新的 [网络会话](/zh-CN/claude-code-on-the-web)，提供任务描述                                                                                                                                                                                                  | `claude --remote "Fix the login bug"`                                                              |
| `--remote-control`, `--rc`                      | 启动启用了 [Remote Control](/zh-CN/remote-control#start-a-remote-control-session) 的交互式会话，以便您也可以从 claude.ai 或 Claude 应用控制它。可选地为会话传递名称                                                                                                                                 | `claude --remote-control "My Project"`                                                             |
| `--remote-control-session-name-prefix <prefix>` | 当未设置显式名称时，[Remote Control](/zh-CN/remote-control) 自动生成会话名称的前缀。默认为您的机器的主机名，生成名称如 `myhost-graceful-unicorn`。设置 `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` 以获得相同效果                                                                                                | `claude remote-control --remote-control-session-name-prefix dev-box`                               |
| `--replay-user-messages`                        | 从 stdin 重新发出用户消息到 stdout 以进行确认。需要 `--input-format stream-json` 和 `--output-format stream-json`                                                                                                                                                                  | `claude -p --input-format stream-json --output-format stream-json --replay-user-messages`          |
| `--resume`, `-r`                                | 按 ID 或名称恢复特定会话，或显示交互式选择器以选择会话。包括使用 `/add-dir` 添加此目录的会话                                                                                                                                                                                                          | `claude --resume auth-refactor`                                                                    |
| `--session-id`                                  | 为对话使用特定的会话 ID（必须是有效的 UUID）                                                                                                                                                                                                                                      | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"`                                       |
| `--setting-sources`                             | 逗号分隔的设置源列表以加载（`user`、`project`、`local`）                                                                                                                                                                                                                         | `claude --setting-sources user,project`                                                            |
| `--settings`                                    | 设置 JSON 文件的路径或内联 JSON 字符串。您在此处设置的值会覆盖此会话的 `settings.json` 文件中的相同键。您省略的键保留其基于文件的值。请参阅 [设置优先级](/zh-CN/settings#settings-precedence)                                                                                                                               | `claude --settings ./settings.json`                                                                |
| `--strict-mcp-config`                           | 仅使用来自 `--mcp-config` 的 MCP 服务器，忽略所有其他 MCP 配置                                                                                                                                                                                                                    | `claude --strict-mcp-config --mcp-config ./mcp.json`                                               |
| `--system-prompt`                               | 用自定义文本替换整个系统提示                                                                                                                                                                                                                                                  | `claude --system-prompt "You are a Python expert"`                                                 |
| `--system-prompt-file`                          | 从文件加载系统提示，替换默认提示                                                                                                                                                                                                                                                | `claude --system-prompt-file ./custom-prompt.txt`                                                  |
| `--teleport`                                    | 在本地终端中恢复 [网络会话](/zh-CN/claude-code-on-the-web)                                                                                                                                                                                                                  | `claude --teleport`                                                                                |
| `--teammate-mode`                               | 设置 [agent team](/zh-CN/agent-teams) 队友的显示方式：`auto`（默认）、`in-process` 或 `tmux`。覆盖此会话的 [`teammateMode`](/zh-CN/settings#available-settings) 设置。请参阅 [选择显示模式](/zh-CN/agent-teams#choose-a-display-mode)                                                              | `claude --teammate-mode in-process`                                                                |
| `--tmux`                                        | 为 worktree 创建 tmux 会话。需要 `--worktree`。在可用时使用 iTerm2 原生窗格；传递 `--tmux=classic` 以使用传统 tmux                                                                                                                                                                         | `claude -w feature-auth --tmux`                                                                    |
| `--tools`                                       | 限制 Claude 可以使用的内置工具。使用 `""` 禁用所有，`"default"` 表示全部，或工具名称如 `"Bash,Edit,Read"`                                                                                                                                                                                     | `claude --tools "Bash,Edit,Read"`                                                                  |
| `--verbose`                                     | 启用详细日志记录，显示完整的逐轮输出。覆盖此会话的 [`viewMode`](/zh-CN/settings#available-settings) 设置                                                                                                                                                                                   | `claude --verbose`                                                                                 |
| `--version`, `-v`                               | 输出版本号                                                                                                                                                                                                                                                           | `claude -v`                                                                                        |
| `--worktree`, `-w`                              | 在隔离的 [git worktree](/zh-CN/worktrees) 中启动 Claude，位于 `<repo>/.claude/worktrees/<name>`。如果未给出名称，则自动生成一个。传递 `#<number>` 或 GitHub 拉取请求 URL 以从 `origin` 获取该 PR 并从其分支 worktree                                                                                        | `claude -w feature-auth`                                                                           |

### 系统提示标志

Claude Code 提供四个标志用于自定义系统提示。所有四个都在交互和非交互模式下工作。

| 标志                            | 行为           | 示例                                                      |
| :---------------------------- | :----------- | :------------------------------------------------------ |
| `--system-prompt`             | 替换整个默认提示     | `claude --system-prompt "You are a Python expert"`      |
| `--system-prompt-file`        | 用文件内容替换      | `claude --system-prompt-file ./prompts/review.txt`      |
| `--append-system-prompt`      | 附加到默认提示      | `claude --append-system-prompt "Always use TypeScript"` |
| `--append-system-prompt-file` | 将文件内容附加到默认提示 | `claude --append-system-prompt-file ./style-rules.txt`  |

`--system-prompt` 和 `--system-prompt-file` 互斥。附加标志可以与任一替换标志组合。

根据 Claude Code 的默认身份是否仍然适合您的任务来选择。当 Claude 应该保持编码助手身份同时遵循您的额外规则时，使用附加标志：每次调用的指令、输出格式或 `-p` 脚本的域上下文。附加保留默认工具指导、安全指令和编码约定，因此您只需提供不同的部分。当表面、身份或权限模型与 Claude Code 的不同时，使用替换标志，例如管道中没有人监视的非编码代理。替换会删除整个默认提示，包括工具指导和安全指令，因此您需要对任务仍然需要的任何内容负责。

这些标志仅适用于当前调用。对于可以在项目中切换和共享的持久化角色，请使用 [输出样式](/zh-CN/output-styles)。对于 Claude 应该始终遵循的项目约定，请使用 [CLAUDE.md](/zh-CN/memory)。[Agent SDK 系统提示指南](/zh-CN/agent-sdk/modifying-system-prompts#decide-on-a-starting-point) 更深入地涵盖了相同的决策。

## 另请参阅

* [Chrome 扩展](/zh-CN/chrome) - 浏览器自动化和网络测试
* [交互模式](/zh-CN/interactive-mode) - 快捷键、输入模式和交互功能
* [快速入门指南](/zh-CN/quickstart) - Claude Code 入门
* [常见工作流](/zh-CN/common-workflows) - 高级工作流和模式
* [设置](/zh-CN/settings) - 配置选项
* [Agent SDK 文档](/zh-CN/agent-sdk/overview) - 编程使用和集成

> ## Documentation Index
>
> Fetch the complete documentation index at: <https://code.claude.com/docs/llms.txt>
> Use this file to discover all available pages before exploring further.

# 命令

> Claude Code 中可用命令的完整参考，包括内置命令和捆绑的 skills。

命令在会话内控制 Claude Code。它们提供了一种快速的方式来切换模型、管理权限、清除上下文、运行工作流等。

输入 `/` 可以查看所有可用命令，或输入 `/` 后跟字母来筛选。

命令只在您的消息开头被识别。命令名称后面的文本作为参数传递给它。

## 典型工作流程中的命令

大多数命令在会话的特定点很有用，从设置项目到发布更改。

**首次在存储库中的会话。** 运行 `/init` 以生成启动器 `CLAUDE.md`，然后运行 `/memory` 以完善它。使用 `/mcp` 和 `/agents` 来设置项目需要的任何服务器或子代理，并使用 `/permissions` 来设置您想要的批准规则。

**在任务期间。** `/plan` 在大型更改前切换到 Plan Mode。`/model` 和 `/effort` 调整您花费的推理量。当对话变长时，`/context` 显示窗口的去向，`/compact` 将其总结下来；使用 `/btw` 进行快速附加说明，不应该增加历史记录。

**并行运行工作。** `/agents` 打开管理器以处理 [子代理](/zh-CN/sub-agents)，Claude 可以将侧面任务委派给这些子代理，`/tasks` 列出当前会话后台运行的内容。`/background` 分离整个会话以继续作为 [后台代理](/zh-CN/agent-view) 运行，并释放您的终端。对于跨越代码库的大型更改，`/batch` 将其分解为独立单元，并在其自己的 [worktrees](/zh-CN/worktrees) 中运行每个单元。请参阅 [并行运行代理](/zh-CN/agents) 以了解这些方法如何相关联。

**在您发布之前。** `/diff` 显示更改的内容，`/simplify` 审阅最近的文件并应用质量和效率修复，`/review` 或 `/security-review` 进行更深入的只读检查。

**在会话之间。** `/clear` 在保持项目内存的同时开始新任务。`/resume` 和 `/branch` 让您返回或分叉早期的对话。`/teleport` 将网络会话拉入此终端，`/remote-control` 让您从另一台设备继续此本地会话。

**当出现问题时。** `/rewind` 将代码和对话回滚到检查点，或总结对话的一部分。`/doctor` 和 `/debug` 诊断安装和运行时问题，`/feedback` 报告附加会话上下文的错误。

## 所有命令

下表列出了 Claude Code 中包含的所有命令。标记为 **[Skill](/zh-CN/skills#bundled-skills)** 的条目是捆绑的 skills。它们使用与您自己编写的 skills 相同的机制：一个提示交给 Claude，Claude 也可以在相关时自动调用。其他所有内容都是内置命令，其行为被编码到 CLI 中。要添加您自己的命令，请参阅 [skills](/zh-CN/skills)。

在下表中，`<arg>` 表示必需的参数，`[arg]` 表示可选参数。

<Note>
  并非每个命令都对每个用户显示。可用性取决于您的平台、计划和环境。例如，`/desktop` 仅在 macOS 和 Windows 上显示，`/upgrade` 仅在 Pro 和 Max 计划上显示。
</Note>

| 命令                                              | 用途                                                                                                                                                                                                                                                                                                                                                                                                          |
| :---------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/add-dir <path>`                               | 为当前会话期间的文件访问添加工作目录。大多数 `.claude/` 配置[不会从添加的目录中发现](/zh-CN/permissions#additional-directories-grant-file-access-not-configuration)。您可以稍后使用 `--continue` 或 `--resume` 从添加的目录恢复会话                                                                                                                                                                                                                               |
| `/agents`                                       | 管理 [agent](/zh-CN/sub-agents) 配置                                                                                                                                                                                                                                                                                                                                                                            |
| `/autofix-pr [prompt]`                          | 生成一个[网络版 Claude Code](/zh-CN/claude-code-on-the-web#auto-fix-pull-requests) 会话，监视当前分支的 PR，并在 CI 失败或审阅者留下评论时推送修复。使用 `gh pr view` 检测已检出分支的开放 PR；要监视不同的 PR，请先检出其分支。默认情况下，远程会话被告知修复每个 CI 失败和审阅评论；传递一个提示以给它不同的说明，例如 `/autofix-pr only fix lint and type errors`。需要 `gh` CLI 和访问[网络版 Claude Code](/zh-CN/claude-code-on-the-web#who-can-use-claude-code-on-the-web)                                               |
| `/background [prompt]`                          | 将当前会话分离以作为[后台 agent](/zh-CN/agent-view) 运行并释放此终端。传递一个提示以在分离前发送一条更多指令。使用 `claude agents` 监视会话。别名：`/bg`                                                                                                                                                                                                                                                                                                       |
| `/batch <instruction>`                          | **[Skill](/zh-CN/skills#bundled-skills).** 在整个代码库中并行编排大规模更改。研究代码库，将工作分解为 5 到 30 个独立单元，并呈现一个计划。获得批准后，在隔离的 [git worktree](/zh-CN/worktrees) 中为每个单元生成一个[后台 subagent](/zh-CN/sub-agents#run-subagents-in-foreground-or-background)。每个 subagent 实现其单元、运行测试并打开一个 pull request。需要一个 git 存储库。示例：`/batch migrate src/ from Solid to React`                                                                           |
| `/branch [name]`                                | 在此点创建当前对话的分支。切换到分支并保留原始分支，您可以使用 `/resume` 返回。别名：`/fork`。当设置 [`CLAUDE_CODE_FORK_SUBAGENT`](/zh-CN/env-vars) 时，`/fork` 改为生成一个[分叉的 subagent](/zh-CN/sub-agents#fork-the-current-conversation)，不再是此命令的别名                                                                                                                                                                                                        |
| `/btw <question>`                               | 提出快速[附加问题](/zh-CN/interactive-mode#side-questions-with-%2Fbtw)，无需添加到对话中                                                                                                                                                                                                                                                                                                                                     |
| `/chrome`                                       | 配置 [Claude in Chrome](/zh-CN/chrome) 设置                                                                                                                                                                                                                                                                                                                                                                     |
| `/claude-api [migrate\|managed-agents-onboard]` | **[Skill](/zh-CN/skills#bundled-skills).** 为您的项目语言（Python、TypeScript、Java、Go、Ruby、C#、PHP 或 cURL）和 Managed Agents 参考加载 Claude API 参考资料。涵盖工具使用、流式传输、批处理、结构化输出和常见陷阱。当您的代码导入 `anthropic` 或 `@anthropic-ai/sdk` 时也会自动激活。运行 `/claude-api migrate` 以将现有 Claude API 代码升级到更新的模型：Claude 询问要扫描哪些文件以及要针对哪个模型，然后更新在版本之间更改的模型 ID、thinking 配置和其他参数。运行 `/claude-api managed-agents-onboard` 以获得交互式演练，从头开始创建新的 Managed Agent |
| `/clear [name]`                                 | 使用空上下文启动新对话。之前的对话在 `/resume` 中保持可用。传递一个名称以在 `/resume` 选择器中标记之前的对话。要在继续同一对话的同时释放上下文，请改用 `/compact`。别名：`/reset`、`/new`                                                                                                                                                                                                                                                                                        |
| `/color [color\|default]`                       | 为当前会话设置提示栏颜色。可用颜色：`red`、`blue`、`green`、`yellow`、`purple`、`orange`、`pink`、`cyan`。使用 `default` 重置，或不带参数运行以选择随机颜色。当 [Remote Control](/zh-CN/remote-control) 连接时，颜色同步到 claude.ai/code                                                                                                                                                                                                                           |
| `/compact [instructions]`                       | 通过总结到目前为止的对话来释放上下文。可选择性地传递焦点说明以进行总结。请参阅[压缩如何处理规则、skills 和内存文件](/zh-CN/context-window#what-survives-compaction)                                                                                                                                                                                                                                                                                              |
| `/config`                                       | 打开[设置](/zh-CN/settings)界面以调整主题、模型、[输出样式](/zh-CN/output-styles)和其他偏好设置。别名：`/settings`                                                                                                                                                                                                                                                                                                                        |
| `/context [all]`                                | 将当前上下文使用情况可视化为彩色网格。显示上下文密集型工具、内存膨胀和容量警告的优化建议。在[全屏模式](/zh-CN/fullscreen)中，每项的分解被折叠以保持网格可见。传递 `all` 以展开它                                                                                                                                                                                                                                                                                                      |
| `/copy [N]`                                     | 将最后一个助手响应复制到剪贴板。传递数字 `N` 以复制第 N 个最新响应：`/copy 2` 复制倒数第二个。当存在代码块时，显示交互式选择器以选择单个块或完整响应。在选择器中按 `w` 将选择内容写入文件而不是剪贴板，这在 SSH 上很有用                                                                                                                                                                                                                                                                                  |
| `/cost`                                         | `/usage` 的别名                                                                                                                                                                                                                                                                                                                                                                                                |
| `/debug [description]`                          | **[Skill](/zh-CN/skills#bundled-skills).** 为当前会话启用调试日志记录并通过读取会话调试日志来排查问题。调试日志默认关闭，除非您使用 `claude --debug` 启动，因此在会话中途运行 `/debug` 会从该点开始捕获日志。可选择性地描述问题以集中分析                                                                                                                                                                                                                                                    |
| `/desktop`                                      | 在 Claude Code Desktop 应用中继续当前会话。仅限 macOS 和 Windows。别名：`/app`                                                                                                                                                                                                                                                                                                                                                |
| `/diff`                                         | 打开交互式差异查看器，显示未提交的更改和每轮差异。使用左/右箭头在当前 git 差异和单个 Claude 轮次之间切换，使用上/下浏览文件                                                                                                                                                                                                                                                                                                                                       |
| `/doctor`                                       | 诊断并验证您的 Claude Code 安装和设置。结果显示状态图标。按 `f` 让 Claude 修复任何报告的问题                                                                                                                                                                                                                                                                                                                                                 |
| `/effort [level\|auto]`                         | 设置模型[工作量级别](/zh-CN/model-config#adjust-effort-level)。接受 `low`、`medium`、`high`、`xhigh` 或 `max`；可用级别取决于模型，`max` 仅限会话。`auto` 重置为模型默认值。不带参数时，打开交互式滑块；使用左右箭头选择级别，按 `Enter` 应用。立即生效，无需等待当前响应完成                                                                                                                                                                                                                    |
| `/exit`                                         | 退出 CLI。在附加的[后台会话](/zh-CN/agent-view#attach-to-a-session)中，这会分离并且会话继续运行。别名：`/quit`                                                                                                                                                                                                                                                                                                                           |
| `/export [filename]`                            | 将当前对话导出为纯文本。使用文件名时，直接写入该文件。不使用文件名时，打开对话框以复制到剪贴板或保存到文件                                                                                                                                                                                                                                                                                                                                                       |
| `/extra-usage`                                  | 配置额外使用量以在达到速率限制时继续工作                                                                                                                                                                                                                                                                                                                                                                                        |
| `/fast [on\|off]`                               | 切换[快速模式](/zh-CN/fast-mode)开启或关闭                                                                                                                                                                                                                                                                                                                                                                             |
| `/feedback [report]`                            | 提交关于 Claude Code 的反馈。别名：`/bug`                                                                                                                                                                                                                                                                                                                                                                              |
| `/fewer-permission-prompts`                     | **[Skill](/zh-CN/skills#bundled-skills).** 扫描您的记录以查找常见的只读 Bash 和 MCP 工具调用，然后向项目 `.claude/settings.json` 添加优先级允许列表以减少权限提示                                                                                                                                                                                                                                                                                    |
| `/focus`                                        | 切换焦点视图，仅显示您的最后一个提示、带有编辑 diffstats 的单行工具调用摘要和最终响应。选择在会话间保持。仅在[全屏渲染](/zh-CN/fullscreen)中可用                                                                                                                                                                                                                                                                                                                    |
| `/goal [condition\|clear]`                      | 设置一个[目标](/zh-CN/goal)：Claude 在多个轮次中继续工作，直到满足条件。不带参数时，显示当前或最近实现的目标。`clear`、`stop`、`off`、`reset`、`none` 或 `cancel` 会提前移除活跃目标                                                                                                                                                                                                                                                                                  |
| `/heapdump`                                     | 将 JavaScript 堆快照和内存分解写入 `~/Desktop`，或在 Linux 上没有 Desktop 文件夹的情况下写入您的主目录，以诊断高内存使用情况。请参阅[故障排除](/zh-CN/troubleshooting#high-cpu-or-memory-usage)                                                                                                                                                                                                                                                               |
| `/help`                                         | 显示帮助和可用命令                                                                                                                                                                                                                                                                                                                                                                                                   |
| `/hooks`                                        | 查看工具事件的 [hook](/zh-CN/hooks) 配置                                                                                                                                                                                                                                                                                                                                                                             |
| `/ide`                                          | 管理 IDE 集成并显示状态                                                                                                                                                                                                                                                                                                                                                                                              |
| `/init`                                         | 使用 `CLAUDE.md` 指南初始化项目。设置 `CLAUDE_CODE_NEW_INIT=1` 以获得交互式流程，该流程还会引导您完成 skills、hooks 和个人内存文件                                                                                                                                                                                                                                                                                                                 |
| `/insights`                                     | 生成报告，分析您的 Claude Code 会话，包括项目领域、交互模式和摩擦点                                                                                                                                                                                                                                                                                                                                                                    |
| `/install-github-app`                           | 为存储库设置 [Claude GitHub Actions](/zh-CN/github-actions) 应用。引导您选择存储库并配置集成                                                                                                                                                                                                                                                                                                                                      |
| `/install-slack-app`                            | 安装 Claude Slack 应用。打开浏览器以完成 OAuth 流程                                                                                                                                                                                                                                                                                                                                                                        |
| `/keybindings`                                  | 打开或创建您的快捷键配置文件                                                                                                                                                                                                                                                                                                                                                                                              |
| `/login`                                        | 登录到您的 Anthropic 账户                                                                                                                                                                                                                                                                                                                                                                                          |
| `/logout`                                       | 从您的 Anthropic 账户登出                                                                                                                                                                                                                                                                                                                                                                                          |
| `/loop [interval] [prompt]`                     | **[Skill](/zh-CN/skills#bundled-skills).** 在会话保持打开状态时重复运行提示。省略间隔，Claude 会在迭代之间自动调整步速。省略提示，Claude 运行自主维护检查，或运行 `.claude/loop.md` 中的提示（如果存在）。示例：`/loop 5m check if the deploy finished`。请参阅[按计划运行提示](/zh-CN/scheduled-tasks)。别名：`/proactive`                                                                                                                                                                  |
| `/mcp`                                          | 管理 MCP server 连接和 OAuth 身份验证                                                                                                                                                                                                                                                                                                                                                                                |
| `/memory`                                       | 编辑 `CLAUDE.md` 内存文件，启用或禁用 [auto-memory](/zh-CN/memory#auto-memory)，并查看自动内存条目                                                                                                                                                                                                                                                                                                                                |
| `/mobile`                                       | 显示二维码以下载 Claude 移动应用。别名：`/ios`、`/android`                                                                                                                                                                                                                                                                                                                                                                   |
| `/model [model]`                                | 选择或更改 AI 模型。对于支持的模型，使用左/右箭头[调整工作量级别](/zh-CN/model-config#adjust-effort-level)。不带参数时，打开一个选择器，当对话有先前输出时要求确认，因为下一个响应会重新读取完整历史记录而不使用缓存的上下文。确认后，更改立即生效，无需等待当前响应完成                                                                                                                                                                                                                                                |
| `/passes`                                       | 与朋友分享一周免费的 Claude Code。仅在您的账户符合条件时可见                                                                                                                                                                                                                                                                                                                                                                        |
| `/permissions`                                  | 管理工具权限的允许、询问和拒绝规则。打开交互式对话框，您可以按范围查看规则、添加或删除规则、管理工作目录，以及查看[最近的自动模式拒绝](/zh-CN/auto-mode-config#review-denials)。别名：`/allowed-tools`                                                                                                                                                                                                                                                                            |
| `/plan [description]`                           | 直接从提示进入 Plan Mode。传递可选描述以进入 Plan Mode 并立即开始该任务，例如 `/plan fix the auth bug`                                                                                                                                                                                                                                                                                                                                  |
| `/plugin`                                       | 管理 Claude Code [plugins](/zh-CN/plugins)                                                                                                                                                                                                                                                                                                                                                                    |
| `/powerup`                                      | 通过带有动画演示的快速交互式课程发现 Claude Code 功能                                                                                                                                                                                                                                                                                                                                                                           |
| `/pr-comments [PR]`                             | {/*max-version: 2.1.90*/}在 v2.1.91 中移除。改为直接询问 Claude 以查看 pull request 评论。在早期版本中，从 GitHub pull request 获取并显示评论；自动检测当前分支的 PR，或传递 PR URL 或编号。需要 `gh` CLI                                                                                                                                                                                                                                                     |
| `/privacy-settings`                             | 查看和更新您的隐私设置。仅对 Pro 和 Max 计划订阅者可用                                                                                                                                                                                                                                                                                                                                                                            |
| `/radio`                                        | 在浏览器中打开 Claude FM lo-fi 电台。当浏览器不可用时打印流 URL。在 Bedrock、Vertex 或 Foundry 上不可用                                                                                                                                                                                                                                                                                                                                  |
| `/recap`                                        | 按需生成当前会话的单行摘要。请参阅[会话摘要](/zh-CN/interactive-mode#session-recap)以了解您离开后出现的自动摘要                                                                                                                                                                                                                                                                                                                                |
| `/release-notes`                                | 在交互式版本选择器中查看更改日志。选择特定版本以查看其发布说明，或选择显示所有版本                                                                                                                                                                                                                                                                                                                                                                   |
| `/reload-plugins`                               | 重新加载所有活跃 [plugins](/zh-CN/plugins) 以应用待处理的更改，无需重启。报告每个已重新加载组件的计数并标记任何加载错误                                                                                                                                                                                                                                                                                                                                   |
| `/remote-control`                               | 使此会话可从 claude.ai 进行[远程控制](/zh-CN/remote-control)。别名：`/rc`                                                                                                                                                                                                                                                                                                                                                   |
| `/remote-env`                                   | 为[使用 `--remote` 启动的网络会话](/zh-CN/claude-code-on-the-web#configure-your-environment)配置默认远程环境                                                                                                                                                                                                                                                                                                                  |
| `/rename [name]`                                | 重命名当前会话并在提示栏上显示名称。不使用名称时，从对话历史记录自动生成一个                                                                                                                                                                                                                                                                                                                                                                      |
| `/resume [session]`                             | 按 ID 或名称恢复对话，或打开会话选择器。别名：`/continue`                                                                                                                                                                                                                                                                                                                                                                        |
| `/review [PR]`                                  | 在当前会话中本地审阅 pull request。要进行更深入的基于云的审阅，请参阅 [`/ultrareview`](/zh-CN/ultrareview)                                                                                                                                                                                                                                                                                                                              |
| `/rewind`                                       | 将对话和/或代码倒回到上一个点，或从选定的消息进行总结。请参阅 [checkpointing](/zh-CN/checkpointing)。别名：`/checkpoint`、`/undo`                                                                                                                                                                                                                                                                                                              |
| `/sandbox`                                      | 切换 [sandbox mode](/zh-CN/sandboxing)。仅在支持的平台上可用                                                                                                                                                                                                                                                                                                                                                             |
| `/schedule [description]`                       | 创建、更新、列出或运行 [routines](/zh-CN/routines)，这些 routines 在 Anthropic 管理的云基础设施上执行。Claude 会以对话方式引导您完成设置。别名：`/routines`                                                                                                                                                                                                                                                                                             |
| `/scroll-speed`                                 | 交互式调整鼠标滚轮[滚动速度](/zh-CN/fullscreen#mouse-wheel-scrolling)，使用标尺，您可以在对话框打开时滚动以预览更改。仅在[全屏渲染](/zh-CN/fullscreen)中可用，在 JetBrains IDE 终端中不可用                                                                                                                                                                                                                                                                       |
| `/security-review`                              | 分析当前分支上的待处理更改以查找安全漏洞。审查 git 差异并识别注入、身份验证问题和数据泄露等风险                                                                                                                                                                                                                                                                                                                                                          |
| `/setup-bedrock`                                | 通过交互式向导配置 [Amazon Bedrock](/zh-CN/amazon-bedrock) 身份验证、区域和模型固定。仅在设置 `CLAUDE_CODE_USE_BEDROCK=1` 时可见。首次 Bedrock 用户也可以从登录屏幕访问此向导                                                                                                                                                                                                                                                                              |
| `/setup-vertex`                                 | 通过交互式向导配置 [Google Vertex AI](/zh-CN/google-vertex-ai) 身份验证、项目、区域和模型固定。仅在设置 `CLAUDE_CODE_USE_VERTEX=1` 时可见。首次 Vertex AI 用户也可以从登录屏幕访问此向导                                                                                                                                                                                                                                                                      |
| `/simplify [focus]`                             | **[Skill](/zh-CN/skills#bundled-skills).** 审阅您最近更改的文件以查找代码重用、质量和效率问题，然后修复它们。并行生成三个审阅 agent，聚合其发现，并应用修复。传递文本以集中关注特定问题：`/simplify focus on memory efficiency`                                                                                                                                                                                                                                                 |
| `/skills`                                       | 列出可用的 [skills](/zh-CN/skills)。按 `t` 按令牌计数排序。按 `Space` 以[从 Claude 或 `/` 菜单中隐藏 skill](/zh-CN/skills#override-skill-visibility-from-settings)，然后按 `Enter` 保存                                                                                                                                                                                                                                                   |
| `/stats`                                        | `/usage` 的别名。在统计选项卡上打开                                                                                                                                                                                                                                                                                                                                                                                      |
| `/status`                                       | 打开设置界面（状态选项卡），显示版本、模型、账户和连接性。在 Claude 响应时工作，无需等待当前响应完成                                                                                                                                                                                                                                                                                                                                                      |
| `/statusline`                                   | 配置 Claude Code 的[状态行](/zh-CN/statusline)。描述您想要的内容，或不带参数运行以从您的 shell 提示自动配置                                                                                                                                                                                                                                                                                                                                  |
| `/stickers`                                     | 订购 Claude Code 贴纸                                                                                                                                                                                                                                                                                                                                                                                           |
| `/stop`                                         | 停止当前[后台会话](/zh-CN/agent-view)。仅在附加到后台会话时可用；记录和任何 worktree 都会保留。要分离而不停止，请使用 `/exit` 或按 `←`                                                                                                                                                                                                                                                                                                                   |
| `/tasks`                                        | 列出并管理后台任务。也可用作 `/bashes`                                                                                                                                                                                                                                                                                                                                                                                    |
| `/team-onboarding`                              | 从您的 Claude Code 使用历史记录生成团队入职指南。Claude 分析您过去 30 天的会话、命令和 MCP server 使用情况，并生成一个 markdown 指南，团队成员可以粘贴为第一条消息以快速设置。对于 Pro、Max、Team 和 Enterprise 计划上的 claude.ai 订阅者，还返回一个共享链接，团队成员可以直接在 Claude Code 中打开                                                                                                                                                                                                           |
| `/teleport`                                     | 将[网络版 Claude Code](/zh-CN/claude-code-on-the-web#from-web-to-terminal) 会话拉入此终端：打开选择器，然后获取分支和对话。也可用作 `/tp`。需要 claude.ai 订阅                                                                                                                                                                                                                                                                                   |
| `/terminal-setup`                               | 为 Shift+Enter 和其他快捷键配置终端快捷键。仅在需要它的终端中可见，如 VS Code、Cursor、Windsurf、Alacritty 或 Zed                                                                                                                                                                                                                                                                                                                           |
| `/theme`                                        | 更改颜色主题。包括跟随您终端深色或浅色背景的 `auto` 选项、浅色和深色变体、色盲友好（道尔顿化）主题、使用您终端颜色调色板的 ANSI 主题，以及来自 `~/.claude/themes/` 或 plugins 的任何[自定义主题](/zh-CN/terminal-config#create-a-custom-theme)。选择\*\*新建自定义主题…\*\*以创建一个                                                                                                                                                                                                               |
| `/tui [default\|fullscreen]`                    | 设置终端 UI 渲染器并使用您的对话完整性重新启动到它。`fullscreen` 启用[无闪烁 alt-screen 渲染器](/zh-CN/fullscreen)。不带参数时，打印活跃渲染器                                                                                                                                                                                                                                                                                                            |
| `/ultraplan <prompt>`                           | 在 [ultraplan](/zh-CN/ultraplan) 会话中起草计划，在浏览器中审阅，然后远程执行或将其发送回您的终端                                                                                                                                                                                                                                                                                                                                            |
| `/ultrareview [PR]`                             | 在云沙箱中运行深度、多 agent 代码审阅，使用 [ultrareview](/zh-CN/ultrareview)。Pro 和 Max 包括 3 次免费运行，然后需要[额外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)                                                                                                                                                                                                                              |
| `/upgrade`                                      | 打开升级页面以切换到更高的计划层级                                                                                                                                                                                                                                                                                                                                                                                           |
| `/usage`                                        | 显示会话成本、计划使用限制和活动统计。有关订阅特定的详细信息，请参阅[成本跟踪指南](/zh-CN/costs#using-the-%2Fusage-command)。`/cost` 和 `/stats` 是别名                                                                                                                                                                                                                                                                                                  |
| `/vim`                                          | {/*max-version: 2.1.91*/}在 v2.1.92 中移除。要在 Vim 和普通编辑模式之间切换，请使用 `/config` → 编辑器模式                                                                                                                                                                                                                                                                                                                           |
| `/voice [hold\|tap\|off]`                       | 切换[语音听写](/zh-CN/voice-dictation)，或在特定模式下启用它。需要 Claude.ai 账户                                                                                                                                                                                                                                                                                                                                                 |
| `/web-setup`                                    | 使用您的本地 `gh` CLI 凭证将您的 GitHub 账户连接到[网络版 Claude Code](/zh-CN/web-quickstart#connect-from-your-terminal)。如果 GitHub 未连接，`/schedule` 会自动提示此操作                                                                                                                                                                                                                                                                    |

## MCP prompts

MCP servers 可以公开显示为命令的 prompts。这些使用格式 `/mcp__<server>__<prompt>`，并从连接的服务器动态发现。有关详细信息，请参阅 [MCP prompts](/zh-CN/mcp#use-mcp-prompts-as-commands)。

## 另请参阅

* [Skills](/zh-CN/skills)：创建您自己的命令
* [Interactive mode](/zh-CN/interactive-mode)：快捷键、Vim 模式和命令历史记录
* [CLI reference](/zh-CN/cli-reference)：启动时标志

> ## Documentation Index
>
> Fetch the complete documentation index at: <https://code.claude.com/docs/llms.txt>
> Use this file to discover all available pages before exploring further.

# 环境变量

> 控制 Claude Code 行为的环境变量完整参考。

Claude Code 支持以下环境变量来控制其行为。在启动 `claude` 之前在 shell 中设置它们，或在 [`settings.json`](/zh-CN/settings#available-settings) 中的 `env` 键下配置它们，以将其应用于每个会话或在团队中推出。

| 变量                                                      | 目的                                                                                                                                                                                                                                                                                                                                     |
| :------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_API_KEY`                                     | 作为 `X-Api-Key` 标头发送的 API 密钥。设置后，即使您已登录，此密钥也会用于替代您的 Claude Pro、Max、Team 或 Enterprise 订阅。在非交互模式（`-p`）中，存在时始终使用该密钥。在交互模式中，系统会提示您在密钥覆盖订阅之前批准一次。要改用您的订阅，请运行 `unset ANTHROPIC_API_KEY`                                                                                                                                                       |
| `ANTHROPIC_AUTH_TOKEN`                                  | `Authorization` 标头的自定义值（您在此处设置的值将以 `Bearer` 为前缀）                                                                                                                                                                                                                                                                                      |
| `ANTHROPIC_AWS_API_KEY`                                 | [Claude Platform on AWS](/zh-CN/claude-platform-on-aws) 的工作区 API 密钥，在 AWS 控制台中生成。作为 `x-api-key` 发送，优先于 AWS SigV4                                                                                                                                                                                                                       |
| `ANTHROPIC_AWS_BASE_URL`                                | 覆盖 [Claude Platform on AWS](/zh-CN/claude-platform-on-aws) 端点 URL。用于自定义区域或通过 [LLM 网关](/zh-CN/llm-gateway)路由时。默认为 `https://aws-external-anthropic.{AWS_REGION}.api.aws`                                                                                                                                                                 |
| `ANTHROPIC_AWS_WORKSPACE_ID`                            | [Claude Platform on AWS](/zh-CN/claude-platform-on-aws) 所需。在每个请求中作为 `anthropic-workspace-id` 标头发送                                                                                                                                                                                                                                      |
| `ANTHROPIC_BASE_URL`                                    | 覆盖 API 端点以通过代理或网关路由请求。设置为非第一方主机时，[MCP 工具搜索](/zh-CN/mcp#scale-with-mcp-tool-search)默认禁用。如果您的代理转发 `tool_reference` 块，请设置 `ENABLE_TOOL_SEARCH=true`                                                                                                                                                                                       |
| `ANTHROPIC_BEDROCK_BASE_URL`                            | 覆盖 Bedrock 端点 URL。用于自定义 Bedrock 端点或通过 [LLM 网关](/zh-CN/llm-gateway)路由时。请参阅 [Amazon Bedrock](/zh-CN/amazon-bedrock)                                                                                                                                                                                                                      |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`                     | 覆盖 Bedrock Mantle 端点 URL。请参阅 [Mantle 端点](/zh-CN/amazon-bedrock#use-the-mantle-endpoint)                                                                                                                                                                                                                                                |
| `ANTHROPIC_BEDROCK_SERVICE_TIER`                        | Bedrock [服务层](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html)（`default`、`flex` 或 `priority`）。作为 `X-Amzn-Bedrock-Service-Tier` 标头发送。请参阅 [Amazon Bedrock](/zh-CN/amazon-bedrock#service-tiers)                                                                                                        |
| `ANTHROPIC_BETAS`                                       | 逗号分隔的其他 `anthropic-beta` 标头值列表，以包含在 API 请求中。Claude Code 已发送其需要的 beta 标头；使用此选项可在 Claude Code 添加原生支持之前选择加入 [Anthropic API beta](https://platform.claude.com/docs/en/api/beta-headers)。与需要 API 密钥身份验证的 [`--betas` 标志](/zh-CN/cli-reference#cli-flags)不同，此变量适用于所有身份验证方法，包括 Claude.ai 订阅                                                    |
| `ANTHROPIC_CUSTOM_HEADERS`                              | 要添加到请求的自定义标头（`Name: Value` 格式，多个标头用换行符分隔）                                                                                                                                                                                                                                                                                              |
| `ANTHROPIC_CUSTOM_MODEL_OPTION`                         | 要在 `/model` 选择器中添加为自定义条目的模型 ID。使用此选项可以使非标准或网关特定的模型可选择，而无需替换内置别名。请参阅[模型配置](/zh-CN/model-config#add-a-custom-model-option)                                                                                                                                                                                                               |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION`             | `/model` 选择器中自定义模型条目的显示描述。未设置时默认为 `Custom model (<model-id>)`                                                                                                                                                                                                                                                                          |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME`                    | `/model` 选择器中自定义模型条目的显示名称。未设置时默认为模型 ID                                                                                                                                                                                                                                                                                                 |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_SUPPORTED_CAPABILITIES`  | 请参阅[模型配置](/zh-CN/model-config#customize-pinned-model-display-and-capabilities)                                                                                                                                                                                                                                                         |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`                         | 请参阅[模型配置](/zh-CN/model-config#environment-variables)                                                                                                                                                                                                                                                                                   |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL_DESCRIPTION`             | 请参阅[模型配置](/zh-CN/model-config#customize-pinned-model-display-and-capabilities)                                                                                                                                                                                                                                                         |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME`                    | 请参阅[模型配置](/zh-CN/model-config#customize-pinned-model-display-and-capabilities)                                                                                                                                                                                                                                                         |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL_SUPPORTED_CAPABILITIES`  | 请参阅[模型配置](/zh-CN/model-config#customize-pinned-model-display-and-capabilities)                                                                                                                                                                                                                                                         |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`                          | 请参阅[模型配置](/zh-CN/model-config#environment-variables)                                                                                                                                                                                                                                                                                   |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION`              | 请参阅[模型配置](/zh-CN/model-config#customize-pinned-model-display-and-capabilities)                                                                                                                                                                                                                                                         |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME`                     | 请参阅[模型配置](/zh-CN/model-config#customize-pinned-model-display-and-capabilities)                                                                                                                                                                                                                                                         |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES`   | 请参阅[模型配置](/zh-CN/model-config#customize-pinned-model-display-and-capabilities)                                                                                                                                                                                                                                                         |
| `ANTHROPIC_DEFAULT_SONNET_MODEL`                        | 请参阅[模型配置](/zh-CN/model-config#environment-variables)                                                                                                                                                                                                                                                                                   |
| `ANTHROPIC_DEFAULT_SONNET_MODEL_DESCRIPTION`            | 请参阅[模型配置](/zh-CN/model-config#customize-pinned-model-display-and-capabilities)                                                                                                                                                                                                                                                         |
| `ANTHROPIC_DEFAULT_SONNET_MODEL_NAME`                   | 请参阅[模型配置](/zh-CN/model-config#customize-pinned-model-display-and-capabilities)                                                                                                                                                                                                                                                         |
| `ANTHROPIC_DEFAULT_SONNET_MODEL_SUPPORTED_CAPABILITIES` | 请参阅[模型配置](/zh-CN/model-config#customize-pinned-model-display-and-capabilities)                                                                                                                                                                                                                                                         |
| `ANTHROPIC_FOUNDRY_API_KEY`                             | Microsoft Foundry 身份验证的 API 密钥（请参阅 [Microsoft Foundry](/zh-CN/microsoft-foundry)）                                                                                                                                                                                                                                                      |
| `ANTHROPIC_FOUNDRY_BASE_URL`                            | Foundry 资源的完整基础 URL（例如，`https://my-resource.services.ai.azure.com/anthropic`）。`ANTHROPIC_FOUNDRY_RESOURCE` 的替代方案（请参阅 [Microsoft Foundry](/zh-CN/microsoft-foundry)）                                                                                                                                                                    |
| `ANTHROPIC_FOUNDRY_RESOURCE`                            | Foundry 资源名称（例如，`my-resource`）。如果未设置 `ANTHROPIC_FOUNDRY_BASE_URL`，则为必需（请参阅 [Microsoft Foundry](/zh-CN/microsoft-foundry)）                                                                                                                                                                                                              |
| `ANTHROPIC_MODEL`                                       | 要使用的模型设置的名称（请参阅[模型配置](/zh-CN/model-config#environment-variables)）                                                                                                                                                                                                                                                                      |
| `ANTHROPIC_SMALL_FAST_MODEL`                            | \[已弃用] [用于后台任务的 Haiku 级模型](/zh-CN/costs)的名称                                                                                                                                                                                                                                                                                            |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`                 | 使用 Bedrock 或 Bedrock Mantle 时覆盖 Haiku 级模型的 AWS 区域。在 Bedrock 上，仅当同时设置 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 或已弃用的 `ANTHROPIC_SMALL_FAST_MODEL` 时才生效，因为 Bedrock 否则会为后台任务使用主模型                                                                                                                                                                  |
| `ANTHROPIC_VERTEX_BASE_URL`                             | 覆盖 Vertex AI 端点 URL。用于自定义 Vertex 端点或通过 [LLM 网关](/zh-CN/llm-gateway)路由时。请参阅 [Google Vertex AI](/zh-CN/google-vertex-ai)                                                                                                                                                                                                                 |
| `ANTHROPIC_VERTEX_PROJECT_ID`                           | Vertex AI 请求的 GCP 项目 ID。被 `GCLOUD_PROJECT`、`GOOGLE_CLOUD_PROJECT` 或您的 `GOOGLE_APPLICATION_CREDENTIALS` 凭证文件中的项目覆盖。请参阅 [Google Vertex AI](/zh-CN/google-vertex-ai)                                                                                                                                                                      |
| `ANTHROPIC_WORKSPACE_ID`                                | [工作负载身份联合](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation)的工作区 ID。当您的联合规则的范围超过一个工作区时设置此选项，以便令牌交换知道要针对哪个工作区                                                                                                                                                                                             |
| `API_TIMEOUT_MS`                                        | API 请求的超时时间（以毫秒为单位）（默认值：600000，或 10 分钟；最大值：2147483647）。在缓慢网络上请求超时或通过代理路由时增加此值。超过最大值的值会导致底层计时器溢出，导致请求立即失败                                                                                                                                                                                                                               |
| `AWS_BEARER_TOKEN_BEDROCK`                              | 用于身份验证的 Bedrock API 密钥（请参阅 [Bedrock API 密钥](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/)）                                                                                                                                                                                    |
| `BASH_DEFAULT_TIMEOUT_MS`                               | 长时间运行的 bash 命令的默认超时（默认值：120000，或 2 分钟）                                                                                                                                                                                                                                                                                                 |
| `BASH_MAX_OUTPUT_LENGTH`                                | bash 输出中的最大字符数，超过此数字后将完整输出保存到文件，Claude 接收路径加上简短预览。请参阅 [Bash 工具行为](/zh-CN/tools-reference#bash-tool-behavior)                                                                                                                                                                                                                           |
| `BASH_MAX_TIMEOUT_MS`                                   | 模型可以为长时间运行的 bash 命令设置的最大超时（默认值：600000，或 10 分钟）                                                                                                                                                                                                                                                                                         |
| `CCR_FORCE_BUNDLE`                                      | 设置为 `1` 以强制 [`claude --remote`](/zh-CN/claude-code-on-the-web#send-local-repositories-without-github) 捆绑并上传您的本地存储库，即使 GitHub 访问可用                                                                                                                                                                                                      |
| `CLAUDECODE`                                            | 在 Claude Code 生成的 shell 环境中设置为 `1`（Bash 工具、tmux 会话）。在 [hooks](/zh-CN/hooks) 或[状态行](/zh-CN/statusline)命令中未设置。用于检测脚本何时在 Claude Code 生成的 shell 内运行                                                                                                                                                                                        |
| `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS`               | 设置为 `1` 以禁用所有内置 [subagent](/zh-CN/sub-agents) 类型，如 Explore 和 Plan。仅适用于非交互模式（`-p` 标志）。对于想要空白状态的 SDK 用户很有用                                                                                                                                                                                                                               |
| `CLAUDE_AGENT_SDK_MCP_NO_PREFIX`                        | 设置为 `1` 以跳过 SDK 创建的 MCP 服务器中工具名称上的 `mcp__<server>__` 前缀。工具使用其原始名称。仅限 SDK 使用                                                                                                                                                                                                                                                            |
| `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`                   | 后台 subagents 的停滞超时（以毫秒为单位）。默认 `600000`（10 分钟）。计时器在每个流式进度事件时重置；如果在窗口内没有进度到达，subagent 会被中止，任务被标记为失败，将任何部分结果呈现给父级                                                                                                                                                                                                                         |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`                       | 设置触发自动压缩的上下文容量百分比（1-100）。默认情况下，自动压缩在大约 95% 容量时触发。使用较低的值（如 `50`）可更早进行压缩。高于默认阈值的值无效。适用于主对话和 subagents。此百分比与[状态行](/zh-CN/statusline)中可用的 `context_window.used_percentage` 字段一致                                                                                                                                                            |
| `CLAUDE_AUTO_BACKGROUND_TASKS`                          | 设置为 `1` 以强制启用长时间运行的代理任务的自动后台处理。启用后，subagents 在运行约两分钟后会移到后台                                                                                                                                                                                                                                                                             |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR`              | 在主会话中每个 Bash 或 PowerShell 命令后返回到原始工作目录                                                                                                                                                                                                                                                                                                 |
| `CLAUDE_CODE_ACCESSIBILITY`                             | 设置为 `1` 以保持原生终端光标可见并禁用反向文本光标指示器。允许 macOS Zoom 等屏幕放大镜跟踪光标位置                                                                                                                                                                                                                                                                             |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`          | 设置为 `1` 以从使用 `--add-dir` 指定的目录加载内存文件。加载 `CLAUDE.md`、`.claude/CLAUDE.md`、`.claude/rules/*.md` 和 `CLAUDE.local.md`。默认情况下，其他目录不加载内存文件                                                                                                                                                                                                     |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`                     | 应刷新凭证的间隔（以毫秒为单位）（使用 [`apiKeyHelper`](/zh-CN/settings#available-settings) 时）                                                                                                                                                                                                                                                            |
| `CLAUDE_CODE_ATTRIBUTION_HEADER`                        | 设置为 `0` 以从系统提示的开头省略归属块（客户端版本和提示指纹）。禁用它会改善通过 [LLM 网关](/zh-CN/llm-gateway)路由时的 prompt caching 命中率。Anthropic API 缓存不受影响                                                                                                                                                                                                                   |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW`                       | 设置用于自动压缩计算的上下文容量（以令牌为单位）。默认为模型的上下文窗口：标准模型为 200K，或[扩展上下文](/zh-CN/model-config#extended-context)模型为 1M。在 1M 模型上使用较低的值（如 `500000`）可将窗口视为 500K 用于压缩目的。该值上限为模型的实际上下文窗口。`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` 作为此值的百分比应用。设置此变量会将压缩阈值与状态行的 `used_percentage` 解耦，后者始终使用模型的完整上下文窗口                                                                  |
| `CLAUDE_CODE_AUTO_CONNECT_IDE`                          | 覆盖自动 [IDE 连接](/zh-CN/vs-code)。默认情况下，在支持的 IDE 的集成终端内启动时，Claude Code 会自动连接。设置为 `false` 以防止这种情况。设置为 `true` 以在自动检测失败时强制连接尝试，例如当 tmux 遮挡父终端时。优先于 [`autoConnectIde`](/zh-CN/settings#global-config-settings) 全局配置设置                                                                                                                          |
| `CLAUDE_CODE_CERT_STORE`                                | TLS 连接的 CA 证书源的逗号分隔列表。`bundled` 是 Claude Code 附带的 Mozilla CA 集。`system` 是操作系统信任存储。默认为 `bundled,system`                                                                                                                                                                                                                                 |
| `CLAUDE_CODE_CLIENT_CERT`                               | 用于 mTLS 身份验证的客户端证书文件的路径                                                                                                                                                                                                                                                                                                                |
| `CLAUDE_CODE_CLIENT_KEY`                                | 用于 mTLS 身份验证的客户端私钥文件的路径                                                                                                                                                                                                                                                                                                                |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`                     | 加密 CLAUDE\_CODE\_CLIENT\_KEY 的密码短语（可选）                                                                                                                                                                                                                                                                                                 |
| `CLAUDE_CODE_DEBUG_LOGS_DIR`                            | 覆盖调试日志文件路径。尽管名称如此，这是文件路径，而不是目录。需要通过 `--debug`、`/debug` 或 `DEBUG` 环境变量单独启用调试模式：仅设置此变量不会启用日志记录。[`--debug-file`](/zh-CN/cli-reference#cli-flags) 标志同时执行两者。默认为 `~/.claude/debug/<session-id>.txt`                                                                                                                                          |
| `CLAUDE_CODE_DEBUG_LOG_LEVEL`                           | 写入调试日志文件的最小日志级别。值：`verbose`、`debug`（默认）、`info`、`warn`、`error`。设置为 `verbose` 以包含高容量诊断（如完整状态行命令输出），或提高到 `error` 以减少噪音                                                                                                                                                                                                                    |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT`                        | 设置为 `1` 以禁用[1M 上下文窗口](/zh-CN/model-config#extended-context)支持。设置后，1M 模型变体在模型选择器中不可用。对于具有合规要求的企业环境很有用                                                                                                                                                                                                                                   |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`                 | 设置为 `1` 以禁用 Opus 4.6 和 Sonnet 4.6 的[自适应推理](/zh-CN/model-config#adjust-effort-level)并回退到由 `MAX_THINKING_TOKENS` 控制的固定思考预算。对 Opus 4.7 无效，它始终使用自适应推理                                                                                                                                                                                      |
| `CLAUDE_CODE_DISABLE_AGENT_VIEW`                        | 设置为 `1` 以关闭[后台代理和代理视图](/zh-CN/agent-view)：`claude agents`、`--bg`、`/background` 和按需监督员。等同于 [`disableAgentView`](/zh-CN/settings#available-settings) 设置                                                                                                                                                                                  |
| `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN`                  | 设置为 `1` 以禁用[全屏渲染](/zh-CN/fullscreen)并使用经典主屏幕渲染器。对话保持在您的终端的原生滚动条中，因此 `Cmd+f` 和 tmux 复制模式可以正常工作。优先于 `CLAUDE_CODE_NO_FLICKER` 和 [`tui`](/zh-CN/settings#available-settings) 设置。您也可以使用 `/tui default` 切换                                                                                                                                   |
| `CLAUDE_CODE_DISABLE_ATTACHMENTS`                       | 设置为 `1` 以禁用附件处理。带有 `@` 语法的文件提及作为纯文本发送，而不是扩展为文件内容                                                                                                                                                                                                                                                                                       |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY`                       | 设置为 `1` 以禁用[自动内存](/zh-CN/memory#auto-memory)。设置为 `0` 以在 `--bare` 模式或 [`autoMemoryEnabled: false`](/zh-CN/settings#available-settings) 会禁用它时强制启用自动内存。禁用后，Claude 不会创建或加载自动内存文件                                                                                                                                                           |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`                  | 设置为 `1` 以禁用所有后台任务功能，包括 Bash 和 subagent 工具上的 `run_in_background` 参数、自动后台处理和 Ctrl+B 快捷键                                                                                                                                                                                                                                                  |
| `CLAUDE_CODE_DISABLE_CLAUDE_MDS`                        | 设置为 `1` 以防止将任何 CLAUDE.md 内存文件加载到上下文中，包括用户、项目和自动内存文件                                                                                                                                                                                                                                                                                    |
| `CLAUDE_CODE_DISABLE_CRON`                              | 设置为 `1` 以禁用[计划任务](/zh-CN/scheduled-tasks)。`/loop` skill 和 cron 工具变为不可用，任何已计划的任务停止触发，包括已在会话中运行的任务                                                                                                                                                                                                                                       |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`                | 设置为 `1` 以从 API 请求中删除 Anthropic 特定的 `anthropic-beta` 请求标头和 beta 工具架构字段（如 `defer_loading` 和 `eager_input_streaming`）。当代理网关拒绝请求并出现"Unexpected value(s) for the `anthropic-beta` header"或"Extra inputs are not permitted"之类的错误时，请使用此选项。标准字段（`name`、`description`、`input_schema`、`cache_control`）被保留。                                       |
| `CLAUDE_CODE_DISABLE_FAST_MODE`                         | 设置为 `1` 以禁用[快速模式](/zh-CN/fast-mode)                                                                                                                                                                                                                                                                                                    |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`                   | 设置为 `1` 以禁用"Claude 表现如何？"会话质量调查。在设置 `DISABLE_TELEMETRY`、`DO_NOT_TRACK` 或 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 时也会禁用调查，除非 `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL` 选择重新启用。要设置样本率而不是完全禁用，请使用 [`feedbackSurveyRate`](/zh-CN/settings#available-settings) 设置。请参阅[会话质量调查](/zh-CN/data-usage#session-quality-surveys)             |
| `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING`                | 设置为 `1` 以禁用文件 [checkpointing](/zh-CN/checkpointing)。`/rewind` 命令将无法恢复代码更改                                                                                                                                                                                                                                                              |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`                  | 设置为 `1` 以从 Claude 的系统提示中删除内置的提交和 PR 工作流说明和 git 状态快照。在使用您自己的 git 工作流 skills 时很有用。设置后优先于 [`includeGitInstructions`](/zh-CN/settings#available-settings) 设置                                                                                                                                                                               |
| `CLAUDE_CODE_DISABLE_LEGACY_MODEL_REMAP`                | 设置为 `1` 以防止在 Anthropic API 上自动重新映射 Opus 4.0 和 4.1 到当前 Opus 版本。当您想要有意固定较旧的模型时使用。重新映射不在 Bedrock、Vertex 或 Foundry 上运行                                                                                                                                                                                                                     |
| `CLAUDE_CODE_DISABLE_MOUSE`                             | 设置为 `1` 以禁用[全屏渲染](/zh-CN/fullscreen)中的鼠标跟踪。使用 `PgUp` 和 `PgDn` 的键盘滚动仍然有效。使用此选项可保持终端的原生选择复制行为                                                                                                                                                                                                                                            |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`              | 等同于设置 `DISABLE_AUTOUPDATER`、`DISABLE_FEEDBACK_COMMAND`、`DISABLE_ERROR_REPORTING` 和 `DISABLE_TELEMETRY`                                                                                                                                                                                                                                 |
| `CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK`             | 设置为 `1` 以禁用流式请求在中途失败时的非流式回退。流式错误会传播到重试层。当代理或网关导致回退产生重复的工具执行时很有用                                                                                                                                                                                                                                                                        |
| `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL`  | 设置为 `1` 以跳过首次运行时官方插件市场的自动添加                                                                                                                                                                                                                                                                                                            |
| `CLAUDE_CODE_DISABLE_POLICY_SKILLS`                     | 设置为 `1` 以跳过从系统范围的托管 skills 目录加载 skills。对于不应加载操作员配置的 skills 的容器或 CI 会话很有用                                                                                                                                                                                                                                                               |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`                    | 设置为 `1` 以禁用基于对话上下文的自动终端标题更新                                                                                                                                                                                                                                                                                                            |
| `CLAUDE_CODE_DISABLE_THINKING`                          | 设置为 `1` 以强制禁用[扩展思考](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)，无论模型支持或其他设置如何。比 `MAX_THINKING_TOKENS=0` 更直接                                                                                                                                                                                               |
| `CLAUDE_CODE_DISABLE_VIRTUAL_SCROLL`                    | 设置为 `1` 以禁用[全屏渲染](/zh-CN/fullscreen)中的虚拟滚动并渲染转录中的每条消息。如果全屏模式中的滚动显示应该出现消息的空白区域，请使用此选项                                                                                                                                                                                                                                                   |
| `CLAUDE_CODE_EFFORT_LEVEL`                              | 为支持的模型设置努力级别。值：`low`、`medium`、`high`、`xhigh`、`max` 或 `auto` 以使用模型默认值。可用级别取决于模型。优先于 `/effort` 和 `effortLevel` 设置。请参阅[调整努力级别](/zh-CN/model-config#adjust-effort-level)                                                                                                                                                                   |
| `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`                       | 覆盖[会话回顾](/zh-CN/interactive-mode#session-recap)可用性。设置为 `0` 以强制关闭回顾，无论 `/config` 切换如何。设置为 `1` 以在 [`awaySummaryEnabled`](/zh-CN/settings#available-settings) 为 `false` 时强制启用回顾。优先于设置和 `/config` 切换                                                                                                                                       |
| `CLAUDE_CODE_ENABLE_BACKGROUND_PLUGIN_REFRESH`          | 设置为 `1` 以在[非交互模式](/zh-CN/headless)中的转换边界处刷新插件状态，在后台安装完成后。默认关闭，因为刷新会在会话中途更改系统提示，这会使该转换的 [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 失效                                                                                                                                                       |
| `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL`           | 设置为 `1` 以在 Anthropic 绑定的非必要流量被阻止时将"Claude 表现如何？"会话质量调查路由到您自己的 [OpenTelemetry 收集器](/zh-CN/monitoring-usage)。调查评分仅作为 OTEL 事件发送到您配置的收集器。在此模式下，不会向 Anthropic 发送任何调查数据。在设置 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`、`DISABLE_TELEMETRY` 或 `DO_NOT_TRACK` 时应用，否则无效。`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` 和组织产品反馈政策优先                       |
| `CLAUDE_CODE_ENABLE_FINE_GRAINED_TOOL_STREAMING`        | 控制工具调用输入是否在 API 生成时从 API 流式传输。关闭此选项时，大型工具输入（如长文件写入）仅在 Claude 完成生成后才到达，这可能看起来像是挂起。对于 Anthropic API 默认启用。在 Bedrock 和 Vertex 上，按模型启用，其中部署的容器支持它。设置为 `0` 以选择退出。设置为 `1` 以在通过 `ANTHROPIC_BASE_URL`、`ANTHROPIC_VERTEX_BASE_URL` 或 `ANTHROPIC_BEDROCK_BASE_URL` 路由到代理时强制启用。对 Foundry 和[网关](/zh-CN/llm-gateway)连接默认关闭                           |
| `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY`            | 设置为 `1` 以在 `ANTHROPIC_BASE_URL` 指向 Anthropic 兼容网关（如 LiteLLM、Kong 或内部代理）时从网关的 `/v1/models` 端点填充 `/model` 选择器。默认关闭，因为由共享 API 密钥支持的网关会显示该密钥可以访问的每个用户的每个模型。发现的模型仍由 [`availableModels`](/zh-CN/settings#available-settings) 允许列表过滤                                                                                                          |
| `CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE`                 | 设置为 `1` 以在 Claude Opus 4.7 上运行[快速模式](/zh-CN/fast-mode)而不是 Opus 4.6。设置此变量后，`/fast` 切换到 Opus 4.7；没有它，`/fast` 继续使用 Opus 4.6                                                                                                                                                                                                               |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`                  | 设置为 `false` 以禁用提示建议（`/config` 中的"提示建议"切换）。这些是在 Claude 响应后出现在提示输入中的灰显预测。请参阅[提示建议](/zh-CN/interactive-mode#prompt-suggestions)                                                                                                                                                                                                           |
| `CLAUDE_CODE_ENABLE_TASKS`                              | 设置为 `1` 以在非交互模式（`-p` 标志）中启用任务跟踪系统。任务在交互模式中默认启用。请参阅[任务列表](/zh-CN/interactive-mode#task-list)                                                                                                                                                                                                                                            |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                          | 设置为 `1` 以启用 OpenTelemetry 数据收集以获取指标和日志。在配置 OTel 导出器之前需要。请参阅[监控](/zh-CN/monitoring-usage)                                                                                                                                                                                                                                               |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY`                     | 查询循环变为空闲后自动退出前等待的时间（以毫秒为单位）。对于使用 SDK 模式的自动化工作流和脚本很有用                                                                                                                                                                                                                                                                                   |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`                  | 设置为 `1` 以启用[代理团队](/zh-CN/agent-teams)。代理团队是实验性的，默认禁用                                                                                                                                                                                                                                                                                   |
| `CLAUDE_CODE_EXTRA_BODY`                                | JSON 对象以合并到每个 API 请求体的顶级。对于传递 Claude Code 不直接公开的提供商特定参数很有用                                                                                                                                                                                                                                                                             |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS`               | 覆盖文件读取的默认令牌限制。当您需要完整读取较大文件时很有用                                                                                                                                                                                                                                                                                                         |
| `CLAUDE_CODE_FORCE_SYNC_OUTPUT`                         | 设置为 `1` 以在您的终端支持但未自动检测到时强制启用 DEC 私有模式 2026 [同步输出](https://gist.github.com/christianparpart/d8a62cc1ab659194337d73e399004036)。对于实现 BSU/ESU 但不回复能力探针的模拟器（如 Emacs `eat`）很有用。在 tmux 下无效                                                                                                                                                    |
| `CLAUDE_CODE_FORK_SUBAGENT`                             | 设置为 `1` 以启用[分叉 subagents](/zh-CN/sub-agents#fork-the-current-conversation)。分叉的 subagent 从主会话继承完整的对话上下文，而不是从头开始。启用后，`/fork` 生成分叉的 subagent 而不是充当 [`/branch`](/zh-CN/commands) 的别名，所有 subagent 生成在后台运行。在交互模式和通过 SDK 或 `claude -p` 中工作                                                                                                    |
| `CLAUDE_CODE_GIT_BASH_PATH`                             | 仅限 Windows：Git Bash 可执行文件 (`bash.exe`) 的路径。当 Git Bash 已安装但不在您的 PATH 中时使用。请参阅 [Windows 设置](/zh-CN/setup#set-up-on-windows)                                                                                                                                                                                                              |
| `CLAUDE_CODE_GLOB_HIDDEN`                               | 设置为 `false` 以在 Claude 调用 [Glob 工具](/zh-CN/tools-reference#glob-tool-behavior)时从结果中排除点文件。默认包含。不影响 `@` 文件自动完成、`ls`、Grep 或 Read                                                                                                                                                                                                           |
| `CLAUDE_CODE_GLOB_NO_IGNORE`                            | 设置为 `false` 以使 [Glob 工具](/zh-CN/tools-reference#glob-tool-behavior)尊重 `.gitignore` 模式。默认情况下，Glob 返回所有匹配的文件，包括被 gitignore 的文件。不影响 `@` 文件自动完成，它有自己的 [`respectGitignore` 设置](/zh-CN/settings#available-settings)                                                                                                                          |
| `CLAUDE_CODE_GLOB_TIMEOUT_SECONDS`                      | Glob 工具文件发现的超时时间（以秒为单位）。在大多数平台上默认为 20 秒，在 WSL 上默认为 60 秒                                                                                                                                                                                                                                                                                |
| `CLAUDE_CODE_HIDE_CWD`                                  | 设置为 `1` 以在启动徽标中隐藏工作目录。对于屏幕共享或录制（其中路径暴露您的操作系统用户名）很有用                                                                                                                                                                                                                                                                                    |
| `CLAUDE_CODE_IDE_HOST_OVERRIDE`                         | 覆盖用于连接到 IDE 扩展的主机地址。默认情况下，Claude Code 自动检测正确的地址，包括 WSL 到 Windows 的路由                                                                                                                                                                                                                                                                   |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`                     | 跳过 IDE 扩展的自动安装。等同于将 [`autoInstallIdeExtension`](/zh-CN/settings#global-config-settings) 设置为 `false`                                                                                                                                                                                                                                    |
| `CLAUDE_CODE_IDE_SKIP_VALID_CHECK`                      | 设置为 `1` 以跳过连接期间 IDE 锁定文件条目的验证。当自动连接无法找到您的 IDE 时使用，尽管它正在运行                                                                                                                                                                                                                                                                              |
| `CLAUDE_CODE_MAX_CONTEXT_TOKENS`                        | 覆盖 Claude Code 为活动模型假设的上下文窗口大小。仅在同时设置 `DISABLE_COMPACT` 时生效。当通过 `ANTHROPIC_BASE_URL` 路由到上下文窗口与其名称的内置大小不匹配的模型时使用                                                                                                                                                                                                                        |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`                         | 设置大多数请求的最大输出令牌数。默认值和上限因模型而异；请参阅[最大输出令牌](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison)。增加此值会减少在[自动压缩](/zh-CN/costs#reduce-token-usage)触发之前可用的有效上下文窗口。                                                                                                                                      |
| `CLAUDE_CODE_MAX_RETRIES`                               | 覆盖重试失败 API 请求的次数（默认值：10）                                                                                                                                                                                                                                                                                                               |
| `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`                  | 可以并行执行的只读工具和 subagents 的最大数量（默认值：10）。更高的值增加并行性但消耗更多资源                                                                                                                                                                                                                                                                                  |
| `CLAUDE_CODE_MAX_TURNS`                                 | 当未传递显式限制时，限制代理转换的数量。等同于传递 [`--max-turns`](/zh-CN/cli-reference#cli-flags)，当两者都设置时优先。不是正整数的值在启动时被拒绝并显示错误，而不是被视为无限制                                                                                                                                                                                                                      |
| `CLAUDE_CODE_MCP_ALLOWLIST_ENV`                         | 设置为 `1` 以使用仅安全基线环境加上服务器的配置 `env` 生成 stdio MCP 服务器，而不是继承您的 shell 环境                                                                                                                                                                                                                                                                     |
| `CLAUDE_CODE_NATIVE_CURSOR`                             | 设置为 `1` 以在输入插入符处显示终端自己的光标，而不是绘制的块。光标尊重终端的闪烁、形状和焦点设置                                                                                                                                                                                                                                                                                    |
| `CLAUDE_CODE_NEW_INIT`                                  | 设置为 `1` 以使 `/init` 运行交互式设置流程。该流程会询问要生成哪些文件，包括 CLAUDE.md、skills 和 hooks，然后再探索代码库并编写它们。没有此变量，`/init` 会自动生成 CLAUDE.md 而不提示。                                                                                                                                                                                                               |
| `CLAUDE_CODE_NO_FLICKER`                                | 设置为 `1` 以启用[全屏渲染](/zh-CN/fullscreen)，这是一个研究预览，可减少闪烁并在长对话中保持内存平坦。等同于 [`tui`](/zh-CN/settings#available-settings) 设置；您也可以使用 `/tui fullscreen` 切换                                                                                                                                                                                         |
| `CLAUDE_CODE_OAUTH_REFRESH_TOKEN`                       | Claude.ai 身份验证的 OAuth 刷新令牌。设置后，`claude auth login` 直接交换此令牌，而不是打开浏览器。需要 `CLAUDE_CODE_OAUTH_SCOPES`。对于在自动化环境中配置身份验证很有用                                                                                                                                                                                                                   |
| `CLAUDE_CODE_OAUTH_SCOPES`                              | 刷新令牌颁发时使用的空格分隔的 OAuth 作用域，例如 `"user:profile user:inference user:sessions:claude_code"`。设置 `CLAUDE_CODE_OAUTH_REFRESH_TOKEN` 时为必需                                                                                                                                                                                                       |
| `CLAUDE_CODE_OAUTH_TOKEN`                               | Claude.ai 身份验证的 OAuth 访问令牌。`/login` 对于 SDK 和自动化环境的替代方案。优先于钥匙链存储的凭证。使用 [`claude setup-token`](/zh-CN/authentication#generate-a-long-lived-token) 生成一个                                                                                                                                                                                   |
| `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE`               | 设置为 `1` 以保持[快速模式](/zh-CN/fast-mode)在 Claude Opus 4.6 上。优先于 `CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE`，所以如果您需要固定 Opus 4.6 无论默认如何变化，请设置此选项                                                                                                                                                                                                  |
| `CLAUDE_CODE_OTEL_FLUSH_TIMEOUT_MS`                     | 刷新待处理 OpenTelemetry spans 的超时时间（以毫秒为单位）（默认值：5000）。请参阅[监控](/zh-CN/monitoring-usage)                                                                                                                                                                                                                                                     |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`           | 刷新动态 OpenTelemetry 标头的间隔（以毫秒为单位）（默认值：1740000 / 29 分钟）。请参阅[动态标头](/zh-CN/monitoring-usage#dynamic-headers)                                                                                                                                                                                                                               |
| `CLAUDE_CODE_OTEL_SHUTDOWN_TIMEOUT_MS`                  | OpenTelemetry 导出器在关闭时完成的超时时间（以毫秒为单位）（默认值：2000）。如果在退出时丢弃指标，请增加此值。请参阅[监控](/zh-CN/monitoring-usage)                                                                                                                                                                                                                                       |
| `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`               | 设置为 `1` 以让 Claude Code 在新版本可用时在后台运行您的包管理器的升级命令。适用于 Homebrew 和 WinGet 安装。其他包管理器继续显示升级命令而不运行它。请参阅[自动更新](/zh-CN/setup#auto-updates)                                                                                                                                                                                                       |
| `CLAUDE_CODE_PERFORCE_MODE`                             | 设置为 `1` 以启用 Perforce 感知的写入保护。设置后，如果目标文件缺少所有者写入位（Perforce 在同步文件上清除，直到 `p4 edit` 打开它们），Edit、Write 和 NotebookEdit 会失败并显示 `p4 edit <file>` 提示。这可防止 Claude Code 绕过 Perforce 变更跟踪                                                                                                                                                            |
| `CLAUDE_CODE_PLUGIN_CACHE_DIR`                          | 覆盖插件根目录。尽管名称如此，这设置的是父目录，而不是缓存本身：市场和插件缓存位于此路径下的子目录中。默认为 `~/.claude/plugins`                                                                                                                                                                                                                                                             |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`                     | 安装或更新插件时 git 操作的超时（以毫秒为单位）（默认值：120000）。对于大型存储库或网络连接缓慢的情况，请增加此值。请参阅[Git 操作超时](/zh-CN/plugin-marketplaces#git-operations-time-out)                                                                                                                                                                                                       |
| `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE`        | 设置为 `1` 以在 `git pull` 失败时保留现有市场缓存，而不是擦除并重新克隆。在离线或隔离环境中很有用，其中重新克隆会以相同方式失败。请参阅[市场更新在离线环境中失败](/zh-CN/plugin-marketplaces#marketplace-updates-fail-in-offline-environments)                                                                                                                                                                |
| `CLAUDE_CODE_PLUGIN_PREFER_HTTPS`                       | 设置为 `1` 以通过 HTTPS 而不是 SSH 克隆 GitHub `owner/repo` 插件源。在 CI 运行器、容器或任何没有为 `github.com` 配置 SSH 密钥的环境中很有用                                                                                                                                                                                                                                   |
| `CLAUDE_CODE_PLUGIN_SEED_DIR`                           | 一个或多个只读插件种子目录的路径，在 Unix 上用 `:` 分隔，在 Windows 上用 `;` 分隔。使用此选项可将预填充的插件目录捆绑到容器镜像中。Claude Code 在启动时从这些目录注册市场，并使用预缓存的插件而无需重新克隆。请参阅[为容器预填充插件](/zh-CN/plugin-marketplaces#pre-populate-plugins-for-containers)                                                                                                                                 |
| `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`                  | 由嵌入 Claude Code 的主机平台设置，并代表其管理模型提供商路由。设置后，提供商选择、端点和身份验证变量（如 `CLAUDE_CODE_USE_BEDROCK`、`ANTHROPIC_BASE_URL` 和 `ANTHROPIC_API_KEY`）在设置文件中被忽略，以便用户设置无法覆盖主机的路由。Bedrock、Vertex 和 Foundry 的自动遥测选择退出也被跳过，因此遥测遵循标准 `DISABLE_TELEMETRY` 选择退出。请参阅[按 API 提供商的默认行为](/zh-CN/data-usage#default-behaviors-by-api-provider)                           |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS`                      | 设置为 `1` 以允许代理执行 DNS 解析而不是调用者。对于代理应处理主机名解析的环境选择加入                                                                                                                                                                                                                                                                                       |
| `CLAUDE_CODE_REMOTE`                                    | 当 Claude Code 作为[云会话](/zh-CN/claude-code-on-the-web)运行时自动设置为 `true`。从 hook 或设置脚本读取此值以检测您是否在云环境中                                                                                                                                                                                                                                        |
| `CLAUDE_CODE_REMOTE_SESSION_ID`                         | 在[云会话](/zh-CN/claude-code-on-the-web)中自动设置为当前会话的 ID。读取此值以构造返回会话转录的链接。请参阅[将工件链接回会话](/zh-CN/claude-code-on-the-web#link-artifacts-back-to-the-session)                                                                                                                                                                                   |
| `CLAUDE_CODE_RESUME_INTERRUPTED_TURN`                   | 设置为 `1` 以在上一个会话在中途结束时自动恢复。在 SDK 模式中使用，以便模型继续而无需 SDK 重新发送提示                                                                                                                                                                                                                                                                             |
| `CLAUDE_CODE_RESUME_PROMPT`                             | 覆盖在恢复在中途结束的会话时注入的继续消息。默认为 `Continue from where you left off.`。长时间运行的代理的生成脚本可以将其设置为更具指导性的启动消息。空字符串使用默认值                                                                                                                                                                                                                                 |
| `CLAUDE_CODE_SCRIPT_CAPS`                               | JSON 对象，当设置 `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` 时限制特定脚本在每个会话中可以调用的次数。键是与命令文本匹配的子字符串；值是整数调用限制。例如，`{"deploy.sh": 2}` 允许 `deploy.sh` 最多被调用两次。匹配是基于子字符串的，所以 shell 扩展技巧如 `./scripts/deploy.sh $(evil)` 仍然计入上限。通过 `xargs` 或 `find -exec` 的运行时扇出不被检测；这是一个深度防御控制                                                                                |
| `CLAUDE_CODE_SCROLL_SPEED`                              | 在[全屏渲染](/zh-CN/fullscreen)中设置鼠标滚轮滚动倍数。接受 1 到 20 的值。设置为 `3` 以匹配 `vim`（如果您的终端每个刻度线发送一个滚轮事件而不进行放大）。在 JetBrains IDE 终端中被忽略，Claude Code 使用其自己的滚动处理                                                                                                                                                                                          |
| `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`               | [SessionEnd](/zh-CN/hooks#sessionend) hooks 的时间预算（以毫秒为单位）。适用于会话退出、`/clear` 和通过交互式 `/resume` 切换会话。默认预算为 1.5 秒，自动提高到设置文件中配置的最高每个 hook `timeout`，最高 60 秒。插件提供的 hooks 上的超时不会提高预算                                                                                                                                                           |
| `CLAUDE_CODE_SESSION_ID`                                | 在 Bash 和 PowerShell 工具子进程中自动设置为当前会话 ID。与传递给 [hooks](/zh-CN/hooks) 的 `session_id` 字段匹配。在 `/clear` 时更新。用于将脚本和外部工具与启动它们的 Claude Code 会话相关联                                                                                                                                                                                                |
| `CLAUDE_CODE_SHELL`                                     | 覆盖自动 shell 检测。当您的登录 shell 与您的首选工作 shell 不同时很有用（例如，`bash` 与 `zsh`）                                                                                                                                                                                                                                                                      |
| `CLAUDE_CODE_SHELL_PREFIX`                              | 命令前缀以包装 Claude Code 生成的所有 bash 命令：Bash 工具调用、[hook](/zh-CN/hooks) 命令和 stdio [MCP server](/zh-CN/mcp) 启动命令。对于日志记录或审计很有用。示例：设置 `/path/to/logger.sh` 将每个命令作为 `/path/to/logger.sh <command>` 运行                                                                                                                                             |
| `CLAUDE_CODE_SIMPLE`                                    | 设置为 `1` 以使用最小系统提示和仅 Bash、文件读取和文件编辑工具运行。MCP 工具来自 `--mcp-config` 仍然可用。禁用 hooks、skills、plugins、MCP servers、自动内存和 CLAUDE.md 的自动发现。[`--bare`](/zh-CN/headless#start-faster-with-bare-mode) CLI 标志设置此选项                                                                                                                                      |
| `CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT`                      | 设置为 `1` 以在任何模型上使用较短的系统提示和缩写的工具描述。设置为 `0`、`false`、`no` 或 `off` 以选择退出，即使在实验或服务器配置会以其他方式启用它的模型上。完整的工具集、hooks、MCP 服务器和 CLAUDE.md 发现保持启用                                                                                                                                                                                                    |
| `CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH`                   | 跳过 [Claude Platform on AWS](/zh-CN/claude-platform-on-aws) 的客户端身份验证，用于自己签署请求的网关                                                                                                                                                                                                                                                        |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`                         | 跳过 Bedrock 的 AWS 身份验证（例如，使用 LLM 网关时）                                                                                                                                                                                                                                                                                                   |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH`                         | 跳过 Microsoft Foundry 的 Azure 身份验证（例如，使用 LLM 网关时）                                                                                                                                                                                                                                                                                       |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`                          | 跳过 Bedrock Mantle 的 AWS 身份验证（例如，使用 LLM 网关时）                                                                                                                                                                                                                                                                                            |
| `CLAUDE_CODE_SKIP_PROMPT_HISTORY`                       | 设置为 `1` 以跳过将提示历史和会话转录写入磁盘。使用此变量启动的会话不会出现在 `--resume`、`--continue` 或向上箭头历史中。对于临时脚本会话很有用                                                                                                                                                                                                                                                 |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`                          | 跳过 Vertex 的 Google 身份验证（例如，使用 LLM 网关时）                                                                                                                                                                                                                                                                                                 |
| `CLAUDE_CODE_SUBAGENT_MODEL`                            | 请参阅[模型配置](/zh-CN/model-config)                                                                                                                                                                                                                                                                                                         |
| `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`                      | 设置为 `1` 以从子进程环境（Bash 工具、hooks、MCP stdio 服务器）中删除 Anthropic 和云提供商凭证。父 Claude 进程为 API 调用保留这些凭证，但子进程无法读取它们，减少了通过 shell 扩展尝试窃取机密的提示注入攻击的暴露。在 Linux 上，这也在隔离的 PID 命名空间中运行 Bash 子进程，以便它们无法通过 `/proc` 读取主机进程环境；作为副作用，`ps`、`pgrep` 和 `kill` 无法看到或信号主机进程。当配置了 `allowed_non_write_users` 时，`claude-code-action` 会自动设置此选项                           |
| `CLAUDE_CODE_SYNC_PLUGIN_INSTALL`                       | 设置为 `1` 在非交互模式（`-p` 标志）中等待插件安装完成后再进行第一个查询。没有这个，插件在后台安装，可能在第一个回合不可用。与 `CLAUDE_CODE_SYNC_PLUGIN_INSTALL_TIMEOUT_MS` 结合以限制等待时间                                                                                                                                                                                                            |
| `CLAUDE_CODE_SYNC_PLUGIN_INSTALL_TIMEOUT_MS`            | 同步插件安装的超时时间（以毫秒为单位）。超过时，Claude Code 继续而不使用插件并记录错误。无默认值：没有此变量，同步安装会等待直到完成                                                                                                                                                                                                                                                               |
| `CLAUDE_CODE_SYNTAX_HIGHLIGHT`                          | 设置为 `false` 以禁用 diff 输出中的语法突出显示。当颜色干扰您的终端设置时很有用。要同时禁用代码块和文件预览中的突出显示，请使用 [`syntaxHighlightingDisabled`](/zh-CN/settings) 设置                                                                                                                                                                                                             |
| `CLAUDE_CODE_TASK_LIST_ID`                              | 跨会话共享任务列表。在多个 Claude Code 实例中设置相同的 ID 以协调共享任务列表。请参阅[任务列表](/zh-CN/interactive-mode#task-list)                                                                                                                                                                                                                                           |
| `CLAUDE_CODE_TEAM_NAME`                                 | 此队友所属的代理团队的名称。在[代理团队](/zh-CN/agent-teams)成员上自动设置                                                                                                                                                                                                                                                                                       |
| `CLAUDE_CODE_TMPDIR`                                    | 覆盖用于内部临时文件的临时目录。Claude Code 将 `/claude-{uid}/`（Unix）或 `/claude/`（Windows）附加到此路径。默认值：macOS 上为 `/tmp`，Linux/Windows 上为 `os.tmpdir()`                                                                                                                                                                                                     |
| `CLAUDE_CODE_TMUX_TRUECOLOR`                            | 设置为 `1` 以允许 tmux 内的 24 位真彩色输出。默认情况下，当设置 `$TMUX` 时，Claude Code 限制为 256 色，因为 tmux 不会通过真彩色转义序列，除非配置为这样做。在将 `set -ga terminal-overrides ',*:Tc'` 添加到您的 `~/.tmux.conf` 后设置此选项。请参阅[终端配置](/zh-CN/terminal-config)了解其他 tmux 设置                                                                                                                 |
| `CLAUDE_CODE_USE_ANTHROPIC_AWS`                         | 使用 [Claude Platform on AWS](/zh-CN/claude-platform-on-aws)                                                                                                                                                                                                                                                                             |
| `CLAUDE_CODE_USE_BEDROCK`                               | 使用 [Bedrock](/zh-CN/amazon-bedrock)                                                                                                                                                                                                                                                                                                    |
| `CLAUDE_CODE_USE_FOUNDRY`                               | 使用 [Microsoft Foundry](/zh-CN/microsoft-foundry)                                                                                                                                                                                                                                                                                       |
| `CLAUDE_CODE_USE_MANTLE`                                | 使用 Bedrock [Mantle 端点](/zh-CN/amazon-bedrock#use-the-mantle-endpoint)                                                                                                                                                                                                                                                                  |
| `CLAUDE_CODE_USE_NATIVE_FILE_SEARCH`                    | 设置为 `1` 以使用 Node.js 文件 API 而不是 ripgrep 发现自定义命令、subagents 和输出样式。如果捆绑的 ripgrep 二进制文件在您的环境中不可用或被阻止，请设置此选项。不影响 Grep 或文件搜索工具                                                                                                                                                                                                                |
| `CLAUDE_CODE_USE_POWERSHELL_TOOL`                       | 控制 PowerShell 工具。在没有 Git Bash 的 Windows 上，该工具会自动启用；设置为 `0` 以禁用它。在安装了 Git Bash 的 Windows 上，该工具正在逐步推出：设置为 `1` 以选择加入或 `0` 以选择退出。在 Linux、macOS 和 WSL 上，设置为 `1` 以启用它，这需要您的 `PATH` 上有 `pwsh`。在 Windows 上启用时，Claude 可以本地运行 PowerShell 命令，而不是通过 Git Bash 路由。请参阅 [PowerShell 工具](/zh-CN/tools-reference#powershell-tool)                        |
| `CLAUDE_CODE_USE_VERTEX`                                | 使用 [Vertex](/zh-CN/google-vertex-ai)                                                                                                                                                                                                                                                                                                   |
| `CLAUDE_CONFIG_DIR`                                     | 覆盖配置目录（默认值：`~/.claude`）。所有设置、凭证、会话历史和插件都存储在此路径下。对于并行运行多个帐户很有用：例如，`alias claude-work='CLAUDE_CONFIG_DIR=~/.claude-work claude'`                                                                                                                                                                                                         |
| `CLAUDE_EFFORT`                                         | 在 Bash 工具子进程和 hook 命令中自动设置为该转换的活动[努力级别](/zh-CN/model-config#adjust-effort-level)：`low`、`medium`、`high`、`xhigh` 或 `max`。与传递给 [hooks](/zh-CN/hooks) 的 `effort.level` 字段匹配。仅在当前模型支持努力参数时设置                                                                                                                                                |
| `CLAUDE_ENABLE_BYTE_WATCHDOG`                           | 设置为 `1` 以强制启用字节级流式空闲监视程序，或设置为 `0` 以强制禁用它。未设置时，监视程序对 Anthropic API 连接默认启用。字节监视程序在 `CLAUDE_STREAM_IDLE_TIMEOUT_MS` 设置的持续时间内没有字节到达线路时中止连接，最少 5 分钟，独立于事件级监视程序                                                                                                                                                                              |
| `CLAUDE_ENABLE_STREAM_WATCHDOG`                         | 设置为 `1` 以启用事件级流式空闲监视程序。默认关闭。对于 Bedrock、Vertex 和 Foundry，这是唯一可用的空闲监视程序。使用 `CLAUDE_STREAM_IDLE_TIMEOUT_MS` 配置超时                                                                                                                                                                                                                          |
| `CLAUDE_ENV_FILE`                                       | Claude Code 在每个 Bash 命令之前在同一 shell 进程中运行的 shell 脚本的路径，因此文件中的导出对命令可见。用于在命令之间保持 virtualenv 或 conda 激活。也由 [SessionStart](/zh-CN/hooks#persist-environment-variables)、[Setup](/zh-CN/hooks#setup)、[CwdChanged](/zh-CN/hooks#cwdchanged) 和 [FileChanged](/zh-CN/hooks#filechanged) hooks 动态填充                                               |
| `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX`             | 当未提供显式名称时，自动生成的[远程控制](/zh-CN/remote-control)会话名称的前缀。默认为您的机器的主机名，生成名称如 `myhost-graceful-unicorn`。`--remote-control-session-name-prefix` CLI 标志为单个调用设置相同的值                                                                                                                                                                               |
| `CLAUDE_STREAM_IDLE_TIMEOUT_MS`                         | 流式空闲监视程序关闭停滞连接前的超时（以毫秒为单位）。默认和最小 `300000`（5 分钟）对于字节级和事件级监视程序；较低的值被静默限制以吸收扩展思考暂停和代理缓冲。对于第三方提供商，需要 `CLAUDE_ENABLE_STREAM_WATCHDOG=1`                                                                                                                                                                                                     |
| `DEBUG`                                                 | 设置为 `1` 以启用调试模式，等同于使用 [`--debug`](/zh-CN/cli-reference#cli-flags) 启动。调试日志写入 `~/.claude/debug/<session-id>.txt`，或写入 `CLAUDE_CODE_DEBUG_LOGS_DIR` 设置的路径。仅真值 `1`、`true`、`yes` 和 `on` 启用调试模式，因此为其他工具设置的命名空间模式如 `DEBUG=express:*` 不会触发它                                                                                                     |
| `DISABLE_AUTOUPDATER`                                   | 设置为 `1` 以禁用自动后台更新。手动 `claude update` 仍然有效。使用 `DISABLE_UPDATES` 以阻止两者                                                                                                                                                                                                                                                                   |
| `DISABLE_AUTO_COMPACT`                                  | 设置为 `1` 以禁用接近上下文限制时的自动压缩。手动 `/compact` 命令仍然可用。当您想要明确控制何时进行压缩时使用                                                                                                                                                                                                                                                                        |
| `DISABLE_COMPACT`                                       | 设置为 `1` 以禁用所有压缩：自动压缩和手动 `/compact` 命令                                                                                                                                                                                                                                                                                                  |
| `DISABLE_COST_WARNINGS`                                 | 设置为 `1` 以禁用成本警告消息                                                                                                                                                                                                                                                                                                                      |
| `DISABLE_DOCTOR_COMMAND`                                | 设置为 `1` 以隐藏 `/doctor` 命令。对于用户不应运行安装诊断的托管部署很有用                                                                                                                                                                                                                                                                                          |
| `DISABLE_ERROR_REPORTING`                               | 设置为 `1` 以选择退出 Sentry 错误报告                                                                                                                                                                                                                                                                                                              |
| `DISABLE_EXTRA_USAGE_COMMAND`                           | 设置为 `1` 以隐藏 `/extra-usage` 命令，该命令允许用户购买超过速率限制的额外使用量                                                                                                                                                                                                                                                                                    |
| `DISABLE_FEEDBACK_COMMAND`                              | 设置为 `1` 以禁用 `/feedback` 命令。也接受较旧的名称 `DISABLE_BUG_COMMAND`                                                                                                                                                                                                                                                                              |
| `DISABLE_GROWTHBOOK`                                    | 设置为 `1` 以禁用 GrowthBook 功能标志获取并对每个标志使用代码默认值。除非同时设置 `DISABLE_TELEMETRY`，否则遥测事件日志记录保持启用                                                                                                                                                                                                                                                   |
| `DISABLE_INSTALLATION_CHECKS`                           | 设置为 `1` 以禁用安装警告。仅在手动管理安装位置时使用，因为这可能会掩盖标准安装的问题                                                                                                                                                                                                                                                                                          |
| `DISABLE_INSTALL_GITHUB_APP_COMMAND`                    | 设置为 `1` 以隐藏 `/install-github-app` 命令。使用第三方提供商（Bedrock、Vertex 或 Foundry）时已隐藏                                                                                                                                                                                                                                                            |
| `DISABLE_INTERLEAVED_THINKING`                          | 设置为 `1` 以防止发送交错思考 beta 标头。当您的 LLM 网关或提供商不支持[交错思考](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#interleaved-thinking)时很有用                                                                                                                                                                                    |
| `DISABLE_LOGIN_COMMAND`                                 | 设置为 `1` 以隐藏 `/login` 命令。当身份验证通过 API 密钥或 `apiKeyHelper` 外部处理时很有用                                                                                                                                                                                                                                                                        |
| `DISABLE_LOGOUT_COMMAND`                                | 设置为 `1` 以隐藏 `/logout` 命令                                                                                                                                                                                                                                                                                                               |
| `DISABLE_PROMPT_CACHING`                                | 设置为 `1` 以禁用所有模型的 prompt caching（优先于每个模型的设置）                                                                                                                                                                                                                                                                                            |
| `DISABLE_PROMPT_CACHING_HAIKU`                          | 设置为 `1` 以禁用 Haiku 模型的 prompt caching                                                                                                                                                                                                                                                                                                   |
| `DISABLE_PROMPT_CACHING_OPUS`                           | 设置为 `1` 以禁用 Opus 模型的 prompt caching                                                                                                                                                                                                                                                                                                    |
| `DISABLE_PROMPT_CACHING_SONNET`                         | 设置为 `1` 以禁用 Sonnet 模型的 prompt caching                                                                                                                                                                                                                                                                                                  |
| `DISABLE_TELEMETRY`                                     | 设置为 `1` 以选择退出遥测。遥测事件不包括用户数据，如代码、文件路径或 bash 命令。也禁用功能标志，因此仍在推出的某些功能可能不可用                                                                                                                                                                                                                                                                 |
| `DISABLE_UPDATES`                                       | 设置为 `1` 以阻止所有更新，包括手动 `claude update` 和 `claude install`。比 `DISABLE_AUTOUPDATER` 更严格。当通过您自己的渠道分发 Claude Code 且用户不应自行更新时使用                                                                                                                                                                                                               |
| `DISABLE_UPGRADE_COMMAND`                               | 设置为 `1` 以隐藏 `/upgrade` 命令                                                                                                                                                                                                                                                                                                              |
| `DO_NOT_TRACK`                                          | 设置为 `1` 以选择退出遥测。等同于设置 `DISABLE_TELEMETRY`。作为[标准跨工具约定](https://consoledonottrack.com/)被遵守                                                                                                                                                                                                                                               |
| `ENABLE_CLAUDEAI_MCP_SERVERS`                           | 设置为 `false` 以禁用 Claude Code 中的 [claude.ai MCP servers](/zh-CN/mcp#use-mcp-servers-from-claude-ai)。对于已登录的用户默认启用                                                                                                                                                                                                                         |
| `ENABLE_PROMPT_CACHING_1H`                              | 设置为 `1` 以请求 1 小时的 prompt cache TTL 而不是默认的 5 分钟。适用于 API 密钥、[Bedrock](/zh-CN/amazon-bedrock)、[Vertex](/zh-CN/google-vertex-ai)、[Foundry](/zh-CN/microsoft-foundry) 和 [Claude Platform on AWS](/zh-CN/claude-platform-on-aws) 用户。订阅用户自动获得 1 小时 TTL。1 小时缓存写入按更高费率计费                                                                        |
| `ENABLE_PROMPT_CACHING_1H_BEDROCK`                      | 已弃用。改用 `ENABLE_PROMPT_CACHING_1H`                                                                                                                                                                                                                                                                                                      |
| `ENABLE_TOOL_SEARCH`                                    | 控制 [MCP 工具搜索](/zh-CN/mcp#scale-with-mcp-tool-search)。未设置：默认延迟所有 MCP 工具，但在 Vertex AI 上或当 `ANTHROPIC_BASE_URL` 指向非第一方主机时提前加载。值：`true`（始终延迟并发送 beta 标头，在 Vertex AI 或不支持 `tool_reference` 的代理上请求失败）、`auto`（阈值模式：如果工具适合在上下文的 10% 内则提前加载）、`auto:N`（自定义阈值，例如 `auto:5` 表示 5%）、`false`（提前加载所有）                                                  |
| `FALLBACK_FOR_ALL_PRIMARY_MODELS`                       | 设置为任何非空值以在任何主模型上重复过载错误后触发回退到 [`--fallback-model`](/zh-CN/cli-reference#cli-flags)。默认情况下，仅 Opus 模型触发回退                                                                                                                                                                                                                                  |
| `FORCE_AUTOUPDATE_PLUGINS`                              | 设置为 `1` 以强制插件自动更新，即使主自动更新程序通过 `DISABLE_AUTOUPDATER` 禁用                                                                                                                                                                                                                                                                                 |
| `FORCE_PROMPT_CACHING_5M`                               | 设置为 `1` 以强制 5 分钟的 prompt cache TTL，即使 1 小时 TTL 会以其他方式应用。覆盖 `ENABLE_PROMPT_CACHING_1H`                                                                                                                                                                                                                                                  |
| `HTTP_PROXY`                                            | 为网络连接指定 HTTP 代理服务器                                                                                                                                                                                                                                                                                                                     |
| `HTTPS_PROXY`                                           | 为网络连接指定 HTTPS 代理服务器                                                                                                                                                                                                                                                                                                                    |
| `IS_DEMO`                                               | 设置为 `1` 以启用演示模式：隐藏标头中的电子邮件和组织名称以及 `/status` 输出，并跳过入门。对于流式传输或录制会话很有用                                                                                                                                                                                                                                                                    |
| `MAX_MCP_OUTPUT_TOKENS`                                 | MCP 工具响应中允许的最大令牌数。Claude Code 在输出超过 10,000 个令牌时显示警告。声明 [`anthropic/maxResultSizeChars`](/zh-CN/mcp#raise-the-limit-for-a-specific-tool) 的工具对文本内容使用该字符限制，但来自这些工具的图像内容仍受此变量约束（默认值：25000）                                                                                                                                                 |
| `MAX_STRUCTURED_OUTPUT_RETRIES`                         | 当模型的响应无法针对非交互模式（`-p` 标志）中的 [`--json-schema`](/zh-CN/cli-reference#cli-flags) 进行验证时重试的次数。默认为 5                                                                                                                                                                                                                                          |
| `MAX_THINKING_TOKENS`                                   | 覆盖[扩展思考](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)令牌预算。上限是模型的[最大输出令牌](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison)减一。设置为 `0` 以完全禁用思考。在具有[自适应推理](/zh-CN/model-config#adjust-effort-level)的模型上，除非通过 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` 禁用自适应推理，否则预算被忽略 |
| `MCP_CLIENT_SECRET`                                     | 需要[预配置凭证](/zh-CN/mcp#use-pre-configured-oauth-credentials)的 MCP 服务器的 OAuth 客户端密钥。在使用 `--client-secret` 添加服务器时避免交互式提示                                                                                                                                                                                                                   |
| `MCP_CONNECTION_NONBLOCKING`                            | 设置为 `true` 在非交互模式（`-p`）中完全跳过 MCP 连接等待。对于不需要 MCP 工具的脚本化管道很有用。没有此变量，第一个查询会等待最多 5 秒以获得 `--mcp-config` 服务器连接。服务器配置为 [`alwaysLoad: true`](/zh-CN/mcp#exempt-a-server-from-deferral) 始终阻止启动，无论此变量如何，因为它们的工具必须在构建第一个提示时存在                                                                                                                     |
| `MCP_CONNECT_TIMEOUT_MS`                                | 第一个查询等待 MCP 连接批处理的时间（以毫秒为单位），然后快照工具列表（默认值：5000）。在截止时间处仍待处理的服务器继续在后台连接，但在下一个查询之前不会出现。与 `MCP_TIMEOUT` 不同，后者限制单个服务器的连接尝试。最相关的是需要慢速连接服务器可见的非交互式会话，这些会话发出单个查询                                                                                                                                                                               |
| `MCP_OAUTH_CALLBACK_PORT`                               | OAuth 重定向回调的固定端口，作为在使用[预配置凭证](/zh-CN/mcp#use-pre-configured-oauth-credentials)添加 MCP 服务器时 `--callback-port` 的替代方案                                                                                                                                                                                                                      |
| `MCP_REMOTE_SERVER_CONNECTION_BATCH_SIZE`               | 启动期间并行连接的远程 MCP 服务器（HTTP/SSE）的最大数量（默认值：20）                                                                                                                                                                                                                                                                                             |
| `MCP_SERVER_CONNECTION_BATCH_SIZE`                      | 启动期间并行连接的本地 MCP 服务器（stdio）的最大数量（默认值：3）                                                                                                                                                                                                                                                                                                 |
| `MCP_TIMEOUT`                                           | MCP 服务器启动的超时（以毫秒为单位）（默认值：30000，或 30 秒）                                                                                                                                                                                                                                                                                                 |
| `MCP_TOOL_TIMEOUT`                                      | MCP 工具执行的超时（以毫秒为单位）（默认值：100000000，约 28 小时）                                                                                                                                                                                                                                                                                             |
| `NO_PROXY`                                              | 域和 IP 列表，对其的请求将直接发出，绕过代理                                                                                                                                                                                                                                                                                                               |
| `OTEL_LOG_RAW_API_BODIES`                               | 设置为 `1` 以将完整的 Anthropic Messages API 请求和响应 JSON 作为 `api_request_body` / `api_response_body` 日志事件发出，或 `file:<dir>` 以将未截断的主体写入磁盘并发出 `body_ref` 路径。默认禁用；主体包括整个对话历史。请参阅[监控](/zh-CN/monitoring-usage#api-request-body-event)                                                                                                                |
| `OTEL_LOG_TOOL_CONTENT`                                 | 设置为 `1` 以在 OpenTelemetry span 事件中包含工具输入和输出内容。默认禁用以保护敏感数据。请参阅[监控](/zh-CN/monitoring-usage)                                                                                                                                                                                                                                              |
| `OTEL_LOG_TOOL_DETAILS`                                 | 设置为 `1` 以在 OpenTelemetry 跟踪和日志中包含工具输入参数、MCP 服务器名称、工具失败时的原始错误字符串和其他工具详情。默认禁用以保护 PII。请参阅[监控](/zh-CN/monitoring-usage)                                                                                                                                                                                                                    |
| `OTEL_LOG_USER_PROMPTS`                                 | 设置为 `1` 以在 OpenTelemetry 跟踪和日志中包含用户提示文本。默认禁用（提示被编辑）。请参阅[监控](/zh-CN/monitoring-usage)                                                                                                                                                                                                                                                   |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID`                     | 设置为 `false` 以从指标属性中排除帐户 UUID（默认值：包含）。请参阅[监控](/zh-CN/monitoring-usage)                                                                                                                                                                                                                                                                  |
| `OTEL_METRICS_INCLUDE_SESSION_ID`                       | 设置为 `false` 以从指标属性中排除会话 ID（默认值：包含）。请参阅[监控](/zh-CN/monitoring-usage)                                                                                                                                                                                                                                                                    |
| `OTEL_METRICS_INCLUDE_VERSION`                          | 设置为 `true` 以在指标属性中包含 Claude Code 版本（默认值：排除）。请参阅[监控](/zh-CN/monitoring-usage)                                                                                                                                                                                                                                                           |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET`                        | 覆盖显示给 [Skill tool](/zh-CN/skills#control-who-invokes-a-skill) 的 skill 元数据的字符预算。预算在上下文窗口的 1% 处动态扩展，回退为 8,000 个字符。为了向后兼容而保留的旧名称                                                                                                                                                                                                          |
| `TASK_MAX_OUTPUT_LENGTH`                                | [subagent](/zh-CN/sub-agents) 输出中的最大字符数，超过此数字后将进行截断（默认值：32000，最大值：160000）。截断时，完整输出保存到磁盘，路径包含在截断的响应中                                                                                                                                                                                                                                    |
| `USE_BUILTIN_RIPGREP`                                   | 设置为 `0` 以使用系统安装的 `rg` 而不是 Claude Code 附带的 `rg`                                                                                                                                                                                                                                                                                         |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU`                        | 使用 Vertex AI 时覆盖 Claude 3.5 Haiku 的区域                                                                                                                                                                                                                                                                                                  |
| `VERTEX_REGION_CLAUDE_3_5_SONNET`                       | 使用 Vertex AI 时覆盖 Claude 3.5 Sonnet 的区域                                                                                                                                                                                                                                                                                                 |
| `VERTEX_REGION_CLAUDE_3_7_SONNET`                       | 使用 Vertex AI 时覆盖 Claude 3.7 Sonnet 的区域                                                                                                                                                                                                                                                                                                 |
| `VERTEX_REGION_CLAUDE_4_0_OPUS`                         | 使用 Vertex AI 时覆盖 Claude 4.0 Opus 的区域                                                                                                                                                                                                                                                                                                   |
| `VERTEX_REGION_CLAUDE_4_0_SONNET`                       | 使用 Vertex AI 时覆盖 Claude 4.0 Sonnet 的区域                                                                                                                                                                                                                                                                                                 |
| `VERTEX_REGION_CLAUDE_4_1_OPUS`                         | 使用 Vertex AI 时覆盖 Claude 4.1 Opus 的区域                                                                                                                                                                                                                                                                                                   |
| `VERTEX_REGION_CLAUDE_4_5_OPUS`                         | 使用 Vertex AI 时覆盖 Claude Opus 4.5 的区域                                                                                                                                                                                                                                                                                                   |
| `VERTEX_REGION_CLAUDE_4_5_SONNET`                       | 使用 Vertex AI 时覆盖 Claude Sonnet 4.5 的区域                                                                                                                                                                                                                                                                                                 |
| `VERTEX_REGION_CLAUDE_4_6_OPUS`                         | 使用 Vertex AI 时覆盖 Claude Opus 4.6 的区域                                                                                                                                                                                                                                                                                                   |
| `VERTEX_REGION_CLAUDE_4_6_SONNET`                       | 使用 Vertex AI 时覆盖 Claude Sonnet 4.6 的区域                                                                                                                                                                                                                                                                                                 |
| `VERTEX_REGION_CLAUDE_4_7_OPUS`                         | 使用 Vertex AI 时覆盖 Claude Opus 4.7 的区域                                                                                                                                                                                                                                                                                                   |
| `VERTEX_REGION_CLAUDE_HAIKU_4_5`                        | 使用 Vertex AI 时覆盖 Claude Haiku 4.5 的区域                                                                                                                                                                                                                                                                                                  |

标准 OpenTelemetry 导出器变量（`OTEL_METRICS_EXPORTER`、`OTEL_LOGS_EXPORTER`、`OTEL_EXPORTER_OTLP_ENDPOINT`、`OTEL_EXPORTER_OTLP_PROTOCOL`、`OTEL_EXPORTER_OTLP_HEADERS`、`OTEL_METRIC_EXPORT_INTERVAL`、`OTEL_RESOURCE_ATTRIBUTES` 和信号特定变体）也受支持。请参阅[监控](/zh-CN/monitoring-usage)了解配置详情。

## 另请参阅

* [设置](/zh-CN/settings)：在 `settings.json` 中配置环境变量，使其应用于每个会话
* [CLI 参考](/zh-CN/cli-reference)：启动时标志
* [网络配置](/zh-CN/network-config)：代理和 TLS 设置
* [监控](/zh-CN/monitoring-usage)：OpenTelemetry 配置

> ## Documentation Index
>
> Fetch the complete documentation index at: <https://code.claude.com/docs/llms.txt>
> Use this file to discover all available pages before exploring further.

# 工具参考

> Claude Code 可以使用的工具的完整参考，包括权限要求和每个工具的行为。

Claude Code 可以访问一组内置工具，帮助它理解和修改您的代码库。工具名称是您在[权限规则](/zh-CN/permissions#tool-specific-permission-rules)、[subagent 工具列表](/zh-CN/sub-agents)和 [hook 匹配器](/zh-CN/hooks)中使用的确切字符串。要完全禁用某个工具，请将其名称添加到[权限设置](/zh-CN/permissions#tool-specific-permission-rules)中的 `deny` 数组。

要添加自定义工具，请连接一个 [MCP server](/zh-CN/mcp)。要使用可重用的基于提示的工作流扩展 Claude，请编写一个 [skill](/zh-CN/skills)，它通过现有的 `Skill` 工具运行，而不是添加新的工具条目。

| 工具                     | 描述                                                                                                                                                                                                                                                                                           | 需要权限 |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--- |
| `Agent`                | 生成一个具有自己 context window 的 [subagent](/zh-CN/sub-agents)，用于处理任务。请参阅 [Agent 工具行为](#agent-tool-behavior)                                                                                                                                                                                        | 否    |
| `AskUserQuestion`      | 提出多选问题以收集需求或澄清歧义                                                                                                                                                                                                                                                                             | 否    |
| `Bash`                 | 在您的环境中执行 shell 命令。请参阅 [Bash 工具行为](#bash-tool-behavior)                                                                                                                                                                                                                                       | 是    |
| `CronCreate`           | 在当前会话中安排定期或一次性提示。任务是会话范围的，在 `--resume` 或 `--continue` 时如果未过期则会恢复。请参阅[计划任务](/zh-CN/scheduled-tasks)                                                                                                                                                                                           | 否    |
| `CronDelete`           | 按 ID 取消计划任务                                                                                                                                                                                                                                                                                  | 否    |
| `CronList`             | 列出会话中的所有计划任务                                                                                                                                                                                                                                                                                 | 否    |
| `Edit`                 | 对特定文件进行有针对性的编辑。请参阅 [Edit 工具行为](#edit-tool-behavior)                                                                                                                                                                                                                                          | 是    |
| `EnterPlanMode`        | 切换到 Plan Mode 以在编码前设计方法                                                                                                                                                                                                                                                                      | 否    |
| `EnterWorktree`        | 创建一个隔离的 [git worktree](/zh-CN/worktrees) 并切换到它。传递 `path` 以切换到当前存储库的现有 worktree，而不是创建新的。不适用于 subagents                                                                                                                                                                                        | 否    |
| `ExitPlanMode`         | 提出计划以供批准并退出 Plan Mode                                                                                                                                                                                                                                                                        | 是    |
| `ExitWorktree`         | 退出 worktree 会话并返回到原始目录。不适用于 subagents                                                                                                                                                                                                                                                        | 否    |
| `Glob`                 | 基于模式匹配查找文件。请参阅 [Glob 工具行为](#glob-tool-behavior)                                                                                                                                                                                                                                              | 否    |
| `Grep`                 | 在文件内容中搜索模式。请参阅 [Grep 工具行为](#grep-tool-behavior)                                                                                                                                                                                                                                              | 否    |
| `ListMcpResourcesTool` | 列出连接的 [MCP servers](/zh-CN/mcp) 公开的资源                                                                                                                                                                                                                                                        | 否    |
| `LSP`                  | 通过语言服务器进行代码智能：跳转到定义、查找引用、报告类型错误和警告。请参阅 [LSP 工具行为](#lsp-tool-behavior)                                                                                                                                                                                                                        | 否    |
| `Monitor`              | 在后台运行命令并将每个输出行反馈给 Claude，以便它可以对日志条目、文件更改或轮询状态做出反应。请参阅 [Monitor 工具](#monitor-tool)                                                                                                                                                                                                            | 是    |
| `NotebookEdit`         | 修改 Jupyter notebook 单元格。请参阅 [NotebookEdit 工具行为](#notebookedit-tool-behavior)                                                                                                                                                                                                                 | 是    |
| `PowerShell`           | 本地执行 PowerShell 命令。请参阅 [PowerShell 工具](#powershell-tool)了解可用性                                                                                                                                                                                                                                | 是    |
| `PushNotification`     | 发送桌面通知，以及当 [Remote Control](/zh-CN/remote-control) 已连接时发送手机推送，以便长时间运行的任务或[计划任务](/zh-CN/scheduled-tasks)可以在您离开时联系您。{/*plan-availability: feature=push-notifications providers=anthropic*/}推送传递通过 Anthropic 托管的基础设施运行，该基础设施无法从 Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry 访问        | 否    |
| `Read`                 | 读取文件内容。请参阅 [Read 工具行为](#read-tool-behavior)                                                                                                                                                                                                                                                  | 否    |
| `ReadMcpResourceTool`  | 按 URI 读取特定 MCP 资源                                                                                                                                                                                                                                                                            | 否    |
| `RemoteTrigger`        | 在 claude.ai 上创建、更新、运行和列出 [Routines](/zh-CN/routines)。支持 `/schedule` 命令。{/*plan-availability: feature=routines plans=pro,max,team,enterprise providers=anthropic*/}Routines 存在于 claude.ai 上，需要 Pro、Max、Team 或 Enterprise 计划，因此此工具无法从 Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry 访问 | 否    |
| `SendMessage`          | 向 [agent team](/zh-CN/agent-teams) 队友发送消息，或按 agent ID [恢复 subagent](/zh-CN/sub-agents#resume-subagents)。已停止的 subagents 在后台自动恢复。仅当设置了 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 时可用                                                                                                            | 否    |
| `ShareOnboardingGuide` | {/*plan-availability: feature=onboarding-guide-share plans=pro,max,team,enterprise providers=anthropic*/}上传 `ONBOARDING.md` 并返回队友可以在 Claude Code 中打开的共享链接。在编写指南后从 `/team-onboarding` 调用。适用于 Pro、Max、Team 和 Enterprise 计划上的 claude.ai 订阅者                                                   | 是    |
| `Skill`                | 在主对话中执行 [skill](/zh-CN/skills#control-who-invokes-a-skill)                                                                                                                                                                                                                                   | 是    |
| `TaskCreate`           | 在任务列表中创建新任务                                                                                                                                                                                                                                                                                  | 否    |
| `TaskGet`              | 检索特定任务的完整详细信息                                                                                                                                                                                                                                                                                | 否    |
| `TaskList`             | 列出所有任务及其当前状态                                                                                                                                                                                                                                                                                 | 否    |
| `TaskOutput`           | （已弃用）检索后台任务的输出。优先使用 `Read` 读取任务的输出文件路径                                                                                                                                                                                                                                                       | 否    |
| `TaskStop`             | 按 ID 终止运行中的后台任务                                                                                                                                                                                                                                                                              | 否    |
| `TaskUpdate`           | 更新任务状态、依赖项、详细信息或删除任务                                                                                                                                                                                                                                                                         | 否    |
| `TeamCreate`           | 创建一个具有多个队友的 [agent team](/zh-CN/agent-teams)。仅当设置了 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 时可用                                                                                                                                                                                              | 否    |
| `TeamDelete`           | 解散 agent team 并清理队友进程。仅当设置了 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 时可用                                                                                                                                                                                                                     | 否    |
| `TodoWrite`            | 管理会话任务清单。在非交互模式和 [Agent SDK](/zh-CN/headless) 中可用；交互式会话改用 TaskCreate、TaskGet、TaskList 和 TaskUpdate                                                                                                                                                                                           | 否    |
| `ToolSearch`           | 当启用 [tool search](/zh-CN/mcp#scale-with-mcp-tool-search) 时搜索并加载延迟工具                                                                                                                                                                                                                          | 否    |
| `WebFetch`             | 从指定 URL 获取内容。请参阅 [WebFetch 工具行为](#webfetch-tool-behavior)                                                                                                                                                                                                                                    | 是    |
| `WebSearch`            | 执行网络搜索。请参阅 [WebSearch 工具行为](#websearch-tool-behavior)                                                                                                                                                                                                                                        | 是    |
| `Write`                | 创建或覆盖文件。请参阅 [Write 工具行为](#write-tool-behavior)                                                                                                                                                                                                                                               | 是    |

## 使用权限规则和 hooks 配置工具

在大多数情况下，Claude 决定何时使用这些工具，您在与 Claude 交互时不需要自己命名它们。当定义权限和其他配置时，您直接引用工具名称：

* 在设置中的 [`permissions.allow` 和 `permissions.deny`](/zh-CN/settings#available-settings)，以及 `/permissions` 界面
* 在 [CLI 标志](/zh-CN/cli-reference)中的 `--allowedTools` 和 `--disallowedTools`
* 在 Agent SDK 的 [`allowedTools` 和 `disallowedTools`](/zh-CN/agent-sdk/permissions#allow-and-deny-rules) 选项中
* 在 [subagent 的 `tools` 或 `disallowedTools`](/zh-CN/sub-agents#supported-frontmatter-fields) frontmatter 中
* 在 [skill 的 `allowed-tools`](/zh-CN/skills#frontmatter-reference) frontmatter 中
* 在 hook 的 [`if` 条件](/zh-CN/hooks-guide#filter-by-tool-name-and-arguments-with-the-if-field)中

所有这些都接受相同的规则格式，`ToolName(specifier)`。specifier 取决于工具，几个工具共享一种格式：

| 规则格式                           | 适用于                     | 详情                                                         |
| :----------------------------- | :---------------------- | :--------------------------------------------------------- |
| `Bash(npm run *)`              | Bash、Monitor            | [命令模式匹配](/zh-CN/permissions#bash)                          |
| `PowerShell(Get-ChildItem *)`  | PowerShell              | [命令模式匹配](/zh-CN/permissions#powershell)                    |
| `Read(~/secrets/**)`           | Read、Grep、Glob、LSP      | [路径模式匹配](/zh-CN/permissions#read-and-edit)                 |
| `Edit(/src/**)`                | Edit、Write、NotebookEdit | [路径模式匹配](/zh-CN/permissions#read-and-edit)                 |
| `Skill(deploy *)`              | Skill                   | [Skill 名称匹配](/zh-CN/skills#restrict-claude's-skill-access) |
| `Agent(Explore)`               | Agent                   | [Subagent 类型匹配](/zh-CN/permissions#agent-subagents)        |
| `WebFetch(domain:example.com)` | WebFetch                | [域名匹配](/zh-CN/permissions#webfetch)                        |
| `WebSearch`                    | WebSearch               | 无 specifier；允许或拒绝整个工具                                      |

此处未列出的工具，例如 `ExitPlanMode` 或 `ShareOnboardingGuide`，仅接受不带 specifier 的裸工具名称。

`Edit(...)` 允许规则也授予对相同路径的读取访问权限，因此您不需要匹配的 `Read(...)` 规则。

Hook `matcher` 字段使用裸工具名称，而不是带括号的规则格式。请参阅[匹配器模式](/zh-CN/hooks#matcher-patterns)了解匹配规则。对于每个工具在 hooks 中传递给 `tool_input` 的字段名称，请参阅 [PreToolUse 输入参考](/zh-CN/hooks#pretooluse-input)。

## Agent 工具行为

Agent 工具在单独的 context window 中生成一个 subagent。subagent 自主地完成其任务，然后向父对话返回单个文本结果。父对话看不到 subagent 的中间工具调用或输出，只看到最终结果。要限制 subagent 运行的轮数，请在 [subagent 定义](/zh-CN/sub-agents#supported-frontmatter-fields)中设置 `maxTurns`。

同一个 Agent 工具也在启用 fork 模式时启动[分叉 subagents](/zh-CN/sub-agents#fork-the-current-conversation)。fork 继承完整的父对话，而不是从头开始，始终在后台运行，并且仍然在您的终端中显示权限提示。本节的其余部分描述命名的 subagents。

命名的 subagent 可以使用哪些工具取决于 [subagent 定义](/zh-CN/sub-agents)中的 `tools` 和 `disallowedTools` 字段：

* **两个字段都未设置**：subagent 继承父对话可用的每个工具。
* **仅设置 `tools`**：subagent 仅获得列出的工具。
* **仅设置 `disallowedTools`**：subagent 获得除列出的工具外的每个父工具。
* **两个都设置**：`disallowedTools` 优先。同时列在两个中的工具会被移除。

启动 subagent 本身不会提示权限。subagent 自己的工具调用在运行时根据您的权限规则进行检查：

* **前台 subagents** 显示您在主对话中会看到的相同权限提示，在每个工具调用发生时。
* **后台 subagents** 不显示提示。它们使用会话中已授予的权限运行，并自动拒绝任何会提示的工具调用。拒绝后，subagent 继续运行而不使用该工具。

要首先限制 subagent 可以访问的内容，请缩小其 `tools` 字段，将 Bash 排除在列表之外，或在设置中设置拒绝规则，如[控制 subagent 功能](/zh-CN/sub-agents#control-subagent-capabilities)中所述。有关选择前台或后台的更多信息，请参阅[在前台或后台运行 subagents](/zh-CN/sub-agents#run-subagents-in-foreground-or-background)。

## Bash 工具行为

Bash 工具在单独的进程中运行每个命令，具有以下持久性行为：

* 当 Claude 在主会话中运行 `cd` 时，只要它保持在项目目录内或您使用 `--add-dir`、`/add-dir` 或设置中的 `additionalDirectories` 添加的[额外工作目录](/zh-CN/permissions#working-directories)内，新的工作目录就会延续到后续的 Bash 命令。Subagent 会话永远不会延续工作目录更改。
  * 如果 `cd` 落在这些目录之外，Claude Code 会重置为项目目录，并将 `Shell cwd was reset to <dir>` 附加到工具结果。
  * 要禁用此延续，使每个 Bash 命令都在项目目录中启动，请设置 `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1`。
* 环境变量不持久。一个命令中的 `export` 在下一个命令中将不可用。

在启动 Claude Code 之前激活您的 virtualenv 或 conda 环境。要使环境变量在 Bash 命令之间保持不变，请在启动 Claude Code 之前将 [`CLAUDE_ENV_FILE`](/zh-CN/env-vars) 设置为 shell 脚本，或使用 [SessionStart hook](/zh-CN/hooks#persist-environment-variables) 动态填充它。

两个限制限制每个命令：

* **超时**：默认为两分钟。Claude 可以使用 `timeout` 参数请求每个命令最多 10 分钟。使用 [`BASH_DEFAULT_TIMEOUT_MS` 和 `BASH_MAX_TIMEOUT_MS`](/zh-CN/env-vars) 覆盖默认值和上限。
* **输出长度**：默认为 30,000 个字符。当命令产生超过该数量的输出时，Claude Code 将完整输出保存到会话目录中的文件，并给 Claude 文件路径加上开头的简短预览。Claude 在需要其余部分时读取或搜索该文件。使用 [`BASH_MAX_OUTPUT_LENGTH`](/zh-CN/env-vars) 提高限制，最高为 150,000 个字符的硬上限。

对于长时间运行的进程，例如开发服务器或监视构建，Claude 可以设置 `run_in_background: true` 以将命令作为后台任务启动并在其运行时继续工作。使用 `/tasks` 列出和停止后台任务。

## Edit 工具行为

Edit 工具执行精确的字符串替换。它接受 `old_string` 和 `new_string` 并用后者替换前者。它不使用正则表达式或模糊匹配。

三个检查必须通过才能应用编辑：

* **编辑前读取**：Claude 必须在当前对话中读取过该文件，并且该文件在该读取后不能在磁盘上更改。此检查首先运行，在任何字符串匹配之前。
* **匹配**：`old_string` 必须在文件中完全按照编写的方式出现。单个空格或缩进差异足以导致不匹配。
* **唯一性**：`old_string` 必须恰好出现一次。当它出现多次时，Claude 要么提供一个更长的字符串，其中包含足够的周围上下文来确定一个出现，要么设置 `replace_all: true` 来替换所有出现。

使用 Bash 查看文件也满足读取前编辑要求，当命令是 `cat path/to/file` 或 `sed -n 'X,Yp' path/to/file` 在单个文件上，没有管道或重定向时。其他 Bash 命令，例如 `head`、`tail` 或管道输出不计数，Claude 在这些情况下必须在编辑前使用 Read。

这仅影响编辑资格，不影响权限。[Read 和 Edit 拒绝规则](/zh-CN/permissions#tool-specific-permission-rules)也适用于 Claude Code 在 Bash 中识别的文件命令，例如 `cat`、`head`、`tail` 和 `sed`，但不适用于间接读取或写入文件的任意子进程，例如自己打开文件的 Python 或 Node 脚本。对于覆盖每个进程的操作系统级别强制，请[启用沙箱](/zh-CN/sandboxing)。

## Glob 工具行为

Glob 工具按名称模式查找文件。它支持标准 glob 语法，包括 `**` 用于递归目录匹配：

* `**/*.js` 匹配任何深度的所有 `.js` 文件
* `src/**/*.ts` 匹配 `src/` 下的所有 `.ts` 文件
* `*.{json,yaml}` 匹配当前目录中的 `.json` 和 `.yaml` 文件

结果按修改时间排序，并限制为 100 个文件。如果达到上限，Claude 会在结果中看到截断标志，并可以缩小模式。

Glob 默认不尊重 `.gitignore`，因此它找到被 gitignore 的文件以及跟踪的文件。这与[Grep](#grep-tool-behavior) 不同，后者跳过被 gitignore 的文件。要使 Glob 尊重 `.gitignore`，请在启动 Claude Code 之前设置 `CLAUDE_CODE_GLOB_NO_IGNORE=false`。

## Grep 工具行为

Grep 工具在文件内容中搜索模式。[Glob](#glob-tool-behavior) 按名称查找文件，Grep 在文件内查找行。

Grep 基于 [ripgrep](https://github.com/BurntSushi/ripgrep) 并使用 ripgrep 的正则表达式语法，而不是 POSIX grep。包含正则表达式元字符的模式需要转义。例如，在 Go 代码中查找 `interface{}` 需要模式 `interface\{\}`。

三种输出模式控制返回的内容：

* `files_with_matches`：仅文件路径，无行内容。这是默认值。
* `content`：匹配的行及其文件和行号。
* `count`：每个文件的匹配计数。

Claude 可以使用 `glob` 参数（例如 `**/*.tsx`）按文件范围结果，或使用 `type` 参数（例如 `py` 或 `rust`）按语言范围结果。默认情况下，模式在单行内匹配。Claude 可以设置 `multiline: true` 以跨行边界匹配。

Grep 尊重 `.gitignore`，因此被 gitignore 的文件会被跳过。要搜索被 gitignore 的文件，Claude 直接传递其路径。

## LSP 工具行为

LSP 工具为 Claude 提供来自运行中的语言服务器的代码智能。在每次文件编辑后，它会自动报告类型错误和警告，以便 Claude 可以在没有单独构建步骤的情况下修复问题。Claude 还可以直接调用它来导航代码：

* 跳转到符号的定义
* 查找对符号的所有引用
* 获取位置处的类型信息
* 列出文件或工作区中的符号
* 查找接口的实现
* 追踪调用层次结构

该工具在您为您的语言安装 [code intelligence plugin](/zh-CN/discover-plugins#code-intelligence) 之前处于非活动状态。该插件捆绑了语言服务器配置，您需要单独安装服务器二进制文件。

## Monitor 工具

<Note>
  Monitor 工具需要 Claude Code v2.1.98 或更高版本。
</Note>

Monitor 工具让 Claude 在后台监视某些内容，并在其更改时做出反应，而无需暂停对话。要求 Claude：

* 跟踪日志文件并在错误出现时标记它们
* 轮询 PR 或 CI 作业并在其状态更改时报告
* 监视目录以查找文件更改
* 跟踪您指向的任何长时间运行脚本的输出

Claude 为监视编写一个小脚本，在后台运行它，并在每行到达时接收它。您可以在同一会话中继续工作，Claude 在事件到达时插入。通过要求 Claude 取消它或结束会话来停止监视。

Monitor 使用与 [Bash 相同的权限规则](/zh-CN/permissions#tool-specific-permission-rules)，因此您为 Bash 设置的 `allow` 和 `deny` 模式也适用于此处。它在 Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry 上不可用。当设置了 `DISABLE_TELEMETRY` 或 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 时，它也不可用。

插件可以声明在插件处于活动状态时自动启动的监视，而不是要求 Claude 启动它们。请参阅 [plugin monitors](/zh-CN/plugins-reference#monitors)。

## NotebookEdit 工具行为

NotebookEdit 一次修改一个 Jupyter notebook 单元格，按其 `cell_id` 定位单元格。它不像 [Edit](#edit-tool-behavior) 在纯文本文件上那样在整个 notebook 中执行字符串替换。

三种编辑模式控制目标单元格发生的情况：

* `replace`：覆盖单元格的源。这是默认值。
* `insert`：在目标后添加新单元格。没有 `cell_id` 时，新单元格位于 notebook 的开始。需要 `cell_type` 设置为 `code` 或 `markdown`。
* `delete`：删除目标单元格。

权限规则使用 `Edit(...)` 路径格式。像 `Edit(notebooks/**)` 这样的规则涵盖该目录中的 NotebookEdit 调用。

## PowerShell 工具

PowerShell 工具让 Claude 本地运行 PowerShell 命令。在 Windows 上，这意味着命令在 PowerShell 中运行，而不是通过 Git Bash 路由。在没有 Git Bash 的 Windows 上，该工具会自动启用。在安装了 Git Bash 的 Windows 上，该工具正在逐步推出。在 Linux、macOS 和 WSL 上，该工具是选择加入的。

### 启用 PowerShell 工具

在您的环境或 `settings.json` 中设置 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`：

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_USE_POWERSHELL_TOOL": "1"
  }
}
```

在 Windows 上，将变量设置为 `0` 以选择退出推出。在 Linux、macOS 和 WSL 上，该工具需要 PowerShell 7 或更高版本：安装 `pwsh` 并确保它在您的 `PATH` 中。

在 Windows 上，Claude Code 自动检测 `pwsh.exe`（PowerShell 7+），回退到 `powershell.exe`（PowerShell 5.1）。启用该工具后，Claude 将 PowerShell 视为主 shell。当安装了 Git Bash 时，Bash 工具仍可用于 POSIX 脚本。

### 设置、hooks 和 skills 中的 shell 选择

三个额外的设置控制 PowerShell 的使用位置：

* [`settings.json`](/zh-CN/settings#available-settings) 中的 `"defaultShell": "powershell"`：通过 PowerShell 路由交互式 `!` 命令。需要启用 PowerShell 工具。
* 单个 [command hooks](/zh-CN/hooks#command-hook-fields) 上的 `"shell": "powershell"`：在 PowerShell 中运行该 hook。Hooks 直接生成 PowerShell，因此无论 `CLAUDE_CODE_USE_POWERSHELL_TOOL` 如何，这都有效。
* [skill frontmatter](/zh-CN/skills#frontmatter-reference) 中的 `shell: powershell`：在 PowerShell 中运行 `` !`command` `` 块。需要启用 PowerShell 工具。

同样的主会话工作目录重置行为（如 Bash 工具部分所述）适用于 PowerShell 命令，包括 `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` 环境变量。

### 预览限制

PowerShell 工具在预览期间有以下已知限制：

* PowerShell 配置文件未加载
* 在 Windows 上，不支持 sandboxing

## Read 工具行为

Read 工具接受文件路径并返回带有行号的内容。Claude 被指示始终传递绝对路径。

默认情况下，Read 从开始返回文件。超过大小阈值的文件返回错误而不是部分内容，提示 Claude 使用 `offset` 和 `limit` 重试以读取特定范围。

Read 处理纯文本之外的几种文件类型：

* **图像**：PNG、JPG 和其他图像格式作为 Claude 可以看到的视觉内容返回，而不是原始字节。Claude Code 在发送前调整大小并重新压缩大图像以适应模型的图像大小限制，因此 Claude 可能会看到大截图的缩小版本。如果 Claude 在大图像中遗漏了细微的像素级细节，请要求它首先裁剪感兴趣的区域，例如使用 ImageMagick 通过 Bash。
* **PDFs**：Claude 完整读取短 `.pdf` 文件。对于超过 10 页的 PDFs，它使用 `pages` 参数（例如 `"1-5"`）按范围读取，一次最多 20 页。
* **Jupyter notebooks**：`.ipynb` 文件返回所有单元格及其输出，包括代码、markdown 和可视化。

Read 仅读取文件，不读取目录。Claude 使用通过 Bash 工具的 `ls` 列出目录内容。

## WebFetch 工具行为

WebFetch 接受 URL 和描述要提取内容的提示。它获取页面，当服务器返回 HTML 时将响应转换为 Markdown，并使用小型快速模型针对内容运行提示。对于大多数获取，Claude 接收该模型的答案，而不是原始页面。转换步骤不可配置。

这使 WebFetch 在设计上是有损的。提取提示确定到达 Claude 的内容，因此说页面不提及某内容的结果可能只意味着提示没有询问它。要求 Claude 使用更具体的提示再次获取，或通过 Bash 使用 `curl` 获取未处理的页面。

几种行为塑造 Claude 接收的响应：

* HTTP URLs 自动升级到 HTTPS。
* 大页面在处理前被截断到固定字符限制。
* 响应缓存 15 分钟，因此相同 URL 的重复获取快速返回。
* 当 URL 重定向到不同的主机时，WebFetch 返回一个文本结果，命名原始 URL 和重定向目标，而不是跟随它。Claude 然后使用第二个 WebFetch 调用获取新 URL。

在默认和 `acceptEdits` 权限模式中，WebFetch 在首次到达新域时提示。要提前允许域而不提示，请添加像 `WebFetch(domain:example.com)` 这样的权限规则。`auto` 和 `bypassPermissions` [权限模式](/zh-CN/permissions#permission-modes)完全跳过提示。

WebFetch 设置以 `Claude-User` 开头的 `User-Agent` 标头，以及优先 Markdown 而不是 HTML 的 `Accept` 标头，以便支持内容协商的服务器可以直接返回 Markdown。[Sandbox](/zh-CN/sandboxing) 网络规则单独配置，因此您希望沙箱进程到达的域仍然需要显式沙箱权限规则。

## WebSearch 工具行为

WebSearch 针对 Anthropic 的[网络搜索](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)后端运行查询，并返回结果标题和 URLs。它不获取结果页面。要读取 Claude 在搜索结果中找到的页面，它使用 [WebFetch](#webfetch-tool-behavior) 进行后续操作。

该工具可能在返回结果之前发出最多八个后端搜索，在内部优化搜索。Claude 可以使用 `allowed_domains` 范围结果以仅包含某些主机，或使用 `blocked_domains` 排除它们。这两个列表不能在单个调用中组合。

搜索后端不可配置。要使用不同的提供商进行搜索，请添加一个 [MCP server](/zh-CN/mcp)，公开搜索工具。

WebSearch 权限规则不接受 specifier。`allow` 或 `deny` 中的裸 `WebSearch` 条目是唯一的形式。

<Note>
  WebSearch 在 Claude API 和 Microsoft Foundry 上可用。在 Google Cloud Vertex AI 上，它适用于 Claude 4 模型，包括 Opus、Sonnet 和 Haiku。Amazon Bedrock 不公开服务器端网络搜索工具。
</Note>

## Write 工具行为

Write 工具创建新文件或用提供的完整内容覆盖现有文件。它不追加或合并。

如果目标路径已存在，Claude 必须在当前对话中至少读取过该文件一次才能覆盖它。对未读现有文件的 Write 失败并出现错误。此约束不适用于新文件。

使用 Bash `cat` 或 `sed -n` 查看文件也满足此要求，如 [Edit 工具行为](#edit-tool-behavior)中所述。

对于现有文件的部分更改，Claude 使用 Edit 而不是 Write。

## 检查哪些工具可用

您的确切工具集取决于您的提供商、平台和设置。要检查在运行中的会话中加载了什么，请直接询问 Claude：

```text theme={null}
What tools do you have access to?
```

Claude 提供对话摘要。对于确切的 MCP 工具名称，请运行 `/mcp`。

## 另请参阅

* [MCP servers](/zh-CN/mcp)：通过连接外部服务器添加自定义工具
* [权限](/zh-CN/permissions)：权限系统、规则语法和工具特定模式
* [Subagents](/zh-CN/sub-agents)：为 subagents 配置工具访问
* [Hooks](/zh-CN/hooks-guide)：在工具执行前后运行自定义命令

> ## Documentation Index
>
> Fetch the complete documentation index at: <https://code.claude.com/docs/llms.txt>
> Use this file to discover all available pages before exploring further.

# 交互模式

> Claude Code 会话中键盘快捷键、输入模式和交互功能的完整参考。

## 键盘快捷键

<Note>
  键盘快捷键可能因平台和终端而异。在[全屏渲染](/zh-CN/fullscreen)中，在转录查看器中按 `?` 查看可用的快捷键。

  **macOS 用户**：Option/Alt 键快捷键（`Alt+B`、`Alt+F`、`Alt+Y`、`Alt+M`、`Alt+P`）需要在终端中将 Option 配置为 Meta：

* **iTerm2**：设置 → 配置文件 → 键 → 常规 → 将左/右 Option 键设置为"Esc+"
* **Apple Terminal**：设置 → 配置文件 → 键盘 → 勾选"使用 Option 作为 Meta 键"
* **VS Code**：在 VS Code 设置中设置 `"terminal.integrated.macOptionIsMeta": true`

  有关详细信息，请参阅[终端配置](/zh-CN/terminal-config)。
</Note>

### 常规控制

| 快捷键                                          | 描述                                                                                           | 上下文                                                                                                                                 |
| :------------------------------------------- | :------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+C`                                     | 取消当前输入或生成                                                                                    | 标准中断                                                                                                                                |
| `Ctrl+X Ctrl+K`                              | 终止此会话中所有运行的[后台子代理](/zh-CN/sub-agents#run-subagents-in-foreground-or-background)。在 3 秒内按两次以确认 | 子代理控制                                                                                                                               |
| `Ctrl+D`                                     | 退出 Claude Code 会话                                                                            | EOF 信号                                                                                                                              |
| `Ctrl+G` 或 `Ctrl+X Ctrl+E`                   | 在默认文本编辑器中打开                                                                                  | 在默认文本编辑器中编辑您的提示或自定义响应。`Ctrl+X Ctrl+E` 是 readline 原生绑定。在 `/config` 中打开"在外部编辑器中显示最后响应"以在您的提示上方将 Claude 的上一个回复作为 `#` 注释上下文预置；保存时会删除注释块 |
| `Ctrl+L`                                     | 重绘屏幕                                                                                         | 强制完整的终端重绘。输入和对话历史被保留。使用此功能可在显示变得混乱或部分空白时恢复                                                                                          |
| `Ctrl+O`                                     | 切换转录查看器                                                                                      | 显示详细的工具使用和执行情况。还会展开 MCP 调用，这些调用默认会折叠为单行，如"Called slack 3 times"                                                                     |
| `Ctrl+R`                                     | 反向搜索命令历史                                                                                     | 交互式搜索以前的命令                                                                                                                          |
| `Ctrl+V` 或 `Cmd+V`（iTerm2）或 `Alt+V`（Windows） | 从剪贴板粘贴图像                                                                                     | 在光标处插入 `[Image #N]` 芯片，以便您可以在提示中按位置引用它                                                                                              |
| `Ctrl+B`                                     | 后台运行任务                                                                                       | 后台运行 bash 命令和代理。Tmux 用户按两次                                                                                                          |
| `Ctrl+T`                                     | 切换任务列表                                                                                       | 在终端状态区域中显示或隐藏[任务列表](#task-list)                                                                                                     |
| `Left/Right arrows`                          | 在对话框选项卡之间循环                                                                                  | 在权限对话框和菜单中的选项卡之间导航                                                                                                                  |
| `Up/Down arrows` 或 `Ctrl+P`/`Ctrl+N`         | 移动光标或导航命令历史                                                                                  | 在多行输入中，首先在提示内移动光标。一旦光标已在顶部或底部边缘，再次按下会导航命令历史                                                                                         |
| `Esc`                                        | 中断 Claude                                                                                    | 停止当前响应或工具调用中途，以便您可以重定向。Claude 保留迄今为止完成的工作                                                                                           |
| `Esc` + `Esc`                                | 回退或总结                                                                                        | 将代码和/或对话恢复到上一个点，或从选定的消息进行总结                                                                                                         |
| `Shift+Tab` 或 `Alt+M`（某些配置）                  | 循环权限模式                                                                                       | 在 `default`、`acceptEdits`、`plan` 和您启用的任何模式（如 `auto` 或 `bypassPermissions`）之间循环。请参阅[权限模式](/zh-CN/permission-modes)。                  |
| `Option+P`（macOS）或 `Alt+P`（Windows/Linux）    | 切换模型                                                                                         | 在不清除提示的情况下切换模型                                                                                                                      |
| `Option+T`（macOS）或 `Alt+T`（Windows/Linux）    | 切换扩展思考                                                                                       | 启用或禁用扩展思考模式。{/*min-version: 2.1.132*/}从 v2.1.132 开始，此快捷键在 macOS 上无需配置 Option 作为 Meta 即可工作                                         |
| `Option+O`（macOS）或 `Alt+O`（Windows/Linux）    | 切换快速模式                                                                                       | 启用或禁用[快速模式](/zh-CN/fast-mode)                                                                                                       |

### 文本编辑

| 快捷键                    | 描述           | 上下文                                                                                           |
| :--------------------- | :----------- | :-------------------------------------------------------------------------------------------- |
| `Ctrl+A`               | 将光标移动到当前行的开始 | 在多行输入中，移动到当前逻辑行的开始                                                                            |
| `Ctrl+E`               | 将光标移动到当前行的末尾 | 在多行输入中，移动到当前逻辑行的末尾                                                                            |
| `Ctrl+K`               | 删除到行尾        | 存储已删除的文本以供粘贴                                                                                  |
| `Ctrl+U`               | 从光标删除到行首     | 存储已删除的文本以供粘贴。重复以清除多行输入中的多行。在 macOS 上，终端模拟器（包括 iTerm2 和 Terminal.app）将 `Cmd+Backspace` 映射到此快捷键 |
| `Ctrl+W`               | 删除上一个单词      | 存储已删除的文本以供粘贴。在 Windows 上，`Ctrl+Backspace` 也会删除上一个单词                                           |
| `Ctrl+Y`               | 粘贴已删除的文本     | 粘贴用 `Ctrl+K`、`Ctrl+U` 或 `Ctrl+W` 删除的文本                                                        |
| `Alt+Y`（在 `Ctrl+Y` 之后） | 循环粘贴历史       | 粘贴后，循环浏览以前删除的文本。在 macOS 上需要[将 Option 作为 Meta](#keyboard-shortcuts)                            |
| `Alt+B`                | 将光标向后移动一个单词  | 单词导航。在 macOS 上需要[将 Option 作为 Meta](#keyboard-shortcuts)                                       |
| `Alt+F`                | 将光标向前移动一个单词  | 单词导航。在 macOS 上需要[将 Option 作为 Meta](#keyboard-shortcuts)                                       |

### 主题和显示

| 快捷键      | 描述           | 上下文                                           |
| :------- | :----------- | :-------------------------------------------- |
| `Ctrl+T` | 切换代码块的语法突出显示 | 仅在 `/theme` 选择器菜单内工作。控制 Claude 响应中的代码是否使用语法着色 |

### 多行输入

| 方法          | 快捷键            | 上下文                                                                                          |
| :---------- | :------------- | :------------------------------------------------------------------------------------------- |
| 快速转义        | `\` + `Enter`  | 在所有终端中工作                                                                                     |
| Option 键    | `Option+Enter` | 在 macOS 上启用[将 Option 作为 Meta](/zh-CN/terminal-config#enable-option-key-shortcuts-on-macos) 后 |
| Shift+Enter | `Shift+Enter`  | 在 iTerm2、WezTerm、Ghostty、Kitty、Warp、Apple Terminal、Windows Terminal 中开箱即用                    |
| 控制序列        | `Ctrl+J`       | 在任何终端中工作，无需配置                                                                                |
| 粘贴模式        | 直接粘贴           | 对于代码块、日志                                                                                     |

<Tip>
  Shift+Enter 在 iTerm2、WezTerm、Ghostty、Kitty、Warp、Apple Terminal 和 Windows Terminal 中无需配置即可工作。对于 VS Code、Cursor、Windsurf、Alacritty 和 Zed，运行 `/terminal-setup` 以安装绑定。
</Tip>

### 快速命令

| 快捷键     | 描述        | 注释                                          |
| :------ | :-------- | :------------------------------------------ |
| `/` 在开始 | 命令或 skill | 请参阅[命令](#commands)和 [skills](/zh-CN/skills) |
| `!` 在开始 | Shell 模式  | 直接运行命令并将执行输出添加到会话                           |
| `@`     | 文件路径提及    | 触发文件路径自动完成                                  |

### 转录查看器

当转录查看器打开时（使用 `Ctrl+O` 切换），这些快捷键可用。在[全屏渲染](/zh-CN/fullscreen)中，按 `?` 显示查看器内的完整快捷键参考面板。`Ctrl+E` 可以通过 [`transcript:toggleShowAll`](/zh-CN/keybindings) 重新绑定。

| 快捷键                | 描述                                                                                                                |
| :----------------- | :---------------------------------------------------------------------------------------------------------------- |
| `?`                | 切换键盘快捷键帮助面板。需要[全屏渲染](/zh-CN/fullscreen)                                                                           |
| `{` / `}`          | 跳转到上一个或下一个用户提示，如 vim 段落运动。需要[全屏渲染](/zh-CN/fullscreen)                                                             |
| `Ctrl+E`           | 切换显示所有内容                                                                                                          |
| `[`                | 将完整对话写入终端的原生滚动缓冲区，以便 `Cmd+F`、tmux 复制模式和其他原生工具可以搜索它。需要[全屏渲染](/zh-CN/fullscreen#search-and-review-the-conversation) |
| `v`                | 将对话写入临时文件并在 `$VISUAL` 或 `$EDITOR` 中打开它。需要[全屏渲染](/zh-CN/fullscreen)                                                |
| `q`、`Ctrl+C`、`Esc` | 退出转录视图。所有三个都可以通过 [`transcript:exit`](/zh-CN/keybindings) 重新绑定                                                     |

### 语音输入

| 快捷键           | 描述   | 注释                                                                                                                         |
| :------------ | :--- | :------------------------------------------------------------------------------------------------------------------------- |
| 按住或点击 `Space` | 语音听写 | 需要启用[语音听写](/zh-CN/voice-dictation)。按住以录制，或运行 `/voice tap` 以进行点击切换。[可重新绑定](/zh-CN/voice-dictation#rebind-the-dictation-key) |

## 命令

在 Claude Code 中键入 `/` 以查看所有可用命令，或键入 `/` 后跟任何字母以进行筛选。`/` 菜单显示您可以调用的所有内容：内置命令、捆绑的和用户编写的 [skills](/zh-CN/skills)，以及由 [plugins](/zh-CN/plugins) 和 [MCP servers](/zh-CN/mcp#use-mcp-prompts-as-commands) 贡献的命令。并非所有内置命令对每个用户都可见，因为某些命令取决于您的平台或计划。

有关 Claude Code 中包含的命令的完整列表，请参阅[命令参考](/zh-CN/commands)。

## Vim 编辑器模式

通过 `/config` → 编辑器模式启用 vim 风格编辑。

### 模式切换

| 命令    | 操作           | 来自模式          |
| :---- | :----------- | :------------ |
| `Esc` | 进入 NORMAL 模式 | INSERT、VISUAL |
| `i`   | 在光标前插入       | NORMAL        |
| `I`   | 在行首插入        | NORMAL        |
| `a`   | 在光标后插入       | NORMAL        |
| `A`   | 在行尾插入        | NORMAL        |
| `o`   | 在下方打开行       | NORMAL        |
| `O`   | 在上方打开行       | NORMAL        |
| `v`   | 开始字符级可视选择    | NORMAL        |
| `V`   | 开始行级可视选择     | NORMAL        |

### 导航（NORMAL 模式）

| 命令              | 操作                  |
| :-------------- | :------------------ |
| `h`/`j`/`k`/`l` | 向左/向下/向上/向右移动       |
| `Space`         | 向右移动                |
| `w`             | 下一个单词               |
| `e`             | 单词末尾                |
| `b`             | 上一个单词               |
| `0`             | 行首                  |
| `$`             | 行尾                  |
| `^`             | 第一个非空白字符            |
| `gg`            | 输入开始                |
| `G`             | 输入结束                |
| `f{char}`       | 跳转到下一个字符出现处         |
| `F{char}`       | 跳转到上一个字符出现处         |
| `t{char}`       | 跳转到下一个字符出现处之前       |
| `T{char}`       | 跳转到上一个字符出现处之后       |
| `;`             | 重复最后一个 f/F/t/T 动作   |
| `,`             | 反向重复最后一个 f/F/t/T 动作 |

<Note>
  在 vim 正常模式下，如果光标在输入的开始或结束处且无法进一步移动，`j`/`k` 和箭头键将导航命令历史。
</Note>

### 编辑（NORMAL 模式）

| 命令             | 操作          |
| :------------- | :---------- |
| `x`            | 删除字符        |
| `dd`           | 删除行         |
| `D`            | 删除到行尾       |
| `dw`/`de`/`db` | 删除单词/到末尾/向后 |
| `cc`           | 更改行         |
| `C`            | 更改到行尾       |
| `cw`/`ce`/`cb` | 更改单词/到末尾/向后 |
| `yy`/`Y`       | 复制行         |
| `yw`/`ye`/`yb` | 复制单词/到末尾/向后 |
| `p`            | 在光标后粘贴      |
| `P`            | 在光标前粘贴      |
| `>>`           | 缩进行         |
| `<<`           | 取消缩进行       |
| `J`            | 连接行         |
| `u`            | 撤销          |
| `.`            | 重复最后一个更改    |

### 文本对象（NORMAL 模式）

文本对象与 `d`、`c` 和 `y` 等运算符一起工作：

| 命令        | 操作               |
| :-------- | :--------------- |
| `iw`/`aw` | 内部/周围单词          |
| `iW`/`aW` | 内部/周围 WORD（空白分隔） |
| `i"`/`a"` | 内部/周围双引号         |
| `i'`/`a'` | 内部/周围单引号         |
| `i(`/`a(` | 内部/周围括号          |
| `i[`/`a[` | 内部/周围方括号         |
| `i{`/`a{` | 内部/周围大括号         |

### 可视模式

按 `v` 进行字符级选择或按 `V` 进行行级选择。动作扩展选择，运算符直接作用于选择。

| 命令               | 操作                   |
| :--------------- | :------------------- |
| `d`/`x`          | 删除选择                 |
| `y`              | 复制选择                 |
| `c`/`s`          | 更改选择                 |
| `p`              | 用寄存器内容替换选择           |
| `r{char}`        | 将每个选定的字符替换为 `{char}` |
| `~`/`u`/`U`      | 切换、小写或大写选择           |
| `>`/`<`          | 缩进或取消缩进选定的行          |
| `J`              | 连接选定的行               |
| `o`              | 交换光标和锚点              |
| `iw`/`aw`/`i"`/… | 选择文本对象               |
| `v`/`V`          | 在字符级和行级之间切换，或退出      |

不支持使用 `Ctrl+V` 的块级可视模式。

## 命令历史

Claude Code 为当前会话维护命令历史：

* 输入历史按工作目录存储
* 当您运行 `/clear` 以启动新会话时，输入历史会重置。上一个会话的对话被保留并可以恢复。
* 使用向上/向下箭头导航（请参阅上面的快捷键）
* **注意**：历史扩展（`!`）默认禁用

### 使用 Ctrl+R 反向搜索

按 `Ctrl+R` 以交互方式搜索您的命令历史：

1. **开始搜索**：按 `Ctrl+R` 激活反向历史搜索
2. **键入查询**：输入文本以在以前的命令中搜索。搜索词在匹配结果中突出显示
3. **导航匹配**：再次按 `Ctrl+R` 以循环浏览较旧的匹配
4. **更改范围**：搜索默认为来自所有项目的提示。按 `Ctrl+S` 在此会话、此项目和所有项目之间循环范围
5. **接受匹配**：
   * 按 `Tab` 或 `Esc` 接受当前匹配并继续编辑
   * 按 `Enter` 接受并立即执行命令
6. **取消搜索**：
   * 按 `Ctrl+C` 取消并恢复原始输入
   * 在空搜索上按 `Backspace` 以取消

搜索显示匹配的命令，搜索词突出显示，因此您可以找到并重用以前的输入。

## 后台 bash 命令

Claude Code 支持在后台运行 bash 命令，允许您在长时间运行的进程执行时继续工作。

### 后台运行的工作原理

当 Claude Code 在后台运行命令时，它异步运行命令并立即返回后台任务 ID。Claude Code 可以在命令继续在后台执行时响应新提示。

要在后台运行命令，您可以：

* 提示 Claude Code 在后台运行命令
* 按 Ctrl+B 将常规 Bash 工具调用移到后台。（Tmux 用户必须按 Ctrl+B 两次，因为 tmux 的前缀键。）

**主要功能：**

* 输出被写入文件，Claude 可以使用 Read 工具检索它
* 后台任务具有唯一的 ID 用于跟踪和输出检索
* 当 Claude Code 退出时，后台任务会自动清理
* 如果输出超过 5GB，后台任务会自动终止，stderr 中会有说明原因的注释

要禁用所有后台任务功能，请将 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` 环境变量设置为 `1`。有关详细信息，请参阅[环境变量](/zh-CN/env-vars)。

**常见的后台命令：**

* 构建工具（webpack、vite、make）
* 包管理器（npm、yarn、pnpm）
* 测试运行器（jest、pytest）
* 开发服务器
* 长时间运行的进程（docker、terraform）

### 使用 `!` 前缀的 Bash 模式

通过在输入前加上 `!` 来直接运行 bash 命令，无需通过 Claude：

```bash theme={null}
! npm test
! git status
! ls -la
```

Bash 模式：

* 将命令及其输出添加到对话上下文
* 显示实时进度和输出
* 支持相同的 `Ctrl+B` 后台运行长时间运行的命令
* 不需要 Claude 解释或批准命令
* 支持基于历史的自动完成：键入部分命令并按 **Tab** 以从当前项目中的上一个 `!` 命令完成
* 使用 `Escape`、`Backspace` 或在空提示上使用 `Ctrl+U` 退出
* 将以 `!` 开头的文本粘贴到空提示中会自动进入 bash 模式，与键入的 `!` 行为相匹配

这对于快速 shell 操作同时保持对话上下文很有用。

## 提示建议

当您首次打开会话时，灰显的示例命令会出现在提示输入中以帮助您入门。Claude Code 从您的项目的 git 历史中选择此命令，因此它反映了您最近一直在处理的文件。

Claude 响应后，建议会根据您的对话历史继续出现，例如多部分请求的后续步骤或工作流的自然延续。

* 按 **Tab** 或 **Right arrow** 将建议放入提示输入中，然后按 **Enter** 提交
* 开始输入以关闭它

建议作为后台请求运行，该请求重用父对话的提示缓存，因此额外成本最小。当缓存冷时，Claude Code 会跳过建议生成以避免不必要的成本。

在对话的第一轮之后、在非交互模式下以及在 Plan Mode 中，建议会自动跳过。

要完全禁用提示建议，请设置环境变量或在 `/config` 中切换设置：

```bash theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## 使用 /btw 的侧面问题

使用 `/btw` 快速提问您当前的工作，而不添加到对话历史。当您想要快速答案但不想混乱主要上下文或使 Claude 偏离长时间运行的任务时，这很有用。

```
/btw what was the name of that config file again?
```

侧面问题可以完全看到当前对话，因此您可以询问 Claude 已经读过的代码、它之前做出的决定或会话中的任何其他内容。问题和答案是短暂的：它们出现在可关闭的覆盖层中，永远不会进入对话历史。

* **Claude 工作时可用**：即使 Claude 正在处理响应时，您也可以运行 `/btw`。侧面问题独立运行，不会中断主要轮次。
* **无工具访问**：侧面问题仅从已在上下文中的内容回答。Claude 在回答侧面问题时无法读取文件、运行命令或搜索。
* **单一响应**：没有后续轮次。如果您需要来回，请改用正常提示。
* **低成本**：侧面问题重用父对话的提示缓存，因此额外成本最小。

按 **Space**、**Enter** 或 **Escape** 关闭答案并返回提示。

`/btw` 是 [subagent](/zh-CN/sub-agents) 的反面：它看到您的完整对话但没有工具，而 subagent 具有完整工具但从空上下文开始。使用 `/btw` 询问 Claude 从此会话已知的内容；使用 subagent 去发现新的东西。

## 任务列表

在处理复杂的多步骤工作时，Claude 会创建任务列表来跟踪进度。任务出现在终端的状态区域中，指示器显示待处理、进行中或完成的内容。

* 按 `Ctrl+T` 切换任务列表视图。显示一次最多 5 个任务
* 要查看所有任务或清除它们，直接询问 Claude："show me all tasks"或"clear all tasks"
* 任务在上下文压缩中持续存在，帮助 Claude 在较大的项目上保持组织
* 要在会话之间共享任务列表，请设置 `CLAUDE_CODE_TASK_LIST_ID` 以使用 `~/.claude/tasks/` 中的命名目录：`CLAUDE_CODE_TASK_LIST_ID=my-project claude`

## 会话回顾

当您从离开后返回终端时，Claude Code 会显示到目前为止会话中发生的情况的单行回顾。回顾在后台生成，一旦自上次完成的轮次以来至少已经过了三分钟且终端未聚焦，就会生成，因此当您切换回来时已准备好。回顾仅在会话至少有三个轮次后出现，并且永远不会连续出现两次。

运行 `/recap` 以按需生成摘要。要关闭自动回顾，打开 `/config` 并禁用**会话回顾**。

会话回顾在每个计划和提供商上默认启用。回顾在非交互模式下始终被跳过。

## PR 审查状态

在处理具有开放拉取请求的分支时，Claude Code 在页脚中显示可点击的 PR 链接（例如"PR #446"）。该链接具有彩色下划线，指示审查状态：

* 绿色：已批准
* 黄色：待审查
* 红色：请求更改
* 灰色：草稿
* 紫色：已合并

`Cmd+click`（Mac）或 `Ctrl+click`（Windows/Linux）链接以在浏览器中打开拉取请求。状态每 60 秒自动更新一次。

<Note>
  PR 状态需要安装并验证 `gh` CLI（`gh auth login`）。
</Note>

## 另请参阅

* [Skills](/zh-CN/skills) - 自定义提示和工作流
* [Checkpointing](/zh-CN/checkpointing) - 回退 Claude 的编辑并恢复以前的状态
* [CLI 参考](/zh-CN/cli-reference) - 命令行标志和选项
* [设置](/zh-CN/settings) - 配置选项
* [内存管理](/zh-CN/memory) - 管理 CLAUDE.md 文件

> ## Documentation Index
>
> Fetch the complete documentation index at: <https://code.claude.com/docs/llms.txt>
> Use this file to discover all available pages before exploring further.

# Checkpointing

> 跟踪、回溯和总结 Claude 的编辑和对话以管理会话状态。

Claude Code 自动跟踪 Claude 在工作时所做的文件编辑，允许您快速撤销更改并回溯到之前的状态，以防任何事情出现偏差。

## checkpointing 如何工作

当您与 Claude 合作时，checkpointing 会自动捕获每次编辑前代码的状态。这个安全网让您可以放心地执行雄心勃勃的大规模任务，因为您始终可以返回到之前的代码状态。

### 自动跟踪

Claude Code 跟踪其文件编辑工具所做的所有更改：

* 每个用户提示都会创建一个新的 checkpoint
* Checkpoints 在会话之间持久存在，因此您可以在恢复的对话中访问它们
* 在 30 天后自动清理（可配置）

### 回溯和总结

按两次 `Esc`（`Esc` + `Esc`）或使用 `/rewind` 命令打开回溯菜单。一个可滚动的列表显示会话中的每个提示。选择您想要操作的点，然后选择一个操作：

* **恢复代码和对话**：将代码和对话都恢复到该点
* **恢复对话**：回溯到该消息，同时保持当前代码
* **恢复代码**：恢复文件更改，同时保持对话
* **从此处总结**：将此点之后的对话压缩为摘要，释放 context window 空间
* **算了**：返回消息列表而不做任何更改

恢复对话或选择"从此处总结"后，所选消息的原始提示会恢复到输入字段中，以便您可以重新发送或编辑它。

选择"算了"会让您留在消息列表，输入字段为空。

#### 恢复与总结

恢复选项恢复状态：它们撤销代码更改、对话历史或两者。总结选项将对话的一部分压缩为 AI 生成的摘要，而不改变磁盘上的文件：

* **从此处总结**：所选消息之前的消息保持不变。所选消息及其后的所有消息被替换为摘要。使用此选项可以放弃旁支讨论，同时保持早期上下文的完整细节。
* **算了总结**：所选消息之前的消息被替换为摘要。所选消息及其后的所有消息保持不变，您留在对话的末尾。使用此选项可以压缩早期设置讨论，同时保持最近工作的完整细节。

在这两种情况下，原始消息都保存在会话记录中，因此 Claude 可以在需要时参考详细信息。您可以输入可选说明来指导摘要的重点。这类似于 `/compact`，但更有针对性：您不是总结整个对话，而是选择所选消息的哪一侧进行压缩。

<Note>
  总结将您保持在同一会话中并压缩上下文。如果您想尝试不同的方法，同时保持原始会话完整，请改用 [fork](/zh-CN/sessions#branch-a-session)（`claude --continue --fork-session`）。
</Note>

## 常见用例

Checkpoints 在以下情况下特别有用：

* **探索替代方案**：尝试不同的实现方法，而不会丢失起点
* **从错误中恢复**：快速撤销引入错误或破坏功能的更改
* **迭代功能**：进行变体实验，知道您可以恢复到工作状态
* **释放上下文空间**：从中点开始总结冗长的调试会话，保持初始说明完整

## 限制

### Bash 命令更改未跟踪

Checkpointing 不跟踪由 bash 命令修改的文件。例如，如果 Claude Code 运行：

```bash theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

这些文件修改无法通过回溯撤销。只有通过 Claude 的文件编辑工具进行的直接文件编辑才会被跟踪。

### 外部更改未跟踪

Checkpointing 仅跟踪在当前会话中编辑过的文件。您在 Claude Code 外部对文件所做的手动更改以及来自其他并发会话的编辑通常不会被捕获，除非它们碰巧修改了与当前会话相同的文件。

### 不是版本控制的替代品

Checkpoints 设计用于快速的会话级恢复。对于永久版本历史和协作：

* 继续使用版本控制（例如 Git）进行提交、分支和长期历史
* Checkpoints 补充但不替代适当的版本控制
* 将 checkpoints 视为"本地撤销"，将 Git 视为"永久历史"

## 另请参阅

* [Interactive mode](/zh-CN/interactive-mode) - 快捷键和会话控制
* [Commands](/zh-CN/commands) - 使用 `/rewind` 访问 checkpoints
* [CLI reference](/zh-CN/cli-reference) - 命令行选项

> ## Documentation Index
>
> Fetch the complete documentation index at: <https://code.claude.com/docs/llms.txt>
> Use this file to discover all available pages before exploring further.

# Hooks 参考

> Claude Code hook 事件、配置架构、JSON 输入/输出格式、退出代码、异步 hooks、HTTP hooks、提示 hooks 和 MCP 工具 hooks 的参考。

<Tip>
  有关包含示例的快速入门指南，请参阅[使用 hooks 自动化工作流](/zh-CN/hooks-guide)。
</Tip>

Hooks 是用户定义的 shell 命令、HTTP 端点或 LLM 提示，在 Claude Code 生命周期中的特定点自动执行。使用此参考查找事件架构、配置选项、JSON 输入/输出格式以及异步 hooks、HTTP hooks 和 MCP 工具 hooks 等高级功能。如果您是第一次设置 hooks，请改为从[指南](/zh-CN/hooks-guide)开始。

## Hook 生命周期

Hooks 在 Claude Code 会话期间的特定点触发。当事件触发且匹配器匹配时，Claude Code 会将关于该事件的 JSON 上下文传递给您的 hook 处理程序。对于命令 hooks，输入通过 stdin 到达。对于 HTTP hooks，它作为 POST 请求体到达。您的处理程序随后可以检查输入、采取行动并可选地返回决定。事件分为三种频率：每个会话一次（`SessionStart`、`SessionEnd`）、每轮一次（`UserPromptSubmit`、`Stop`、`StopFailure`）以及代理循环内的每个工具调用（`PreToolUse`、`PostToolUse`）：

<div style={{maxWidth: "500px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/ZIW26Z9pnpsXLhbS/images/hooks-lifecycle.svg?fit=max&auto=format&n=ZIW26Z9pnpsXLhbS&q=85&s=ee23691324deb6501df09bfdae560b64" alt="Hook 生命周期图，显示可选的 Setup 流入 SessionStart，然后是每轮循环，包含 UserPromptSubmit、用于 slash commands 的 UserPromptExpansion、嵌套的代理循环（PreToolUse、PermissionRequest、PostToolUse、PostToolUseFailure、PostToolBatch、SubagentStart/Stop、TaskCreated、TaskCompleted）和 Stop 或 StopFailure，然后是 TeammateIdle、PreCompact、PostCompact 和 SessionEnd，Elicitation 和 ElicitationResult 嵌套在 MCP 工具执行内，PermissionDenied 作为 PermissionRequest 的副分支用于自动模式拒绝，WorktreeCreate、WorktreeRemove、Notification、ConfigChange、InstructionsLoaded、CwdChanged 和 FileChanged 作为独立异步事件" width="520" height="1228" data-path="images/hooks-lifecycle.svg" />
  </Frame>
</div>

下表总结了每个事件何时触发。[Hook 事件](#hook-events)部分记录了每个事件的完整输入架构和决定控制选项。

| Event                 | When it fires                                                                                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`        | When a session begins or resumes                                                                                                                       |
| `Setup`               | When you start Claude Code with `--init-only`, or with `--init` or `--maintenance` in `-p` mode. For one-time preparation in CI or scripts             |
| `UserPromptSubmit`    | When you submit a prompt, before Claude processes it                                                                                                   |
| `UserPromptExpansion` | When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion                                                     |
| `PreToolUse`          | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`   | When a permission dialog appears                                                                                                                       |
| `PermissionDenied`    | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call                     |
| `PostToolUse`         | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure`  | After a tool call fails                                                                                                                                |
| `PostToolBatch`       | After a full batch of parallel tool calls resolves, before the next model call                                                                         |
| `Notification`        | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`       | When a subagent is spawned                                                                                                                             |
| `SubagentStop`        | When a subagent finishes                                                                                                                               |
| `TaskCreated`         | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`       | When a task is being marked as completed                                                                                                               |
| `Stop`                | When Claude finishes responding                                                                                                                        |
| `StopFailure`         | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`        | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `InstructionsLoaded`  | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`        | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`          | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`         | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`      | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`      | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`          | Before context compaction                                                                                                                              |
| `PostCompact`         | After context compaction completes                                                                                                                     |
| `Elicitation`         | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`   | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`          | When a session terminates                                                                                                                              |

### Hook 如何解析

要了解这些部分如何组合在一起，请考虑这个 `PreToolUse` hook，它阻止破坏性 shell 命令。`matcher` 缩小到 Bash 工具调用，`if` 条件进一步缩小到匹配 `rm *` 的 Bash 子命令，因此 `block-rm.sh` 仅在两个过滤器都匹配时生成：

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh",
            "args": []
          }
        ]
      }
    ]
  }
}
```

该脚本从 stdin 读取 JSON 输入，提取命令，如果包含 `rm -rf`，则返回 `permissionDecision` 为 `"deny"`：

```bash theme={null}
#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # allow the command
fi
```

现在假设 Claude Code 决定运行 `Bash "rm -rf /tmp/build"`。以下是发生的情况：

<Frame>
  <img src="https://mintcdn.com/claude-code/-tYw1BD_DEqfyyOZ/images/hook-resolution.svg?fit=max&auto=format&n=-tYw1BD_DEqfyyOZ&q=85&s=c73ebc1eeda2037570427d7af1e0a891" alt="Hook 解析流程：PreToolUse 事件触发，匹配器检查 Bash 匹配，if 条件检查 Bash(rm *) 匹配，hook 处理程序运行，结果返回到 Claude Code" width="930" height="290" data-path="images/hook-resolution.svg" />
</Frame>

<Steps>
  <Step title="事件触发">
    `PreToolUse` 事件触发。Claude Code 将工具输入作为 JSON 通过 stdin 发送到 hook：

    ```json theme={null}
    { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
    ```
  </Step>

  <Step title="匹配器检查">
    匹配器 `"Bash"` 与工具名称匹配，因此此 hook 组激活。如果您省略匹配器或使用 `"*"`，该组在事件的每次出现时激活。
  </Step>

  <Step title="If 条件检查">
    `if` 条件 `"Bash(rm *)"` 匹配，因为 `rm -rf /tmp/build` 是匹配 `rm *` 的子命令，因此此处理程序生成。如果命令是 `npm test`，`if` 检查会失败，`block-rm.sh` 永远不会运行，避免进程生成开销。`if` 字段是可选的；没有它，匹配组中的每个处理程序都运行。
  </Step>

  <Step title="Hook 处理程序运行">
    脚本检查完整命令并找到 `rm -rf`，因此它将决定打印到 stdout：

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Destructive command blocked by hook"
      }
    }
    ```

    如果命令是更安全的 `rm` 变体，如 `rm file.txt`，脚本会改为执行 `exit 0`，这告诉 Claude Code 允许工具调用而无需进一步操作。
  </Step>

  <Step title="Claude Code 对结果采取行动">
    Claude Code 读取 JSON 决定，阻止工具调用，并向 Claude 显示原因。
  </Step>
</Steps>

下面的[配置](#configuration)部分记录了完整的架构，每个[hook 事件](#hook-events)部分记录了您的命令接收的输入以及它可以返回的输出。

## 配置

Hooks 在 JSON 设置文件中定义。配置有三个嵌套级别：

1. 选择要响应的[hook 事件](#hook-events)，如 `PreToolUse` 或 `Stop`
2. 添加[匹配器组](#matcher-patterns)以过滤何时触发，如"仅针对 Bash 工具"
3. 定义一个或多个[hook 处理程序](#hook-handler-fields)以在匹配时运行

有关完整的演练和带注释的示例，请参阅上面的[Hook 如何解析](#how-a-hook-resolves)。

<Note>
  此页面为每个级别使用特定术语：**hook 事件**表示生命周期点，**匹配器组**表示过滤器，**hook 处理程序**表示运行的 shell 命令、HTTP 端点、MCP 工具、提示或代理。"Hook"本身指的是一般功能。
</Note>

### Hook 位置

您定义 hook 的位置决定了其范围：

| 位置                                                          | 范围     | 可共享          |
| :---------------------------------------------------------- | :----- | :----------- |
| `~/.claude/settings.json`                                   | 您的所有项目 | 否，本地于您的计算机   |
| `.claude/settings.json`                                     | 单个项目   | 是，可以提交到仓库    |
| `.claude/settings.local.json`                               | 单个项目   | 否，gitignored |
| 托管策略设置                                                      | 组织范围   | 是，管理员控制      |
| [Plugin](/zh-CN/plugins) `hooks/hooks.json`                 | 启用插件时  | 是，与插件捆绑      |
| [Skill](/zh-CN/skills) 或[代理](/zh-CN/sub-agents) frontmatter | 组件活跃时  | 是，在组件文件中定义   |

有关设置文件解析的详细信息，请参阅[设置](/zh-CN/settings)。企业管理员可以使用 `allowManagedHooksOnly` 来阻止用户、项目和插件 hooks。在托管设置 `enabledPlugins` 中强制启用的插件中的 Hooks 是豁免的，因此管理员可以通过组织市场分发经过审查的 hooks。请参阅[Hook 配置](/zh-CN/settings#hook-configuration)。

### 匹配器模式

`matcher` 字段过滤 hooks 何时触发。匹配器的评估方式取决于它包含的字符：

| 匹配器值              | 评估为                    | 示例                                                                        |
| :---------------- | :--------------------- | :------------------------------------------------------------------------ |
| `"*"`、`""` 或省略    | 匹配所有                   | 在事件的每次出现时触发                                                               |
| 仅字母、数字、`_` 和 `\|` | 精确字符串或 `\|` 分隔的精确字符串列表 | `Bash` 仅匹配 Bash 工具；`Edit\|Write` 精确匹配任一工具                                 |
| 包含任何其他字符          | JavaScript 正则表达式       | `^Notebook` 匹配任何以 Notebook 开头的工具；`mcp__memory__.*` 匹配来自 `memory` 服务器的每个工具 |

`FileChanged` 事件在构建其监视列表时不遵循这些规则。请参阅 [FileChanged](#filechanged)。

每个事件类型在不同的字段上匹配：

| 事件                                                                                                                       | 匹配器过滤的内容                                  | 示例匹配器值                                                                                                                                      |
| :----------------------------------------------------------------------------------------------------------------------- | :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`、`PermissionDenied`                                   | 工具名称                                      | `Bash`、`Edit\|Write`、`mcp__.*`                                                                                                              |
| `SessionStart`                                                                                                           | 会话如何启动                                    | `startup`、`resume`、`clear`、`compact`                                                                                                        |
| `Setup`                                                                                                                  | 哪个 CLI 标志触发了设置                            | `init`、`maintenance`                                                                                                                        |
| `SessionEnd`                                                                                                             | 会话为何结束                                    | `clear`、`resume`、`logout`、`prompt_input_exit`、`bypass_permissions_disabled`、`other`                                                         |
| `Notification`                                                                                                           | 通知类型                                      | `permission_prompt`、`idle_prompt`、`auth_success`、`elicitation_dialog`、`elicitation_complete`、`elicitation_response`                         |
| `SubagentStart`                                                                                                          | 代理类型                                      | `general-purpose`、`Explore`、`Plan` 或自定义代理名称                                                                                                 |
| `PreCompact`、`PostCompact`                                                                                               | 触发压缩的原因                                   | `manual`、`auto`                                                                                                                             |
| `SubagentStop`                                                                                                           | 代理类型                                      | 与 `SubagentStart` 相同的值                                                                                                                      |
| `ConfigChange`                                                                                                           | 配置源                                       | `user_settings`、`project_settings`、`local_settings`、`policy_settings`、`skills`                                                              |
| `CwdChanged`                                                                                                             | 不支持匹配器                                    | 总是在每次目录更改时触发                                                                                                                                |
| `FileChanged`                                                                                                            | 文字文件名以监视（请参阅 [FileChanged](#filechanged)） | `.envrc\|.env`                                                                                                                              |
| `StopFailure`                                                                                                            | 错误类型                                      | `rate_limit`、`authentication_failed`、`oauth_org_not_allowed`、`billing_error`、`invalid_request`、`server_error`、`max_output_tokens`、`unknown` |
| `InstructionsLoaded`                                                                                                     | 加载原因                                      | `session_start`、`nested_traversal`、`path_glob_match`、`include`、`compact`                                                                    |
| `UserPromptExpansion`                                                                                                    | 命令名称                                      | 您的 skill 或命令名称                                                                                                                              |
| `Elicitation`                                                                                                            | MCP 服务器名称                                 | 您配置的 MCP 服务器名称                                                                                                                              |
| `ElicitationResult`                                                                                                      | MCP 服务器名称                                 | 与 `Elicitation` 相同的值                                                                                                                        |
| `UserPromptSubmit`、`PostToolBatch`、`Stop`、`TeammateIdle`、`TaskCreated`、`TaskCompleted`、`WorktreeCreate`、`WorktreeRemove` | 不支持匹配器                                    | 总是在每次出现时触发                                                                                                                                  |

匹配器针对 Claude Code 在 stdin 上发送给您的 hook 的[JSON 输入](#hook-input-and-output)中的字段运行。对于工具事件，该字段是 `tool_name`。每个[hook 事件](#hook-events)部分列出了完整的匹配器值集和该事件的输入架构。

此示例仅在 Claude 写入或编辑文件时运行 linting 脚本：

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

`UserPromptSubmit`、`PostToolBatch`、`Stop`、`TeammateIdle`、`TaskCreated`、`TaskCompleted`、`WorktreeCreate`、`WorktreeRemove` 和 `CwdChanged` 不支持匹配器，总是在每次出现时触发。如果您向这些事件添加 `matcher` 字段，它会被静默忽略。

对于工具事件，您可以通过在单个 hook 处理程序上设置[`if` 字段](#common-fields)来更狭隘地过滤。`if` 使用[权限规则语法](/zh-CN/permissions)来匹配工具名称和参数，因此 `"Bash(git *)"` 仅在任何 Bash 输入的子命令与 `git *` 匹配时运行，`"Edit(*.ts)"` 仅对 TypeScript 文件运行。

#### 匹配 MCP 工具

[MCP](/zh-CN/mcp) 服务器工具在工具事件中显示为常规工具（`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`、`PermissionDenied`），因此您可以像匹配任何其他工具名称一样匹配它们。

MCP 工具遵循命名模式 `mcp__<server>__<tool>`，例如：

* `mcp__memory__create_entities`：Memory 服务器的创建实体工具
* `mcp__filesystem__read_file`：Filesystem 服务器的读取文件工具
* `mcp__github__search_repositories`：GitHub 服务器的搜索工具

要匹配来自服务器的每个工具，请在服务器前缀后追加 `.*`。`.*` 是必需的：像 `mcp__memory` 这样的匹配器仅包含字母和下划线，因此它作为精确字符串进行比较，不匹配任何工具。

* `mcp__memory__.*` 匹配来自 `memory` 服务器的所有工具
* `mcp__.*__write.*` 匹配来自任何服务器的任何名称以 `write` 开头的工具

此示例记录所有内存服务器操作并验证来自任何 MCP 服务器的写入操作：

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

### Hook 处理程序字段

内部 `hooks` 数组中的每个对象都是一个 hook 处理程序：当匹配器匹配时运行的 shell 命令、HTTP 端点、MCP 工具、LLM 提示或代理。有五种类型：

* **[命令 hooks](#command-hook-fields)**（`type: "command"`）：运行 shell 命令。您的脚本在 stdin 上接收事件的[JSON 输入](#hook-input-and-output)，并通过退出代码和 stdout 传回结果。
* **[HTTP hooks](#http-hook-fields)**（`type: "http"`）：将事件的 JSON 输入作为 HTTP POST 请求发送到 URL。端点通过使用与命令 hooks 相同的[JSON 输出格式](#json-output)的响应体传回结果。
* **[MCP 工具 hooks](#mcp-tool-hook-fields)**（`type: "mcp_tool"`）：在已连接的[MCP 服务器](/zh-CN/mcp)上调用工具。工具的文本输出被视为命令 hook stdout。
* **[提示 hooks](#prompt-and-agent-hook-fields)**（`type: "prompt"`）：向 Claude 模型发送提示以进行单轮评估。模型返回 yes/no 决定作为 JSON。请参阅[基于提示的 hooks](#prompt-based-hooks)。
* **[代理 hooks](#prompt-and-agent-hook-fields)**（`type: "agent"`）：生成一个可以使用 Read、Grep 和 Glob 等工具来验证条件的 subagent，然后返回决定。代理 hooks 是实验性的，可能会改变。请参阅[基于代理的 hooks](#agent-based-hooks)。

#### 通用字段

这些字段适用于所有 hook 类型：

| 字段              | 必需 | 描述                                                                                                                                                                                                                                                                      |
| :-------------- | :- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`          | 是  | `"command"`、`"http"`、`"mcp_tool"`、`"prompt"` 或 `"agent"`                                                                                                                                                                                                                |
| `if`            | 否  | 权限规则语法以过滤此 hook 何时运行，例如 `"Bash(git *)"` 或 `"Edit(*.ts)"`。仅当工具调用与模式匹配时，hook 才会生成，或当 Bash 命令太复杂而无法解析时。仅在工具事件上评估：`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest` 和 `PermissionDenied`。在其他事件上，设置了 `if` 的 hook 永远不会运行。使用与[权限规则](/zh-CN/permissions)相同的语法 |
| `timeout`       | 否  | 取消前的秒数。默认值：`command`、`http` 和 `mcp_tool` 为 600；`prompt` 为 30；`agent` 为 60。[`UserPromptSubmit`](#userpromptsubmit) 将 `command`、`http` 和 `mcp_tool` 的默认值降低到 30                                                                                                            |
| `statusMessage` | 否  | hook 运行时显示的自定义加载程序消息                                                                                                                                                                                                                                                    |
| `once`          | 否  | 如果为 `true`，每个会话仅运行一次，然后被移除。仅在[skill frontmatter](#hooks-in-skills-and-agents)中声明的 hooks 中受尊重；在设置文件和代理 frontmatter 中被忽略                                                                                                                                                  |

`if` 字段恰好包含一个权限规则。没有 `&&`、`||` 或列表语法来组合规则；要应用多个条件，请为每个条件定义一个单独的 hook 处理程序。对于 Bash，规则针对工具输入的每个子命令进行匹配，在去除前导 `VAR=value` 赋值后，因此 `if: "Bash(git push *)"` 既匹配 `FOO=bar git push` 也匹配 `npm test && git push`。如果任何子命令匹配，hook 会运行，并且在命令太复杂而无法解析时总是运行。

#### 命令 hook 字段

除了[通用字段](#common-fields)外，命令 hooks 还接受这些字段：

| 字段            | 必需 | 描述                                                                                                                                                                             |
| :------------ | :- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `command`     | 是  | 要执行的 shell 命令。与 `args` 一起，要直接生成的可执行文件。请参阅[Exec 形式和 shell 形式](#exec-form-and-shell-form)                                                                                        |
| `args`        | 否  | 参数列表。存在时，`command` 被解析为可执行文件并直接使用 `args` 作为参数向量生成，不涉及 shell。请参阅[Exec 形式和 shell 形式](#exec-form-and-shell-form)                                                                  |
| `async`       | 否  | 如果为 `true`，在后台运行而不阻止。请参阅[在后台运行 hooks](#run-hooks-in-the-background)                                                                                                            |
| `asyncRewake` | 否  | 如果为 `true`，在后台运行并在退出代码 2 时唤醒 Claude。暗示 `async`。Hook 的 stderr，或 stdout（如果 stderr 为空），作为系统提醒显示给 Claude，以便它可以对长时间运行的后台失败做出反应                                                      |
| `shell`       | 否  | 用于此 hook 的 shell。接受 `"bash"`（默认）或 `"powershell"`。设置 `"powershell"` 在 Windows 上通过 PowerShell 运行命令。不需要 `CLAUDE_CODE_USE_POWERSHELL_TOOL`，因为 hooks 直接生成 PowerShell。设置 `args` 时被忽略 |

<a id="exec-form-and-shell-form" />

##### Exec 形式和 shell 形式

当设置 `args` 时，命令 hook 以 exec 形式运行，当省略 `args` 时以 shell 形式运行。每当 hook 引用[路径占位符](#reference-scripts-by-path)时设置 `args`，因为每个元素作为一个参数传递，不带引号。当您需要 shell 功能（如管道或 `&&`）时，或当两个问题都不适用时，省略 `args`。

**Exec 形式**在存在 `args` 时运行。Claude Code 在 `PATH` 上解析 `command` 作为可执行文件，并直接使用 `args` 作为参数向量生成它。没有 shell，因此每个 `args` 元素恰好是一个参数，完全按照编写的方式，路径占位符如 `${CLAUDE_PLUGIN_ROOT}` 被替换为 `command` 和每个 `args` 元素中的纯字符串。特殊字符如撇号、`$` 和反引号逐字通过，因为没有 shell 来解释它们。在任何平台上都不会发生 shell 标记化。

**Shell 形式**在省略 `args` 时运行。`command` 字符串被传递给 shell：在 macOS 和 Linux 上为 `sh -c`，在 Windows 上为 Git Bash，或在未安装 Git Bash 时为 PowerShell。设置 `shell` 字段以显式选择。shell 标记化字符串，展开变量，并解释管道、`&&`、重定向和 glob。

<Note>
  在 Windows 上，exec 形式需要 `command` 解析为真实可执行文件，如 `.exe`。npm、npx、eslint 和其他工具在 `node_modules/.bin` 中安装的 `.cmd` 和 `.bat` 垫片不是可执行文件，不能在没有 shell 的情况下生成。要在 exec 形式中运行它们，直接使用 `node` 调用底层脚本，例如 `"command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/node_modules/eslint/bin/eslint.js"]`。`node` 加脚本路径模式在每个平台上都有效，因为 `node.exe` 是真实二进制文件。要按名称运行 `.cmd` 或 `.bat` 垫片，请使用 shell 形式。
</Note>

此示例运行与插件捆绑的 Node 脚本。Exec 形式将解析的脚本路径作为一个参数传递，不带引号：

```json theme={null}
{
  "type": "command",
  "command": "node",
  "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/format.js", "--fix"]
}
```

等效的 shell 形式需要引号来处理包含空格或特殊字符的路径：

```json theme={null}
{
  "type": "command",
  "command": "node \"${CLAUDE_PLUGIN_ROOT}\"/scripts/format.js --fix"
}
```

两种形式都支持相同的[路径占位符](#reference-scripts-by-path)，并且都将它们作为环境变量 `CLAUDE_PROJECT_DIR`、`CLAUDE_PLUGIN_ROOT` 和 `CLAUDE_PLUGIN_DATA` 导出到生成的进程上，因此脚本可以读取 `process.env.CLAUDE_PLUGIN_ROOT`，无论它是如何启动的。插件 hooks 另外替换 `${user_config.*}` 值；请参阅[用户配置](/zh-CN/plugins-reference#user-configuration)。

<Note>
  在 exec 形式中，`command` 仅是可执行文件名或路径。如果 `command` 是没有路径分隔符的裸名称，并且与 `args` 一起包含空格，Claude Code 会记录警告，因为生成会失败：没有名为 `node script.js` 的可执行文件。将额外的令牌移到 `args` 中。包含空格的绝对路径，如 `C:\Program Files\nodejs\node.exe`，是单个有效的可执行文件，不会触发警告。
</Note>

#### HTTP hook 字段

除了[通用字段](#common-fields)外，HTTP hooks 还接受这些字段：

| 字段               | 必需 | 描述                                                                                      |
| :--------------- | :- | :-------------------------------------------------------------------------------------- |
| `url`            | 是  | 发送 POST 请求的 URL                                                                         |
| `headers`        | 否  | 其他 HTTP 标头作为键值对。值支持使用 `$VAR_NAME` 或 `${VAR_NAME}` 语法的环境变量插值。仅解析 `allowedEnvVars` 中列出的变量 |
| `allowedEnvVars` | 否  | 可能被插值到标头值中的环境变量名称列表。对未列出变量的引用被替换为空字符串。任何环境变量插值都需要此项                                     |

Claude Code 使用 `Content-Type: application/json` 将 hook 的[JSON 输入](#hook-input-and-output)作为 POST 请求体发送。响应体使用与命令 hooks 相同的[JSON 输出格式](#json-output)。

错误处理与命令 hooks 不同：非 2xx 响应、连接失败和超时都会产生非阻止错误，允许执行继续。要阻止工具调用或拒绝权限，返回 2xx 响应，其 JSON 体包含 `decision: "block"` 或 `hookSpecificOutput` 与 `permissionDecision: "deny"`。

此示例将 `PreToolUse` 事件发送到本地验证服务，使用来自 `MY_TOKEN` 环境变量的令牌进行身份验证：

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

#### MCP 工具 hook 字段

除了[通用字段](#common-fields)外，MCP 工具 hooks 还接受这些字段：

| 字段       | 必需 | 描述                                                                                                     |
| :------- | :- | :----------------------------------------------------------------------------------------------------- |
| `server` | 是  | 已配置的 MCP 服务器的名称。服务器必须已连接；hook 永远不会触发 OAuth 或连接流                                                        |
| `tool`   | 是  | 该服务器上要调用的工具的名称                                                                                         |
| `input`  | 否  | 传递给工具的参数。字符串值支持从 hook 的[JSON 输入](#hook-input-and-output)进行 `${path}` 替换，例如 `"${tool_input.file_path}"` |

工具的文本内容被视为命令 hook stdout：如果它解析为有效的[JSON 输出](#json-output)，则作为决定进行处理，否则显示为纯文本。如果命名的服务器未连接，或工具返回 `isError: true`，hook 会产生非阻止错误，执行继续。

MCP 工具 hooks 在 Claude Code 连接到您的 MCP 服务器后在每个 hook 事件上可用。`SessionStart` 和 `Setup` 通常在服务器完成连接之前触发，因此这些事件上的 hooks 应该期望在首次运行时出现"未连接"错误。

此示例在每个 `Write` 或 `Edit` 后在 `my_server` MCP 服务器上调用 `security_scan` 工具，传递编辑文件的路径：

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "mcp_tool",
            "server": "my_server",
            "tool": "security_scan",
            "input": { "file_path": "${tool_input.file_path}" }
          }
        ]
      }
    ]
  }
}
```

#### 提示和代理 hook 字段

除了[通用字段](#common-fields)外，提示和代理 hooks 还接受这些字段：

| 字段       | 必需 | 描述                                               |
| :------- | :- | :----------------------------------------------- |
| `prompt` | 是  | 要发送给模型的提示文本。使用 `$ARGUMENTS` 作为 hook 输入 JSON 的占位符 |
| `model`  | 否  | 用于评估的模型。默认为快速模型                                  |

所有匹配的 hooks 并行运行，相同的处理程序会自动去重。命令 hooks 按命令字符串和 `args` 去重，HTTP hooks 按 URL 去重。处理程序在当前目录中运行，使用 Claude Code 的环境。在远程 web 环境中，`$CLAUDE_CODE_REMOTE` 环境变量设置为 `"true"`，在本地 CLI 中未设置。

### 按路径引用脚本

使用这些占位符按项目或插件根目录引用 hook 脚本，无论 hook 运行时的工作目录如何：

* `${CLAUDE_PROJECT_DIR}`：项目根目录。
* `${CLAUDE_PLUGIN_ROOT}`：插件的安装目录，用于与[插件](/zh-CN/plugins)捆绑的脚本。在每次插件更新时更改。
* `${CLAUDE_PLUGIN_DATA}`：插件的[持久数据目录](/zh-CN/plugins-reference#persistent-data-directory)，用于应该在插件更新后保留的依赖项和状态。

对于任何引用路径占位符的 hook，优先使用[exec 形式](#exec-form-and-shell-form)。Exec 形式将每个 `args` 元素作为一个参数传递，不带 shell 标记化，因此包含空格或特殊字符的路径不需要引号。在 shell 形式中，用双引号包装每个占位符。

<Tabs>
  <Tab title="项目脚本">
    此示例使用 `${CLAUDE_PROJECT_DIR}` 在任何 `Write` 或 `Edit` 工具调用后从项目的 `.claude/hooks/` 目录运行样式检查器：

    ```json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/check-style.sh",
                "args": []
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="插件脚本">
    在 `hooks/hooks.json` 中定义插件 hooks，带有可选的顶级 `description` 字段。启用插件时，其 hooks 与您的用户和项目 hooks 合并。

    此示例运行与插件捆绑的格式化脚本：

    ```json theme={null}
    {
      "description": "Automatic code formatting",
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
                "args": [],
                "timeout": 30
              }
            ]
          }
        ]
      }
    }
    ```

    有关创建插件 hooks 的详细信息，请参阅[插件组件参考](/zh-CN/plugins-reference#hooks)。
  </Tab>
</Tabs>

### Skills 和代理中的 Hooks

除了设置文件和插件外，hooks 还可以使用 frontmatter 直接在[skills](/zh-CN/skills)和[subagents](/zh-CN/sub-agents)中定义。这些 hooks 的范围限于组件的生命周期，仅在该组件活跃时运行。

支持所有 hook 事件。对于 subagents，`Stop` hooks 会自动转换为 `SubagentStop`，因为这是 subagent 完成时触发的事件。

Hooks 使用与基于设置的 hooks 相同的配置格式，但范围限于组件的生命周期，并在其完成时清理。

此 skill 定义了一个 `PreToolUse` hook，在每个 `Bash` 命令之前运行安全验证脚本：

```yaml theme={null}
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

代理在其 YAML frontmatter 中使用相同的格式。

### `/hooks` 菜单

在 Claude Code 中键入 `/hooks` 以打开您配置的 hooks 的只读浏览器。菜单显示每个 hook 事件及其配置的 hooks 计数，让您深入了解匹配器，并显示每个 hook 处理程序的完整详细信息。使用它来验证配置、检查 hook 来自哪个设置文件，或检查 hook 的命令、提示或 URL。

菜单显示所有五种 hook 类型：`command`、`prompt`、`agent`、`http` 和 `mcp_tool`。每个 hook 都标有 `[type]` 前缀和指示其定义位置的源：

* `User`：来自 `~/.claude/settings.json`
* `Project`：来自 `.claude/settings.json`
* `Local`：来自 `.claude/settings.local.json`
* `Plugin`：来自插件的 `hooks/hooks.json`
* `Session`：在当前会话中在内存中注册
* `Built-in`：由 Claude Code 内部注册

选择 hook 会打开详细视图，显示其事件、匹配器、类型、源文件以及完整的命令、提示或 URL。菜单是只读的：要添加、修改或移除 hooks，请直接编辑设置 JSON 或要求 Claude 进行更改。

### 禁用或移除 hooks

要移除 hook，请从设置 JSON 文件中删除其条目。

要临时禁用所有 hooks 而不移除它们，请在设置文件中设置 `"disableAllHooks": true`。没有办法在保持 hook 在配置中的同时禁用单个 hook。

`disableAllHooks` 设置遵守托管设置层次结构。如果管理员通过托管策略设置配置了 hooks，则在用户、项目或本地设置中设置的 `disableAllHooks` 无法禁用这些托管 hooks。仅在托管设置级别设置的 `disableAllHooks` 可以禁用托管 hooks。

对设置文件中 hooks 的直接编辑通常由文件监视程序自动拾取。

## Hook 输入和输出

命令 hooks 通过 stdin 接收 JSON 数据，并通过退出代码、stdout 和 stderr 传回结果。HTTP hooks 接收相同的 JSON 作为 POST 请求体，并通过 HTTP 响应体传回结果。本部分涵盖所有事件通用的字段和行为。每个事件在[Hook 事件](#hook-events)下的部分包括其特定的输入架构和决定控制选项。

从 v2.1.139 开始，在 macOS 和 Linux 上，命令 hooks 在没有控制终端的自己的会话中运行。hook 进程和任何子进程无法打开 `/dev/tty` 或直接向 Claude Code 界面发送转义序列。Windows 没有 `/dev/tty`。要在任何平台上向用户显示消息，请在 JSON 输出中返回[`systemMessage`](#json-output)。要触发桌面通知、设置窗口标题或响铃，请改为返回[`terminalSequence`](#emit-terminal-notifications)。

### 通用输入字段

Hook 事件接收这些字段作为 JSON，除了每个[hook 事件](#hook-events)部分中记录的事件特定字段。对于命令 hooks，此 JSON 通过 stdin 到达。对于 HTTP hooks，它作为 POST 请求体到达。

| 字段                | 描述                                                                                                                                                                                                                                                                                                                                                                      |
| :---------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `session_id`      | 当前会话标识符                                                                                                                                                                                                                                                                                                                                                                 |
| `transcript_path` | 对话 JSON 的路径                                                                                                                                                                                                                                                                                                                                                             |
| `cwd`             | 调用 hook 时的当前工作目录                                                                                                                                                                                                                                                                                                                                                        |
| `permission_mode` | 当前[权限模式](/zh-CN/permissions#permission-modes)：`"default"`、`"plan"`、`"acceptEdits"`、`"auto"`、`"dontAsk"` 或 `"bypassPermissions"`。并非所有事件都接收此字段：请参阅下面每个事件的 JSON 示例以检查                                                                                                                                                                                                      |
| `effort`          | 对象，其中 `level` 字段保存该轮次的活跃[努力级别](/zh-CN/model-config#adjust-effort-level)：`"low"`、`"medium"`、`"high"`、`"xhigh"` 或 `"max"`。如果请求的努力级别超过当前模型支持的级别，这是模型实际使用的降级级别，而不是您请求的级别。该对象与[状态行](/zh-CN/statusline#available-data) `effort` 字段匹配。存在于在工具使用上下文中触发的事件中，例如 `PreToolUse`、`PostToolUse`、`Stop` 和 `SubagentStop`，当当前模型支持努力参数时。该级别也可作为 `$CLAUDE_EFFORT` 环境变量提供给 hook 命令和 Bash 工具。 |
| `hook_event_name` | 触发的事件名称                                                                                                                                                                                                                                                                                                                                                                 |

使用 `--agent` 运行或在 subagent 内部时，包括两个额外字段：

| 字段           | 描述                                                                                                                                                                                                           |
| :----------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`   | Subagent 的唯一标识符。仅当 hook 在 subagent 调用内触发时存在。使用此来区分 subagent hook 调用和主线程调用。                                                                                                                                   |
| `agent_type` | 代理名称（例如，`"Explore"` 或 `"security-reviewer"`）。当会话使用 `--agent` 或 hook 在 subagent 内触发时存在。对于 subagents，subagent 的类型优先于会话的 `--agent` 值。对于[自定义 subagents](/zh-CN/sub-agents)，这是代理 frontmatter 中的 `name` 字段，而不是文件名。 |

仅[`SessionStart`](#sessionstart) hooks 接收 `model` 字段。没有 `$CLAUDE_MODEL` 环境变量。Hook 进程继承父环境，因此如果您在 shell 中设置了 `$ANTHROPIC_MODEL`，它可以读取该值，但当您在会话期间使用 `/model` 切换模型时，该值不会改变。

例如，Bash 命令的 `PreToolUse` hook 在 stdin 上接收：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

`tool_name` 和 `tool_input` 字段是事件特定的。每个[hook 事件](#hook-events)部分记录了该事件的额外字段。

### 退出代码输出

您的 hook 命令的退出代码告诉 Claude Code 操作是否应该继续、被阻止或被忽略。

**退出 0** 表示成功。Claude Code 解析 stdout 以获取[JSON 输出字段](#json-output)。JSON 输出仅在退出 0 时处理。对于大多数事件，stdout 被写入调试日志，但不显示在成绩单中。例外是 `UserPromptSubmit`、`UserPromptExpansion` 和 `SessionStart`，其中 stdout 作为 Claude 可以看到和作用的上下文添加。

**退出 2** 表示阻止错误。Claude Code 忽略 stdout 和其中的任何 JSON。相反，stderr 文本被反馈给 Claude 作为错误消息。效果取决于事件：`PreToolUse` 阻止工具调用，`UserPromptSubmit` 拒绝提示，等等。有关完整列表，请参阅[每个事件的退出代码 2 行为](#exit-code-2-behavior-per-event)。

**任何其他退出代码** 是大多数 hook 事件的非阻止错误。成绩单显示 `<hook name> hook error` 通知，然后是 stderr 的第一行，因此您可以在不使用 `--debug` 的情况下识别原因。执行继续，完整的 stderr 被写入调试日志。

例如，一个 hook 命令脚本，阻止危险的 Bash 命令：

```bash theme={null}
#!/bin/bash
# 从 stdin 读取 JSON 输入，检查命令
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # 阻止错误：工具调用被阻止
fi

exit 0  # 成功：工具调用继续
```

<Warning>
  对于大多数 hook 事件，仅退出代码 2 阻止操作。Claude Code 将退出代码 1 视为非阻止错误并继续操作，尽管 1 是传统的 Unix 失败代码。如果您的 hook 旨在强制执行策略，请使用 `exit 2`。例外是 `WorktreeCreate`，其中任何非零退出代码都会中止 worktree 创建。
</Warning>

#### 每个事件的退出代码 2 行为

退出代码 2 是 hook 发出"停止，不要这样做"的方式。效果取决于事件，因为某些事件代表可以被阻止的操作（如尚未发生的工具调用），而其他事件代表已经发生或无法防止的事情。

| Hook 事件               | 可以阻止？ | 退出 2 时发生的情况                                                                |
| :-------------------- | :---- | :------------------------------------------------------------------------- |
| `PreToolUse`          | 是     | 阻止工具调用                                                                     |
| `PermissionRequest`   | 是     | 拒绝权限                                                                       |
| `UserPromptSubmit`    | 是     | 阻止提示处理并从上下文中删除提示                                                           |
| `UserPromptExpansion` | 是     | 阻止扩展                                                                       |
| `Stop`                | 是     | 防止 Claude 停止，继续对话                                                          |
| `SubagentStop`        | 是     | 防止 subagent 停止                                                             |
| `TeammateIdle`        | 是     | 防止队友空闲（队友继续工作）                                                             |
| `TaskCreated`         | 是     | 回滚任务创建                                                                     |
| `TaskCompleted`       | 是     | 防止任务被标记为已完成                                                                |
| `ConfigChange`        | 是     | 阻止配置更改生效（除了 `policy_settings`）                                             |
| `StopFailure`         | 否     | 输出和退出代码被忽略                                                                 |
| `PostToolUse`         | 否     | 向 Claude 显示 stderr（工具已运行）                                                  |
| `PostToolUseFailure`  | 否     | 向 Claude 显示 stderr（工具已失败）                                                  |
| `PostToolBatch`       | 是     | 在下一个模型调用之前停止代理循环                                                           |
| `PermissionDenied`    | 否     | 退出代码和 stderr 被忽略（拒绝已发生）。使用 JSON `hookSpecificOutput.retry: true` 告诉模型它可能重试 |
| `Notification`        | 否     | 仅向用户显示 stderr                                                              |
| `SubagentStart`       | 否     | 仅向用户显示 stderr                                                              |
| `SessionStart`        | 否     | 仅向用户显示 stderr                                                              |
| `Setup`               | 否     | 仅向用户显示 stderr                                                              |
| `SessionEnd`          | 否     | 仅向用户显示 stderr                                                              |
| `CwdChanged`          | 否     | 仅向用户显示 stderr                                                              |
| `FileChanged`         | 否     | 仅向用户显示 stderr                                                              |
| `PreCompact`          | 是     | 阻止压缩                                                                       |
| `PostCompact`         | 否     | 仅向用户显示 stderr                                                              |
| `Elicitation`         | 是     | 拒绝 elicitation                                                             |
| `ElicitationResult`   | 是     | 阻止响应（操作变为 decline）                                                         |
| `WorktreeCreate`      | 是     | 任何非零退出代码都会导致 worktree 创建失败                                                 |
| `WorktreeRemove`      | 否     | 失败仅在调试模式下记录                                                                |
| `InstructionsLoaded`  | 否     | 退出代码被忽略                                                                    |

### HTTP 响应处理

HTTP hooks 使用 HTTP 状态代码和响应体而不是退出代码和 stdout：

* **2xx 带空体**：成功，等同于退出代码 0 且无输出
* **2xx 带纯文本体**：成功，文本作为上下文添加
* **2xx 带 JSON 体**：成功，使用与命令 hooks 相同的[JSON 输出](#json-output)架构解析
* **非 2xx 状态**：非阻止错误，执行继续
* **连接失败或超时**：非阻止错误，执行继续

与命令 hooks 不同，HTTP hooks 无法仅通过状态代码发出阻止错误信号。要阻止工具调用或拒绝权限，返回 2xx 响应，其 JSON 体包含适当的决定字段。

### JSON 输出

退出代码让您允许或阻止，但 JSON 输出提供更细粒度的控制。与其使用代码 2 退出来阻止，不如退出 0 并将 JSON 对象打印到 stdout。Claude Code 从该 JSON 读取特定字段以控制行为，包括[决定控制](#decision-control)以阻止、允许或升级给用户。

<Note>
  您必须为每个 hook 选择一种方法，而不是两种：要么单独使用退出代码进行信号传递，要么退出 0 并打印 JSON 以进行结构化控制。Claude Code 仅在退出 0 时处理 JSON。如果您退出 2，任何 JSON 都会被忽略。
</Note>

您的 hook 的 stdout 必须仅包含 JSON 对象。如果您的 shell 配置文件在启动时打印文本，它可能会干扰 JSON 解析。请参阅故障排除指南中的[JSON 验证失败](/zh-CN/hooks-guide#json-validation-failed)。

Hook 输出字符串，包括 `additionalContext`、`systemMessage` 和纯 stdout，上限为 10,000 个字符。超过此限制的输出被保存到文件并替换为预览和文件路径，与大型工具结果的处理方式相同。

JSON 对象支持三种字段：

* **通用字段**，如 `continue`，在所有事件中工作。这些列在下表中。
* **顶级 `decision` 和 `reason`** 由某些事件用于阻止或提供反馈。
* **`hookSpecificOutput`** 是一个嵌套对象，用于需要更丰富控制的事件。它需要一个设置为事件名称的 `hookEventName` 字段。

| 字段                 | 默认      | 描述                                                                                                                                         |
| :----------------- | :------ | :----------------------------------------------------------------------------------------------------------------------------------------- |
| `continue`         | `true`  | 如果为 `false`，Claude 在 hook 运行后完全停止处理。优先于任何事件特定的决定字段                                                                                         |
| `stopReason`       | 无       | 当 `continue` 为 `false` 时向用户显示的消息。不向 Claude 显示                                                                                              |
| `suppressOutput`   | `false` | 如果为 `true`，从调试日志中隐藏 stdout                                                                                                                 |
| `systemMessage`    | 无       | 向用户显示的警告消息                                                                                                                                 |
| `terminalSequence` | 无       | Claude Code 代表您发出的终端转义序列，例如桌面通知、窗口标题或响铃。限制为 OSC `0`/`1`/`2`/`9`/`99`/`777` 和 BEL。如果值包含允许列表之外的任何内容，该字段将被忽略。使用此而不是写入 `/dev/tty`，这对 hooks 不可用 |

要无论事件类型如何都完全停止 Claude：

```json theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

#### 发出终端通知

`terminalSequence` 字段需要 Claude Code v2.1.141 或更高版本。

Hooks 运行时没有控制终端，因此直接向 `/dev/tty` 写入转义序列会失败。相反，在 `terminalSequence` 字段中返回转义序列，Claude Code 通过其自己的终端写入路径为您发出它。这是无竞争的，在 tmux 和 GNU screen 内工作，并在 Windows 上工作，其中没有 `/dev/tty`。

该字段接受一个或多个允许列表转义序列的字符串：

* OSC `0`、`1`、`2`：窗口和图标标题
* OSC `9`：iTerm2、ConEmu、Windows Terminal 和 WezTerm 通知，包括 `9;4` 任务栏进度
* OSC `99`：Kitty 通知
* OSC `777`：urxvt、Ghostty 和 Warp 通知
* 裸 BEL

序列可以用 BEL 或 ST 终止。允许列表之外的任何内容，包括 CSI 光标和颜色序列、OSC 调色板序列、OSC 8 超链接、OSC 52 剪贴板写入和 OSC 1337，都会被拒绝，该字段将被忽略。

下面的示例从 `Notification` hook 触发桌面通知。转义序列使用 `printf` 八进制转义构建，因此控制字节永远不会出现在 shell 命令行上，`jq -n --arg` 构建 JSON 输出，因此通知消息中的引号、反斜杠和换行符被正确转义：

```bash theme={null}
#!/bin/bash
# Notification hook：当 Claude Code 需要注意时 ping 桌面。
input=$(cat)
title="Claude Code'
body=$(jq -r '.message // 'Needs your attention"' <<<"$input")
seq=$(printf '\033]777;notify;%s;%s\007' "$title" "$body")
jq -nc --arg seq "$seq" '{terminalSequence: $seq}'
```

`{ "terminalSequence": "..." }` 形状从任何 shell 或语言都相同。在 Windows 上，在 PowerShell 或脚本中构建转义字符串并发出相同的 JSON 对象。

<Note>
  `terminalSequence` 是之前直接向 `/dev/tty` 写入转义序列的 hooks 的受支持替代品。允许列表限制为无法移动光标或改变颜色的序列，因此 hook 永远无法破坏屏幕上的提示。
</Note>

#### 为 Claude 添加上下文

`additionalContext` 字段将来自您的 hook 的字符串传递到 Claude 的上下文窗口中。Claude Code 将字符串包装在系统提醒中，并将其插入到 hook 触发的对话点。Claude 在下一个模型请求时读取提醒，但它不会在界面中显示为聊天消息。

在 `hookSpecificOutput` 中返回 `additionalContext` 以及事件名称：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "This file is generated. Edit src/schema.ts and run `bun generate` instead."
  }
}
```

提醒出现的位置取决于事件：

* [SessionStart](#sessionstart)、[Setup](#setup) 和 [SubagentStart](#subagentstart)：在对话开始，在第一个提示之前
* [UserPromptSubmit](#userpromptsubmit) 和 [UserPromptExpansion](#userpromptexpansion)：与提交的提示一起
* [PreToolUse](#pretooluse)、[PostToolUse](#posttooluse)、[PostToolUseFailure](#posttoolusefailure) 和 [PostToolBatch](#posttoolbatch)：在工具结果旁边

当多个 hooks 为同一事件返回 `additionalContext` 时，Claude 接收所有值。如果值超过 10,000 个字符，Claude Code 将完整文本写入会话目录中的文件，并将 Claude 传递文件路径以及简短预览。

使用 `additionalContext` 来获取 Claude 应该了解的有关您的环境当前状态或刚刚运行的操作的信息：

* **环境状态**：当前分支、部署目标或活跃的功能标志
* **条件项目规则**：哪个测试命令适用于刚刚编辑的文件，哪些目录在此 worktree 中是只读的
* **外部数据**：分配给您的开放问题、最近的 CI 结果、从内部服务获取的内容

对于永不改变的说明，更倾向于[CLAUDE.md](/zh-CN/memory)。它加载时无需运行脚本，是静态项目约定的标准位置。

将文本写成事实陈述而不是命令式系统指令。措辞如"部署目标是生产"或"此 repo 使用 `bun test`"读作项目信息。框架为带外系统命令的文本可能会触发 Claude 的提示注入防御，这会导致 Claude 将文本呈现给您，而不是将其视为上下文。

一旦注入，文本就会保存在会话成绩单中。对于 `PostToolUse` 或 `UserPromptSubmit` 等中期事件，使用 `--continue` 或 `--resume` 恢复会重放保存的文本，而不是为过去的轮次重新运行 hook，因此时间戳或提交 SHA 等值在恢复时变得陈旧。`SessionStart` hooks 在使用 `source` 设置为 `"resume"` 的 `--resume` 恢复时再次运行，因此它们可以刷新其上下文。

#### 决定控制

并非每个事件都支持通过 JSON 阻止或控制行为。支持的事件各自使用不同的字段集来表达该决定。在编写 hook 之前，使用此表作为快速参考：

| 事件                                                                                                                          | 决定模式                    | 关键字段                                                                                               |
| :-------------------------------------------------------------------------------------------------------------------------- | :---------------------- | :------------------------------------------------------------------------------------------------- |
| UserPromptSubmit、UserPromptExpansion、PostToolUse、PostToolUseFailure、PostToolBatch、Stop、SubagentStop、ConfigChange、PreCompact | 顶级 `decision`           | `decision: "block"`、`reason`                                                                       |
| TeammateIdle、TaskCreated、TaskCompleted                                                                                      | 退出代码或 `continue: false` | 退出代码 2 使用 stderr 反馈阻止操作。JSON `{"continue": false, "stopReason": "..."}` 也会完全停止队友，匹配 `Stop` hook 行为 |
| PreToolUse                                                                                                                  | `hookSpecificOutput`    | `permissionDecision`（allow/deny/ask/defer）、`permissionDecisionReason`                              |
| PermissionRequest                                                                                                           | `hookSpecificOutput`    | `decision.behavior`（allow/deny）                                                                    |
| PermissionDenied                                                                                                            | `hookSpecificOutput`    | `retry: true` 告诉模型它可能重试被拒绝的工具调用                                                                    |
| WorktreeCreate                                                                                                              | 路径返回                    | 命令 hook 在 stdout 上打印路径；HTTP hook 通过 `hookSpecificOutput.worktreePath` 返回。Hook 失败或缺少路径会导致创建失败       |
| Elicitation                                                                                                                 | `hookSpecificOutput`    | `action`（accept/decline/cancel）、`content`（form 字段值用于 accept）                                       |
| ElicitationResult                                                                                                           | `hookSpecificOutput`    | `action`（accept/decline/cancel）、`content`（form 字段值覆盖）                                              |
| WorktreeRemove、Notification、SessionEnd、PostCompact、InstructionsLoaded、StopFailure、CwdChanged、FileChanged                    | 无                       | 无决定控制。用于日志记录或清理等副作用                                                                                |

以下是每种模式的实际示例：

<Tabs>
  <Tab title="顶级决定">
    由 `UserPromptSubmit`、`UserPromptExpansion`、`PostToolUse`、`PostToolUseFailure`、`PostToolBatch`、`Stop`、`SubagentStop`、`ConfigChange` 和 `PreCompact` 使用。唯一的值是 `"block"`。要允许操作继续，从您的 JSON 中省略 `decision`，或退出 0 而不带任何 JSON：

    ```json theme={null}
    {
      "decision": "block",
      "reason": "Test suite must pass before proceeding"
    }
    ```
  </Tab>

  <Tab title="PreToolUse">
    使用 `hookSpecificOutput` 以获得更丰富的控制：允许、拒绝或升级给用户。您还可以在运行前修改工具输入或为 Claude 注入额外上下文。有关完整的选项集，请参阅[PreToolUse 决定控制](#pretooluse-decision-control)。

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Database writes are not allowed"
      }
    }
    ```
  </Tab>

  <Tab title="PermissionRequest">
    使用 `hookSpecificOutput` 代表用户允许或拒绝权限请求。允许时，您还可以修改工具的输入或应用权限规则，以便用户不会再次被提示。有关完整的选项集，请参阅[PermissionRequest 决定控制](#permissionrequest-decision-control)。

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PermissionRequest",
        "decision": {
          "behavior": "allow",
          "updatedInput": {
            "command": "npm run lint"
          }
        }
      }
    }
    ```
  </Tab>
</Tabs>

有关扩展示例，包括 Bash 命令验证、提示过滤和自动批准脚本，请参阅指南中的[您可以自动化的内容](/zh-CN/hooks-guide#what-you-can-automate)以及[Bash 命令验证器参考实现](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)。

## Hook 事件

每个事件对应于 Claude Code 生命周期中 hooks 可以运行的一个点。下面的部分按照生命周期排序：从会话设置通过代理循环到会话结束。每个部分描述事件何时触发、它支持的匹配器、它接收的 JSON 输入以及如何通过输出控制行为。

### SessionStart

在 Claude Code 启动新会话或恢复现有会话时运行。用于加载开发上下文，如现有问题或代码库的最近更改，或设置环境变量。对于不需要脚本的静态上下文，请改用[CLAUDE.md](/zh-CN/memory)。

SessionStart 在每个会话上运行，因此保持这些 hooks 快速。仅支持 `type: "command"` 和 `type: "mcp_tool"` hooks。

匹配器值对应于会话的启动方式：

| 匹配器       | 何时触发                                |
| :-------- | :---------------------------------- |
| `startup` | 新会话                                 |
| `resume`  | `--resume`、`--continue` 或 `/resume` |
| `clear`   | `/clear`                            |
| `compact` | 自动或手动压缩                             |

#### SessionStart 输入

除了[通用输入字段](#common-input-fields)外，SessionStart hooks 还接收 `source`、`model` 和可选的 `agent_type`。`source` 字段指示会话如何启动：新会话为 `"startup"`，恢复会话为 `"resume"`，`/clear` 后为 `"clear"`，压缩后为 `"compact"`。`model` 字段包含模型标识符。如果您使用 `claude --agent <name>` 启动 Claude Code，`agent_type` 字段包含代理名称。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

#### SessionStart 决定控制

您的 hook 脚本打印到 stdout 的任何文本都作为 Claude 的上下文添加。除了所有 hooks 可用的[JSON 输出字段](#json-output)外，您还可以返回这些事件特定字段：

| 字段                  | 描述                                                                                                        |
| :------------------ | :-------------------------------------------------------------------------------------------------------- |
| `additionalContext` | 添加到 Claude 上下文开始处的字符串，在第一个提示之前。请参阅[为 Claude 添加上下文](#add-context-for-claude)了解文本如何传递、放入什么内容以及恢复的会话如何处理过去的值 |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Current branch: feat/auth-refactor\nUncommitted changes: src/auth.ts, src/login.tsx\nActive issue: #4211 Migrate to OAuth2"
  }
}
```

由于纯 stdout 已经为此事件到达 Claude，仅加载上下文的 hook 可以直接打印到 stdout 而无需构建 JSON。当您需要将上下文与其他字段（如 `suppressOutput`）结合时，使用 JSON 形式。

#### 持久化环境变量

SessionStart hooks 可以访问 `CLAUDE_ENV_FILE` 环境变量，该变量提供一个文件路径，您可以在其中为后续 Bash 命令持久化环境变量。

要设置单个环境变量，请将 `export` 语句写入 `CLAUDE_ENV_FILE`。使用追加（`>>`）来保留由其他 hooks 设置的变量：

```bash theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

要捕获设置命令中的所有环境更改，请比较之前和之后导出的变量：

```bash theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# 运行修改环境的设置命令
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

写入此文件的任何变量都将在会话期间 Claude Code 执行的所有后续 Bash 命令中可用。

<Note>
  `CLAUDE_ENV_FILE` 可用于 SessionStart、[Setup](#setup)、[CwdChanged](#cwdchanged) 和 [FileChanged](#filechanged) hooks。其他 hook 类型无法访问此变量。
</Note>

### Setup

仅当您使用 `--init-only` 启动 Claude Code，或在打印模式（`-p`）中使用 `--init` 或 `--maintenance` 时触发。它不在正常启动时触发。使用它进行一次性依赖安装或您从 CI 或脚本显式触发的计划清理，与正常会话启动分开。对于每个会话的初始化，请改用[SessionStart](#sessionstart)。

匹配器值对应于触发 hook 的 CLI 标志：

| 匹配器           | 何时触发                                      |
| :------------ | :---------------------------------------- |
| `init`        | `claude --init-only` 或 `claude -p --init` |
| `maintenance` | `claude -p --maintenance`                 |

`--init-only` 运行 Setup hooks 和 SessionStart hooks（带 `startup` 匹配器），然后退出而不启动对话。`--init` 和 `--maintenance` 仅在与 `-p`（打印模式）结合时触发 Setup hooks；在交互式会话中，这两个标志目前不触发 Setup hooks。

因为 Setup 不在每次启动时触发，需要安装依赖的插件不能仅依赖 Setup。实际的模式是在首次使用时检查依赖，如果缺失则安装，例如测试 `${CLAUDE_PLUGIN_DATA}/node_modules` 的 hook 或 skill，如果不存在则运行 `npm install`。请参阅[持久数据目录](/zh-CN/plugins-reference#persistent-data-directory)了解在何处存储已安装的依赖。

#### Setup 输入

除了[通用输入字段](#common-input-fields)外，Setup hooks 还接收一个 `trigger` 字段，设置为 `"init"` 或 `"maintenance"`：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Setup",
  "trigger": "init"
}
```

#### Setup 决定控制

Setup hooks 无法阻止。退出代码 2 时，stderr 向用户显示；任何其他非零退出代码时，stderr 仅在您使用 `--verbose` 启动时出现。在两种情况下，执行都继续。要将信息传入 Claude 的上下文，在 JSON 输出中返回 `additionalContext`；纯 stdout 仅写入调试日志。除了所有 hooks 可用的[JSON 输出字段](#json-output)外，您还可以返回这些事件特定字段：

| 字段                  | 描述                                |
| :------------------ | :-------------------------------- |
| `additionalContext` | 添加到 Claude 上下文的字符串。多个 hooks 的值被连接 |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Setup",
    "additionalContext": "Dependencies installed: node_modules, .venv"
  }
}
```

Setup hooks 可以访问 `CLAUDE_ENV_FILE`。写入该文件的变量持久化到会话的后续 Bash 命令中，就像在[SessionStart hooks](#persist-environment-variables)中一样。仅支持 `type: "command"` 和 `type: "mcp_tool"` hooks。

### InstructionsLoaded

当 `CLAUDE.md` 或 `.claude/rules/*.md` 文件加载到上下文中时触发。此事件在会话启动时为急切加载的文件触发，稍后当文件被懒加载时再次触发，例如当 Claude 访问包含嵌套 `CLAUDE.md` 的子目录或条件规则与 `paths:` frontmatter 匹配时。该 hook 不支持阻止或决定控制。它异步运行以用于可观测性目的。

匹配器针对 `load_reason` 运行。例如，使用 `"matcher": "session_start"` 仅对会话启动时加载的文件触发，或使用 `"matcher": "path_glob_match|nested_traversal"` 仅对懒加载触发。

#### InstructionsLoaded 输入

除了[通用输入字段](#common-input-fields)外，InstructionsLoaded hooks 还接收这些字段：

| 字段                  | 描述                                                                                                                           |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------- |
| `file_path`         | 加载的指令文件的绝对路径                                                                                                                 |
| `memory_type`       | 文件的范围：`"User"`、`"Project"`、`"Local"` 或 `"Managed"`                                                                           |
| `load_reason`       | 文件被加载的原因：`"session_start"`、`"nested_traversal"`、`"path_glob_match"`、`"include"` 或 `"compact"`。`"compact"` 值在压缩事件后重新加载指令文件时触发 |
| `globs`             | 文件 `paths:` frontmatter 中的路径 glob 模式（如果有）。仅对 `path_glob_match` 加载存在                                                          |
| `trigger_file_path` | 触发此加载的文件的路径，用于懒加载                                                                                                            |
| `parent_file_path`  | 包含此文件的父指令文件的路径，用于 `include` 加载                                                                                               |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

#### InstructionsLoaded 决定控制

InstructionsLoaded hooks 没有决定控制。它们无法阻止或修改指令加载。使用此事件进行审计日志记录、合规性跟踪或可观测性。

### UserPromptSubmit

在用户提交提示时运行，在 Claude 处理之前。这允许您根据提示/对话添加额外上下文、验证提示或阻止某些类型的提示。

`UserPromptSubmit` hooks 对 `command`、`http` 和 `mcp_tool` 类型的默认超时为 30 秒，比这些类型在其他事件上的 600 秒默认值更短。因为此 hook 在每个提示之前运行并阻止模型处理直到完成，卡住的 hook 会停滞会话。如果您的 hook 需要更多时间，在 hook 条目中设置 `timeout` 字段。

#### UserPromptSubmit 输入

除了[通用输入字段](#common-input-fields)外，UserPromptSubmit hooks 还接收包含用户提交的文本的 `prompt` 字段。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

#### UserPromptSubmit 决定控制

`UserPromptSubmit` hooks 可以控制用户提示是否被处理并添加上下文。所有[JSON 输出字段](#json-output)都可用。

有两种方法可以在退出代码 0 时向对话添加上下文：

* **纯文本 stdout**：写入 stdout 的任何非 JSON 文本都作为上下文添加
* **带 `additionalContext` 的 JSON**：使用下面的 JSON 格式以获得更多控制。`additionalContext` 字段作为上下文添加

纯 stdout 在成绩单中显示为 hook 输出。`additionalContext` 字段更谨慎地添加。

要阻止提示，返回一个 JSON 对象，其中 `decision` 设置为 `"block"`：

| 字段                  | 描述                                                                       |
| :------------------ | :----------------------------------------------------------------------- |
| `decision`          | `"block"` 防止提示被处理并从上下文中删除。省略以允许提示继续                                      |
| `reason`            | 当 `decision` 为 `"block"` 时向用户显示。不添加到上下文                                  |
| `additionalContext` | 添加到 Claude 上下文的字符串，与提交的提示一起。请参阅[为 Claude 添加上下文](#add-context-for-claude) |
| `sessionTitle`      | 设置会话标题。使用此根据提示内容自动命名会话                                                   |

```json theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here",
    "sessionTitle": "My session title"
  }
}
```

<Note>
  JSON 格式对于简单用例不是必需的。要添加上下文，您可以使用退出代码 0 将纯文本打印到 stdout。当您需要阻止提示或想要更结构化的控制时，使用 JSON。
</Note>

### UserPromptExpansion

当用户输入的斜杠命令在到达 Claude 之前展开为提示时运行。使用此来阻止特定命令的直接调用、为特定 skill 注入上下文或记录用户调用哪些命令。例如，匹配 `deploy` 的 hook 可以阻止 `/deploy`，除非存在批准文件，或匹配审查 skill 的 hook 可以将团队的审查清单附加为 `additionalContext`。

此事件涵盖 `PreToolUse` 不涵盖的路径：匹配 `Skill` 工具的 `PreToolUse` hook 仅在 Claude 调用工具时触发，但直接输入 `/skillname` 绕过 `PreToolUse`。`UserPromptExpansion` 在该直接路径上触发。

在 `command_name` 上匹配。留空匹配器以对每个提示类型斜杠命令触发。

#### UserPromptExpansion 输入

除了[通用输入字段](#common-input-fields)外，UserPromptExpansion hooks 还接收 `expansion_type`、`command_name`、`command_args`、`command_source` 和原始 `prompt` 字符串。`expansion_type` 字段对于 skill 和自定义命令为 `slash_command`，或对于 MCP 服务器提示为 `mcp_prompt`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../00893aaf.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptExpansion",
  "expansion_type": "slash_command",
  "command_name": "example-skill",
  "command_args": "arg1 arg2",
  "command_source": "plugin",
  "prompt": "/example-skill arg1 arg2"
}
```

#### UserPromptExpansion 决定控制

`UserPromptExpansion` hooks 可以阻止展开或添加上下文。所有[JSON 输出字段](#json-output)都可用。

| 字段                  | 描述                                                                       |
| :------------------ | :----------------------------------------------------------------------- |
| `decision`          | `"block"` 防止斜杠命令展开。省略以允许它继续                                              |
| `reason`            | 当 `decision` 为 `"block"` 时向用户显示                                          |
| `additionalContext` | 添加到 Claude 上下文的字符串，与展开的提示一起。请参阅[为 Claude 添加上下文](#add-context-for-claude) |

```json theme={null}
{
  "decision": "block",
  "reason": "This slash command is not available",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptExpansion",
    "additionalContext": "Additional context for this expansion"
  }
}
```

### PreToolUse

在 Claude 创建工具参数后和处理工具调用之前运行。在工具名称上匹配：`Bash`、`Edit`、`Write`、`Read`、`Glob`、`Grep`、`Agent`、`WebFetch`、`WebSearch`、`AskUserQuestion`、`ExitPlanMode` 和任何[MCP 工具名称](#match-mcp-tools)。

使用[PreToolUse 决定控制](#pretooluse-decision-control)来允许、拒绝、询问或延迟工具调用。

#### PreToolUse 输入

除了[通用输入字段](#common-input-fields)外，PreToolUse hooks 还接收 `tool_name`、`tool_input` 和 `tool_use_id`。`tool_input` 字段取决于工具：

##### Bash

执行 shell 命令。

| 字段                  | 类型      | 示例                 | 描述            |
| :------------------ | :------ | :----------------- | :------------ |
| `command`           | string  | `"npm test"`       | 要执行的 shell 命令 |
| `description`       | string  | `"Run test suite"` | 命令执行操作的可选描述   |
| `timeout`           | number  | `120000`           | 可选超时（毫秒）      |
| `run_in_background` | boolean | `false`            | 是否在后台运行命令     |

##### Write

创建或覆盖文件。

| 字段          | 类型     | 示例                    | 描述          |
| :---------- | :----- | :-------------------- | :---------- |
| `file_path` | string | `"/path/to/file.txt"` | 要写入的文件的绝对路径 |
| `content`   | string | `"file content"`      | 要写入文件的内容    |

##### Edit

替换现有文件中的字符串。

| 字段            | 类型      | 示例                    | 描述          |
| :------------ | :------ | :-------------------- | :---------- |
| `file_path`   | string  | `"/path/to/file.txt"` | 要编辑的文件的绝对路径 |
| `old_string`  | string  | `"original text"`     | 要查找和替换的文本   |
| `new_string`  | string  | `"replacement text"`  | 替换文本        |
| `replace_all` | boolean | `false`               | 是否替换所有出现    |

##### Read

读取文件内容。

| 字段          | 类型     | 示例                    | 描述          |
| :---------- | :----- | :-------------------- | :---------- |
| `file_path` | string | `"/path/to/file.txt"` | 要读取的文件的绝对路径 |
| `offset`    | number | `10`                  | 可选的开始读取的行号  |
| `limit`     | number | `50`                  | 可选的要读取的行数   |

##### Glob

查找与 glob 模式匹配的文件。

| 字段        | 类型     | 示例               | 描述                |
| :-------- | :----- | :--------------- | :---------------- |
| `pattern` | string | `"**/*.ts"`      | 要匹配文件的 Glob 模式    |
| `path`    | string | `"/path/to/dir"` | 可选的搜索目录。默认为当前工作目录 |

##### Grep

使用正则表达式搜索文件内容。

| 字段            | 类型      | 示例               | 描述                                                                        |
| :------------ | :------ | :--------------- | :------------------------------------------------------------------------ |
| `pattern`     | string  | `"TODO.*fix"`    | 要搜索的正则表达式模式                                                               |
| `path`        | string  | `"/path/to/dir"` | 可选的要搜索的文件或目录                                                              |
| `glob`        | string  | `"*.ts"`         | 可选的 glob 模式以过滤文件                                                          |
| `output_mode` | string  | `"content"`      | `"content"`、`"files_with_matches"` 或 `"count"`。默认为 `"files_with_matches"` |
| `-i`          | boolean | `true`           | 不区分大小写的搜索                                                                 |
| `multiline`   | boolean | `false`          | 启用多行匹配                                                                    |

##### WebFetch

获取和处理 web 内容。

| 字段       | 类型     | 示例                            | 描述           |
| :------- | :----- | :---------------------------- | :----------- |
| `url`    | string | `"https://example.com/api"`   | 要获取内容的 URL   |
| `prompt` | string | `"Extract the API endpoints"` | 在获取的内容上运行的提示 |

##### WebSearch

搜索网络。

| 字段                | 类型     | 示例                             | 描述             |
| :---------------- | :----- | :----------------------------- | :------------- |
| `query`           | string | `"react hooks best practices"` | 搜索查询           |
| `allowed_domains` | array  | `["docs.example.com"]`         | 可选：仅包含来自这些域的结果 |
| `blocked_domains` | array  | `["spam.example.com"]`         | 可选：排除来自这些域的结果  |

##### Agent

生成一个[subagent](/zh-CN/sub-agents)。

| 字段              | 类型     | 示例                         | 描述            |
| :-------------- | :----- | :------------------------- | :------------ |
| `prompt`        | string | `"Find all API endpoints"` | 代理要执行的任务      |
| `description`   | string | `"Find API endpoints"`     | 任务的简短描述       |
| `subagent_type` | string | `"Explore"`                | 要使用的专门代理的类型   |
| `model`         | string | `"sonnet"`                 | 可选的模型别名以覆盖默认值 |

在 `PostToolUse` 中，已完成的 Agent 调用的 `tool_response` 携带 subagent 的最终文本以及使用遥测。读取这些字段以从 hook 记录每个 subagent 的成本：

| 字段                  | 类型     | 示例                                                    | 描述                                                                                              |
| :------------------ | :----- | :---------------------------------------------------- | :---------------------------------------------------------------------------------------------- |
| `status`            | string | `"completed"`                                         | 同步调用为 `"completed"`，`run_in_background: true` 为 `"async_launched"`                              |
| `agentId`           | string | `"a4d2c8f1e0b3a297"`                                  | subagent 运行的标识符                                                                                 |
| `content`           | array  | `[{"type": "text", "text": "Found 12 endpoints..."}]` | subagent 的最终文本块                                                                                 |
| `totalTokens`       | number | `12450`                                               | 在 subagent 轮次中计费的总令牌数                                                                           |
| `totalDurationMs`   | number | `48211`                                               | subagent 运行的挂钟时间                                                                                |
| `totalToolUseCount` | number | `7`                                                   | subagent 进行的工具调用计数                                                                              |
| `usage`             | object | `{"input_tokens": 8320, ...}`                         | 按类型的令牌分解：`input_tokens`、`output_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens` |

对于 `run_in_background: true` 调用，工具在启动 subagent 后立即返回，因此 `tool_response` 不携带使用字段。它具有 `status: "async_launched"`、`agentId`、`description`、`prompt` 和 `outputFile`。

##### AskUserQuestion

向用户提出一到四个多选题。

| 字段          | 类型     | 示例                                                                                                                 | 描述                                                                         |
| :---------- | :----- | :----------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `questions` | array  | `[{"question": "Which framework?", "header": "Framework", "options": [{"label": "React"}], "multiSelect": false}]` | 要呈现的问题，每个都有 `question` 字符串、短 `header`、`options` 数组和可选的 `multiSelect` 标志    |
| `answers`   | object | `{"Which framework?": "React"}`                                                                                    | 可选。将问题文本映射到选定的选项标签。多选答案用逗号连接标签。Claude 不设置此字段；通过 `updatedInput` 提供它以以编程方式回答 |

##### ExitPlanMode

呈现一个计划并要求用户在 Claude 离开[Plan Mode](/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)之前批准它。Claude 在调用工具之前将计划写入磁盘上的文件，因此来自模型的字面 `tool_input` 仅携带 `allowedPrompts`。Claude Code 在将输入传递给 hooks 之前注入计划内容和文件路径。

| 字段               | 类型     | 示例                                          | 描述                                                       |
| :--------------- | :----- | :------------------------------------------ | :------------------------------------------------------- |
| `plan`           | string | `"## Refactor auth\n1. Extract..."`         | Markdown 中的计划内容。从磁盘上的计划文件注入                              |
| `planFilePath`   | string | `"/Users/.../plans/refactor-auth.md"`       | 计划文件的路径。注入                                               |
| `allowedPrompts` | array  | `[{"tool": "Bash", "prompt": "run tests"}]` | 可选。Claude 请求实现计划的基于提示的权限，每个都有 `tool` 名称和描述操作类别的 `prompt` |

在 `PostToolUse` 中，`tool_response` 是一个对象，具有 `plan` 和 `filePath` 字段，保存批准的计划，加上内部状态标志。读取 `tool_response.plan` 以获取计划内容，而不是从磁盘重新读取文件。

#### PreToolUse 决定控制

`PreToolUse` hooks 可以控制工具调用是否继续。与使用顶级 `decision` 字段的其他 hooks 不同，PreToolUse 在 `hookSpecificOutput` 对象内返回其决定。这给了它更丰富的控制：四个结果（允许、拒绝、询问或延迟）加上在执行前修改工具输入的能力。

| 字段                         | 描述                                                                                                                                           |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissionDecision`       | `"allow"` 绕过权限提示。`"deny"` 防止工具调用。`"ask"` 提示用户确认。`"defer"` 优雅地退出，以便工具稍后可以恢复。[拒绝和询问规则](/zh-CN/permissions#manage-permissions)在 hook 返回什么时仍然被评估 |
| `permissionDecisionReason` | 对于 `"allow"` 和 `"ask"`，向用户显示但不向 Claude 显示。对于 `"deny"`，向 Claude 显示。对于 `"defer"`，被忽略                                                           |
| `updatedInput`             | 在执行前修改工具的输入参数。替换整个输入对象，因此包括未修改的字段以及修改后的字段。与 `"allow"` 结合以自动批准，或与 `"ask"` 结合以向用户显示修改后的输入。对于 `"defer"`，被忽略                                     |
| `additionalContext`        | 在工具执行前添加到 Claude 上下文的字符串。对于 `"defer"`，被忽略。请参阅[为 Claude 添加上下文](#add-context-for-claude)                                                       |

当多个 PreToolUse hooks 返回不同的决定时，优先级是 `deny` > `defer` > `ask` > `allow`。

当 hook 返回 `"ask"` 时，向用户显示的权限提示包括一个标签，标识 hook 来自何处：例如，`[User]`、`[Project]`、`[Plugin]` 或 `[Local]`。这帮助用户了解哪个配置源正在请求确认。

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

`AskUserQuestion` 和 `ExitPlanMode` 需要用户交互，通常在[非交互模式](/zh-CN/headless)中使用 `-p` 标志时阻止。返回 `permissionDecision: "allow"` 以及 `updatedInput` 满足该要求：hook 从 stdin 读取工具的输入，通过您自己的 UI 收集答案，并在 `updatedInput` 中返回它，以便工具运行而不提示。仅返回 `"allow"` 对这些工具不足够。对于 `AskUserQuestion`，回显原始 `questions` 数组并添加一个[`answers`](#askuserquestion)对象，将每个问题的文本映射到选定的答案。

<Note>
  PreToolUse 之前使用顶级 `decision` 和 `reason` 字段，但这些对此事件已弃用。改用 `hookSpecificOutput.permissionDecision` 和 `hookSpecificOutput.permissionDecisionReason`。已弃用的值 `"approve"` 和 `"block"` 映射到 `"allow"` 和 `"deny"`。PostToolUse 和 Stop 等其他事件继续使用顶级 `decision` 和 `reason` 作为其当前格式。
</Note>

#### 延迟工具调用以供稍后使用

`"defer"` 用于运行 `claude -p` 作为子进程并读取其 JSON 输出的集成，例如 Agent SDK 应用或构建在 Claude Code 之上的自定义 UI。它让该调用进程在工具调用处暂停 Claude，通过其自己的界面收集输入，并从中断处恢复。Claude Code 仅在[非交互模式](/zh-CN/headless)中使用 `-p` 标志时遵守此值。在交互式会话中，它记录警告并忽略 hook 结果。

<Note>
  `defer` 值需要 Claude Code v2.1.89 或更高版本。早期版本不识别它，工具通过正常权限流程进行。
</Note>

`AskUserQuestion` 工具是典型情况：Claude 想要询问用户一些事情，但没有终端来回答。往返工作如下：

1. Claude 调用 `AskUserQuestion`。`PreToolUse` hook 触发。
2. Hook 返回 `permissionDecision: "defer"`。工具不执行。进程以 `stop_reason: "tool_deferred"` 退出，待处理的工具调用保留在成绩单中。
3. 调用进程从 SDK 结果读取 `deferred_tool_use`，在其自己的 UI 中显示问题，并等待答案。
4. 调用进程运行 `claude -p --resume <session-id>`。相同的工具调用再次触发 `PreToolUse`。
5. Hook 返回 `permissionDecision: "allow"` 和 `updatedInput` 中的答案。工具执行，Claude 继续。

`deferred_tool_use` 字段携带工具的 `id`、`name` 和 `input`。`input` 是 Claude 为工具调用生成的参数，在执行前捕获：

```json theme={null}
{
  "type": "result",
  "subtype": "success",
  "stop_reason": "tool_deferred",
  "session_id": "abc123",
  "deferred_tool_use": {
    "id": "toolu_01abc",
    "name": "AskUserQuestion",
    "input": { "questions": [{ "question": "Which framework?", "header": "Framework", "options": [{"label": "React"}, {"label": "Vue"}], "multiSelect": false }] }
  }
}
```

没有超时或重试限制。会话保留在磁盘上，直到您恢复它，受到 [`cleanupPeriodDays`](/zh-CN/settings#available-settings) 保留扫描的约束，该扫描默认在 30 天后删除会话文件。如果恢复时答案还没有准备好，hook 可以再次返回 `"defer"`，进程以相同的方式退出。调用进程控制何时通过最终返回 `"allow"` 或 `"deny"` 从 hook 中断循环。

`"defer"` 仅在 Claude 在轮次中进行单个工具调用时有效。如果 Claude 一次进行多个工具调用，`"defer"` 被忽略并显示警告，工具通过正常权限流程进行。约束存在是因为恢复只能重新运行一个工具：没有办法延迟一个调用而不留下其他调用未解决。

如果恢复时延迟的工具不再可用，进程以 `stop_reason: "tool_deferred_unavailable"` 和 `is_error: true` 退出，在 hook 触发之前。这发生在为恢复的会话未连接提供工具的 MCP 服务器时。`deferred_tool_use` 有效负载仍然包括，以便您可以识别哪个工具丢失。

<Note>
  `--resume` 恢复工具被延迟时活跃的权限模式，因此您不需要再次传递 `--permission-mode`。例外是 `plan` 和 `bypassPermissions`，它们永远不会被携带。在恢复时显式传递 `--permission-mode` 会覆盖恢复的值。
</Note>

### PermissionRequest

在向用户显示权限对话框时运行。使用[PermissionRequest 决定控制](#permissionrequest-decision-control)代表用户允许或拒绝。

在工具名称上匹配，与 PreToolUse 相同的值。

#### PermissionRequest 输入

PermissionRequest hooks 接收 `tool_name` 和 `tool_input` 字段，如 PreToolUse hooks，但没有 `tool_use_id`。可选的 `permission_suggestions` 数组包含用户通常在权限对话框中看到的"总是允许"选项。区别在于 hook 何时触发：PermissionRequest hooks 在权限对话框即将显示给用户时运行，而 PreToolUse hooks 在工具执行前运行，无论权限状态如何。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Remove node_modules directory"
  },
  "permission_suggestions": [
    {
      "type": "addRules",
      "rules": [{ "toolName": "Bash", "ruleContent": "rm -rf node_modules" }],
      "behavior": "allow",
      "destination": "localSettings"
    }
  ]
}
```

#### PermissionRequest 决定控制

`PermissionRequest` hooks 可以允许或拒绝权限请求。除了所有 hooks 可用的[JSON 输出字段](#json-output)外，您的 hook 脚本可以返回一个 `decision` 对象，其中包含这些事件特定字段：

| 字段                   | 描述                                                                                                                  |
| :------------------- | :------------------------------------------------------------------------------------------------------------------ |
| `behavior`           | `"allow"` 授予权限，`"deny"` 拒绝它。[拒绝和询问规则](/zh-CN/permissions#manage-permissions)仍然被评估，所以返回 `"allow"` 的 hook 不会覆盖匹配的拒绝规则 |
| `updatedInput`       | 仅对 `"allow"`：在执行前修改工具的输入参数。替换整个输入对象，因此包括未修改的字段以及修改后的字段。修改后的输入会重新针对拒绝和询问规则进行评估                                       |
| `updatedPermissions` | 仅对 `"allow"`：应用权限规则更新的[权限更新条目](#permission-update-entries)数组，例如添加允许规则或更改会话权限模式                                      |
| `message`            | 仅对 `"deny"`：告诉 Claude 为什么权限被拒绝                                                                                      |
| `interrupt`          | 仅对 `"deny"`：如果为 `true`，停止 Claude                                                                                    |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

#### 权限更新条目

`updatedPermissions` 输出字段和[`permission_suggestions` 输入字段](#permissionrequest-input)都使用相同的条目对象数组。每个条目都有一个 `type` 来确定其其他字段，以及一个 `destination` 来控制更改的写入位置。

| `type`              | 字段                               | 效果                                                                                                                   |
| :------------------ | :------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| `addRules`          | `rules`、`behavior`、`destination` | 添加权限规则。`rules` 是 `{toolName, ruleContent?}` 对象的数组。省略 `ruleContent` 以匹配整个工具。`behavior` 是 `"allow"`、`"deny"` 或 `"ask"` |
| `replaceRules`      | `rules`、`behavior`、`destination` | 用提供的 `rules` 替换 `destination` 处给定 `behavior` 的所有规则                                                                   |
| `removeRules`       | `rules`、`behavior`、`destination` | 移除给定 `behavior` 的匹配规则                                                                                                |
| `setMode`           | `mode`、`destination`             | 更改权限模式。有效模式为 `default`、`acceptEdits`、`dontAsk`、`bypassPermissions` 和 `plan`                                          |
| `addDirectories`    | `directories`、`destination`      | 添加工作目录。`directories` 是路径字符串的数组                                                                                       |
| `removeDirectories` | `directories`、`destination`      | 移除工作目录                                                                                                               |

<Note>
  `setMode` 与 `bypassPermissions` 仅在会话已启动时生效，绕过模式已可用：`--dangerously-skip-permissions`、`--permission-mode bypassPermissions`、`--allow-dangerously-skip-permissions` 或设置中的 `permissions.defaultMode: "bypassPermissions"`，且模式未被 [`permissions.disableBypassPermissionsMode`](/zh-CN/permissions#managed-settings) 禁用。否则更新是无操作。`bypassPermissions` 无论 `destination` 如何都永远不会作为 `defaultMode` 持久化。
</Note>

每个条目上的 `destination` 字段确定更改是保留在内存中还是持久化到设置文件。

| `destination`     | 写入                            |
| :---------------- | :---------------------------- |
| `session`         | 仅在内存中，会话结束时丢弃                 |
| `localSettings`   | `.claude/settings.local.json` |
| `projectSettings` | `.claude/settings.json`       |
| `userSettings`    | `~/.claude/settings.json`     |

Hook 可以回显它接收的 `permission_suggestions` 之一作为其自己的 `updatedPermissions` 输出，这等同于用户在对话框中选择该"总是允许"选项。

### PostToolUse

在工具成功完成后立即运行。

在工具名称上匹配，与 PreToolUse 相同的值。

#### PostToolUse 输入

`PostToolUse` hooks 在工具已经成功执行后触发。输入包括 `tool_input`（发送给工具的参数）和 `tool_response`（它返回的结果）。两者的确切架构取决于工具。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123...",
  "duration_ms": 12
}
```

| 字段            | 描述                                             |
| :------------ | :--------------------------------------------- |
| `duration_ms` | 可选。工具执行时间（毫秒）。不包括权限提示和 PreToolUse hooks 中花费的时间 |

#### PostToolUse 决定控制

`PostToolUse` hooks 可以在工具执行后向 Claude 提供反馈。除了所有 hooks 可用的[JSON 输出字段](#json-output)外，您的 hook 脚本可以返回这些事件特定字段：

| 字段                     | 描述                                                                         |
| :--------------------- | :------------------------------------------------------------------------- |
| `decision`             | `"block"` 用 `reason` 提示 Claude。Claude 仍然看到原始输出；要替换它，使用 `updatedToolOutput` |
| `reason`               | 当 `decision` 为 `"block"` 时向 Claude 显示的解释                                   |
| `additionalContext`    | 添加到 Claude 上下文的字符串，与工具结果一起。请参阅[为 Claude 添加上下文](#add-context-for-claude)    |
| `updatedToolOutput`    | 用提供的值替换工具的输出，然后将其发送给 Claude。该值必须与工具的输出形状匹配                                 |
| `updatedMCPToolOutput` | 仅对[MCP 工具](#match-mcp-tools)替换输出。优先使用 `updatedToolOutput`，它适用于所有工具         |

下面的示例替换 `Bash` 调用的输出。替换值与 `Bash` 工具的输出形状匹配：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude",
    "updatedToolOutput": {
      "stdout": "[redacted]",
      "stderr": "",
      "interrupted": false,
      "isImage": false
    }
  }
}
```

<Warning>
  `updatedToolOutput` 仅改变 Claude 看到的内容。工具已经在 hook 触发时运行，所以任何写入的文件、执行的命令或发送的网络请求都已生效。遥测，如 OpenTelemetry 工具跨度和分析事件，也在 hook 运行前捕获原始输出。要在运行前防止或修改工具调用，请改用[PreToolUse](#pretooluse) hook。

  替换值必须与工具的输出形状匹配。内置工具返回结构化对象而不是纯字符串。例如，`Bash` 返回一个具有 `stdout`、`stderr`、`interrupted` 和 `isImage` 字段的对象。对于内置工具，不与工具的输出架构匹配的值被忽略，使用原始输出。MCP 工具输出通过而不进行架构验证。剥离 Claude 需要的错误详细信息可能导致它基于错误的假设继续。
</Warning>

### PostToolUseFailure

当工具执行失败时运行。此事件对于抛出错误或返回失败结果的工具调用触发。使用此来记录失败、发送警报或向 Claude 提供纠正反馈。

在工具名称上匹配，与 PreToolUse 相同的值。

#### PostToolUseFailure 输入

PostToolUseFailure hooks 接收与 PostToolUse 相同的 `tool_name` 和 `tool_input` 字段，以及作为顶级字段的错误信息：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false,
  "duration_ms": 4187
}
```

| 字段             | 描述                                             |
| :------------- | :--------------------------------------------- |
| `error`        | 描述出错原因的字符串                                     |
| `is_interrupt` | 可选的布尔值，指示失败是否由用户中断引起                           |
| `duration_ms`  | 可选。工具执行时间（毫秒）。不包括权限提示和 PreToolUse hooks 中花费的时间 |

#### PostToolUseFailure 决定控制

`PostToolUseFailure` hooks 可以在工具失败后向 Claude 提供上下文。除了所有 hooks 可用的[JSON 输出字段](#json-output)外，您的 hook 脚本可以返回这些事件特定字段：

| 字段                  | 描述                                                                    |
| :------------------ | :-------------------------------------------------------------------- |
| `additionalContext` | 添加到 Claude 上下文的字符串，与错误一起。请参阅[为 Claude 添加上下文](#add-context-for-claude) |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### PostToolBatch

在批次中的每个工具调用都已解决后运行一次，在 Claude Code 向模型发送下一个请求之前。`PostToolUse` 每个工具触发一次，这意味着当 Claude 进行并行工具调用时它并发触发。`PostToolBatch` 恰好触发一次，包含完整批次，因此它是注入取决于运行的工具集而不是任何单个工具的上下文的正确位置。此事件没有匹配器。

#### PostToolBatch 输入

除了[通用输入字段](#common-input-fields)外，PostToolBatch hooks 还接收 `tool_calls`，一个描述批次中每个工具调用的数组：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolBatch",
  "tool_calls": [
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/accounts.py"},
      "tool_use_id": "toolu_01...",
      "tool_response": "     1\tfrom __future__ import annotations\n     2\t..."
    },
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/transactions.py"},
      "tool_use_id": "toolu_02...",
      "tool_response": "     1\tfrom __future__ import annotations\n     2\t..."
    }
  ]
}
```

`tool_response` 包含与模型在相应 `tool_result` 块中接收的内容相同的内容。该值是序列化的字符串或内容块数组，完全如工具发出的那样。对于 `Read`，这意味着行号前缀的文本而不是原始文件内容。响应可能很大，因此仅解析您需要的字段。

<Note>
  `tool_response` 形状与 `PostToolUse` 的不同。`PostToolUse` 传递工具的结构化 `Output` 对象，例如 `{filePath: "...", success: true}` 对于 `Write`；`PostToolBatch` 传递序列化的 `tool_result` 内容模型看到的。
</Note>

#### PostToolBatch 决定控制

`PostToolBatch` hooks 可以为 Claude 注入上下文。除了所有 hooks 可用的[JSON 输出字段](#json-output)外，您的 hook 脚本可以返回这些事件特定字段：

| 字段                  | 描述                                                                                           |
| :------------------ | :------------------------------------------------------------------------------------------- |
| `additionalContext` | 在下一个模型调用之前注入的上下文字符串。请参阅[为 Claude 添加上下文](#add-context-for-claude)了解传递详情、放入什么内容以及恢复的会话如何处理过去的值 |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolBatch",
    "additionalContext": "These files are part of the ledger module. Run pytest before marking the task complete."
  }
}
```

返回 `decision: "block"` 或 `continue: false` 在下一个模型调用之前停止代理循环。

### PermissionDenied

当[自动模式](/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)分类器拒绝工具调用时运行。此 hook 仅在自动模式中触发：当您手动拒绝权限对话框、`PreToolUse` hook 阻止调用或 `deny` 规则匹配时，它不运行。使用它来记录分类器拒绝、调整配置或告诉模型它可能重试工具调用。

在工具名称上匹配，与 PreToolUse 相同的值。

#### PermissionDenied 输入

除了[通用输入字段](#common-input-fields)外，PermissionDenied hooks 还接收 `tool_name`、`tool_input`、`tool_use_id` 和 `reason`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "auto",
  "hook_event_name": "PermissionDenied",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/build",
    "description": "Clean build directory"
  },
  "tool_use_id": "toolu_01ABC123...",
  "reason": "Auto mode denied: command targets a path outside the project"
}
```

| 字段       | 描述                 |
| :------- | :----------------- |
| `reason` | 分类器解释为什么工具调用被拒绝的原因 |

#### PermissionDenied 决定控制

PermissionDenied hooks 可以告诉模型它可能重试被拒绝的工具调用。返回一个 JSON 对象，其中 `hookSpecificOutput.retry` 设置为 `true`：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

当 `retry` 为 `true` 时，Claude Code 向对话添加一条消息，告诉模型它可能重试工具调用。拒绝本身不被反转。如果您的 hook 不返回 JSON，或返回 `retry: false`，拒绝成立，模型接收原始拒绝消息。

### Notification

在 Claude Code 发送通知时运行。在通知类型上匹配：`permission_prompt`、`idle_prompt`、`auth_success`、`elicitation_dialog`、`elicitation_complete`、`elicitation_response`。省略匹配器以为所有通知类型运行 hooks。

使用单独的匹配器根据通知类型运行不同的处理程序。此配置在 Claude 需要权限批准时触发权限特定的警报脚本，在 Claude 空闲时触发不同的通知：

```json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

#### Notification 输入

除了[通用输入字段](#common-input-fields)外，Notification hooks 还接收 `message` 和通知文本、可选的 `title` 和 `notification_type` 指示哪个类型触发。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

Notification hooks 无法阻止或修改通知。它们用于副作用，例如将通知转发到外部服务。[通用 JSON 输出字段](#json-output)如 `systemMessage` 适用。

### SubagentStart

当通过 Agent 工具生成 Claude Code subagent 时运行。支持匹配器以按代理类型名称过滤。对于内置代理，这是代理名称，如 `general-purpose`、`Explore` 或 `Plan`。对于[自定义 subagents](/zh-CN/sub-agents)，这是代理 frontmatter 中的 `name` 字段，而不是文件名。

#### SubagentStart 输入

除了[通用输入字段](#common-input-fields)外，SubagentStart hooks 还接收 `agent_id` 和 subagent 的唯一标识符以及 `agent_type` 和代理名称（内置代理如 `"general-purpose"`、`"Explore"`、`"Plan"` 或自定义代理名称）。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

SubagentStart hooks 无法阻止 subagent 创建，但它们可以向 subagent 注入上下文。除了所有 hooks 可用的[JSON 输出字段](#json-output)外，您可以返回：

| 字段                  | 描述                                                                             |
| :------------------ | :----------------------------------------------------------------------------- |
| `additionalContext` | 添加到 subagent 上下文开始处的字符串，在其第一个提示之前。请参阅[为 Claude 添加上下文](#add-context-for-claude) |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

### SubagentStop

当 Claude Code subagent 完成响应时运行。在代理类型上匹配，与 SubagentStart 相同的值。

#### SubagentStop 输入

除了[通用输入字段](#common-input-fields)外，SubagentStop hooks 还接收 `stop_hook_active`、`agent_id`、`agent_type`、`agent_transcript_path` 和 `last_assistant_message`。`agent_type` 字段是用于匹配器过滤的值。`transcript_path` 是主会话的成绩单，而 `agent_transcript_path` 是 subagent 自己的成绩单，存储在嵌套的 `subagents/` 文件夹中。`last_assistant_message` 字段包含 subagent 最终响应的文本内容，因此 hooks 可以访问它而无需解析成绩单文件。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues..."
}
```

SubagentStop hooks 使用与[Stop hooks](#stop-decision-control)相同的决定控制格式。它们不支持 `additionalContext`。返回 `decision: "block"` 和 `reason` 保持 subagent 运行并将 `reason` 作为其下一个指令传递给 subagent。要在 subagent 返回后向父会话注入上下文，请改用 `Agent` 工具上的[`PostToolUse`](#posttooluse) hook。

### TaskCreated

当通过 `TaskCreate` 工具创建任务时运行。使用此来强制执行命名约定、要求任务描述或防止创建某些任务。

当 `TaskCreated` hook 以代码 2 退出时，任务不被创建，stderr 消息作为反馈反馈给模型。要完全停止队友而不是重新运行它，返回 JSON `{"continue": false, "stopReason": "..."}` 。TaskCreated hooks 不支持匹配器，在每次出现时触发。

#### TaskCreated 输入

除了[通用输入字段](#common-input-fields)外，TaskCreated hooks 还接收 `task_id`、`task_subject` 和可选的 `task_description`、`teammate_name` 和 `team_name`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCreated",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| 字段                 | 描述               |
| :----------------- | :--------------- |
| `task_id`          | 被创建的任务的标识符       |
| `task_subject`     | 任务的标题            |
| `task_description` | 任务的详细描述。可能不存在    |
| `teammate_name`    | 创建任务的队友的名称。可能不存在 |
| `team_name`        | 团队的名称。可能不存在      |

#### TaskCreated 决定控制

TaskCreated hooks 支持两种方式来控制任务创建：

* **退出代码 2**：任务不被创建，stderr 消息作为反馈反馈给模型。
* **JSON `{"continue": false, "stopReason": "..."}`**：完全停止队友，匹配 `Stop` hook 行为。`stopReason` 向用户显示。

此示例阻止主题不遵循所需格式的任务：

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

if [[ ! "$TASK_SUBJECT" =~ ^\[TICKET-[0-9]+\] ]]; then
  echo "Task subject must start with a ticket number, e.g. '[TICKET-123] Add feature'" >&2
  exit 2
fi

exit 0
```

### TaskCompleted

当任务被标记为已完成时运行。这在两种情况下触发：当任何代理通过 TaskUpdate 工具显式标记任务为已完成时，或当[代理团队](/zh-CN/agent-teams)队友完成其轮次且有进行中的任务时。使用此来强制执行完成标准，如通过测试或 lint 检查，然后任务才能关闭。

当 `TaskCompleted` hook 以代码 2 退出时，任务不被标记为已完成，stderr 消息作为反馈反馈给模型。要完全停止队友而不是重新运行它，返回 JSON `{"continue": false, "stopReason": "..."}` 。TaskCompleted hooks 不支持匹配器，在每次出现时触发。

#### TaskCompleted 输入

除了[通用输入字段](#common-input-fields)外，TaskCompleted hooks 还接收 `task_id`、`task_subject` 和可选的 `task_description`、`teammate_name` 和 `team_name`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| 字段                 | 描述               |
| :----------------- | :--------------- |
| `task_id`          | 被完成的任务的标识符       |
| `task_subject`     | 任务的标题            |
| `task_description` | 任务的详细描述。可能不存在    |
| `teammate_name`    | 完成任务的队友的名称。可能不存在 |
| `team_name`        | 团队的名称。可能不存在      |

#### TaskCompleted 决定控制

TaskCompleted hooks 支持两种方式来控制任务完成：

* **退出代码 2**：任务不被标记为已完成，stderr 消息作为反馈反馈给模型。
* **JSON `{"continue": false, "stopReason": "..."}`**：完全停止队友，匹配 `Stop` hook 行为。`stopReason` 向用户显示。

此示例运行测试并在失败时阻止任务完成：

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# 运行测试套件
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### Stop

在主 Claude Code 代理完成响应时运行。如果停止是由于用户中断，则不运行。API 错误触发[StopFailure](#stopfailure)。

<Tip>
  [`/goal`](/zh-CN/goal)命令是会话范围的基于提示的 Stop hook 的内置快捷方式。当您想要 Claude 继续工作直到条件成立而不编写 hook 配置时使用它。
</Tip>

#### Stop 输入

除了[通用输入字段](#common-input-fields)外，Stop hooks 还接收 `stop_hook_active` 和 `last_assistant_message`。`stop_hook_active` 字段在 Claude Code 已经作为 stop hook 的结果继续时为 `true`。检查此值或处理成绩单以防止 Claude Code 无限运行。`last_assistant_message` 字段包含 Claude 最终响应的文本内容，因此 hooks 可以访问它而无需解析成绩单文件。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary..."
}
```

#### Stop 决定控制

`Stop` 和 `SubagentStop` hooks 可以控制 Claude 是否继续。除了所有 hooks 可用的[JSON 输出字段](#json-output)外，您的 hook 脚本可以返回这些事件特定字段：

| 字段         | 描述                                              |
| :--------- | :---------------------------------------------- |
| `decision` | `"block"` 防止 Claude 停止。省略以允许 Claude 停止          |
| `reason`   | 当 `decision` 为 `"block"` 时必需。告诉 Claude 为什么它应该继续 |

```json theme={null}
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

### StopFailure

当轮次因 API 错误而结束时运行，而不是[Stop](#stop)。输出和退出代码被忽略。使用此来记录失败、发送警报或在 Claude 因速率限制、身份验证问题或其他 API 错误而无法完成响应时采取恢复操作。

#### StopFailure 输入

除了[通用输入字段](#common-input-fields)外，StopFailure hooks 还接收 `error`、可选的 `error_details` 和可选的 `last_assistant_message`。`error` 字段标识错误类型，用于匹配器过滤。

| 字段                       | 描述                                                                                                                                                 |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| `error`                  | 错误类型：`rate_limit`、`authentication_failed`、`oauth_org_not_allowed`、`billing_error`、`invalid_request`、`server_error`、`max_output_tokens` 或 `unknown` |
| `error_details`          | 关于错误的额外详细信息（如果可用）                                                                                                                                  |
| `last_assistant_message` | 在对话中显示的呈现错误文本。与 `Stop` 和 `SubagentStop` 不同，其中此字段包含 Claude 的对话输出，对于 `StopFailure` 它包含 API 错误字符串本身，例如 `"API Error: Rate limit reached"`              |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "StopFailure",
  "error": "rate_limit",
  "error_details": "429 Too Many Requests",
  "last_assistant_message": "API Error: Rate limit reached"
}
```

StopFailure hooks 没有决定控制。它们仅为通知和日志记录目的运行。

### TeammateIdle

当[代理团队](/zh-CN/agent-teams)队友在完成其轮次后即将空闲时运行。使用此来强制执行质量门，如要求通过 lint 检查或验证输出文件存在。

当 `TeammateIdle` hook 以代码 2 退出时，队友接收 stderr 消息作为反馈并继续工作而不是空闲。要完全停止队友而不是重新运行它，返回 JSON `{"continue": false, "stopReason": "..."}` 。TeammateIdle hooks 不支持匹配器，在每次出现时触发。

#### TeammateIdle 输入

除了[通用输入字段](#common-input-fields)外，TeammateIdle hooks 还接收 `teammate_name` 和 `team_name`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

| 字段              | 描述         |
| :-------------- | :--------- |
| `teammate_name` | 即将空闲的队友的名称 |
| `team_name`     | 团队的名称      |

#### TeammateIdle 决定控制

TeammateIdle hooks 支持两种方式来控制队友行为：

* **退出代码 2**：队友接收 stderr 消息作为反馈并继续工作而不是空闲。
* **JSON `{"continue": false, "stopReason": "..."}`**：完全停止队友，匹配 `Stop` hook 行为。`stopReason` 向用户显示。

此示例检查构建工件是否存在，然后允许队友空闲：

```bash theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### ConfigChange

当会话期间配置文件更改时运行。使用此来审计设置更改、强制执行安全策略或阻止对配置文件的未授权修改。

ConfigChange hooks 对设置文件、托管策略设置和 skill 文件的更改触发。输入中的 `source` 字段告诉您哪种类型的配置更改，可选的 `file_path` 字段提供更改文件的路径。

匹配器在配置源上过滤：

| 匹配器                | 何时触发                             |
| :----------------- | :------------------------------- |
| `user_settings`    | `~/.claude/settings.json` 更改     |
| `project_settings` | `.claude/settings.json` 更改       |
| `local_settings`   | `.claude/settings.local.json` 更改 |
| `policy_settings`  | 托管策略设置更改                         |
| `skills`           | `.claude/skills/` 中的 skill 文件更改  |

此示例记录所有配置更改以进行安全审计：

```json theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/audit-config-change.sh"
          }
        ]
      }
    ]
  }
}
```

#### ConfigChange 输入

除了[通用输入字段](#common-input-fields)外，ConfigChange hooks 还接收 `source` 和可选的 `file_path`。`source` 字段指示哪种配置类型更改，`file_path` 提供被修改的特定文件的路径。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

#### ConfigChange 决定控制

ConfigChange hooks 可以阻止配置更改生效。使用退出代码 2 或 JSON `decision` 来防止更改。被阻止时，新设置不应用于运行中的会话。

| 字段         | 描述                                 |
| :--------- | :--------------------------------- |
| `decision` | `"block"` 防止配置更改被应用。省略以允许更改        |
| `reason`   | 当 `decision` 为 `"block"` 时向用户显示的解释 |

```json theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

`policy_settings` 更改无法被阻止。Hooks 仍然对 `policy_settings` 源触发，因此您可以使用它们进行审计日志记录，但任何阻止决定都被忽略。这确保企业管理的设置始终生效。

### CwdChanged

当会话期间工作目录更改时运行，例如当 Claude 执行 `cd` 命令时。使用此来对目录更改做出反应：重新加载环境变量、激活项目特定的工具链或自动运行设置脚本。与[FileChanged](#filechanged)配对，用于[direnv](https://direnv.net/)等管理每个目录环境的工具。

CwdChanged hooks 可以访问 `CLAUDE_ENV_FILE`。写入该文件的变量持久化到会话的后续 Bash 命令中，就像在[SessionStart hooks](#persist-environment-variables)中一样。

CwdChanged 不支持匹配器，在每次目录更改时触发。

#### CwdChanged 输入

除了[通用输入字段](#common-input-fields)外，CwdChanged hooks 还接收 `old_cwd` 和 `new_cwd`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project/src",
  "hook_event_name": "CwdChanged",
  "old_cwd": "/Users/my-project",
  "new_cwd": "/Users/my-project/src"
}
```

#### CwdChanged 输出

除了所有 hooks 可用的[JSON 输出字段](#json-output)外，CwdChanged hooks 还可以返回 `watchPaths` 来动态设置[FileChanged](#filechanged)监视的文件路径：

| 字段           | 描述                                                                     |
| :----------- | :--------------------------------------------------------------------- |
| `watchPaths` | 绝对路径的数组。替换当前动态监视列表（来自您的 `matcher` 配置的路径始终被监视）。返回空数组会清除动态列表，这在进入新目录时很典型 |

CwdChanged hooks 没有决定控制。它们无法阻止目录更改。

### FileChanged

当监视的文件在磁盘上更改时运行。用于在项目配置文件修改时重新加载环境变量。

此事件的 `matcher` 有两个作用：

* **构建监视列表**：值在 `|` 上分割，每个段注册为工作目录中的文字文件名，因此 `".envrc|.env"` 监视恰好这两个文件。正则表达式模式在这里不有用：像 `^\.env` 这样的值会监视一个字面上名为 `^\.env` 的文件。
* **过滤哪些 hooks 运行**：当监视的文件更改时，相同的值使用标准[匹配器规则](#matcher-patterns)针对更改文件的基名过滤哪些 hook 组运行。

FileChanged hooks 可以访问 `CLAUDE_ENV_FILE`。写入该文件的变量持久化到会话的后续 Bash 命令中，就像在[SessionStart hooks](#persist-environment-variables)中一样。

#### FileChanged 输入

除了[通用输入字段](#common-input-fields)外，FileChanged hooks 还接收 `file_path` 和 `event`。

| 字段          | 描述                                                     |
| :---------- | :----------------------------------------------------- |
| `file_path` | 更改文件的绝对路径                                              |
| `event`     | 发生了什么：`"change"`（文件修改）、`"add"`（文件创建）或 `"unlink"`（文件删除） |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "FileChanged",
  "file_path": "/Users/my-project/.envrc",
  "event": "change"
}
```

#### FileChanged 输出

除了所有 hooks 可用的[JSON 输出字段](#json-output)外，FileChanged hooks 还可以返回 `watchPaths` 来动态更新监视的文件路径：

| 字段           | 描述                                                                              |
| :----------- | :------------------------------------------------------------------------------ |
| `watchPaths` | 绝对路径的数组。替换当前动态监视列表（来自您的 `matcher` 配置的路径始终被监视）。当您的 hook 脚本根据更改的文件发现要监视的其他文件时使用此项 |

FileChanged hooks 没有决定控制。它们无法阻止文件更改的发生。

### WorktreeCreate

当您运行 `claude --worktree` 或[subagent 使用 `isolation: "worktree"`](/zh-CN/sub-agents#choose-the-subagent-scope)时，Claude Code 使用 `git worktree` 创建隔离的工作副本。如果您配置 WorktreeCreate hook，它替换默认的 git 行为，让您使用不同的版本控制系统，如 SVN、Perforce 或 Mercurial。

因为 hook 完全替换默认行为，[`.worktreeinclude`](/zh-CN/worktrees#copy-gitignored-files-into-worktrees)不被处理。如果您需要将本地配置文件（如 `.env`）复制到新 worktree，请在您的 hook 脚本内执行。

Hook 必须返回创建的 worktree 目录的绝对路径。Claude Code 使用此路径作为隔离会话的工作目录。命令 hooks 在 stdout 上打印它；HTTP hooks 通过 `hookSpecificOutput.worktreePath` 返回它。

此示例创建 SVN 工作副本并打印路径供 Claude Code 使用。用您自己的替换仓库 URL：

```json theme={null}
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

Hook 从 stdin 上的 JSON 输入读取 worktree `name`，将新副本检出到新目录，并打印目录路径。最后一行的 `echo` 是 Claude Code 读取的 worktree 路径。将任何其他输出重定向到 stderr，以便它不会干扰路径。

#### WorktreeCreate 输入

除了[通用输入字段](#common-input-fields)外，WorktreeCreate hooks 还接收 `name` 字段。这是新 worktree 的 slug 标识符，由用户指定或自动生成（例如，`bold-oak-a3f2`）。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### WorktreeCreate 输出

WorktreeCreate hooks 不使用标准的允许/阻止决定模型。相反，hook 的成功或失败决定结果。Hook 必须返回创建的 worktree 目录的绝对路径：

* **命令 hooks**（`type: "command"`）：在 stdout 上打印路径。
* **HTTP hooks**（`type: "http"`）：在响应体中返回 `{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/absolute/path" } }`。

如果 hook 失败或不产生路径，worktree 创建失败并出现错误。

### WorktreeRemove

[WorktreeCreate](#worktreecreate) 的清理对应物。此 hook 在 worktree 被移除时触发，要么当您退出 `--worktree` 会话并选择移除它时，要么当具有 `isolation: "worktree"` 的 subagent 完成时。对于基于 git 的 worktrees，Claude 使用 `git worktree remove` 自动处理清理。如果您为非 git 版本控制系统配置了 WorktreeCreate hook，将其与 WorktreeRemove hook 配对以处理清理。没有它，worktree 目录留在磁盘上。

Claude Code 将 WorktreeCreate 返回的路径作为 `worktree_path` 在 hook 输入中传递。此示例读取该路径并移除目录：

```json theme={null}
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'jq -r .worktree_path | xargs rm -rf'"
          }
        ]
      }
    ]
  }
}
```

#### WorktreeRemove 输入

除了[通用输入字段](#common-input-fields)外，WorktreeRemove hooks 还接收 `worktree_path` 字段，这是被移除的 worktree 的绝对路径。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

WorktreeRemove hooks 没有决定控制。它们无法阻止 worktree 移除，但可以执行清理任务，如移除版本控制状态或存档更改。Hook 失败仅在调试模式下记录。

### PreCompact

在 Claude Code 即将运行压缩操作之前运行。

匹配器值指示压缩是手动还是自动触发：

| 匹配器      | 何时触发         |
| :------- | :----------- |
| `manual` | `/compact`   |
| `auto`   | 当上下文窗口满时自动压缩 |

退出代码 2 以阻止压缩。对于手动 `/compact`，stderr 消息向用户显示。您也可以通过返回带有 `"decision": "block"` 的 JSON 来阻止。

阻止自动压缩有不同的效果，取决于何时触发。如果压缩在上下文限制之前主动触发，Claude Code 跳过它，对话继续未压缩。如果压缩被触发以从已由 API 返回的上下文限制错误恢复，底层错误浮出并且当前请求失败。

#### PreCompact 输入

除了[通用输入字段](#common-input-fields)外，PreCompact hooks 还接收 `trigger` 和 `custom_instructions`。对于 `manual`，`custom_instructions` 包含用户传入 `/compact` 的内容。对于 `auto`，`custom_instructions` 为空。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### PostCompact

在 Claude Code 完成压缩操作后运行。使用此事件对新的压缩状态做出反应，例如记录生成的摘要或更新外部状态。

与 `PreCompact` 相同的匹配器值适用：

| 匹配器      | 何时触发           |
| :------- | :------------- |
| `manual` | 在 `/compact` 后 |
| `auto`   | 在上下文窗口满时自动压缩后  |

#### PostCompact 输入

除了[通用输入字段](#common-input-fields)外，PostCompact hooks 还接收 `trigger` 和 `compact_summary`。`compact_summary` 字段包含压缩操作生成的对话摘要。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostCompact",
  "trigger": "manual",
  "compact_summary": "Summary of the compacted conversation..."
}
```

PostCompact hooks 没有决定控制。它们无法影响压缩结果，但可以执行后续任务。

### SessionEnd

当 Claude Code 会话结束时运行。用于清理任务、记录会话统计或保存会话状态。支持匹配器以按退出原因过滤。

hook 输入中的 `reason` 字段指示会话为何结束：

| 原因                            | 描述                   |
| :---------------------------- | :------------------- |
| `clear`                       | 会话使用 `/clear` 命令清除   |
| `resume`                      | 通过交互式 `/resume` 切换会话 |
| `logout`                      | 用户登出                 |
| `prompt_input_exit`           | 用户在提示输入可见时退出         |
| `bypass_permissions_disabled` | 绕过权限模式被禁用            |
| `other`                       | 其他退出原因               |

#### SessionEnd 输入

除了[通用输入字段](#common-input-fields)外，SessionEnd hooks 还接收 `reason` 字段，指示会话为何结束。有关所有值，请参阅上面的[原因表](#sessionend)。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

SessionEnd hooks 没有决定控制。它们无法阻止会话终止，但可以执行清理任务。

SessionEnd hooks 的默认超时为 1.5 秒。这适用于会话退出、`/clear` 和通过交互式 `/resume` 切换会话。如果 hook 需要更多时间，在 hook 配置中设置 `timeout`。总体预算自动提高到配置的最高每个 hook 超时，最多 60 秒。在插件提供的 hooks 上设置的超时不会提高预算。要显式覆盖预算，请在毫秒中设置 `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` 环境变量。

```bash theme={null}
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
```

### Elicitation

当 MCP 服务器在任务中途请求用户输入时运行。默认情况下，Claude Code 显示交互式对话供用户响应。Hooks 可以拦截此请求并以编程方式响应，完全跳过对话。

匹配器字段与 MCP 服务器名称匹配。

#### Elicitation 输入

除了[通用输入字段](#common-input-fields)外，Elicitation hooks 还接收 `mcp_server_name`、`message` 和可选的 `mode`、`url`、`elicitation_id` 和 `requested_schema` 字段。

对于 form 模式 elicitation（最常见的情况）：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please provide your credentials",
  "mode": "form",
  "requested_schema": {
    "type": "object",
    "properties": {
      "username": { "type": "string", "title": "Username" }
    }
  }
}
```

对于 URL 模式 elicitation（基于浏览器的身份验证）：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please authenticate",
  "mode": "url",
  "url": "https://auth.example.com/login"
}
```

#### Elicitation 输出

要以编程方式响应而不显示对话，返回带有 `hookSpecificOutput` 的 JSON 对象：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",
    "content": {
      "username": "alice"
    }
  }
}
```

| 字段        | 值                           | 描述                                       |
| :-------- | :-------------------------- | :--------------------------------------- |
| `action`  | `accept`、`decline`、`cancel` | 是否接受、拒绝或取消请求                             |
| `content` | object                      | 要提交的 form 字段值。仅在 `action` 为 `accept` 时使用 |

退出代码 2 拒绝 elicitation 并向用户显示 stderr。

### ElicitationResult

在用户响应 MCP elicitation 后运行。Hooks 可以观察、修改或阻止响应，然后将其发送回 MCP 服务器。

匹配器字段与 MCP 服务器名称匹配。

#### ElicitationResult 输入

除了[通用输入字段](#common-input-fields)外，ElicitationResult hooks 还接收 `mcp_server_name`、`action` 和可选的 `mode`、`elicitation_id` 和 `content` 字段。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "ElicitationResult",
  "mcp_server_name": "my-mcp-server",
  "action": "accept",
  "content": { "username": "alice" },
  "mode": "form",
  "elicitation_id": "elicit-123"
}
```

#### ElicitationResult 输出

要覆盖用户的响应，返回带有 `hookSpecificOutput` 的 JSON 对象：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "decline",
    "content": {}
  }
}
```

| 字段        | 值                           | 描述                                      |
| :-------- | :-------------------------- | :-------------------------------------- |
| `action`  | `accept`、`decline`、`cancel` | 覆盖用户的操作                                 |
| `content` | object                      | 覆盖 form 字段值。仅在 `action` 为 `accept` 时有意义 |

退出代码 2 阻止响应，将有效操作更改为 `decline`。

## 基于提示的 hooks

除了命令、HTTP 和 MCP tool hooks 外，Claude Code 还支持基于提示的 hooks（`type: "prompt"`），使用 LLM 来评估是否允许或阻止操作，以及代理 hooks（`type: "agent"`），生成具有工具访问权限的代理验证器。并非所有事件都支持每种 hook 类型。

支持所有五种 hook 类型（`command`、`http`、`mcp_tool`、`prompt` 和 `agent`）的事件：

* `PermissionRequest`
* `PostToolBatch`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `TaskCreated`
* `UserPromptExpansion`
* `UserPromptSubmit`

支持 `command`、`http` 和 `mcp_tool` hooks 但不支持 `prompt` 或 `agent` 的事件：

* `ConfigChange`
* `CwdChanged`
* `Elicitation`
* `ElicitationResult`
* `FileChanged`
* `InstructionsLoaded`
* `Notification`
* `PermissionDenied`
* `PostCompact`
* `PreCompact`
* `SessionEnd`
* `StopFailure`
* `SubagentStart`
* `TeammateIdle`
* `WorktreeCreate`
* `WorktreeRemove`

`SessionStart` 和 `Setup` 支持 `command` 和 `mcp_tool` hooks。它们不支持 `http`、`prompt` 或 `agent` hooks。

### 基于提示的 hooks 如何工作

基于提示的 hooks 不执行 Bash 命令，而是：

1. 将 hook 输入和您的提示发送到 Claude 模型，默认为 Haiku
2. LLM 使用包含决定的结构化 JSON 响应
3. Claude Code 自动处理决定

### 提示 hook 配置

将 `type` 设置为 `"prompt"` 并提供 `prompt` 字符串而不是 `command`。使用 `$ARGUMENTS` 占位符将 hook 的 JSON 输入数据注入到您的提示文本中。Claude Code 将组合的提示和输入发送到快速 Claude 模型，该模型返回 JSON 决定。

此 `Stop` hook 要求 LLM 在允许 Claude 完成之前评估是否应该停止：

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

| 字段                | 必需 | 描述                                                                                                                                            |
| :---------------- | :- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`            | 是  | 必须是 `"prompt"`                                                                                                                                |
| `prompt`          | 是  | 要发送给 LLM 的提示文本。使用 `$ARGUMENTS` 作为 hook 输入 JSON 的占位符。如果 `$ARGUMENTS` 不存在，输入 JSON 被追加到提示                                                        |
| `model`           | 否  | 用于评估的模型。默认为快速模型                                                                                                                               |
| `timeout`         | 否  | 超时（秒）。默认值：30                                                                                                                                  |
| `continueOnBlock` | 否  | 当提示返回 `ok: false` 时，将原因反馈给 Claude 并继续转轮而不是停止。默认值：`false`。在生成的 `decision: "block"` 上实现为 `continue: true`。有关每个事件的行为，请参阅[响应架构](#response-schema) |

### 响应架构

LLM 必须使用包含以下内容的 JSON 响应：

```json theme={null}
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

| 字段       | 描述                                                    |
| :------- | :---------------------------------------------------- |
| `ok`     | `true` 允许。`false` 产生 `decision: "block"`。请参阅下面的每个事件行为 |
| `reason` | 当 `ok` 为 `false` 时必需。用作阻止原因                           |

`ok: false` 时发生的情况取决于事件：

* `Stop` 和 `SubagentStop`：原因被反馈给 Claude 作为其下一条指令，转轮继续
* `PreToolUse`：工具调用被拒绝，原因作为工具错误返回给 Claude，等同于命令 hook 的 `permissionDecision: "deny"`
* `PostToolUse`：默认情况下转轮结束，原因在聊天中显示为警告行。设置 `continueOnBlock: true` 以将原因反馈给 Claude 并继续转轮
* `PostToolBatch`、`UserPromptSubmit` 和 `UserPromptExpansion`：转轮结束，原因显示为警告行。这些事件在 `decision: "block"` 上结束转轮，无论 `continue` 如何
* `PostToolUseFailure`、`TaskCreated` 和 `TaskCompleted`：原因作为工具错误返回给 Claude，类似于 `PreToolUse`
* `PermissionRequest`：`ok: false` 无效。要从 hook 拒绝批准，请使用[命令 hook](#command-hook-fields)，返回 `hookSpecificOutput.decision.behavior: "deny"`

如果您需要对任何事件进行更精细的控制，请使用[命令 hook](#command-hook-fields)，其中包含[决定控制](#decision-control)中描述的每个事件字段。

### 示例：多条件 Stop hook

此 `Stop` hook 使用详细提示检查三个条件，然后允许 Claude 停止。如果 `"ok"` 为 `false`，Claude 继续工作，提供的原因作为其下一条指令。`SubagentStop` hooks 使用相同的格式来评估[子代理](/zh-CN/sub-agents)是否应该停止：

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## 基于代理的 hooks

<Warning>
  代理 hooks 是实验性的。行为和配置可能在未来版本中更改。对于生产工作流，建议使用[命令 hooks](#command-hook-fields)。
</Warning>

基于代理的 hooks（`type: "agent"`）类似于基于提示的 hooks，但具有多轮工具访问。代理 hook 生成一个可以读取文件、搜索代码和检查代码库以验证条件的 subagent，而不是单个 LLM 调用。代理 hooks 支持与基于提示的 hooks 相同的事件。

### 基于代理的 hooks 如何工作

当代理 hook 触发时：

1. Claude Code 生成一个 subagent，带有您的提示和 hook 的 JSON 输入
2. Subagent 可以使用 Read、Grep 和 Glob 等工具进行调查
3. 在最多 50 轮后，subagent 返回结构化的 `{ "ok": true/false }` 决定
4. Claude Code 以与提示 hook 相同的方式处理决定

代理 hooks 在验证需要检查实际文件或测试输出时很有用，而不仅仅是评估 hook 输入数据。

### 代理 hook 配置

将 `type` 设置为 `"agent"` 并提供 `prompt` 字符串。配置字段与[提示 hooks](#prompt-hook-configuration)相同，但超时更长：

| 字段        | 必需 | 描述                                               |
| :-------- | :- | :----------------------------------------------- |
| `type`    | 是  | 必须是 `"agent"`                                    |
| `prompt`  | 是  | 描述要验证的内容的提示。使用 `$ARGUMENTS` 作为 hook 输入 JSON 的占位符 |
| `model`   | 否  | 要使用的模型。默认为快速模型                                   |
| `timeout` | 否  | 超时（秒）。默认值：60                                     |

响应架构与提示 hooks 相同：`{ "ok": true }` 允许或 `{ "ok": false, "reason": "..." }` 阻止。

此 `Stop` hook 验证所有单元测试通过，然后允许 Claude 完成：

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## 在后台运行 Hooks

默认情况下，hooks 阻止 Claude 的执行，直到它们完成。对于长时间运行的任务，如部署、测试套件或外部 API 调用，设置 `"async": true` 以在后台运行 hook，同时 Claude 继续工作。异步 hooks 无法阻止或控制 Claude 的行为：响应字段如 `decision`、`permissionDecision` 和 `continue` 无效，因为它们会控制的操作已经完成。

### 配置异步 Hook

将 `"async": true` 添加到命令 hook 的配置以在后台运行它而不阻止 Claude。此字段仅在 `type: "command"` hooks 上可用。

此 hook 在每个 `Write` 工具调用后运行测试脚本。Claude 立即继续工作，同时 `run-tests.sh` 执行最多 120 秒。脚本完成时，其输出在下一个对话轮次上传递：

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

`timeout` 字段设置后台进程的最大时间（秒）。如果未指定，异步 hooks 使用与同步 hooks 相同的 10 分钟默认值。

### 异步 Hooks 如何执行

当异步 hook 触发时，Claude Code 启动 hook 进程并立即继续，不等待其完成。Hook 通过 stdin 接收与同步 hook 相同的 JSON 输入。

后台进程退出后，如果 hook 产生了带有 `additionalContext` 字段的 JSON 响应，该内容在下一个对话轮次作为上下文传递给 Claude。`systemMessage` 字段显示给你，而不是 Claude。

异步 hook 完成通知默认被抑制。要查看它们，请使用 `Ctrl+O` 启用详细模式或使用 `--verbose` 启动 Claude Code。

### 示例：文件更改后运行测试

此 hook 在 Claude 写入文件时在后台启动测试套件，然后在测试完成时将结果报告回 Claude。将此脚本保存到项目中的 `.claude/hooks/run-tests-async.sh` 并使用 `chmod +x` 使其可执行：

```bash theme={null}
#!/bin/bash
# run-tests-async.sh

# 从 stdin 读取 hook 输入
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# 仅对源文件运行测试
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# 运行测试并通过 additionalContext 向 Claude 报告结果
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  MSG="Tests passed after editing $FILE_PATH"
else
  MSG="Tests failed after editing $FILE_PATH: $RESULT"
fi
jq -nc --arg msg "$MSG" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $msg}}'
```

然后将此配置添加到项目根目录中的 `.claude/settings.json`。`async: true` 标志让 Claude 在测试运行时继续工作：

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/run-tests-async.sh",
            "args": [],
            "async": true,
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

### 限制

异步 hooks 与同步 hooks 相比有几个限制：

* 仅 `type: "command"` hooks 支持 `async`。基于提示的 hooks 无法异步运行。
* 异步 hooks 无法阻止工具调用或返回决定。到 hook 完成时，触发操作已经进行。
* Hook 输出在下一个对话轮次传递。如果会话空闲，响应等待直到下一个用户交互。例外：`asyncRewake` hook 在退出代码 2 时立即唤醒 Claude，即使会话空闲。
* 每次执行创建一个单独的后台进程。同一异步 hook 的多个触发之间没有去重。

## 安全考虑

### 免责声明

命令 hooks 使用您的系统用户的完整权限运行。

<Warning>
  命令 hooks 使用您的完整用户权限执行 shell 命令。它们可以修改、删除或访问您的用户帐户可以访问的任何文件。在将任何 hook 命令添加到您的配置之前，请审查并测试它们。
</Warning>

### 安全最佳实践

编写 hooks 时请记住这些实践：

* **验证和清理输入**：永远不要盲目信任输入数据
* **始终引用 shell 变量**：使用 `"$VAR"` 而不是 `$VAR`
* **阻止路径遍历**：检查文件路径中的 `..`
* **使用绝对路径**：为脚本指定完整路径。在 exec 形式中，使用 `${CLAUDE_PROJECT_DIR}` 且路径无需引用。在 shell 形式中，将其包装在双引号中
* **跳过敏感文件**：避免 `.env`、`.git/`、密钥等

## Windows PowerShell 工具

在 Windows 上，您可以通过在命令 hook 上设置 `"shell": "powershell"` 在 PowerShell 中运行单个 hooks。Hooks 直接生成 PowerShell，因此这适用于是否设置了 `CLAUDE_CODE_USE_POWERSHELL_TOOL`。Claude Code 自动检测 `pwsh.exe`（PowerShell 7+），回退到 `powershell.exe`（5.1）。

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "Write-Host 'File written'"
          }
        ]
      }
    ]
  }
}
```

## 调试 hooks

Hook 执行详细信息，包括哪些 hooks 匹配、它们的退出代码和完整 stdout 和 stderr，被写入调试日志文件。使用 `claude --debug-file <path>` 启动 Claude Code 以将日志写入已知位置，或运行 `claude --debug` 并在 `~/.claude/debug/<session-id>.txt` 读取日志。`--debug` 标志不打印到终端。

```text theme={null}
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

对于更细粒度的 hook 匹配详细信息，设置 `CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose` 以查看额外的日志行，例如 hook 匹配器计数和查询匹配。

有关故障排除常见问题，如 hooks 不触发、无限 Stop hook 循环或配置错误，请参阅指南中的[限制和故障排除](/zh-CN/hooks-guide#limitations-and-troubleshooting)。有关涵盖 `/context`、`/doctor` 和设置优先级的更广泛的诊断演练，请参阅[调试你的配置](/zh-CN/debug-your-config)。

> ## Documentation Index
>
> Fetch the complete documentation index at: <https://code.claude.com/docs/llms.txt>
> Use this file to discover all available pages before exploring further.

# Plugins 参考

> Claude Code 插件系统的完整技术参考，包括架构、CLI 命令和组件规范。

<Tip>
  想要安装插件？请参阅[发现和安装插件](/zh-CN/discover-plugins)。如需创建插件，请参阅[Plugins](/zh-CN/plugins)。如需分发插件，请参阅[Plugin marketplaces](/zh-CN/plugin-marketplaces)。
</Tip>

本参考提供了 Claude Code 插件系统的完整技术规范，包括组件架构、CLI 命令和开发工具。

**plugin** 是一个自包含的组件目录，用于扩展 Claude Code 的自定义功能。插件组件包括 skills、agents、hooks、MCP servers、LSP servers 和 monitors。

## Plugin 组件参考

### Skills

Plugins 向 Claude Code 添加 skills，创建可由您或 Claude 调用的 `/name` 快捷方式。

**位置**：插件根目录中的 `skills/` 或 `commands/` 目录

**文件格式**：Skills 是包含 `SKILL.md` 的目录；commands 是简单的 markdown 文件

**Skill 结构**：

```text theme={null}
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (可选)
│   └── scripts/ (可选)
└── code-reviewer/
    └── SKILL.md
```

**集成行为**：

* 安装插件时会自动发现 Skills 和 commands
* Claude 可以根据任务上下文自动调用它们
* Skills 可以在 SKILL.md 旁边包含支持文件

有关完整详情，请参阅 [Skills](/zh-CN/skills)。

### Agents

Plugins 可以为特定任务提供专门的 subagents，Claude 可以在适当时自动调用。

**位置**：插件根目录中的 `agents/` 目录

**文件格式**：描述 agent 功能的 Markdown 文件

**Agent 结构**：

```markdown theme={null}
---
name: agent-name
description: 该 agent 的专长以及 Claude 应何时调用它
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

详细的系统提示，描述 agent 的角色、专业知识和行为。
```

Plugin agents 支持 `name`、`description`、`model`、`effort`、`maxTurns`、`tools`、`disallowedTools`、`skills`、`memory`、`background` 和 `isolation` frontmatter 字段。唯一有效的 `isolation` 值是 `"worktree"`。出于安全原因，plugin 提供的 agents 不支持 `hooks`、`mcpServers` 和 `permissionMode`。

**集成点**：

* Agents 出现在 `/agents` 界面中
* Claude 可以根据任务上下文自动调用 agents
* Agents 可以由用户手动调用
* Plugin agents 与内置 Claude agents 一起工作

有关完整详情，请参阅 [Subagents](/zh-CN/sub-agents)。

### Hooks

Plugins 可以提供事件处理程序，自动响应 Claude Code 事件。

**位置**：插件根目录中的 `hooks/hooks.json`，或在 plugin.json 中内联

**格式**：具有事件匹配器和操作的 JSON 配置

**Hook 配置**：

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

Plugin hooks 响应与 [用户定义的 hooks](/zh-CN/hooks) 相同的生命周期事件：

| Event                 | When it fires                                                                                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`        | When a session begins or resumes                                                                                                                       |
| `Setup`               | When you start Claude Code with `--init-only`, or with `--init` or `--maintenance` in `-p` mode. For one-time preparation in CI or scripts             |
| `UserPromptSubmit`    | When you submit a prompt, before Claude processes it                                                                                                   |
| `UserPromptExpansion` | When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion                                                     |
| `PreToolUse`          | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`   | When a permission dialog appears                                                                                                                       |
| `PermissionDenied`    | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call                     |
| `PostToolUse`         | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure`  | After a tool call fails                                                                                                                                |
| `PostToolBatch`       | After a full batch of parallel tool calls resolves, before the next model call                                                                         |
| `Notification`        | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`       | When a subagent is spawned                                                                                                                             |
| `SubagentStop`        | When a subagent finishes                                                                                                                               |
| `TaskCreated`         | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`       | When a task is being marked as completed                                                                                                               |
| `Stop`                | When Claude finishes responding                                                                                                                        |
| `StopFailure`         | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`        | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `InstructionsLoaded`  | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`        | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`          | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`         | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`      | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`      | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`          | Before context compaction                                                                                                                              |
| `PostCompact`         | After context compaction completes                                                                                                                     |
| `Elicitation`         | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`   | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`          | When a session terminates                                                                                                                              |

**Hook 类型**：

* `command`：执行 shell 命令或脚本
* `http`：将事件 JSON 作为 POST 请求发送到 URL
* `mcp_tool`：在配置的 [MCP server](/zh-CN/mcp) 上调用工具
* `prompt`：使用 LLM 评估提示（使用 `$ARGUMENTS` 占位符表示上下文）
* `agent`：运行具有工具的 agentic 验证器以完成复杂验证任务

### MCP servers

Plugins 可以捆绑 Model Context Protocol (MCP) servers 以将 Claude Code 与外部工具和服务连接。

**位置**：插件根目录中的 `.mcp.json`，或在 plugin.json 中内联

**格式**：标准 MCP server 配置

**MCP server 配置**：

```json theme={null}
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**集成行为**：

* 启用插件时，Plugin MCP servers 会自动启动
* Servers 在 Claude 的工具包中显示为标准 MCP 工具
* Server 功能与 Claude 的现有工具无缝集成
* Plugin servers 可以独立于用户 MCP servers 进行配置

### LSP servers

<Tip>
  想要使用 LSP plugins？从官方市场安装它们：在 `/plugin` Discover 选项卡中搜索"lsp"。本部分记录了如何为官方市场未涵盖的语言创建 LSP plugins。
</Tip>

Plugins 可以提供 [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) servers，在处理代码库时为 Claude 提供实时代码智能。

LSP 集成提供：

* **即时诊断**：Claude 在每次编辑后立即看到错误和警告
* **代码导航**：转到定义、查找引用和悬停信息
* **语言感知**：代码符号的类型信息和文档

**位置**：插件根目录中的 `.lsp.json`，或在 `plugin.json` 中内联

**格式**：将语言服务器名称映射到其配置的 JSON 配置

**`.lsp.json` 文件格式**：

```json theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**在 `plugin.json` 中内联**：

```json theme={null}
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**必需字段：**

| 字段                    | 描述                         |
| :-------------------- | :------------------------- |
| `command`             | 要执行的 LSP 二进制文件（必须在 PATH 中） |
| `extensionToLanguage` | 将文件扩展名映射到语言标识符             |

**可选字段：**

| 字段                      | 描述                                          |
| :---------------------- | :------------------------------------------ |
| `args`                  | LSP server 的命令行参数                           |
| `transport`             | 通信传输：`stdio`（默认）或 `socket`                  |
| `env`                   | 启动 server 时要设置的环境变量                         |
| `initializationOptions` | 在初始化期间传递给 server 的选项                        |
| `settings`              | 通过 `workspace/didChangeConfiguration` 传递的设置 |
| `workspaceFolder`       | server 的工作区文件夹路径                            |
| `startupTimeout`        | 等待 server 启动的最长时间（毫秒）                       |
| `shutdownTimeout`       | 等待正常关闭的最长时间（毫秒）                             |
| `restartOnCrash`        | server 崩溃时是否自动重启                            |
| `maxRestarts`           | 放弃前的最大重启尝试次数                                |

<Warning>
  **您必须单独安装语言服务器二进制文件。** LSP plugins 配置 Claude Code 如何连接到语言服务器，但它们不包括服务器本身。如果在 `/plugin` Errors 选项卡中看到 `Executable not found in $PATH`，请为您的语言安装所需的二进制文件。
</Warning>

**可用的 LSP plugins：**

| Plugin              | 语言服务器                      | 安装命令                                                                            |
| :------------------ | :------------------------- | :------------------------------------------------------------------------------ |
| `pyright-lsp`       | Pyright (Python)           | `pip install pyright` 或 `npm install -g pyright`                                |
| `typescript-lsp`    | TypeScript Language Server | `npm install -g typescript-language-server typescript`                          |
| `rust-analyzer-lsp` | rust-analyzer              | [参阅 rust-analyzer 安装](https://rust-analyzer.github.io/manual.html#installation) |

首先安装语言服务器，然后从市场安装 plugin。

### Monitors

Plugins 可以声明后台 monitors，Claude Code 在 plugin 激活时自动启动。每个 monitor 为会话的生命周期运行一个 shell 命令，并将每个 stdout 行作为通知传递给 Claude，以便 Claude 可以对日志条目、状态更改或轮询事件做出反应，而无需被要求启动监视本身。

Plugin monitors 使用与 [Monitor tool](/zh-CN/tools-reference#monitor-tool) 相同的机制，并共享其可用性约束。它们仅在交互式 CLI 会话中运行，在与 [hooks](#hooks) 相同的信任级别上无沙箱运行，并在 Monitor tool 不可用的主机上跳过。

<Note>
  Plugin monitors 需要 Claude Code v2.1.105 或更高版本。
</Note>

**位置**：插件根目录中的 `monitors/monitors.json`，或在 plugin.json 中内联

**格式**：监视器条目的 JSON 数组

以下 `monitors/monitors.json` 监视部署状态端点和本地错误日志：

```json theme={null}
[
  {
    "name": "deploy-status",
    "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/poll-deploy.sh ${user_config.api_endpoint}",
    "description": "Deployment status changes"
  },
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log",
    "when": "on-skill-invoke:debug"
  }
]
```

要内联声明 monitors，请将 `plugin.json` 中的 `experimental.monitors` 设置为相同的数组。要从非默认路径加载，请将 `experimental.monitors` 设置为相对路径字符串，例如 `"./config/monitors.json"`。Monitors 是一个 [实验性组件](#experimental-components)。

**必需字段：**

| 字段            | 描述                                     |
| :------------ | :------------------------------------- |
| `name`        | 在插件中唯一的标识符。防止插件重新加载或再次调用 skill 时出现重复进程 |
| `command`     | 在会话工作目录中作为持久后台进程运行的 shell 命令           |
| `description` | 正在监视的内容的简短摘要。显示在任务面板和通知摘要中             |

**可选字段：**

| 字段     | 描述                                                                                                          |
| :----- | :---------------------------------------------------------------------------------------------------------- |
| `when` | 控制 monitor 何时启动。`"always"` 在会话启动和插件重新加载时启动它，这是默认值。`"on-skill-invoke:<skill-name>"` 在此插件中的命名 skill 首次被分派时启动它 |

`command` 值支持与 MCP 和 LSP server 配置相同的 [变量替换](#environment-variables)：`${CLAUDE_PLUGIN_ROOT}`、`${CLAUDE_PLUGIN_DATA}`、`${CLAUDE_PROJECT_DIR}`、`${user_config.*}` 和环境中的任何 `${ENV_VAR}`。如果脚本需要从插件自己的目录运行，请在命令前加上 `cd "${CLAUDE_PLUGIN_ROOT}" &&`。

在会话中途禁用插件不会停止已在运行的 monitors。它们在会话结束时停止。

### Themes

Plugins 可以提供颜色主题，这些主题与内置预设和用户的本地主题一起出现在 `/theme` 中。主题是 `themes/` 中的 JSON 文件，具有 `base` 预设和稀疏的 `overrides` 颜色令牌映射。Themes 是一个 [实验性组件](#experimental-components)。

```json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

选择 plugin 主题会在用户的配置中持久化 `custom:<plugin-name>:<slug>`。Plugin 主题是只读的；在 `/theme` 中按 `Ctrl+E` 会将其复制到 `~/.claude/themes/`，以便用户可以编辑副本。

***

## Plugin 安装范围

安装 plugin 时，您选择一个**范围**，确定 plugin 的可用位置以及谁可以使用它：

| 范围        | 设置文件                                               | 用例                       |
| :-------- | :------------------------------------------------- | :----------------------- |
| `user`    | `~/.claude/settings.json`                          | 在所有项目中可用的个人 plugins（默认）  |
| `project` | `.claude/settings.json`                            | 通过版本控制共享的团队 plugins      |
| `local`   | `.claude/settings.local.json`                      | 项目特定的 plugins，gitignored |
| `managed` | [Managed settings](/zh-CN/settings#settings-files) | 托管 plugins（只读，仅更新）       |

Plugins 使用与其他 Claude Code 配置相同的范围系统。有关安装说明和范围标志，请参阅[安装 plugins](/zh-CN/discover-plugins#install-plugins)。有关范围的完整说明，请参阅[Configuration scopes](/zh-CN/settings#configuration-scopes)。

***

## Plugin 清单架构

`.claude-plugin/plugin.json` 文件定义了您的 plugin 的元数据和配置。本部分记录了所有支持的字段和选项。

清单是可选的。如果省略，Claude Code 会自动发现[默认位置](#file-locations-reference)中的组件，并从目录名称派生 plugin 名称。当您需要提供元数据或自定义组件路径时，使用清单。

### 完整架构

```json theme={null}
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": ["./custom/agents/reviewer.md"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json",
  "experimental": {
    "themes": "./themes/",
    "monitors": "./monitors.json"
  },
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

### 必需字段

如果包含清单，`name` 是唯一必需的字段。

| 字段     | 类型     | 描述                    | 示例                   |
| :----- | :----- | :-------------------- | :------------------- |
| `name` | string | 唯一标识符（kebab-case，无空格） | `"deployment-tools"` |

此名称用于命名空间组件。例如，在 UI 中，名为 `plugin-dev` 的 plugin 的 agent `agent-creator` 将显示为 `plugin-dev:agent-creator`。

### 元数据字段

| 字段            | 类型     | 描述                                                                                                                                                                       | 示例                                                                |
| :------------ | :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------- |
| `$schema`     | string | 用于编辑器自动完成和验证的 JSON Schema URL。Claude Code 在加载时忽略此字段。                                                                                                                     | `"https://json.schemastore.org/claude-code-plugin-manifest.json"` |
| `version`     | string | 可选。语义版本。设置此项会将 plugin 固定到该版本字符串，因此用户仅在您提升版本时才会收到更新。如果省略，Claude Code 会回退到 git commit SHA，因此每个 commit 都被视为新版本。如果也在市场条目中设置，`plugin.json` 优先。请参阅[版本管理](#version-management)。 | `"2.1.0"`                                                         |
| `description` | string | plugin 目的的简要说明                                                                                                                                                           | `"Deployment automation tools"`                                   |
| `author`      | object | 作者信息                                                                                                                                                                     | `{"name": "Dev Team", "email": "dev@company.com"}`                |
| `homepage`    | string | 文档 URL                                                                                                                                                                   | `"https://docs.example.com"`                                      |
| `repository`  | string | 源代码 URL                                                                                                                                                                  | `"https://github.com/user/plugin"`                                |
| `license`     | string | 许可证标识符                                                                                                                                                                   | `"MIT"`、`"Apache-2.0"`                                            |
| `keywords`    | array  | 发现标签                                                                                                                                                                     | `["deployment", "ci-cd"]`                                         |

### 组件路径字段

| 字段                      | 类型                    | 描述                                                                                                     | 示例                                                   |
| :---------------------- | :-------------------- | :----------------------------------------------------------------------------------------------------- | :--------------------------------------------------- |
| `skills`                | string\|array         | 包含 `<name>/SKILL.md` 的自定义 skill 目录（除了默认 `skills/`）                                                     | `"./custom/skills/"`                                 |
| `commands`              | string\|array         | 自定义平面 `.md` skill 文件或目录（替换默认 `commands/`）                                                              | `"./custom/cmd.md"` 或 `["./cmd1.md"]`                |
| `agents`                | string\|array         | 自定义 agent 文件（替换默认 `agents/`）                                                                           | `"./custom/agents/reviewer.md"`                      |
| `hooks`                 | string\|array\|object | Hook 配置路径或内联配置                                                                                         | `"./my-extra-hooks.json"`                            |
| `mcpServers`            | string\|array\|object | MCP 配置路径或内联配置                                                                                          | `"./my-extra-mcp-config.json"`                       |
| `outputStyles`          | string\|array         | 自定义输出样式文件/目录（替换默认 `output-styles/`）                                                                    | `"./styles/"`                                        |
| `lspServers`            | string\|array\|object | [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) 配置用于代码智能（转到定义、查找引用等） | `"./.lsp.json"`                                      |
| `experimental.themes`   | string\|array         | 颜色主题文件/目录（替换默认 `themes/`）。请参阅[Themes](#themes)                                                         | `"./themes/"`                                        |
| `experimental.monitors` | string\|array         | 后台[Monitor](/zh-CN/tools-reference#monitor-tool)配置，在 plugin 激活时自动启动。请参阅[Monitors](#monitors)           | `"./monitors.json"`                                  |
| `userConfig`            | object                | 用户可配置的值，在启用时提示。请参阅[用户配置](#user-configuration)                                                          | 见下文                                                  |
| `channels`              | array                 | 消息注入的频道声明（Telegram、Slack、Discord 风格）。请参阅[Channels](#channels)                                          | 见下文                                                  |
| `dependencies`          | array                 | 此 plugin 需要的其他 plugins，可选择带有 semver 版本约束。请参阅[约束 plugin 依赖版本](/zh-CN/plugin-dependencies)               | `[{ "name": "secrets-vault", "version": "~2.1.0" }]` |

### 实验性组件

`experimental` 键下的组件，`themes` 和 `monitors`，具有在稳定期间可能在版本之间更改的清单架构。您声明它们的位置是一个单独的迁移：顶级仍然有效，`claude plugin validate` 发出警告，未来的版本将需要 `experimental.*`。

### 用户配置

`userConfig` 字段声明了 Claude Code 在启用 plugin 时提示用户的值。使用此字段而不是要求用户手动编辑 `settings.json`。

```json theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "type": "string",
      "title": "API endpoint",
      "description": "Your team's API endpoint"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "API authentication token",
      "sensitive": true
    }
  }
}
```

键必须是有效的标识符。每个选项支持这些字段：

| 字段            | 必需 | 描述                                                    |
| :------------ | :- | :---------------------------------------------------- |
| `type`        | 是  | 以下之一：`string`、`number`、`boolean`、`directory` 或 `file` |
| `title`       | 是  | 在配置对话框中显示的标签                                          |
| `description` | 是  | 显示在字段下方的帮助文本                                          |
| `sensitive`   | 否  | 如果为 `true`，掩盖输入并将值存储在安全存储中而不是 `settings.json`         |
| `required`    | 否  | 如果为 `true`，当字段为空时验证失败                                 |
| `default`     | 否  | 用户未提供任何内容时使用的值                                        |
| `multiple`    | 否  | 对于 `string` 类型，允许字符串数组                                |
| `min` / `max` | 否  | `number` 类型的边界                                        |

每个值都可用于在 MCP 和 LSP server 配置、hook 命令和 monitor 命令中作为 `${user_config.KEY}` 进行替换。非敏感值也可以在 skill 和 agent 内容中替换。所有值都作为 `CLAUDE_PLUGIN_OPTION_<KEY>` 环境变量导出到 plugin 子进程。

非敏感值存储在 `settings.json` 中的 `pluginConfigs[<plugin-id>].options` 下。敏感值进入系统钥匙链（或在钥匙链不可用的地方进入 `~/.claude/.credentials.json`）。钥匙链存储与 OAuth 令牌共享，总限制约为 2 KB，因此请保持敏感值较小。

### Channels

`channels` 字段允许 plugin 声明一个或多个消息频道，将内容注入到对话中。每个频道绑定到 plugin 提供的 MCP server。

```json theme={null}
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Telegram bot token",
          "sensitive": true
        },
        "owner_id": {
          "type": "string",
          "title": "Owner ID",
          "description": "Your Telegram user ID"
        }
      }
    }
  ]
}
```

`server` 字段是必需的，必须与 plugin 的 `mcpServers` 中的键匹配。可选的每个频道 `userConfig` 使用与顶级字段相同的架构，允许 plugin 在启用 plugin 时提示输入机器人令牌或所有者 ID。

### 路径行为规则

自定义路径是否替换或扩展 plugin 的默认目录取决于该字段：

* **替换默认值**：`commands`、`agents`、`outputStyles`、`experimental.themes`、`experimental.monitors`。例如，当清单指定 `commands` 时，不会扫描默认 `commands/` 目录。要保留默认值并添加更多，请明确列出它：`"commands": ["./commands/", "./extras/"]`
* **添加到默认值**：`skills`。默认 `skills/` 目录始终被扫描，`skills` 中列出的目录与其一起加载
* **自己的合并规则**：[hooks](#hooks)、[MCP servers](#mcp-servers) 和 [LSP servers](#lsp-servers)。请参阅每个部分了解多个源如何组合

当 plugin 同时具有默认文件夹和匹配的清单键时，Claude Code v2.1.140 及更高版本在 `/doctor`、`claude plugin list` 和 `/plugin` 详细视图中标记被忽略的文件夹。plugin 仍然使用清单路径加载。当清单键指向默认文件夹时不显示警告，例如 `"commands": ["./commands/deploy.md"]`，因为在这种情况下文件夹被明确寻址。

对于所有路径字段：

* 所有路径必须相对于 plugin 根目录，并以 `./` 开头
* 来自自定义路径的组件使用相同的命名和命名空间规则
* 可以将多个路径指定为数组
* 当 skill 路径指向直接包含 `SKILL.md` 的目录时，例如 `"skills": ["./"]` 指向 plugin 根目录，frontmatter 中的 `name` 字段确定 skill 的调用名称。这提供了一个稳定的名称，无论安装目录如何。如果 frontmatter 中未设置 `name`，则使用目录基名作为后备。

**路径示例**：

```json theme={null}
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### 环境变量

Claude Code 提供三个变量用于引用路径。所有这些变量都在 skill 内容、agent 内容、hook 命令、monitor 命令以及 MCP 或 LSP server 配置中出现的任何地方进行内联替换。所有这些变量也都作为环境变量导出到 hook 进程和 MCP 或 LSP server 子进程。

**`${CLAUDE_PLUGIN_ROOT}`**：plugin 安装目录的绝对路径。使用此路径引用与 plugin 捆绑的脚本、二进制文件和配置文件。在 hook 命令中，使用[执行形式](/zh-CN/hooks#exec-form-and-shell-form)与 `args` 以便路径作为一个参数传递，无需引用。在 shell 形式的 hooks 和 monitor 命令中，用双引号包装它，如 `"${CLAUDE_PLUGIN_ROOT}"`。当 plugin 更新时，此路径会更改。前一个版本的目录在更新后约七天内保留在磁盘上以进行清理，但应将其视为临时的，不要在此处写入状态。

当 plugin 在会话中期更新时，hook 命令、monitors、MCP servers 和 LSP servers 继续使用前一个版本的路径。运行 `/reload-plugins` 以将 hooks、MCP servers 和 LSP servers 切换到新路径；monitors 需要会话重启。

**`${CLAUDE_PLUGIN_DATA}`**：用于 plugin 状态的持久目录，在更新后保留。使用此目录用于已安装的依赖项，如 `node_modules` 或 Python 虚拟环境、生成的代码、缓存以及任何应在 plugin 版本之间保留的其他文件。首次引用此变量时，目录会自动创建。

**`${CLAUDE_PROJECT_DIR}`**：项目根目录。这是 hooks 在其 `CLAUDE_PROJECT_DIR` 变量中接收的相同目录。使用此路径引用项目本地脚本或配置文件。用引号包装以处理包含空格的路径，例如 `"${CLAUDE_PROJECT_DIR}/scripts/server.sh"`。MCP servers 也可以调用 MCP `roots/list` 请求，该请求返回启动 Claude Code 的目录。

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

#### 持久数据目录

`${CLAUDE_PLUGIN_DATA}` 目录解析为 `~/.claude/plugins/data/{id}/`，其中 `{id}` 是 plugin 标识符，其中 `a-z`、`A-Z`、`0-9`、`_` 和 `-` 之外的字符被替换为 `-`。对于安装为 `formatter@my-marketplace` 的 plugin，目录是 `~/.claude/plugins/data/formatter-my-marketplace/`。

常见用途是一次安装语言依赖项并在会话和 plugin 更新中重复使用它们。由于数据目录的生命周期长于任何单个 plugin 版本，仅检查目录存在性无法检测到更新何时更改了 plugin 的依赖项清单。推荐的模式是将捆绑的清单与数据目录中的副本进行比较，并在它们不同时重新安装。

此 `SessionStart` hook 在第一次运行时安装 `node_modules`，并在 plugin 更新包含更改的 `package.json` 时再次安装：

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

当存储的副本缺失或与捆绑的副本不同时，`diff` 退出非零，涵盖第一次运行和依赖项更改的更新。如果 `npm install` 失败，尾部的 `rm` 会删除复制的清单，以便下一个会话重试。

捆绑在 `${CLAUDE_PLUGIN_ROOT}` 中的脚本可以针对持久的 `node_modules` 运行：

```json theme={null}
{
  "mcpServers": {
    "routines": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```

当您从最后一个安装了 plugin 的范围卸载 plugin 时，数据目录会自动删除。`/plugin` 界面显示目录大小并在删除前提示。CLI 默认删除；传递 [`--keep-data`](#plugin-uninstall) 以保留它。

***

## Plugin 缓存和文件解析

Plugins 通过以下两种方式之一指定：

* 通过 `claude --plugin-dir` 或 `claude --plugin-url`，用于会话期间。
* 通过市场，为将来的会话安装。

出于安全和验证目的，Claude Code 将\_市场\_ plugins 复制到用户的本地 **plugin 缓存**（`~/.claude/plugins/cache`），而不是就地使用它们。在开发引用外部文件的 plugins 时，理解此行为很重要。

每个已安装的版本是缓存中的单独目录。当您更新或卸载 plugin 时，前一个版本目录被标记为孤立，并在 7 天后自动删除。宽限期允许已加载旧版本的并发 Claude Code 会话继续运行而不出错。

Claude 的 Glob 和 Grep 工具在搜索期间跳过孤立版本目录，因此文件结果不包括过时的插件代码。

### 路径遍历限制

已安装的 plugins 无法引用其目录外的文件。遍历 plugin 根目录外的路径（例如 `../shared-utils`）在安装后将不起作用，因为这些外部文件不会被复制到缓存中。

### 使用符号链接在市场内共享文件

如果您的 plugin 需要与同一市场的其他部分共享文件，您可以在 plugin 目录中创建符号链接。当 plugin 被复制到缓存中时，符号链接的处理方式取决于其目标的解析位置：

* **在 plugin 自己的目录内：** 符号链接在缓存中被保留为相对符号链接，因此它在运行时继续解析到复制的目标。
* **在同一市场内的其他位置：** 符号链接被解引用。目标的内容被复制到缓存中以替代它。这允许元 plugin 的 `skills/` 目录链接到市场中其他 plugins 定义的技能。
* **在市场外：** 符号链接出于安全考虑被跳过。这防止 plugins 从任意主机文件（如系统路径）拉入缓存。

对于使用 `--plugin-dir` 安装或从本地路径安装的 plugins，只有解析到 plugin 自己目录内的符号链接被保留。所有其他的都被跳过。

以下命令创建从市场 plugin 内部到由同级 plugin 定义的共享技能的链接。在 Windows 上，从提升的命令提示符使用 `mklink /D` 或启用开发者模式：

```bash theme={null}
ln -s ../../shared-plugin/skills/foo ./skills/foo
```

这在保持缓存系统安全优势的同时提供了灵活性。

***

## Plugin 目录结构

### 标准 plugin 布局

完整的 plugin 遵循此结构：

```text theme={null}
enterprise-plugin/
├── .claude-plugin/           # 元数据目录（可选）
│   └── plugin.json             # plugin 清单
├── skills/                   # Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── commands/                 # Skills 作为平面 .md 文件
│   ├── status.md
│   └── logs.md
├── agents/                   # Subagent 定义
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── output-styles/            # 输出样式定义
│   └── terse.md
├── themes/                   # 颜色主题定义
│   └── dracula.json
├── monitors/                 # 后台 monitor 配置
│   └── monitors.json
├── hooks/                    # Hook 配置
│   ├── hooks.json           # 主 hook 配置
│   └── security-hooks.json  # 其他 hooks
├── bin/                      # 添加到 PATH 的 plugin 可执行文件
│   └── my-tool               # 在 Bash tool 中可作为裸命令调用
├── settings.json            # plugin 的默认设置
├── .mcp.json                # MCP server 定义
├── .lsp.json                # LSP server 配置
├── scripts/                 # Hook 和实用脚本
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # 许可证文件
└── CHANGELOG.md             # 版本历史
```

<Warning>
  `.claude-plugin/` 目录包含 `plugin.json` 文件。所有其他目录（commands/、agents/、skills/、output-styles/、themes/、monitors/、hooks/）必须在 plugin 根目录，而不是在 `.claude-plugin/` 内。
</Warning>

plugin 根目录中的 `CLAUDE.md` 文件不会作为项目上下文加载。Plugins 通过 skills、agents 和 hooks 而不是 CLAUDE.md 来贡献上下文。要提供加载到 Claude 上下文中的说明，请将其放在 [skill](#skills) 中。

### 文件位置参考

| 组件                | 默认位置                         | 目的                                                                                                                        |
| :---------------- | :--------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| **清单**            | `.claude-plugin/plugin.json` | Plugin 元数据和配置（可选）                                                                                                         |
| **Skills**        | `skills/`                    | 具有 `<name>/SKILL.md` 结构的 Skills                                                                                           |
| **Commands**      | `commands/`                  | Skills 作为平面 Markdown 文件。新 plugins 使用 `skills/`                                                                            |
| **Agents**        | `agents/`                    | Subagent Markdown 文件                                                                                                      |
| **Output styles** | `output-styles/`             | 输出样式定义                                                                                                                    |
| **Themes**        | `themes/`                    | 颜色主题定义                                                                                                                    |
| **Hooks**         | `hooks/hooks.json`           | Hook 配置                                                                                                                   |
| **MCP servers**   | `.mcp.json`                  | MCP server 定义                                                                                                             |
| **LSP servers**   | `.lsp.json`                  | 语言服务器配置                                                                                                                   |
| **Monitors**      | `monitors/monitors.json`     | 后台 monitor 配置                                                                                                             |
| **Executables**   | `bin/`                       | 添加到 Bash tool 的 `PATH` 的可执行文件。此处的文件在 plugin 启用时可作为任何 Bash tool 调用中的裸命令调用                                                  |
| **Settings**      | `settings.json`              | 启用 plugin 时应用的默认配置。目前仅支持 [`agent`](/zh-CN/sub-agents) 和 [`subagentStatusLine`](/zh-CN/statusline#subagent-status-lines) 键 |

***

## CLI 命令参考

Claude Code 提供了用于非交互式 plugin 管理的 CLI 命令，对脚本和自动化很有用。

### plugin install

从可用市场安装 plugin。

```bash theme={null}
claude plugin install <plugin> [options]
```

**参数：**

* `<plugin>`：Plugin 名称或 `plugin-name@marketplace-name` 用于特定市场

**选项：**

| 选项                    | 描述                              | 默认值    |
| :-------------------- | :------------------------------ | :----- |
| `-s, --scope <scope>` | 安装范围：`user`、`project` 或 `local` | `user` |
| `-h, --help`          | 显示命令帮助                          |        |

范围确定将已安装的 plugin 添加到哪个设置文件。例如，`--scope project` 写入 `.claude/settings.json` 中的 `enabledPlugins`，使 plugin 对克隆项目存储库的每个人都可用。

**示例：**

```bash theme={null}
# 安装到用户范围（默认）
claude plugin install formatter@my-marketplace

# 安装到项目范围（与团队共享）
claude plugin install formatter@my-marketplace --scope project

# 安装到本地范围（gitignored）
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

删除已安装的 plugin。

```bash theme={null}
claude plugin uninstall <plugin> [options]
```

**参数：**

* `<plugin>`：Plugin 名称或 `plugin-name@marketplace-name`

**选项：**

| 选项                    | 描述                                                          | 默认值    |
| :-------------------- | :---------------------------------------------------------- | :----- |
| `-s, --scope <scope>` | 从范围卸载：`user`、`project` 或 `local`                            | `user` |
| `--keep-data`         | 保留插件的[持久数据目录](#persistent-data-directory)                   |        |
| `--prune`             | 同时删除其他 plugin 不需要的自动安装依赖项。请参阅 [plugin prune](#plugin-prune) |        |
| `-y, --yes`           | 跳过 `--prune` 确认提示。当 stdin 不是 TTY 时需要                        |        |
| `-h, --help`          | 显示命令帮助                                                      |        |

**别名：** `remove`、`rm`

默认情况下，从最后一个剩余范围卸载也会删除插件的 `${CLAUDE_PLUGIN_DATA}` 目录。使用 `--keep-data` 保留它，例如在测试新版本后重新安装时。

### plugin prune

删除不再被任何已安装 plugin 需要的自动安装 plugin 依赖项。Claude Code 为满足另一个 plugin 的 [`dependencies`](/zh-CN/plugin-dependencies) 字段而引入的依赖项将被删除；您直接安装的 plugin 永远不会被触及。

```bash theme={null}
claude plugin prune [options]
```

**选项：**

| 选项                    | 描述                                | 默认值    |
| :-------------------- | :-------------------------------- | :----- |
| `-s, --scope <scope>` | 在范围处修剪：`user`、`project` 或 `local` | `user` |
| `--dry-run`           | 列出将被删除的内容而不实际删除                   |        |
| `-y, --yes`           | 跳过确认提示。当 stdin 不是 TTY 时需要         |        |
| `-h, --help`          | 显示命令帮助                            |        |

**别名：** `autoremove`

该命令列出孤立的依赖项，并在删除前要求确认。要在一个步骤中删除 plugin 并清理其依赖项，请运行 `claude plugin uninstall <plugin> --prune`。

<Note>
  `claude plugin prune` 需要 Claude Code v2.1.121 或更高版本。
</Note>

### plugin enable

启用已禁用的 plugin。

```bash theme={null}
claude plugin enable <plugin> [options]
```

**参数：**

* `<plugin>`：Plugin 名称或 `plugin-name@marketplace-name`

**选项：**

| 选项                    | 描述                                | 默认值    |
| :-------------------- | :-------------------------------- | :----- |
| `-s, --scope <scope>` | 要启用的范围：`user`、`project` 或 `local` | `user` |
| `-h, --help`          | 显示命令帮助                            |        |

### plugin disable

禁用 plugin 而不卸载它。

```bash theme={null}
claude plugin disable <plugin> [options]
```

**参数：**

* `<plugin>`：Plugin 名称或 `plugin-name@marketplace-name`

**选项：**

| 选项                    | 描述                                | 默认值    |
| :-------------------- | :-------------------------------- | :----- |
| `-s, --scope <scope>` | 要禁用的范围：`user`、`project` 或 `local` | `user` |
| `-h, --help`          | 显示命令帮助                            |        |

### plugin update

将 plugin 更新到最新版本。

```bash theme={null}
claude plugin update <plugin> [options]
```

**参数：**

* `<plugin>`：Plugin 名称或 `plugin-name@marketplace-name`

**选项：**

| 选项                    | 描述                                          | 默认值    |
| :-------------------- | :------------------------------------------ | :----- |
| `-s, --scope <scope>` | 要更新的范围：`user`、`project`、`local` 或 `managed` | `user` |
| `-h, --help`          | 显示命令帮助                                      |        |

***

### plugin list

列出已安装的 plugins 及其版本、源市场和启用状态。

```bash theme={null}
claude plugin list [options]
```

**选项：**

| 选项            | 描述                            | 默认值 |
| :------------ | :---------------------------- | :-- |
| `--json`      | 输出为 JSON                      |     |
| `--available` | 包括来自市场的可用 plugins。需要 `--json` |     |
| `-h, --help`  | 显示命令帮助                        |     |

### plugin details

显示 plugin 的组件清单和预计令牌成本。输出列出 plugin 贡献的所有组件，分组为 Skills（技能和命令）、Agents、Hooks 和 MCP servers，以及它为每个会话添加多少令牌的估计。

```bash theme={null}
claude plugin details <name>
```

**参数：**

* `<name>`：Plugin 名称或 `plugin-name@marketplace-name`

**选项：**

| 选项           | 描述     | 默认值 |
| :----------- | :----- | :-- |
| `-h, --help` | 显示命令帮助 |     |

输出为每个组件显示两个成本数字：

* **Always-on：** plugin 的列表文本（如技能描述、agent 描述和命令名称）添加到每个会话的令牌，无论是否有任何组件触发。
* **On-invoke：** 组件触发时的成本令牌。按组件显示，而不是作为 plugin 总计，因为典型会话仅调用组件的子集。

此示例显示具有两个技能的 plugin 的输出外观：

```
security-guidance 1.2.0
  Real-time security analysis for Claude Code sessions
  Source: security-guidance@claude-code-marketplace

Component inventory
  Skills (2)  scan-dependencies, review-changes
  Agents (0)
  Hooks (1)  (harness-only — no model context cost)
  MCP servers (0)

Projected token cost
  Always-on:   ~180 tok   added to every session

Per-component (rounded)
  component            always-on  on-invoke
  scan-dependencies        ~100      ~2400
  review-changes            ~80      ~1800

  On-invoke cost is paid each time a skill or agent fires.
  Token counts are estimates and may differ from actual usage.
```

always-on 总计通过您的活跃模型的 `count_tokens` API 计算。按组件的数字按比例从该总计缩放。如果 API 无法访问，该命令会回退到基于字符的估计。

### plugin tag

为当前目录中的 plugin 创建发布 git 标签。从 plugin 的文件夹内运行。请参阅[标记 plugin 发布](/zh-CN/plugin-dependencies#tag-plugin-releases-for-version-resolution)。

```bash theme={null}
claude plugin tag [options]
```

**选项：**

| 选项            | 描述                   | 默认值 |
| :------------ | :------------------- | :-- |
| `--push`      | 创建标签后将其推送到远程         |     |
| `--dry-run`   | 打印将被标记的内容而不创建标签      |     |
| `-f, --force` | 即使工作树是脏的或标签已存在，也创建标签 |     |
| `-h, --help`  | 显示命令帮助               |     |

***

## 调试和开发工具

### 调试命令

使用 `claude --debug` 查看 plugin 加载详情：

这显示：

* 正在加载哪些 plugins
* plugin 清单中的任何错误
* Skill、agent 和 hook 注册
* MCP server 初始化

### 常见问题

| 问题                                  | 原因                         | 解决方案                                                                                                                            |
| :---------------------------------- | :------------------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| Plugin 未加载                          | 无效的 `plugin.json`          | 运行 `claude plugin validate` 或 `/plugin validate` 检查 `plugin.json`、skill/agent/command frontmatter 和 `hooks/hooks.json` 的语法和架构错误 |
| Skills 未出现                          | 目录结构错误                     | 确保 `skills/` 或 `commands/` 在根目录，而不是在 `.claude-plugin/` 中                                                                        |
| Hooks 未触发                           | 脚本不可执行                     | 运行 `chmod +x script.sh`                                                                                                         |
| MCP server 失败                       | 缺少 `${CLAUDE_PLUGIN_ROOT}` | 对所有 plugin 路径使用变量                                                                                                               |
| 路径错误                                | 使用了绝对路径                    | 所有路径必须是相对的，并以 `./` 开头                                                                                                           |
| LSP `Executable not found in $PATH` | 语言服务器未安装                   | 安装二进制文件（例如，`npm install -g typescript-language-server typescript`）                                                              |

### 示例错误消息

**清单验证错误**：

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`：检查缺少的逗号、多余的逗号或未引用的字符串
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`：缺少必需字段
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`：JSON 语法错误

**Plugin 加载错误**：

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`：命令路径存在但不包含有效的命令文件
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`：marketplace.json 中的 `source` 路径指向不存在的目录
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`：删除重复的组件定义或删除 marketplace 条目中的 `strict: false`

### Hook 故障排除

**Hook 脚本未执行**：

1. 检查脚本是否可执行：`chmod +x ./scripts/your-script.sh`
2. 验证 shebang 行：第一行应该是 `#!/bin/bash` 或 `#!/usr/bin/env bash`
3. 检查路径是否使用 `${CLAUDE_PLUGIN_ROOT}`：`"command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/your-script.sh"`
4. 手动测试脚本：`./scripts/your-script.sh`

**Hook 未在预期事件上触发**：

1. 验证事件名称是否正确（区分大小写）：`PostToolUse`，而不是 `postToolUse`
2. 检查匹配器模式是否与您的工具匹配：`"matcher": "Write|Edit"` 用于文件操作
3. 确认 hook 类型有效：`command`、`http`、`mcp_tool`、`prompt` 或 `agent`

### MCP server 故障排除

**Server 未启动**：

1. 检查命令是否存在且可执行
2. 验证所有路径是否使用 `${CLAUDE_PLUGIN_ROOT}` 变量
3. 检查 MCP server 日志：`claude --debug` 显示初始化错误
4. 在 Claude Code 外手动测试 server

**Server 工具未出现**：

1. 确保 server 在 `.mcp.json` 或 `plugin.json` 中正确配置
2. 验证 server 是否正确实现 MCP 协议
3. 检查调试输出中的连接超时

### 目录结构错误

**症状**：Plugin 加载但组件（skills、agents、hooks）缺失。

**正确结构**：组件必须在 plugin 根目录，而不是在 `.claude-plugin/` 内。只有 `plugin.json` 属于 `.claude-plugin/`。

```text theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← 仅清单在此处
├── commands/            ← 在根级别
├── agents/              ← 在根级别
└── hooks/               ← 在根级别
```

如果您的组件在 `.claude-plugin/` 内，请将它们移到 plugin 根目录。

**调试清单**：

1. 运行 `claude --debug` 并查找"loading plugin"消息
2. 检查每个组件目录是否在调试输出中列出
3. 验证文件权限允许读取 plugin 文件

***

## 分发和版本管理参考

### 版本管理

Claude Code 使用 plugin 的版本作为缓存键，以确定是否有可用的更新。当你运行 `/plugin update` 或自动更新触发时，Claude Code 会计算当前版本，如果与已安装的版本匹配，则跳过更新。

版本从以下第一个设置的字段解析：

1. plugin 的 `plugin.json` 中的 `version` 字段
2. plugin 的 `marketplace.json` 中的市场条目中的 `version` 字段
3. plugin 源的 git 提交 SHA，用于 git 托管市场中的 `github`、`url`、`git-subdir` 和相对路径源
4. `unknown`，用于 `npm` 源或不在 git 仓库内的本地目录

这为你提供了两种方式来对 plugin 进行版本管理：

| 方法            | 如何操作                                     | 更新行为                                                        | 最适合                 |
| :------------ | :--------------------------------------- | :---------------------------------------------------------- | :------------------ |
| **显式版本**      | 在 `plugin.json` 中设置 `"version": "2.1.0"` | 用户仅在你提升此字段时获得更新。推送新提交而不提升它没有效果，`/plugin update` 报告"已是最新版本"。 | 具有稳定发布周期的已发布 plugin |
| **提交 SHA 版本** | 从 `plugin.json` 和市场条目中省略 `version`       | 用户在每次对 plugin 的 git 源进行新提交时获得更新                             | 正在积极开发的内部或团队 plugin |

<Warning>
  如果你在 `plugin.json` 中设置 `version`，你必须在每次想让用户接收更改时提升它。仅推送新提交是不够的，因为 Claude Code 看到相同的版本字符串并保留缓存副本。如果你迭代速度很快，请不设置 `version`，以便改用 git 提交 SHA。
</Warning>

如果你使用显式版本，请遵循[语义版本控制](https://semver.org)（`MAJOR.MINOR.PATCH`）：为破坏性更改提升 MAJOR，为新功能提升 MINOR，为错误修复提升 PATCH。在 `CHANGELOG.md` 中记录更改。

***

## 另请参阅

* [Plugins](/zh-CN/plugins) - 教程和实际用法
* [Plugin marketplaces](/zh-CN/plugin-marketplaces) - 创建和管理市场
* [Skills](/zh-CN/skills) - Skill 开发详情
* [Subagents](/zh-CN/sub-agents) - Agent 配置和功能
* [Hooks](/zh-CN/hooks) - 事件处理和自动化
* [MCP](/zh-CN/mcp) - 外部工具集成
* [Settings](/zh-CN/settings) - Plugins 的配置选项

> ## Documentation Index
>
> Fetch the complete documentation index at: <https://code.claude.com/docs/llms.txt>
> Use this file to discover all available pages before exploring further.

# Channels 参考

> 构建一个 MCP 服务器，将 webhooks、警报和聊天消息推送到 Claude Code 会话中。频道合约的参考：能力声明、通知事件、回复工具、发送者门控和权限中继。

<Note>
  Channels 处于[研究预览](/zh-CN/channels#research-preview)阶段，需要 Claude Code v2.1.80 或更高版本。它们需要 claude.ai 登录。不支持控制台和 API 密钥身份验证。Team 和 Enterprise 组织必须[明确启用它们](/zh-CN/channels#enterprise-controls)。
</Note>

Channel 是一个 MCP 服务器，它将事件推送到 Claude Code 会话中，以便 Claude 可以对终端外发生的事情做出反应。

您可以构建单向或双向频道。单向频道转发警报、webhooks 或监控事件供 Claude 处理。双向频道（如聊天桥接）也[公开回复工具](#expose-a-reply-tool)，以便 Claude 可以发送消息回复。具有受信任发送者路径的频道也可以选择加入[中继权限提示](#relay-permission-prompts)，以便您可以远程批准或拒绝工具使用。

本页涵盖：

* [概述](#overview)：频道如何工作
* [您需要什么](#what-you-need)：要求和一般步骤
* [示例：构建 webhook 接收器](#example-build-a-webhook-receiver)：最小单向演练
* [服务器选项](#server-options)：构造函数字段
* [通知格式](#notification-format)：事件有效负载
* [公开回复工具](#expose-a-reply-tool)：让 Claude 发送消息回复
* [门控入站消息](#gate-inbound-messages)：发送者检查以防止提示注入
* [中继权限提示](#relay-permission-prompts)：将工具批准提示转发到远程频道

要使用现有频道而不是构建一个，请参阅 [Channels](/zh-CN/channels)。Telegram、Discord、iMessage 和 fakechat 包含在研究预览中。

## 概述

Channel 是一个在与 Claude Code 相同的机器上运行的 [MCP](https://modelcontextprotocol.io) 服务器。Claude Code 将其作为子进程生成并通过 stdio 进行通信。您的频道服务器是外部系统和 Claude Code 会话之间的桥梁：

* **聊天平台**（Telegram、Discord）：您的插件在本地运行并轮询平台的 API 以获取新消息。当有人向您的机器人发送 DM 时，插件接收消息并将其转发给 Claude。无需公开 URL。
* **Webhooks**（CI、监控）：您的服务器在本地 HTTP 端口上侦听。外部系统 POST 到该端口，您的服务器将有效负载推送到 Claude。

<img src="https://mintlify.s3.us-west-1.amazonaws.com/claude-code/zh-CN/images/channel-architecture.svg" alt="架构图显示外部系统连接到您的本地频道服务器，该服务器通过 stdio 与 Claude Code 通信" />

## 您需要什么

唯一的硬性要求是 [`@modelcontextprotocol/sdk`](https://www.npmjs.com/package/@modelcontextprotocol/sdk) 包和 Node.js 兼容的运行时。[Bun](https://bun.sh)、[Node](https://nodejs.org) 和 [Deno](https://deno.com) 都可以工作。研究预览中的预构建插件使用 Bun，但您的频道不一定要使用。

您的服务器需要：

1. 声明 `claude/channel` 能力，以便 Claude Code 注册通知侦听器
2. 当发生某事时发出 `notifications/claude/channel` 事件
3. 通过 [stdio transport](https://modelcontextprotocol.io/docs/concepts/transports#standard-io) 连接（Claude Code 将您的服务器作为子进程生成）

[服务器选项](#server-options)和[通知格式](#notification-format)部分详细介绍了每一项。有关完整演练，请参阅[示例：构建 webhook 接收器](#example-build-a-webhook-receiver)。

在研究预览期间，自定义频道不在[批准的允许列表](/zh-CN/channels#supported-channels)上。使用 `--dangerously-load-development-channels` 在本地测试。有关详细信息，请参阅[在研究预览期间测试](#test-during-the-research-preview)。

## 示例：构建 webhook 接收器

本演练构建一个单文件服务器，该服务器侦听 HTTP 请求并将其转发到您的 Claude Code 会话中。最后，任何可以发送 HTTP POST 的东西，如 CI 管道、监控警报或 `curl` 命令，都可以将事件推送到 Claude。

此示例使用 [Bun](https://bun.sh) 作为运行时，用于其内置的 HTTP 服务器和 TypeScript 支持。您可以改用 [Node](https://nodejs.org) 或 [Deno](https://deno.com)；唯一的要求是 [MCP SDK](https://www.npmjs.com/package/@modelcontextprotocol/sdk)。

<Steps>
  <Step title="创建项目">
    创建一个新目录并安装 MCP SDK：

    ```bash theme={null}
    mkdir webhook-channel && cd webhook-channel
    bun add @modelcontextprotocol/sdk
    ```
  </Step>

  <Step title="编写频道服务器">
    创建一个名为 `webhook.ts` 的文件。这是您的整个频道服务器：它通过 stdio 连接到 Claude Code，并在端口 8788 上侦听 HTTP POST。当请求到达时，它将主体作为频道事件推送到 Claude。

    ```ts title="webhook.ts" theme={null}
    #!/usr/bin/env bun
    import { Server } from '@modelcontextprotocol/sdk/server/index.js'
    import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'

    // 创建 MCP 服务器并将其声明为频道
    const mcp = new Server(
      { name: 'webhook', version: '0.0.1' },
      {
        // 这个键使其成为频道 — Claude Code 为其注册侦听器
        capabilities: { experimental: { 'claude/channel': {} } },
        // 添加到 Claude 的系统提示，以便它知道如何处理这些事件
        instructions: 'Events from the webhook channel arrive as <channel source="webhook" ...>. They are one-way: read them and act, no reply expected.',
      },
    )

    // 通过 stdio 连接到 Claude Code（Claude Code 生成此进程）
    await mcp.connect(new StdioServerTransport())

    // 启动一个 HTTP 服务器，将每个 POST 转发给 Claude
    Bun.serve({
      port: 8788,  // 任何开放端口都可以
      // 仅限本地主机：此机器外的任何东西都无法 POST
      hostname: '127.0.0.1',
      async fetch(req) {
        const body = await req.text()
        await mcp.notification({
          method: 'notifications/claude/channel',
          params: {
            content: body,  // 成为 <channel> 标签的主体
            // 每个键都成为标签属性，例如 <channel path="/" method="POST">
            meta: { path: new URL(req.url).pathname, method: req.method },
          },
        })
        return new Response('ok')
      },
    })
    ```

    该文件按顺序执行三项操作：

    * **服务器配置**：使用 `claude/channel` 在其能力中创建 MCP 服务器，这是告诉 Claude Code 这是一个频道的原因。[`instructions`](#server-options) 字符串进入 Claude 的系统提示：告诉 Claude 期望什么事件、是否回复以及如果应该回复，使用哪个工具和传回哪个属性。
    * **Stdio 连接**：通过 stdin/stdout 连接到 Claude Code。这对任何 [MCP 服务器](https://modelcontextprotocol.io/docs/concepts/transports#standard-io) 都是标准的：Claude Code 将其作为子进程生成。
    * **HTTP 侦听器**：在端口 8788 上启动本地 Web 服务器。每个 POST 主体都通过 `mcp.notification()` 作为频道事件转发给 Claude。`content` 成为事件主体，每个 `meta` 条目成为 `<channel>` 标签上的属性。侦听器需要访问 `mcp` 实例，因此它在同一进程中运行。对于更大的项目，您可以将其拆分为单独的模块。
  </Step>

  <Step title="向 Claude Code 注册您的服务器">
    将服务器添加到您的 MCP 配置中，以便 Claude Code 知道如何启动它。对于同一目录中的项目级 `.mcp.json`，使用相对路径。对于 `~/.claude.json` 中的用户级配置，使用完整的绝对路径，以便可以从任何项目找到服务器：

    ```json title=".mcp.json" theme={null}
    {
      "mcpServers": {
        "webhook": { "command": "bun", "args": ["./webhook.ts"] }
      }
    }
    ```

    Claude Code 在启动时读取您的 MCP 配置并将每个服务器作为子进程生成。
  </Step>

  <Step title="测试它">
    在研究预览期间，自定义频道不在允许列表上，因此使用开发标志启动 Claude Code：

    ```bash theme={null}
    claude --dangerously-load-development-channels server:webhook
    ```

    当 Claude Code 启动时，它读取您的 MCP 配置，将您的 `webhook.ts` 作为子进程生成，HTTP 侦听器自动在您配置的端口上启动（此示例中为 8788）。您不需要自己运行服务器。

    如果您看到"被组织政策阻止"，您的 Team 或 Enterprise 管理员需要[启用频道](/zh-CN/channels#enterprise-controls)。

    在单独的终端中，通过向您的服务器发送带有消息的 HTTP POST 来模拟 webhook。此示例向端口 8788 发送 CI 失败警报（或您配置的任何端口）：

    ```bash theme={null}
    curl -X POST localhost:8788 -d "build failed on main: https://ci.example.com/run/1234"
    ```

    有效负载作为 `<channel>` 标签到达您的 Claude Code 会话中：

    ```text theme={null}
    <channel source="webhook" path="/" method="POST">build failed on main: https://ci.example.com/run/1234</channel>
    ```

    在您的 Claude Code 终端中，您会看到 Claude 接收消息并开始响应：读取文件、运行命令或消息要求的任何操作。这是一个单向频道，因此 Claude 在您的会话中行动，但不会通过 webhook 发送任何内容回复。要添加回复，请参阅[公开回复工具](#expose-a-reply-tool)。

    如果事件没有到达，诊断取决于 `curl` 返回的内容：

    * **`curl` 成功但没有任何内容到达 Claude**：在您的会话中运行 `/mcp` 以检查服务器的状态。"Failed to connect"通常意味着您的服务器文件中存在依赖项或导入错误；检查 `~/.claude/debug/<session-id>.txt` 处的调试日志以获取 stderr 跟踪。
    * **`curl` 失败，显示"connection refused"**：端口要么尚未绑定，要么来自较早运行的陈旧进程正在占用它。`lsof -i :<port>` 显示正在侦听的内容；在重新启动会话之前 `kill` 陈旧进程。
  </Step>
</Steps>

[fakechat 服务器](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/fakechat)使用 Web UI、文件附件和用于双向聊天的回复工具扩展此模式。

## 在研究预览期间测试

在研究预览期间，每个频道都必须在[批准的允许列表](/zh-CN/channels#research-preview)上才能注册。开发标志在确认提示后绕过特定条目的允许列表。此示例显示两种条目类型：

```bash theme={null}
# 测试您正在开发的插件
claude --dangerously-load-development-channels plugin:yourplugin@yourmarketplace

# 测试裸 .mcp.json 服务器（尚无插件包装器）
claude --dangerously-load-development-channels server:webhook
```

绕过是按条目的。将此标志与 `--channels` 结合不会将绕过扩展到 `--channels` 条目。在研究预览期间，批准的允许列表由 Anthropic 策划，因此您的频道在您构建和测试时保持在开发标志上。

<Note>
  此标志仅跳过允许列表。`channelsEnabled` 组织政策仍然适用。不要使用它来运行来自不受信任来源的频道。
</Note>

## 服务器选项

频道在 [`Server`](https://modelcontextprotocol.io/docs/concepts/servers) 构造函数中设置这些选项。`instructions` 和 `capabilities.tools` 字段是[标准 MCP](https://modelcontextprotocol.io/docs/concepts/servers)；`capabilities.experimental['claude/channel']` 和 `capabilities.experimental['claude/channel/permission']` 是频道特定的添加：

| 字段                                                       | 类型       | 描述                                                                                                                |
| :------------------------------------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------- |
| `capabilities.experimental['claude/channel']`            | `object` | 必需。始终为 `{}`。存在注册通知侦听器。                                                                                            |
| `capabilities.experimental['claude/channel/permission']` | `object` | 可选。始终为 `{}`。声明此频道可以接收权限中继请求。声明后，Claude Code 将工具批准提示转发到您的频道，以便您可以远程批准或拒绝它们。请参阅[中继权限提示](#relay-permission-prompts)。 |
| `capabilities.tools`                                     | `object` | 仅双向。始终为 `{}`。标准 MCP 工具能力。请参阅[公开回复工具](#expose-a-reply-tool)。                                                       |
| `instructions`                                           | `string` | 推荐。添加到 Claude 的系统提示。告诉 Claude 期望什么事件、`<channel>` 标签属性的含义、是否回复，如果是，使用哪个工具以及传回哪个属性（如 `chat_id`）。                    |

要创建单向频道，请省略 `capabilities.tools`。此示例显示双向设置，其中频道能力、工具和说明已设置：

```ts theme={null}
import { Server } from '@modelcontextprotocol/sdk/server/index.js'

const mcp = new Server(
  { name: 'your-channel', version: '0.0.1' },
  {
    capabilities: {
      experimental: { 'claude/channel': {} },  // 注册频道侦听器
      tools: {},  // 对于单向频道省略
    },
    // 添加到 Claude 的系统提示，以便它知道如何处理您的事件
    instructions: 'Messages arrive as <channel source="your-channel" ...>. Reply with the reply tool.',
  },
)
```

要推送事件，请使用方法 `notifications/claude/channel` 调用 `mcp.notification()`。参数在下一部分中。

## 通知格式

您的服务器使用两个参数发出 `notifications/claude/channel`：

| 字段        | 类型                       | 描述                                                                                             |
| :-------- | :----------------------- | :--------------------------------------------------------------------------------------------- |
| `content` | `string`                 | 事件主体。作为 `<channel>` 标签的主体传递。                                                                   |
| `meta`    | `Record<string, string>` | 可选。每个条目成为 `<channel>` 标签上的属性，用于路由上下文，如聊天 ID、发送者名称或警报严重性。键必须是标识符：仅字母、数字和下划线。包含连字符或其他字符的键会被静默删除。 |

您的服务器通过在 `Server` 实例上调用 `mcp.notification()` 来推送事件。此示例推送带有两个元键的 CI 失败警报：

```ts theme={null}
await mcp.notification({
  method: 'notifications/claude/channel',
  params: {
    content: 'build failed on main: https://ci.example.com/run/1234',
    meta: { severity: 'high', run_id: '1234' },
  },
})
```

事件在 Claude 的上下文中到达，包装在 `<channel>` 标签中。`source` 属性从您的服务器配置的名称自动设置：

```text theme={null}
<channel source="your-channel" severity="high" run_id="1234">
build failed on main: https://ci.example.com/run/1234
</channel>
```

## 公开回复工具

如果您的频道是双向的，如聊天桥接而不是警报转发器，请公开一个标准 [MCP 工具](https://modelcontextprotocol.io/docs/concepts/tools)，Claude 可以调用它来发送消息回复。关于工具注册的任何内容都不是频道特定的。回复工具有三个组件：

1. 您的 `Server` 构造函数能力中的 `tools: {}` 条目，以便 Claude Code 发现工具
2. 定义工具的架构并实现发送逻辑的工具处理程序
3. 您的 `Server` 构造函数中的 `instructions` 字符串，告诉 Claude 何时以及如何调用工具

要将这些添加到上面的[webhook 接收器](#example-build-a-webhook-receiver)：

<Steps>
  <Step title="启用工具发现">
    在您的 `Server` 构造函数中的 `webhook.ts` 中，将 `tools: {}` 添加到能力中，以便 Claude Code 知道您的服务器提供工具：

    ```ts theme={null}
    capabilities: {
      experimental: { 'claude/channel': {} },
      tools: {},  // 启用工具发现
    },
    ```
  </Step>

  <Step title="注册回复工具">
    将以下内容添加到 `webhook.ts`。`import` 与您的其他导入一起位于文件顶部；两个处理程序位于 `Server` 构造函数和 `mcp.connect()` 之间。这注册了一个 `reply` 工具，Claude 可以使用 `chat_id` 和 `text` 调用它：

    ```ts theme={null}
    // 在 webhook.ts 顶部添加此导入
    import { ListToolsRequestSchema, CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js'

    // Claude 在启动时查询此项以发现您的服务器提供什么工具
    mcp.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [{
        name: 'reply',
        description: 'Send a message back over this channel',
        // inputSchema 告诉 Claude 要传递什么参数
        inputSchema: {
          type: 'object',
          properties: {
            chat_id: { type: 'string', description: 'The conversation to reply in' },
            text: { type: 'string', description: 'The message to send' },
          },
          required: ['chat_id', 'text'],
        },
      }],
    }))

    // Claude 想要调用工具时调用此项
    mcp.setRequestHandler(CallToolRequestSchema, async req => {
      if (req.params.name === 'reply') {
        const { chat_id, text } = req.params.arguments as { chat_id: string; text: string }
        // send() 是您的出站：POST 到您的聊天平台，或用于本地
        // 测试下面完整示例中显示的 SSE 广播。
        send(`Reply to ${chat_id}: ${text}`)
        return { content: [{ type: 'text', text: 'sent' }] }
      }
      throw new Error(`unknown tool: ${req.params.name}`)
    })
    ```
  </Step>

  <Step title="更新说明">
    更新您的 `Server` 构造函数中的 `instructions` 字符串，以便 Claude 知道通过工具将回复路由回去。此示例告诉 Claude 从入站标签传递 `chat_id`：

    ```ts theme={null}
    instructions: 'Messages arrive as <channel source="webhook" chat_id="...">. Reply with the reply tool, passing the chat_id from the tag.'
    ```
  </Step>
</Steps>

这是完整的 `webhook.ts`，具有双向支持。出站回复通过 `GET /events` 使用 [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) (SSE) 流式传输，因此 `curl -N localhost:8788/events` 可以实时观看它们；入站聊天到达 `POST /`：

```ts title="Full webhook.ts with reply tool' expandable theme={null}
#!/usr/bin/env bun
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { ListToolsRequestSchema, CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js'

// --- 出站：写入 /events 上的任何 curl -N 侦听器 ---
// 真实的桥接会改为 POST 到您的聊天平台。
const listeners = new Set<(chunk: string) => void>()
function send(text: string) {
  const chunk = text.split('\n').map(l => `data: ${l}\n`).join('') + '\n'
  for (const emit of listeners) emit(chunk)
}

const mcp = new Server(
  { name: 'webhook', version: '0.0.1' },
  {
    capabilities: {
      experimental: { 'claude/channel': {} },
      tools: {},
    },
    instructions: 'Messages arrive as <channel source="webhook" chat_id="...">. Reply with the reply tool, passing the chat_id from the tag.',
  },
)

mcp.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'reply',
    description: 'Send a message back over this channel',
    inputSchema: {
      type: 'object',
      properties: {
        chat_id: { type: 'string', description: 'The conversation to reply in' },
        text: { type: 'string', description: 'The message to send' },
      },
      required: ['chat_id', 'text'],
    },
  }],
}))

mcp.setRequestHandler(CallToolRequestSchema, async req => {
  if (req.params.name === 'reply') {
    const { chat_id, text } = req.params.arguments as { chat_id: string; text: string }
    send(`Reply to ${chat_id}: ${text}`)
    return { content: [{ type: 'text', text: 'sent' }] }
  }
  throw new Error(`unknown tool: ${req.params.name}`)
})

await mcp.connect(new StdioServerTransport())

let nextId = 1
Bun.serve({
  port: 8788,
  hostname: '127.0.0.1',
  idleTimeout: 0,  // 不要关闭空闲 SSE 流
  async fetch(req) {
    const url = new URL(req.url)

    // GET /events：SSE 流，以便 curl -N 可以实时观看 Claude 的回复
    if (req.method === 'GET' && url.pathname === '/events') {
      const stream = new ReadableStream({
        start(ctrl) {
          ctrl.enqueue(': connected\n\n')  // 所以 curl 立即显示一些内容
          const emit = (chunk: string) => ctrl.enqueue(chunk)
          listeners.add(emit)
          req.signal.addEventListener('abort', () => listeners.delete(emit))
        },
      })
      return new Response(stream, {
        headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' },
      })
    }

    // POST：作为频道事件转发给 Claude
    const body = await req.text()
    const chat_id = String(nextId++)
    await mcp.notification({
      method: 'notifications/claude/channel',
      params: {
        content: body,
        meta: { chat_id, path: url.pathname, method: req.method },
      },
    })
    return new Response('ok')
  },
})
```

[fakechat 服务器](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/fakechat)显示了一个更完整的示例，具有文件附件和消息编辑。

## 门控入站消息

未门控的频道是提示注入向量。任何可以到达您的端点的人都可以在 Claude 前面放置文本。侦听聊天平台或公共端点的频道需要在发出任何内容之前进行真正的发送者检查。

在调用 `mcp.notification()` 之前，根据允许列表检查发送者。此示例删除来自不在集合中的发送者的任何消息：

```ts theme={null}
const allowed = new Set(loadAllowlist())  // 从您的 access.json 或等效项

// 在您的消息处理程序中，在发出之前：
if (!allowed.has(message.from.id)) {  // 发送者，不是房间
  return  // 静默删除
}
await mcp.notification({ ... })
```

根据发送者的身份而不是聊天或房间身份进行门控：示例中的 `message.from.id`，而不是 `message.chat.id`。在群组聊天中，这些不同，根据房间进行门控会让允许列表中的任何人向会话注入消息。

[Telegram](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/telegram) 和 [Discord](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/discord) 频道以相同的方式在发送者允许列表上进行门控。它们通过配对引导列表：用户向机器人发送 DM，机器人回复配对代码，用户在其 Claude Code 会话中批准它，其平台 ID 被添加。有关完整配对流程，请参阅任一实现。[iMessage](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/imessage) 频道采用不同的方法：它在启动时从 Messages 数据库检测用户自己的地址，并自动让它们通过，其他发送者通过句柄添加。

## 中继权限提示

<Note>
  权限中继需要 Claude Code v2.1.81 或更高版本。较早的版本忽略 `claude/channel/permission` 能力。
</Note>

当 Claude 调用需要批准的工具时，本地终端对话打开，会话等待。双向频道可以选择加入以在并行接收相同的提示，并将其中继到您的另一台设备。两者都保持活动：您可以在终端或手机上回答，Claude Code 应用先到达的任何答案并关闭另一个。

中继涵盖工具使用批准，如 Bash、Write 和 Edit。项目信任和 MCP 服务器同意对话不中继；这些仅在本地终端中出现。

### 中继如何工作

当权限提示打开时，中继循环有四个步骤：

1. Claude Code 生成一个短请求 ID 并通知您的服务器
2. 您的服务器将提示和 ID 转发到您的聊天应用
3. 远程用户使用该 ID 回复是或否
4. 您的入站处理程序将回复解析为判决，Claude Code 仅在 ID 匹配开放请求时应用它

本地终端对话在所有这一切中保持打开。如果终端上的某人在远程判决到达之前回答，该答案将被应用，待处理的远程请求将被删除。

<img src="https://mintlify.s3.us-west-1.amazonaws.com/claude-code/zh-CN/images/channel-permission-relay.svg" alt="序列图：Claude Code 向频道服务器发送 permission_request 通知，服务器格式化并将提示发送到聊天应用，人类使用判决回复，服务器将该回复解析为权限通知回到 Claude Code" />

### 权限请求字段

来自 Claude Code 的出站通知是 `notifications/claude/channel/permission_request`。与[频道通知](#notification-format)一样，传输是标准 MCP，但方法和架构是 Claude Code 扩展。`params` 对象有四个字符串字段，您的服务器将其格式化为出站提示：

| 字段              | 描述                                                                                                                                             |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `request_id`    | 从 `a`-`z` 中抽取的五个小写字母，不包括 `l`，因此在手机上输入时永远不会读作 `1` 或 `I`。将其包含在您的出站提示中，以便可以在回复中回显。Claude Code 仅接受携带其发出的 ID 的判决。本地终端对话不显示此 ID，因此您的出站处理程序是了解它的唯一方式。 |
| `tool_name`     | Claude 想要使用的工具的名称，例如 `Bash` 或 `Write`。                                                                                                         |
| `description`   | 此特定工具调用执行的操作的人类可读摘要，与本地终端对话显示的文本相同。对于 Bash 调用，这是 Claude 对命令的描述，或者如果没有给出，则是命令本身。                                                                |
| `input_preview` | 工具的参数作为 JSON 字符串，截断为 200 个字符。对于 Bash，这是命令；对于 Write，这是文件路径和内容的前缀。如果您只有一行消息的空间，请从您的提示中省略它。您的服务器决定显示什么。                                           |

您的服务器发送回的判决是 `notifications/claude/channel/permission`，有两个字段：`request_id` 回显上面的 ID，`behavior` 设置为 `'allow'` 或 `'deny'`。允许让工具调用继续；拒绝拒绝它，与在本地对话中回答"否"相同。两个判决都不影响未来的调用。

### 向聊天桥接添加中继

向双向频道添加权限中继需要三个组件：

1. 您的 `Server` 构造函数中 `experimental` 能力下的 `claude/channel/permission: {}` 条目，以便 Claude Code 知道转发提示
2. `notifications/claude/channel/permission_request` 的通知处理程序，格式化提示并通过您的平台 API 发送它
3. 您的入站消息处理程序中的检查，识别 `yes <id>` 或 `no <id>` 并发出 `notifications/claude/channel/permission` 判决通知，而不是将文本转发给 Claude

仅在您的频道[验证发送者](#gate-inbound-messages)时声明该能力，因为任何可以通过您的频道回复的人都可以批准或拒绝您会话中的工具使用。

要将这些添加到在[公开回复工具](#expose-a-reply-tool)中组装的双向聊天桥接：

<Steps>
  <Step title="声明权限能力">
    在您的 `Server` 构造函数中，在 `experimental` 下的 `claude/channel` 旁边添加 `claude/channel/permission: {}`：

    ```ts theme={null}
    capabilities: {
      experimental: {
        'claude/channel': {},
        'claude/channel/permission': {},  // 选择加入权限中继
      },
      tools: {},
    },
    ```
  </Step>

  <Step title="处理传入请求">
    在您的 `Server` 构造函数和 `mcp.connect()` 之间注册一个通知处理程序。当权限对话打开时，Claude Code 使用[四个请求字段](#permission-request-fields)调用它。您的处理程序为您的平台格式化提示，并包括使用 ID 回复的说明：

    ```ts theme={null}
    import { z } from 'zod'

    // setNotificationHandler 通过 z.literal 在方法字段上路由，
    // 所以这个架构既是验证器又是调度键
    const PermissionRequestSchema = z.object({
      method: z.literal('notifications/claude/channel/permission_request'),
      params: z.object({
        request_id: z.string(),     // 五个小写字母，在您的提示中逐字包含
        tool_name: z.string(),      // 例如 "Bash"、"Write"
        description: z.string(),    // 此调用的人类可读摘要
        input_preview: z.string(),  // 工具参数作为 JSON，截断为 ~200 个字符
      }),
    })

    mcp.setNotificationHandler(PermissionRequestSchema, async ({ params }) => {
      // send() 是您的出站：POST 到您的聊天平台，或用于本地
      // 测试下面完整示例中显示的 SSE 广播。
      send(
        `Claude wants to run ${params.tool_name}: ${params.description}\n\n` +
        // 说明中的 ID 是您的入站处理程序在步骤 3 中解析的内容
        `Reply "yes ${params.request_id}" or "no ${params.request_id}"`,
      )
    })
    ```
  </Step>

  <Step title="在您的入站处理程序中拦截判决">
    您的入站处理程序是接收来自您的平台的消息的循环或回调：与您[根据发送者进行门控](#gate-inbound-messages)和发出 `notifications/claude/channel` 以将聊天转发给 Claude 的地方相同。在聊天转发调用之前添加一个检查，识别判决格式并改为发出权限通知。

    正则表达式匹配 Claude Code 生成的 ID 格式：五个字母，永远不是 `l`。`/i` 标志容忍手机自动更正将回复大写；在将其发送回之前将捕获的 ID 小写。

    ```ts theme={null}
    // 匹配 "y abcde"、"yes abcde"、"n abcde"、"no abcde"
    // [a-km-z] 是 Claude Code 使用的 ID 字母表（小写，跳过 'l'）
    // /i 容忍手机自动更正；在发送前小写捕获
    const PERMISSION_REPLY_RE = /^\s*(y|yes|n|no)\s+([a-km-z]{5})\s*$/i

    async function onInbound(message: PlatformMessage) {
      if (!allowed.has(message.from.id)) return  // 首先根据发送者进行门控

      const m = PERMISSION_REPLY_RE.exec(message.text)
      if (m) {
        // m[1] 是判决词，m[2] 是请求 ID
        // 将判决通知发出回 Claude Code，而不是聊天
        await mcp.notification({
          method: 'notifications/claude/channel/permission',
          params: {
            request_id: m[2].toLowerCase(),  // 在自动更正大写的情况下规范化
            behavior: m[1].toLowerCase().startsWith('y') ? 'allow' : 'deny',
          },
        })
        return  // 作为判决处理，不要也转发为聊天
      }

      // 不匹配判决格式：落入正常聊天路径
      await mcp.notification({
        method: 'notifications/claude/channel',
        params: { content: message.text, meta: { chat_id: String(message.chat.id) } },
      })
    }
    ```
  </Step>
</Steps>

Claude Code 也保持本地终端对话打开，因此您可以在任一地方回答，第一个到达的答案被应用。不完全匹配预期格式的远程回复以两种方式之一失败，在两种情况下对话都保持打开：

* **不同格式**：您的入站处理程序的正则表达式无法匹配，因此 `approve it` 或 `yes` 之类的文本（没有 ID）会作为正常消息落入 Claude。
* **正确格式，错误的 ID**：您的服务器发出判决，但 Claude Code 找不到具有该 ID 的开放请求并静默删除它。

### 完整示例

下面组装的 `webhook.ts` 结合了本页的所有三个扩展：回复工具、发送者门控和权限中继。如果您从这里开始，您还需要初始演练中的[项目设置和 `.mcp.json` 条目](#example-build-a-webhook-receiver)。

为了使两个方向都可以从 curl 测试，HTTP 侦听器提供两个路径：

* **`GET /events`**：保持 SSE 流打开并将每个出站消息作为 `data:` 行推送，因此 `curl -N` 可以实时观看 Claude 的回复和权限提示到达。
* **`POST /`**：入站端，与之前相同的处理程序，现在在聊天转发分支之前插入了判决格式检查。

```ts title="Full webhook.ts with permission relay' expandable theme={null}
#!/usr/bin/env bun
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { ListToolsRequestSchema, CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js'
import { z } from 'zod'

// --- 出站：写入 /events 上的任何 curl -N 侦听器 ---
// 真实的桥接会改为 POST 到您的聊天平台。
const listeners = new Set<(chunk: string) => void>()
function send(text: string) {
  const chunk = text.split('\n').map(l => `data: ${l}\n`).join('') + '\n'
  for (const emit of listeners) emit(chunk)
}

// 发送者允许列表。对于本地演练，我们信任单个 X-Sender
// 标头值 "dev"；真实的桥接会检查平台的用户 ID。
const allowed = new Set(['dev'])

const mcp = new Server(
  { name: 'webhook', version: '0.0.1' },
  {
    capabilities: {
      experimental: {
        'claude/channel': {},
        'claude/channel/permission': {},  // 选择加入权限中继
      },
      tools: {},
    },
    instructions:
      'Messages arrive as <channel source="webhook" chat_id="...">. ' +
      'Reply with the reply tool, passing the chat_id from the tag.',
  },
)

// --- 回复工具：Claude 调用此项以发送消息回复 ---
mcp.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'reply',
    description: 'Send a message back over this channel',
    inputSchema: {
      type: 'object',
      properties: {
        chat_id: { type: 'string', description: 'The conversation to reply in' },
        text: { type: 'string', description: 'The message to send' },
      },
      required: ['chat_id', 'text'],
    },
  }],
}))

mcp.setRequestHandler(CallToolRequestSchema, async req => {
  if (req.params.name === 'reply') {
    const { chat_id, text } = req.params.arguments as { chat_id: string; text: string }
    send(`Reply to ${chat_id}: ${text}`)
    return { content: [{ type: 'text', text: 'sent' }] }
  }
  throw new Error(`unknown tool: ${req.params.name}`)
})

// --- 权限中继：当对话打开时，Claude Code（不是 Claude）调用此项
const PermissionRequestSchema = z.object({
  method: z.literal('notifications/claude/channel/permission_request'),
  params: z.object({
    request_id: z.string(),
    tool_name: z.string(),
    description: z.string(),
    input_preview: z.string(),
  }),
})

mcp.setNotificationHandler(PermissionRequestSchema, async ({ params }) => {
  send(
    `Claude wants to run ${params.tool_name}: ${params.description}\n\n` +
    `Reply "yes ${params.request_id}" or "no ${params.request_id}"`,
  )
})

await mcp.connect(new StdioServerTransport())

// --- HTTP on :8788：GET /events 流出站，POST 路由入站 ---
const PERMISSION_REPLY_RE = /^\s*(y|yes|n|no)\s+([a-km-z]{5})\s*$/i
let nextId = 1

Bun.serve({
  port: 8788,
  hostname: '127.0.0.1',
  idleTimeout: 0,  // 不要关闭空闲 SSE 流
  async fetch(req) {
    const url = new URL(req.url)

    // GET /events：SSE 流，以便 curl -N 可以实时观看回复和提示
    if (req.method === 'GET' && url.pathname === '/events') {
      const stream = new ReadableStream({
        start(ctrl) {
          ctrl.enqueue(': connected\n\n')  // 所以 curl 立即显示一些内容
          const emit = (chunk: string) => ctrl.enqueue(chunk)
          listeners.add(emit)
          req.signal.addEventListener('abort', () => listeners.delete(emit))
        },
      })
      return new Response(stream, {
        headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' },
      })
    }

    // 其他一切都是入站：首先根据发送者进行门控
    const body = await req.text()
    const sender = req.headers.get('X-Sender') ?? ''
    if (!allowed.has(sender)) return new Response('forbidden', { status: 403 })

    // 在将其视为聊天之前检查判决格式
    const m = PERMISSION_REPLY_RE.exec(body)
    if (m) {
      await mcp.notification({
        method: 'notifications/claude/channel/permission',
        params: {
          request_id: m[2].toLowerCase(),
          behavior: m[1].toLowerCase().startsWith('y') ? 'allow' : 'deny',
        },
      })
      return new Response('verdict recorded')
    }

    // 正常聊天：作为频道事件转发给 Claude
    const chat_id = String(nextId++)
    await mcp.notification({
      method: 'notifications/claude/channel',
      params: { content: body, meta: { chat_id, path: url.pathname } },
    })
    return new Response('ok')
  },
})
```

在三个终端中测试判决路径。第一个是您的 Claude Code 会话，使用[开发标志](#test-during-the-research-preview)启动，以便它生成 `webhook.ts`：

```bash theme={null}
claude --dangerously-load-development-channels server:webhook
```

在第二个中，流出站端，以便您可以看到 Claude 的回复和任何权限提示在它们触发时到达：

```bash theme={null}
curl -N localhost:8788/events
```

在第三个中，发送一条消息，使 Claude 尝试运行命令：

```bash theme={null}
curl -d "list the files in this directory" -H "X-Sender: dev" localhost:8788
```

本地权限对话在您的 Claude Code 终端中打开。片刻后，提示出现在 `/events` 流中，包括五字母 ID。从远程端批准它：

```bash theme={null}
curl -d "yes <id>" -H "X-Sender: dev" localhost:8788
```

本地对话关闭，工具运行。Claude 的回复通过 `reply` 工具返回并也在流中着陆。

此文件中的三个频道特定部分：

* **`Server` 构造函数中的能力**：`claude/channel` 注册通知侦听器，`claude/channel/permission` 选择加入权限中继，`tools` 让 Claude 发现回复工具。
* **出站路径**：`reply` 工具处理程序是 Claude 为会话响应调用的；`PermissionRequestSchema` 通知处理程序是当权限对话打开时 Claude Code 调用的。两者都调用 `send()` 通过 `/events` 广播，但它们由系统的不同部分触发。
* **HTTP 处理程序**：`GET /events` 保持 SSE 流打开，以便 curl 可以实时观看出站；`POST` 是入站，根据 `X-Sender` 标头进行门控。`yes <id>` 或 `no <id>` 主体作为判决通知进入 Claude Code，永远不会到达 Claude；其他任何东西都作为频道事件转发给 Claude。

## 打包为插件

要使您的频道可安装和可共享，请将其包装在[插件](/zh-CN/plugins)中并将其发布到[市场](/zh-CN/plugin-marketplaces)。用户使用 `/plugin install` 安装它，然后使用 `--channels plugin:<name>@<marketplace>` 按会话启用它。

发布到您自己的市场的频道仍然需要 `--dangerously-load-development-channels` 来运行，因为它不在[批准的允许列表](/zh-CN/channels#supported-channels)上。要将其添加，[将其提交到官方市场](/zh-CN/plugins#submit-your-plugin-to-the-official-marketplace)。频道插件在被批准之前经过安全审查。在 Team 和 Enterprise 计划上，管理员可以改为将您的插件包含在组织自己的 [`allowedChannelPlugins`](/zh-CN/channels#restrict-which-channel-plugins-can-run) 列表中，该列表替换默认的 Anthropic 允许列表。

## 另请参阅

* [Channels](/zh-CN/channels) 安装和使用 Telegram、Discord、iMessage 或 fakechat 演示，以及为 Team 或 Enterprise 组织启用频道
* [工作频道实现](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins)用于具有配对流、回复工具和文件附件的完整服务器代码
* [MCP](/zh-CN/mcp) 用于频道服务器实现的基础协议
* [Plugins](/zh-CN/plugins) 打包您的频道，以便用户可以使用 `/plugin install` 安装它

> ## Documentation Index
>
> Fetch the complete documentation index at: <https://code.claude.com/docs/llms.txt>
> Use this file to discover all available pages before exploring further.

# 术语表

> Claude Code 术语定义。了解 agentic loop、compaction、CLAUDE.md、hooks、subagents、MCP 和其他核心概念的含义。

本术语表定义了 Claude Code 术语。每个条目都链接到深入讨论该概念的页面。对于模型级概念（如 tokens、temperature 和 RAG），请参阅[平台术语表](https://platform.claude.com/docs/zh-CN/about-claude/glossary)。

## A

### Agent teams

由团队负责人协调的多个独立 Claude Code 会话，具有共享任务列表和点对点消息传递。与在单个会话中运行且仅向父级报告的 [subagents](#subagent) 不同，团队成员各自拥有自己的上下文窗口，您可以直接与任何一个交互。Agent teams 是实验性的，必须通过设置 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 来启用。

了解更多：[运行 agent teams](/zh-CN/agent-teams)

### Agentic coding

一种工作流程，其中 AI 可以自主读取文件、运行命令和进行更改，而您可以观看、重定向或离开，与只能用文本响应的基于聊天的助手相反，您必须自己应用这些响应。Claude Code 是 agentic 的，因为它拥有允许它采取行动而不仅仅是建议的[工具](#tool)。

了解更多：[Claude Code 如何工作](/zh-CN/how-claude-code-works)

### Agentic harness

将语言模型转变为能力强大的编码代理的工具、上下文管理和执行环境。Claude Code 是 harness；Claude 是其中的模型。Harness 提供文件访问、shell 执行、权限控制、内存加载以及链接操作的循环。

了解更多：[Claude Code 如何工作](/zh-CN/how-claude-code-works)

### Agentic loop

Claude 为每个任务所经历的循环：收集上下文、采取行动、验证结果并重复直到完成。每个工具使用都会返回信息，为下一步提供信息。您可以随时中断循环进行重定向。大多数扩展点，包括 [hooks](#hook)、[skills](#skill) 和 [MCP](#mcp-model-context-protocol)，都插入到此循环的特定阶段。

了解更多：[Claude Code 如何工作](/zh-CN/how-claude-code-works#the-agentic-loop)

### Auto memory

Claude 根据您的更正和偏好为自己编写的笔记，按 git 存储库存储在 `~/.claude/projects/` 下。同一存储库的所有 worktrees 共享一个 auto memory 目录。`MEMORY.md` 索引的前 200 行或 25 KB 在每个会话开始时加载。Auto memory 是 Claude 编写的对应物，与您编写的 [CLAUDE.md](#claude-md) 相对。

了解更多：[Auto memory](/zh-CN/memory#auto-memory)

### Auto mode

一种[权限模式](#permission-mode)，其中单独的分类器模型在后台审查每个操作，而不是向您显示批准提示。分类器阻止范围升级、不受信任的基础设施和[提示注入](#prompt-injection)。它永远看不到工具结果，因此注入的指令无法影响其决策。Auto mode 是在 Max、Team、Enterprise 和 API 计划上提供的研究预览。

了解更多：[使用 auto mode 消除提示](/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)

## B

### Bare mode

一个启动标志 `--bare`，跳过 hooks、skills、plugins、MCP servers、auto memory 和 CLAUDE.md 的自动发现。只有您显式传递的标志才会生效。建议用于 CI 和脚本调用，其中您需要在不同机器上的相同行为，无论本地配置如何。

了解更多：[使用 bare mode 更快启动](/zh-CN/headless#start-faster-with-bare-mode)

### Bundled skills

包含在 Claude Code 中的基于提示的 playbooks，例如 `/batch`、`/simplify`、`/debug` 和 `/loop`。与执行固定逻辑的内置命令不同，bundled skills 为 Claude 提供详细的提示并让它编排工作，因此它们可以生成代理、读取文件并适应您的代码库。

了解更多：[Bundled skills](/zh-CN/skills#bundled-skills)

## C

### Channel

一个 [MCP server](#mcp-model-context-protocol)，将事件推送到您正在运行的会话中，以便 Claude 可以对您离开终端时发生的事情做出反应。Channels 可以是双向的：Claude 读取入站事件并通过同一 channel 回复。Telegram、Discord 和 iMessage 包含在研究预览中。

了解更多：[Channels](/zh-CN/channels)

### Checkpoint

在每个您发送的提示处创建的还原点。Claude Code 在每次编辑之前对文件进行快照，以便 checkpoint 可以恢复它们。按两次 `Esc` 或运行 `/rewind` 将代码、对话或两者恢复到较早的点，或从选定的消息总结对话的一部分。Checkpoints 是会话本地的，与 git 分开，不跟踪通过 Bash 工具进行的更改。

了解更多：[Checkpointing](/zh-CN/checkpointing)

### `.claude` directory

Claude Code 读取项目范围配置的目录：settings、hooks、skills、subagents、rules 和 auto memory。项目在其根目录有 `.claude/`；您的用户级默认值在 `~/.claude/`。

了解更多：[The `.claude` directory](/zh-CN/claude-directory)

### CLAUDE.md

一个 markdown 文件，包含您为 Claude 编写的持久指令，在每个会话开始时作为系统提示后的用户消息加载。在此处放置项目约定、架构笔记和"始终执行 X"规则。CLAUDE.md 在 [compaction](#compaction) 期间保留，之后从磁盘重新读取。

您可以在项目范围内的 `./CLAUDE.md` 或 `./.claude/CLAUDE.md`、用户范围内的 `~/.claude/CLAUDE.md` 或作为组织的[托管策略](#managed-settings)放置 CLAUDE.md。更具体的位置优先。

了解更多：[CLAUDE.md files](/zh-CN/memory#claude-md-files)

### Command

一个可重用的指令，您可以通过在提示中键入 `/name` 来调用。内置命令（如 `/clear`、`/model` 和 `/compact`）控制会话。您可以在 `.claude/commands/` 中将自己的命令定义为文件，或从 [plugin](#plugin) 安装它们。[Skills](#skill) 是打包多步骤命令的推荐方式。

了解更多：[Commands](/zh-CN/commands) · [Skills](/zh-CN/skills)

### Compaction

当 [context window](#context-window) 接近其限制时，自动总结您的对话。首先清除较旧的工具输出，然后总结对话。项目根 CLAUDE.md 和 auto memory 在 compaction 期间保留并从磁盘重新加载；仅在对话中给出的指令可能会丢失。运行 `/compact` 手动触发，可选择使用焦点，如 `/compact focus on the API changes`。

了解更多：[What survives compaction](/zh-CN/context-window#what-survives-compaction) · [When context fills up](/zh-CN/how-claude-code-works#when-context-fills-up)

### Context window

会话的工作内存，保存对话历史、文件内容、命令输出、CLAUDE.md、auto memory、加载的 skills 和系统指令。当您工作时，上下文会填满直到 [compaction](#compaction) 总结它。运行 `/context` 查看什么在使用空间。对于底层模型概念，请参阅[平台术语表](https://platform.claude.com/docs/zh-CN/about-claude/glossary#context-window)。

了解更多：[Explore the context window](/zh-CN/context-window)

## D

### Dispatch

一个电话启动的任务路由器，当您从 Claude 移动应用发送编码任务时，在 Desktop 应用中生成 Claude Code 会话。您的提示自动路由到正确的工具。在 Pro 和 Max 计划上可用。

了解更多：[来自 Dispatch 的会话](/zh-CN/desktop#sessions-from-dispatch)

## E

### Effort level

一个设置，控制 Claude 在每个回合上使用多少自适应推理思考预算。更高的努力意味着更多的思考 tokens 和更深入的推理；更低的努力更快且更便宜。Effort 在 Opus 4.7、Opus 4.6 和 Sonnet 4.6 上受支持。

了解更多：[调整 effort level](/zh-CN/model-config#adjust-effort-level)

### Extended thinking

模型在响应前执行的可见逐步推理。您可以使用 `MAX_THINKING_TOKENS` 限制思考 tokens 或调整 [effort level](#effort-level)。思考在终端中以灰色斜体文本显示。

了解更多：[使用 extended thinking](/zh-CN/model-config#extended-thinking)

## H

### Hook

一个用户定义的处理程序，在 Claude Code 生命周期中的特定点自动执行，例如在工具运行之前、文件编辑之后或会话开始时。处理程序可以是 shell 命令、HTTP 端点、MCP 工具、LLM 提示或 subagent。Hooks 是确定性的：它们在固定的生命周期点触发，而不是由模型自行决定。

Hook 配置有三个级别：

* **Hook event**：生命周期点
* **Matcher**：过滤哪些事件触发它
* **Hook handler**：运行什么

了解更多：[开始使用 hooks](/zh-CN/hooks-guide) · [Hooks 参考](/zh-CN/hooks)

## M

### Managed settings

由 IT 或 DevOps 在组织范围内强制执行的设置文件，放置在 `~/.claude` 之外的操作系统级路径。用户无法覆盖或排除托管设置。使用此功能可实现安全策略、合规要求或跨一个群体的标准化工具。

了解更多：[服务器管理的设置](/zh-CN/server-managed-settings)

### MCP (Model Context Protocol)

一个开放标准，用于将 AI 工具连接到外部数据源和服务。MCP servers 为 Claude 提供 Slack、Jira、数据库、浏览器和数百个其他集成的新工具。您可以通过 `/mcp` 连接服务器或将它们添加到 `.mcp.json`。对于协议本身，请参阅[平台术语表](https://platform.claude.com/docs/zh-CN/about-claude/glossary#mcp-model-context-protocol)。

了解更多：[Model Context Protocol](/zh-CN/mcp)

### MCP Tool Search

一个上下文节省机制，延迟 MCP 工具 schemas 直到需要。只有工具名称在启动时加载；Claude 在决定使用特定工具时按需获取完整 schema。这使空闲 MCP servers 不会消耗太多上下文。

了解更多：[使用 MCP Tool Search 扩展](/zh-CN/mcp#scale-with-mcp-tool-search)

## N

### Non-interactive mode

一种执行单个提示并退出而不进行对话会话的模式，使用 `-p` 或 `--print` 调用。用于 CI、脚本和管道。[Agent SDK](/zh-CN/agent-sdk/overview) 是 Python 和 TypeScript 等效项。以前称为 headless mode。

了解更多：[以编程方式运行 Claude Code](/zh-CN/headless)

## O

### Output style

一个配置，修改 Claude 的系统提示以改变响应行为、语气或格式。Output styles 关闭默认系统提示的软件工程特定部分，与 [CLAUDE.md](#claude-md) 不同，后者作为系统提示后的用户消息传递。内置样式包括 Default、Proactive、Explanatory 和 Learning。

了解更多：[Output styles](/zh-CN/output-styles)

## P

### Permission mode

会话的基线批准行为。在 CLI 中使用 `Shift+Tab` 循环或在 VS Code、Desktop 和 claude.ai 中使用模式选择器。可用模式为 `default`、`acceptEdits`、`plan`、`auto`、`dontAsk` 和 `bypassPermissions`。

了解更多：[选择权限模式](/zh-CN/permission-modes)

### Permission rule

一个设置条目，根据工具名称和参数模式允许、询问或拒绝工具调用。规则按 deny→ask→allow 顺序评估，首先匹配获胜。Permission rules 是分层在更广泛的 [permission mode](#permission-mode) 之上的细粒度控制。

了解更多：[配置权限](/zh-CN/permissions)

### Plan mode

一种 [permission mode](#permission-mode)，其中 Claude 研究并提议更改而不编辑您的源文件。它可以读取、搜索和运行探索命令，然后在触及任何内容之前提出批准计划。使用 `/plan` 或按 `Shift+Tab` 进入 plan mode。

了解更多：[使用 plan mode 分析后再编辑](/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)

### Plugin

一个 skills、hooks、subagents 和 MCP servers 的包，打包为单个可安装单元。Plugin skills 命名为 `plugin-name:skill-name`，以便多个 plugins 共存。通过[市场](/zh-CN/plugin-marketplaces)跨团队分发 plugins。

了解更多：[Plugins](/zh-CN/plugins)

### Project trust

一个一次性对话，在 Claude Code 加载其配置之前接受目录。Trust 控制市场 plugins 的自动安装和项目定义的 hooks 的执行。信任目录意味着其 `.claude/settings.json`、`.mcp.json` 和其他配置文件生效。

了解更多：[`.claude` directory](/zh-CN/claude-directory)

### Prompt injection

嵌入在文件、网页或工具结果中的恶意指令，试图将 Claude 重定向到您从未要求的操作。Claude Code 的防御包括权限系统、命令黑名单和信任验证。[Auto mode](#auto-mode) 添加了一个服务器端探针，扫描工具结果中的可疑内容，以及一个永远看不到工具结果的分类器，因此注入的文本无法影响其批准决策。

了解更多：[防止提示注入](/zh-CN/security#protect-against-prompt-injection)

## R

### Remote Control

一种通过 claude.ai 从您的手机或浏览器继续本地 Claude Code 会话的方式。您的代码保留在您的机器上；只有 UI 是远程的。与在 web 上运行的 Claude Code 不同，后者在云沙箱中运行。

了解更多：[Remote Control](/zh-CN/remote-control)

### Rules

`.claude/rules/` 中的模块化指令文件，与 CLAUDE.md 一起加载。规则可以使用 YAML `paths:` frontmatter 进行路径范围限定，因此它仅在 Claude 读取匹配文件时加载，保持上下文精简直到相关。

了解更多：[使用 `.claude/rules/` 组织规则](/zh-CN/memory#organize-rules-with-claude/rules/)

## S

### Sandboxing

Bash 工具的操作系统级文件系统和网络隔离。命令在您预先定义的边界内运行，因此 Claude 可以在其中自由工作，无需每个命令的批准提示。Sandboxing 是与 [permission rules](#permission-rule) 分开的一层。

了解更多：[Sandboxing](/zh-CN/sandboxing)

### Session

与您当前目录相关的对话，具有自己独立的 [context window](#context-window)。会话可以使用 `claude -c` 恢复，使用 `--fork-session` 分叉以在新会话 ID 下保留历史，或在终端中并行运行。运行 `/clear` 启动新会话；前一个会话保持存储并可通过 `/resume` 获得。每个会话的记录存储在 `~/.claude/projects/` 下。

了解更多：[使用会话](/zh-CN/how-claude-code-works#work-with-sessions)

### Settings layers

Claude Code 读取配置的层次结构，按优先级顺序从最高到最低：[托管策略](#managed-settings)、命令行参数、`.claude/settings.local.json` 处的本地设置、`.claude/settings.json` 处的项目设置，然后是 `~/.claude/settings.json` 处的用户设置。数组跨层合并；更高层的标量覆盖较低的。

了解更多：[Settings files](/zh-CN/settings#settings-files)

### Skill

一个 `SKILL.md` 文件，包含 Claude 添加到其工具包中的指令、知识或工作流。Claude 在相关时自动加载 skill，或您可以使用 `/skill-name` 直接调用它。Skills 遵循 Agent Skills 开放标准；Claude Code 使用调用控制和 subagent 执行扩展它。

Skills 是自定义命令的推荐后继。`.claude/commands/deploy.md` 处的文件和 `.claude/skills/deploy/SKILL.md` 处的文件都创建 `/deploy` 并以相同方式工作；现有命令文件继续工作。

了解更多：[使用 skills 扩展 Claude](/zh-CN/skills)

### Subagent

一个专门的 AI 助手，在其自己的上下文窗口中运行，具有自定义系统提示、特定工具访问和独立权限。它处理委派任务并向主对话返回摘要。使用 subagents 将大型探索保留在主上下文之外或运行并行研究。与 [agent teams](#agent-teams) 不同，其中每个代理都是您可以直接交谈的完整独立会话。

内置 subagents 包括 Explore、Plan 和通用目的。

了解更多：[创建自定义 subagents](/zh-CN/sub-agents)

### Surface

您访问 Claude Code 的任何地方：CLI、VS Code、JetBrains、Desktop 或 claude.ai。所有 surfaces 共享相同的引擎，因此您的 CLAUDE.md、settings 和 skills 在所有 surfaces 上以相同方式工作。Slack 和 Chrome 扩展是连接到 surface 的集成，而不是 surfaces 本身。

了解更多：[平台和集成](/zh-CN/platforms)

## T

### Teleport

一个命令 `/teleport`，将云 Claude Code 会话拉入您的本地终端。Claude 获取分支、加载对话历史并从 web 会话的最后状态恢复。反向方向是 `--remote`，它将本地任务发送到 web 上运行。

了解更多：[从 web 到终端](/zh-CN/claude-code-on-the-web#from-web-to-terminal)

### Tool

Claude 可以采取的操作：读取文件、编辑代码、运行 shell 命令、搜索 web、生成 subagent。Tools 是使 Claude Code agentic 的原因。没有它们，Claude 只能用文本响应。每个工具使用都会返回一个结果，为 [agentic loop](#agentic-loop) 中 Claude 的下一个决策提供信息。

了解更多：[Claude 可用的工具](/zh-CN/tools-reference)

### Turn

Claude 在一个 [session](#session) 中的一个完整响应。一个 turn 从您发送消息开始，到 Claude 完成响应结束，中间可能有任意数量的 [tool](#tool) 调用。[Stop hooks](#hook) 在每个 turn 的末尾触发。一个 session 由许多 turn 组成，[agentic loop](#agentic-loop) 描述了在一个 turn 内发生的情况。

了解更多：[Claude Code 如何工作](/zh-CN/how-claude-code-works#the-agentic-loop)

## W

### Worktree isolation

一个隔离模式，在 `.claude/worktrees/` 下的单独 git worktree 中运行 Claude，使用 `-w` 标志或 subagent 配置中的 `isolation: worktree` 启用。更改保留在单独分支的单独目录中，因此并行代理不会覆盖彼此的文件。

了解更多：[使用 git worktrees 运行并行会话](/zh-CN/worktrees)

***

## 已弃用和重命名的术语

这些术语出现在较旧的文档、博客文章和社区内容中。搜索此网站时使用当前名称。

| 旧术语             | 现在称为                                          | 注释                         |
| --------------- | --------------------------------------------- | -------------------------- |
| Headless mode   | [Non-interactive mode](#non-interactive-mode) | 相同的 `-p` 标志，相同的行为          |
| Custom commands | [Skills](#skill)                              | `.claude/commands/` 文件仍然有效 |
| Slash commands  | Commands                                      | "Slash"从产品副本中删除            |
