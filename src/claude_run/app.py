"""claude-run 主 TUI 应用。

分层：
  Header           ← 标题栏
  UnifiedSearch    ← 可选：顶部常驻搜索框 (B/both)
  Main             ← 内容区：左侧分组 + 右侧参数表单
  FuzzySearch      ← 可选：底部临时搜索框 (A/both)
  StatusBar        ← 状态栏：已选数量 + 命令预览
  Footer           ← 底部提示：显示已绑定快捷键
"""
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import (
    Header, Footer, Static, Input, Checkbox, Button,
    ListView, ListItem, RadioSet,
)

from claude_run.flags import Flag, FlagGroup, load_flags, FlagsLoadError
from claude_run.search import search_flags
from claude_run.runner import build_argv, validate_argv, SelectedFlag
from claude_run.widgets import FlagRow
from claude_run.help import HelpScreen


GROUP_LABELS: dict[str, tuple[str, str]] = {
    "model":      ("模型", "Model"),
    "permission": ("权限", "Permission"),
    "output":     ("输出", "Output"),
    "session":    ("会话", "Session"),
    "tools":      ("工具", "Tools"),
    "dev":        ("开发", "Dev"),
    "debug":      ("调试", "Debug"),
    "mcp":        ("MCP",  "MCP"),
}


class MainApp(App):
    """用两种主色（$accent / $success）+ 中性色，布局用 fr/% 自适应。"""

    CSS = """
    Screen { background: $surface; }

    /* 顶部统一搜索（B/both 模式） */
    #unified-bar {
        height: 3;
        display: none;
        border-bottom: solid $accent;
    }

    /* 内容区 */
    #main { height: 1fr; }
    #sidebar {
        width: 20%;
        min-width: 14;
        max-width: 28;
        border-right: solid $accent;
        padding: 0 1;
    }
    #content { padding: 0 1; }
    #group-list > ListItem.--highlight {
        background: $accent 30%;
        color: $text;
    }

    /* 底部模糊搜索（A/both 模式临时） */
    #search-bar {
        height: 3;
        display: none;
        border-top: solid $accent;
    }

    /* 状态栏 */
    #statusbar {
        height: 1;
        padding: 0 1;
        background: $panel;
        color: $text-muted;
    }

    /* 通用 */
    .title { text-style: bold; color: $accent; }
    .empty { color: $text-muted; padding: 1 2; }
    """

    TITLE = "claude-run"
    SUB_TITLE = "选择 Claude CLI 参数并执行"

    # 快捷键遵循规则 4：hjkl/方向、Enter、q/Esc、?。
    BINDINGS = [
        Binding("q,ctrl+c", "quit", "退出", priority=True),
        Binding("question_mark", "help", "帮助"),
        Binding("/,ctrl+s", "activate_search", "搜索"),
        Binding("ctrl+u", "toggle_unified", "统一搜索", priority=True),
        Binding("escape", "deactivate_search", "关闭搜索"),
        Binding("f5,ctrl+r", "execute", "执行", priority=True),
        Binding("j,down", "nav_down", show=False),
        Binding("k,up", "nav_up", show=False),
        Binding("h,left", "nav_left", show=False),
        Binding("l,right", "nav_right", show=False),
    ]

    def __init__(self, prefs):
        super().__init__()
        self.prefs = prefs
        self.lang = prefs.language
        try:
            self.flags = load_flags()
        except Exception as e:  # 规则 7：错误状态
            self.flags = []
            self._load_error = str(e)
        else:
            self._load_error = None
        self.groups = FlagGroup.group_by(self.flags)
        self.group_names = list(self.groups.keys())
        self.current_group_index = 0
        self._state: dict[str, object] = {}
        self.search_active = False
        self.unified_active = False

    # ——— 布局 ———————————————————————————————————
    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)

        with Container(id="unified-bar"):
            yield Input(placeholder="统一搜索 · 实时过滤所有参数", id="unified-input")

        with Horizontal(id="main"):
            with VerticalScroll(id="sidebar"):
                yield Static("分组", classes="title")
                yield ListView(id="group-list")
            with VerticalScroll(id="content"):
                yield Static("", id="content-title", classes="title")
                yield Container(id="flag-list")

        with Container(id="search-bar"):
            yield Input(placeholder="模糊搜索 · Esc 关闭", id="search-input")

        yield Static("", id="statusbar")
        yield Footer()

    def on_mount(self) -> None:
        if self._load_error:
            self.query_one("#content-title", Static).update("⚠ 加载失败")
            self.query_one("#flag-list", Container).mount(
                Static(f"无法加载参数定义：{self._load_error}", classes="empty")
            )
            self._update_status()
            return

        lv = self.query_one("#group-list", ListView)
        for name in self.group_names:
            lv.append(ListItem(Static(self._group_label(name))))
        if self.group_names:
            lv.index = 0
            self._show_group(self.group_names[0])

        if self.prefs.search_mode in ("B", "both"):
            self._set_unified_visible(True)
        else:
            lv.focus()
        self._update_status()

    # ——— 渲染 ———————————————————————————————————
    def _group_label(self, name: str) -> str:
        zh, en = GROUP_LABELS.get(name, (name, name))
        return zh if self.lang == "zh" else en

    def _show_group(self, group_name: str) -> None:
        self.query_one("#content-title", Static).update(
            f"◆ {self._group_label(group_name)}"
        )
        self._render_flags(self.groups.get(group_name, []))

    def _render_flags(self, flags_list: list[Flag]) -> None:
        container = self.query_one("#flag-list", Container)
        container.remove_children()
        if not flags_list:
            container.mount(Static("（空·无匹配参数）", classes="empty"))
            return
        for f in flags_list:
            container.mount(FlagRow(f, self.lang, self._state))

    def _update_status(self) -> None:
        argv = build_argv(self._collect_selected())
        count = len(argv) - 1  # 扣掉 "claude"
        bar = self.query_one("#statusbar", Static)
        if count == 0:
            bar.update("已选 0 项 · 按 ? 查看帮助")
        else:
            bar.update(f"已选 {count} 项 · $ {' '.join(argv)}")

    # ——— 事件 ———————————————————————————————————
    @on(ListView.Highlighted, "#group-list")
    def on_group_highlighted(self, event: ListView.Highlighted) -> None:
        idx = event.list_view.index
        if idx is None:
            return
        self.current_group_index = idx
        if not self._search_query_active():
            self._show_group(self.group_names[idx])

    @on(ListView.Selected, "#group-list")
    def on_group_selected(self, _: ListView.Selected) -> None:
        # Enter 在分组列表上 = 执行，符合规则 4。
        self.action_execute()

    @on(Checkbox.Changed)
    def on_cb_changed(self, event: Checkbox.Changed) -> None:
        row = self._find_row(event.control)
        if row is None:
            return
        self._state[row.flag.flag] = event.value
        row.refresh_border()
        self._update_status()

    @on(RadioSet.Changed)
    def on_rs_changed(self, event: RadioSet.Changed) -> None:
        row = self._find_row(event.control)
        if row is None:
            return
        val = event.pressed.name if event.pressed is not None else None
        self._state[row.flag.flag] = val
        row.refresh_border()
        self._update_status()

    @on(Input.Changed, "#search-input")
    def on_fuzzy_changed(self, event: Input.Changed) -> None:
        if self.search_active:
            self._apply_search(event.value)

    @on(Input.Changed, "#unified-input")
    def on_unified_changed(self, event: Input.Changed) -> None:
        if self.unified_active:
            self._apply_search(event.value)

    @on(Input.Changed)
    def on_value_input_changed(self, event: Input.Changed) -> None:
        if event.input.id in ("search-input", "unified-input"):
            return
        row = self._find_row(event.input)
        if row is None or row.flag.type != "value":
            return
        self._state[row.flag.flag] = event.value
        row.refresh_border()
        self._update_status()

    # ——— Actions ————————————————————————————————
    def action_help(self) -> None:
        self.push_screen(HelpScreen())

    def action_nav_down(self) -> None:
        if self._in_text_input():
            return
        lv = self.query_one("#group-list", ListView)
        if not lv.has_focus:
            lv.focus()
        lv.action_cursor_down()

    def action_nav_up(self) -> None:
        if self._in_text_input():
            return
        lv = self.query_one("#group-list", ListView)
        if not lv.has_focus:
            lv.focus()
        lv.action_cursor_up()

    def action_nav_left(self) -> None:
        if self._in_text_input():
            return
        self.query_one("#group-list", ListView).focus()

    def action_nav_right(self) -> None:
        if self._in_text_input():
            return
        # 把焦点送入右侧第一个可交互控件
        for row in self.query(FlagRow):
            for cls in (RadioSet, Checkbox, Input):
                widgets = row.query(cls)
                if widgets:
                    widgets.first().focus()
                    return

    def action_activate_search(self) -> None:
        bar = self.query_one("#search-bar", Container)
        bar.styles.display = "block"
        self.search_active = True
        inp = self.query_one("#search-input", Input)
        inp.focus()
        self._apply_search(inp.value)

    def action_deactivate_search(self) -> None:
        if self.search_active:
            self.search_active = False
            self.query_one("#search-bar", Container).styles.display = "none"
            self.query_one("#search-input", Input).value = ""
            if not (self.unified_active and
                    self.query_one("#unified-input", Input).value.strip()):
                self._show_group(self.group_names[self.current_group_index])
            self.query_one("#group-list", ListView).focus()

    def action_toggle_unified(self) -> None:
        self._set_unified_visible(not self.unified_active)

    def action_execute(self) -> None:
        """执行：构建 argv，验证，然后退出。"""
        argv = build_argv(self._collect_selected())
        # 验证命令是否可执行
        valid, err_msg = validate_argv(argv)
        if not valid:
            # 在状态栏显示错误
            bar = self.query_one("#statusbar", Static)
            bar.update(f"❌ {err_msg}")
            return
        self.exit(argv)

    # ——— 内部辅助 ——————————————————————————————
    def _in_text_input(self) -> bool:
        return isinstance(self.focused, Input)

    def _search_query_active(self) -> bool:
        return (self.search_active or
                (self.unified_active and
                 bool(self.query_one("#unified-input", Input).value.strip())))

    def _set_unified_visible(self, visible: bool) -> None:
        self.unified_active = visible
        wrap = self.query_one("#unified-bar", Container)
        wrap.styles.display = "block" if visible else "none"
        if visible:
            self.query_one("#unified-input", Input).focus()
        else:
            self.query_one("#unified-input", Input).value = ""
            if not self.search_active:
                self._show_group(self.group_names[self.current_group_index])

    def _apply_search(self, query: str) -> None:
        if not query.strip():
            self._show_group(self.group_names[self.current_group_index])
            return
        results = search_flags(self.flags, query, self.lang)
        self.query_one("#content-title", Static).update(
            f"◆ 搜索：“{query}”  ({len(results)} 项)"
        )
        self._render_flags(results)

    def _find_row(self, widget) -> FlagRow | None:
        node = widget
        while node is not None:
            if isinstance(node, FlagRow):
                return node
            node = node.parent
        return None

    def _collect_selected(self) -> list[SelectedFlag]:
        res: list[SelectedFlag] = []
        by_name = {f.flag: f for f in self.flags}
        for flag_name, val in self._state.items():
            f = by_name.get(flag_name)
            if f is None:
                continue
            if f.type == "multi" and val is True:
                res.append(SelectedFlag(flag_name))
            elif f.type == "single" and isinstance(val, str) and val:
                res.append(SelectedFlag(flag_name, val))
            elif f.type == "value" and isinstance(val, str) and val:
                res.append(SelectedFlag(flag_name, val))
        return res
