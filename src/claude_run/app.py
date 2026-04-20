# src/claude_run/app.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, RadioButton, Checkbox, Input, Button
from textual.containers import Container, Horizontal, VerticalScroll
from textual.binding import Binding
from claude_run.config import load_preferences
from claude_run.flags import Flag, FlagGroup, load_flags
from claude_run.search import search_flags
from claude_run.runner import build_argv, execute_claude, SelectedFlag

# Mapping from group name to (zh_label, en_label)
GROUP_LABELS = {
    "model": ("模型", "Model"),
    "permission": ("权限模式", "Permission"),
    "output": ("输出模式", "Output"),
    "session": ("会话", "Session"),
    "tools": ("工具", "Tools"),
    "dev": ("开发模式", "Dev"),
    "debug": ("调试", "Debug"),
    "mcp": ("MCP", "MCP"),
}


class FlagItem(VerticalScroll):
    """Widget displaying a single flag with its options."""

    def __init__(self, flag: Flag, lang: str):
        super().__init__()
        self.flag = flag
        self.lang = lang

    def compose(self) -> ComposeResult:
        label = self.flag.label(self.lang)
        yield Static(f"[b]{self.flag.flag}[/b] — {label}", classes="flag-desc")

        if self.flag.type == "single" and self.flag.choices:
            with Horizontal():
                for c in self.flag.choices:
                    yield RadioButton(
                        c.label_str(self.lang),
                        value=c.value,
                        name=self.flag.flag,
                        id=f"rb-{self.flag.flag}",
                    )
        elif self.flag.type == "multi":
            yield Checkbox(self.flag.flag, value=False, name=self.flag.flag, id=f"cb-{self.flag.flag}")
        elif self.flag.requires_value():
            placeholder = self.flag.required_args[0].placeholder_str(self.lang)
            yield Input(placeholder=placeholder, id=f"input-{self.flag.flag}")

    def get_selected_value(self) -> str | None:
        """Return the selected value for this flag, or None if not selected."""
        if self.flag.type == "single":
            for rb in self.query(RadioButton):
                if rb.value and rb.value != "":
                    return rb.value
            return None
        elif self.flag.type == "multi":
            cb = self.query_one(Checkbox)
            return self.flag.flag if cb.value else None
        elif self.flag.requires_value():
            inp = self.query_one(Input)
            return inp.value if inp.value else None
        return None


class MainApp(App):
    """Main TUI application for claude-run."""

    CSS = """
    #groups { width: 25; border-right: solid green; padding: 1; }
    #detail { width: 75; padding: 1; }
    #search-bar { height: 3; border-top: solid green; }
    .flag-desc { margin-bottom: 1; }
    .section-title { text-style: bold; margin-bottom: 1; }
    .selected-group { background: $primary; }
    """

    BINDINGS = [
        Binding("q", "quit", "退出"),
        Binding("/", "activate_search", "搜索"),
        Binding("ctrl+s", "activate_search", "搜索"),
        Binding("escape", "deactivate_search", "退出搜索"),
        Binding("enter", "execute", "执行"),
    ]

    def __init__(self, prefs):
        super().__init__()
        self.prefs = prefs
        self.lang = prefs.language
        self.flags = load_flags()
        self.groups = FlagGroup.group_by(self.flags)
        self.search_active = False
        self.current_group: str | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with VerticalScroll(id="groups"):
                yield Static("预设组", classes="section-title")
                for group_name in self.groups:
                    label_zh, label_en = GROUP_LABELS.get(group_name, (group_name, group_name))
                    label = label_zh if self.lang == "zh" else label_en
                    yield Button(label, id=f"group-{group_name}", variant="primary")
            with VerticalScroll(id="detail"):
                yield Static("← 请从左侧选择一个分组", id="detail-content")
        with Container(id="search-bar"):
            yield Input(placeholder="输入搜索关键词...", id="search-input")
        yield Footer()

    def on_mount(self) -> None:
        # Hide search bar initially
        search_bar = self.query_one("#search-bar")
        search_bar.display = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id or ""
        if btn_id.startswith("group-"):
            group_name = btn_id[len("group-"):]
            self.current_group = group_name
            self._render_group_detail(group_name)
        elif btn_id == "clear":
            self.current_group = None
            detail = self.query_one("#detail-content", Static)
            detail.update("← 请从左侧选择一个分组")

    def _render_group_detail(self, group_name: str) -> None:
        detail = self.query_one("#detail")
        detail.remove_children()
        group_flags = self.groups.get(group_name, [])
        if not group_flags:
            detail.mount(Static("该分组暂无参数"))
            return
        for flag in group_flags:
            detail.mount(FlagItem(flag, self.lang))

    def action_activate_search(self) -> None:
        self.search_active = True
        search_bar = self.query_one("#search-bar")
        search_bar.display = True
        inp = self.query_one("#search-input", Input)
        inp.focus()

    def action_deactivate_search(self) -> None:
        self.search_active = False
        search_bar = self.query_one("#search-bar")
        search_bar.display = False
        inp = self.query_one("#search-input", Input)
        inp.value = ""
        # Clear detail and show groups
        detail = self.query_one("#detail")
        detail.remove_children()
        detail.mount(Static("← 请从左侧选择一个分组"))

    def on_input_changed(self, event: Input.Changed) -> None:
        if self.search_active:
            query = event.value
            if query:
                results = search_flags(self.flags, query, self.lang)
                self._render_search_results(results)
            else:
                detail = self.query_one("#detail")
                detail.remove_children()
                detail.mount(Static("← 请从左侧选择一个分组"))

    def _render_search_results(self, results: list[Flag]) -> None:
        detail = self.query_one("#detail")
        detail.remove_children()
        if not results:
            detail.mount(Static("未找到匹配的参数"))
            return
        for flag in results:
            detail.mount(FlagItem(flag, self.lang))

    def action_execute(self) -> None:
        selected_args = []
        for fi in self.query(FlagItem):
            val = fi.get_selected_value()
            if val:
                if fi.flag.type == "multi":
                    selected_args.append(SelectedFlag(val))
                else:
                    selected_args.append(SelectedFlag(fi.flag.flag, val))

        argv = build_argv(selected_args)
        self.exit()
        execute_claude(argv)