"""crun 主交互逻辑。

主界面用 prompt_toolkit 构建（直接全量展示所有参数，/ 触发实时搜索）。
子选项追问和确认步骤用 questionary。
"""
import os
from datetime import datetime, timezone

import questionary
from questionary import Style as QStyle
from prompt_toolkit import Application
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style as PTStyle

from claude_run.flags import Flag, load_flags, FlagsLoadError
from claude_run.search import search_flags
from claude_run.runner import build_argv, validate_argv, SelectedFlag
from claude_run.config import load_last_config, save_last_config, ConfigError


# ── 样式 ─────────────────────────────────────────────────────────────────────

_Q_STYLE = QStyle([
    ("qmark",       "fg:#5f87ff bold"),
    ("question",    "bold"),
    ("answer",      "fg:#5fffaf bold"),
    ("pointer",     "fg:#5f87ff bold"),
    ("highlighted", "fg:#5f87ff bold"),
    ("selected",    "fg:#5fffaf"),
    ("separator",   "fg:#6c6c6c"),
    ("instruction", "fg:#6c6c6c"),
    ("disabled",    "fg:#6c6c6c italic"),
])

_PT_STYLE = PTStyle.from_dict({
    "hint":          "fg:ansibrightblack",
    "search-bar":    "fg:ansiyellow bold",
    "sep":           "fg:ansibrightblack",
    "scroll":        "fg:ansibrightblack",
    "item-cur":      "fg:ansiblue bold reverse",
    "item-cur-chk":  "fg:ansigreen bold reverse",
    "item-chk":      "fg:ansigreen",
    "item":          "",
    "item-val":      "fg:ansicyan",
    "status":        "fg:ansibrightblack italic",
    "group-label":   "fg:ansibrightblack italic",
})

# ── 分组标签 ──────────────────────────────────────────────────────────────────

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


def _glabel(name: str, lang: str) -> str:
    zh, en = _GROUP_LABELS.get(name, (name, name))
    return zh if lang == "zh" else en


# ── 子选项追问（questionary） ──────────────────────────────────────────────────

def _prompt_flag_value(f: Flag, lang: str, existing: dict[str, str]) -> str | None:
    """为 single/value 参数弹出子选项或文本输入，返回 None 表示取消。"""
    if f.type == "single" and f.choices:
        choices = [
            questionary.Choice(c.label_str(lang), value=c.value)
            for c in f.choices
        ]
        default_val = existing.get(f.flag)
        matched = next((c for c in choices if c.value == default_val), None)
        return questionary.select(
            f"  {f.flag} — {f.label(lang)}:",
            choices=choices,
            default=matched,
            style=_Q_STYLE,
        ).ask()

    if f.type == "value":
        arg = f.required_args[0] if f.required_args else None
        label = arg.label_str(lang) if arg else f.flag
        placeholder = arg.placeholder_str(lang) if arg else ""
        hint = f" [{placeholder}]" if placeholder else ""
        return questionary.text(
            f"  {label}{hint}:",
            default=existing.get(f.flag, ""),
            style=_Q_STYLE,
        ).ask()

    return None


# ── prompt_toolkit 主选择界面 ─────────────────────────────────────────────────

def _run_selector(
    flags: list[Flag],
    lang: str,
    init_checked: set[str],
    value_state: dict[str, str],
) -> set[str] | None:
    """
    全量标志选择器。
    - 直接展示所有参数（按分组排列）
    - 输入 / 进入实时搜索模式，Esc 退出搜索
    - 空格切换选中，回车确认，Esc（非搜索时）退出
    返回选中的 flag 名集合，或 None 表示取消。
    """
    try:
        term_h = os.get_terminal_size().lines - 6
        viewport_h = max(8, min(term_h, 20))
    except OSError:
        viewport_h = 15

    checked: set[str] = set(init_checked)

    ctx = {
        "cursor":    0,
        "viewport":  0,
        "in_search": False,
        "search":    "",
        "filtered":  list(flags),
    }

    def _get_filtered() -> list[Flag]:
        q = ctx["search"]
        return search_flags(flags, q, lang) if q else list(flags)

    def _clamp() -> None:
        n = len(ctx["filtered"])
        if n == 0:
            ctx["cursor"] = 0
            ctx["viewport"] = 0
            return
        ctx["cursor"] = max(0, min(ctx["cursor"], n - 1))
        c, v = ctx["cursor"], ctx["viewport"]
        if c < v:
            ctx["viewport"] = c
        elif c >= v + viewport_h:
            ctx["viewport"] = c - viewport_h + 1

    # ── 渲染函数 ──────────────────────────────────────────────────────────────
    def _render():
        lines: list[tuple[str, str]] = []

        # 标题 / 搜索栏
        if ctx["in_search"]:
            q = ctx["search"]
            n = len(ctx["filtered"])
            bar = (f"搜索: {q}▌  ({n} 项)  Esc 退出搜索"
                   if lang == "zh" else
                   f"Search: {q}▌  ({n} results)  Esc to exit")
            lines.append(("class:search-bar", bar + "\n"))
        else:
            hint = ("/ 搜索  空格 选中  回车 确认  Esc 退出"
                    if lang == "zh" else
                    "/ search  Space toggle  Enter confirm  Esc quit")
            lines.append(("class:hint", hint + "\n"))

        lines.append(("class:sep", "─" * 60 + "\n"))

        filtered = ctx["filtered"]
        vstart = ctx["viewport"]
        vend = vstart + viewport_h

        if vstart > 0:
            lines.append(("class:scroll", "  ↑\n"))

        prev_group = None
        for i, f in enumerate(filtered[vstart:vend]):
            abs_i = vstart + i
            is_cur = abs_i == ctx["cursor"]
            is_chk = f.flag in checked

            # 分组小标题（仅非搜索模式）
            if not ctx["in_search"] and f.group != prev_group:
                g = f"── {_glabel(f.group, lang)} "
                lines.append(("class:group-label", g + "\n"))
                prev_group = f.group

            mark = "●" if is_chk else "○"
            val = value_state.get(f.flag, "")

            if f.type == "single" and f.choices:
                suffix = f"  ={val}" if val else ("  [单选]" if lang == "zh" else "  [choice]")
            elif f.type == "value":
                suffix = f"  ={val}" if val else ("  [输入]" if lang == "zh" else "  [input]")
            else:
                suffix = ""

            line = f" {mark} {f.flag}  {f.label(lang)}{suffix}\n"

            if is_cur:
                style = "class:item-cur-chk" if is_chk else "class:item-cur"
            elif is_chk:
                style = "class:item-chk"
            else:
                style = "class:item"

            lines.append((style, line))

        if vend < len(filtered):
            lines.append(("class:scroll", "  ↓\n"))

        n_chk = len(checked)
        status = (f"  已选 {n_chk} 项" if lang == "zh" else f"  {n_chk} selected")
        lines.append(("class:status", "\n" + status))

        return lines

    # ── 按键绑定 ──────────────────────────────────────────────────────────────
    kb = KeyBindings()
    in_search_filter = Condition(lambda: ctx["in_search"])

    @kb.add("up", eager=True)
    @kb.add("k", eager=True, filter=~in_search_filter)
    def _up(event):
        ctx["cursor"] = max(0, ctx["cursor"] - 1)
        _clamp()
        event.app.invalidate()

    @kb.add("down", eager=True)
    @kb.add("j", eager=True, filter=~in_search_filter)
    def _down(event):
        ctx["cursor"] = min(len(ctx["filtered"]) - 1, ctx["cursor"] + 1)
        _clamp()
        event.app.invalidate()

    @kb.add("pageup", eager=True)
    def _pgup(event):
        ctx["cursor"] = max(0, ctx["cursor"] - viewport_h)
        _clamp()
        event.app.invalidate()

    @kb.add("pagedown", eager=True)
    def _pgdn(event):
        ctx["cursor"] = min(len(ctx["filtered"]) - 1, ctx["cursor"] + viewport_h)
        _clamp()
        event.app.invalidate()

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

    @kb.add("/", eager=True, filter=~in_search_filter)
    def _enter_search(event):
        ctx["in_search"] = True
        ctx["search"] = ""
        ctx["filtered"] = list(flags)
        ctx["cursor"] = 0
        ctx["viewport"] = 0
        event.app.invalidate()

    @kb.add("escape", eager=True)
    def _escape(event):
        if ctx["in_search"]:
            ctx["in_search"] = False
            ctx["search"] = ""
            ctx["filtered"] = list(flags)
            ctx["cursor"] = 0
            ctx["viewport"] = 0
            event.app.invalidate()
        else:
            event.app.exit(result=None)

    @kb.add("backspace", eager=True)
    def _backspace(event):
        if ctx["in_search"] and ctx["search"]:
            ctx["search"] = ctx["search"][:-1]
            ctx["filtered"] = _get_filtered()
            ctx["cursor"] = 0
            ctx["viewport"] = 0
            event.app.invalidate()

    @kb.add("enter", eager=True)
    def _enter(event):
        event.app.exit(result=checked)

    @kb.add("c-c", eager=True)
    def _ctrl_c(event):
        event.app.exit(result=None)

    @kb.add("<any>")
    def _any(event):
        if not ctx["in_search"]:
            return
        key = event.key_sequence[0].key
        if isinstance(key, str) and key.isprintable():
            ctx["search"] += key
            ctx["filtered"] = _get_filtered()
            ctx["cursor"] = 0
            ctx["viewport"] = 0
            event.app.invalidate()

    app = Application(
        layout=Layout(Window(FormattedTextControl(_render, focusable=True))),
        key_bindings=kb,
        style=_PT_STYLE,
        full_screen=False,
        mouse_support=False,
    )

    return app.run()


# ── 构建 SelectedFlag 列表 ───────────────────────────────────────────────────


def _build_selected(
    flag_objs: list[Flag],
    value_state: dict[str, str],
) -> list[SelectedFlag]:
    res: list[SelectedFlag] = []
    for f in flag_objs:
        if f.type == "multi":
            res.append(SelectedFlag(f.flag))
        elif f.type in ("single", "value"):
            v = value_state.get(f.flag, "")
            if v:
                res.append(SelectedFlag(f.flag, v))
    return res


def _build_last_config_snapshot(
    selected: list[SelectedFlag],
    flags_by_name: dict[str, Flag],
) -> dict:
    payload: list[dict] = []
    for sel in selected:
        f = flags_by_name.get(sel.flag)
        if f is None:
            continue
        if f.type == "multi":
            payload.append({"flag": f.flag, "type": "multi", "value": True})
        elif f.type in ("single", "value") and sel.value:
            payload.append({"flag": f.flag, "type": f.type, "value": sel.value})

    return {
        "version": 1,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "selected": payload,
    }


def _sanitize_last_config(last_cfg: dict | None, flags: list[Flag]) -> tuple[list[SelectedFlag], int]:
    """将历史配置清洗为当前可用的 SelectedFlag 列表，返回 (结果, 丢弃数量)。"""
    if not isinstance(last_cfg, dict):
        return [], 0
    items = last_cfg.get("selected")
    if not isinstance(items, list):
        return [], 0

    by_name = {f.flag: f for f in flags}
    result: list[SelectedFlag] = []
    dropped = 0

    for item in items:
        if not isinstance(item, dict):
            dropped += 1
            continue
        flag_name = item.get("flag")
        item_type = item.get("type")
        item_value = item.get("value")

        if not isinstance(flag_name, str) or not isinstance(item_type, str):
            dropped += 1
            continue

        f = by_name.get(flag_name)
        if f is None or f.type != item_type:
            dropped += 1
            continue

        if f.type == "multi":
            if item_value is True:
                result.append(SelectedFlag(flag_name))
            else:
                dropped += 1
        elif f.type == "single":
            if not isinstance(item_value, str) or not item_value:
                dropped += 1
                continue
            allowed = {c.value for c in (f.choices or [])}
            if item_value not in allowed:
                dropped += 1
                continue
            result.append(SelectedFlag(flag_name, item_value))
        elif f.type == "value":
            if not isinstance(item_value, str) or not item_value:
                dropped += 1
                continue
            result.append(SelectedFlag(flag_name, item_value))

    return result, dropped


# ── 主入口 ────────────────────────────────────────────────────────────────────

def run_app(prefs) -> list[str] | None:
    """主交互入口。返回 argv 列表，或 None 表示用户取消。"""
    try:
        flags = load_flags()
    except FlagsLoadError as e:
        print(f"❌ 无法加载参数定义：{e}")
        return None

    flags_by_name = {f.flag: f for f in flags}
    lang = prefs.language
    checked: set[str] = set()
    value_state: dict[str, str] = {}

    if lang == "zh":
        print("crun · 选择 Claude CLI 启动参数\n")
    else:
        print("crun · Select Claude CLI startup flags\n")

    while True:
        prev_checked = set(checked)

        result = _run_selector(flags, lang, checked, value_state)

        if result is None:
            return None

        checked = result

        for name in prev_checked - checked:
            value_state.pop(name, None)

        # 清理互斥 flag 的 value_state
        for f in flags:
            if f.flag in checked and f.conflicts_with:
                for c in f.conflicts_with:
                    if c not in checked:
                        value_state.pop(c, None)

        newly_added = [
            f for f in flags
            if f.flag in (checked - prev_checked) and f.type in ("single", "value")
        ]
        if newly_added:
            if lang == "zh":
                print("\n  ↳ 以下参数需要指定值：")
            else:
                print("\n  ↳ The following flags need a value:")
            for f in newly_added:
                val = _prompt_flag_value(f, lang, value_state)
                if val is None:
                    checked.discard(f.flag)
                    continue
                value_state[f.flag] = val

        selected_objs = [f for f in flags if f.flag in checked]
        print()
        if not selected_objs:
            print("（尚未选择任何参数）" if lang == "zh" else "(No flags selected)")
        else:
            print("当前已选：" if lang == "zh" else "Currently selected:")
            for f in selected_objs:
                val = value_state.get(f.flag)
                suffix = f"  = {val}" if val else ""
                print(f"  {f.flag}{suffix}")
        print()

        action = questionary.select(
            "下一步：" if lang == "zh" else "Next:",
            choices=[
                questionary.Choice("▶ 执行" if lang == "zh" else "▶ Run", value="run"),
                questionary.Choice("＋ 继续选择" if lang == "zh" else "＋ More", value="more"),
                questionary.Choice("✎ 修改已选值" if lang == "zh" else "✎ Edit", value="edit"),
                questionary.Choice("✗ 清空重选" if lang == "zh" else "✗ Reset", value="reset"),
                questionary.Choice("✗ 取消退出" if lang == "zh" else "✗ Quit", value="quit"),
            ],
            style=_Q_STYLE,
        ).ask()

        if action is None or action == "quit":
            return None

        if action == "reset":
            checked.clear()
            value_state.clear()
            continue

        if action == "more":
            continue

        if action == "edit":
            editable = [f for f in selected_objs if f.type in ("single", "value")]
            if not editable:
                print("没有可编辑的参数。\n" if lang == "zh" else "Nothing to edit.\n")
                continue
            for f in editable:
                val = _prompt_flag_value(f, lang, value_state)
                if val is not None:
                    value_state[f.flag] = val
            continue

        selected: list[SelectedFlag]
        argv: list[str]

        if not selected_objs:
            last_cfg = load_last_config()
            restored, dropped = _sanitize_last_config(last_cfg, flags)
            if not restored:
                print("未找到可用的上次配置。\n" if lang == "zh" else "No usable last configuration found.\n")
                continue

            argv = build_argv(restored)
            if dropped > 0:
                print(
                    f"检测到 {dropped} 个历史参数已失效，已自动忽略。"
                    if lang == "zh"
                    else f"{dropped} stale history items were ignored."
                )
            print(f"\n上次配置：{' '.join(argv)}\n" if lang == "zh" else f"\nLast config: {' '.join(argv)}\n")

            reuse = questionary.select(
                "当前未选择参数，是否使用上次配置？" if lang == "zh" else "No flags selected. Use last config?",
                choices=[
                    questionary.Choice("使用上次配置" if lang == "zh" else "Use last config", value="use"),
                    questionary.Choice("重新选择" if lang == "zh" else "Reselect", value="reselect"),
                    questionary.Choice("取消退出" if lang == "zh" else "Cancel", value="cancel"),
                ],
                style=_Q_STYLE,
            ).ask()

            if reuse == "reselect":
                continue
            if reuse != "use":
                return None
            selected = restored
        else:
            selected = _build_selected(selected_objs, value_state)
            argv = build_argv(selected)

        valid, err_msg = validate_argv(argv)
        if not valid:
            print(f"❌ {err_msg}\n")
            continue

        cmd_preview = " ".join(argv)
        print(f"\n将执行：{cmd_preview}\n" if lang == "zh" else f"\nWill run: {cmd_preview}\n")

        confirm = questionary.confirm(
            "确认执行？" if lang == "zh" else "Confirm?",
            default=True,
            style=_Q_STYLE,
        ).ask()

        if confirm:
            try:
                save_last_config(_build_last_config_snapshot(selected, flags_by_name))
            except ConfigError as e:
                print(f"⚠ 保存上次配置失败: {e}" if lang == "zh" else f"⚠ Failed to save last config: {e}")
            return argv
