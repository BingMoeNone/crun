# src/claude_run/app.py
import os
from textual.app import App, ComposeResult
from textual.widgets import (
    Header, Footer, Static, RadioButton, Checkbox,
    Input, ListView, ListItem
)
from textual.containers import VerticalScroll, Horizontal
from textual.binding import Binding
from textual import on
from claude_run.config import load_preferences
from claude_run.flags import Flag, FlagGroup, load_flags
from claude_run.search import search_flags
from claude_run.runner import build_argv, SelectedFlag

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


class MainApp(App):

    BINDINGS = [
        Binding("q", "quit", "退出"),
        Binding("/", "activate_search", "搜索"),
        Binding("escape", "deactivate_search", "取消"),
        Binding("enter", "execute", "执行"),
        Binding("up", "prev_group", "上一个"),
        Binding("down", "next_group", "下一个"),
    ]

    def __init__(self, prefs):
        super().__init__()
        self.prefs = prefs
        self.lang = prefs.language
        self.flags = load_flags()
        self.groups = FlagGroup.group_by(self.flags)
        self.group_names = list(self.groups.keys())
        self.current_group_index = 0
        self.search_active = False
        self._selected: dict[str, str | None] = {}  # flag -> value
        self._checkbox_state: dict[str, bool] = {}   # flag -> checked

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main"):
            with VerticalScroll(id="left"):
                yield Static("分组列表", id="group-header")
                yield ListView(id="group-list")
            with VerticalScroll(id="right"):
                yield Static("", id="detail-header")
                yield Static("", id="detail-content")
        yield Input(placeholder="输入搜索关键词...", id="search-input")
        yield Footer()

    def on_mount(self) -> None:
        # 隐藏搜索框
        self.query_one("#search-input", Input).display = False

        # 填充分组列表
        lv = self.query_one("#group-list", ListView)
        for name in self.group_names:
            zh, en = GROUP_LABELS.get(name, (name, name))
            label = zh if self.lang == "zh" else en
            lv.append(ListItem(Static(label), id=f"gl-{name}"))

        # 默认选中第一个分组
        lv.index = 0
        self._show_group(self.group_names[0])

    def _show_group(self, group_name: str) -> None:
        zh, en = GROUP_LABELS.get(group_name, (group_name, group_name))
        header = self.query_one("#detail-header", Static)
        header.update(f"== {zh if self.lang == 'zh' else en} ==")

        content = self.query_one("#detail-content", Static)
        group_flags = self.groups.get(group_name, [])

        lines = []
        for i, flag in enumerate(group_flags):
            flag_label = flag.label(self.lang)
            if flag.type == "single" and flag.choices:
                lines.append(f"[{i+1}] {flag.flag}")
                lines.append(f"    {flag_label}")
                for c in flag.choices:
                    lines.append(f"    - {c.label_str(self.lang)}")
            elif flag.type == "multi":
                checked = self._checkbox_state.get(flag.flag, False)
                mark = "[x]" if checked else "[ ]"
                lines.append(f"[{i+1}] {mark} {flag.flag}")
                lines.append(f"    {flag_label}")
            elif flag.type == "value":
                val = self._selected.get(flag.flag, "") or ""
                lines.append(f"[{i+1}] {flag.flag} = {val}")
                lines.append(f"    {flag_label}")

        content.update("\n".join(lines) if lines else "(无参数)")

    @on(ListView.Selected)
    def on_group_selected(self, event: ListView.Selected) -> None:
        self.current_group_index = event.list_view.index
        self._show_group(self.group_names[self.current_group_index])

    def action_prev_group(self) -> None:
        lv = self.query_one("#group-list", ListView)
        self.current_group_index = (self.current_group_index - 1) % len(self.group_names)
        lv.index = self.current_group_index

    def action_next_group(self) -> None:
        lv = self.query_one("#group-list", ListView)
        self.current_group_index = (self.current_group_index + 1) % len(self.group_names)
        lv.index = self.current_group_index

    def action_activate_search(self) -> None:
        self.search_active = True
        inp = self.query_one("#search-input", Input)
        inp.display = True
        inp.focus()
        header = self.query_one("#detail-header", Static)
        header.update("== 搜索结果 ==")

    def action_deactivate_search(self) -> None:
        self.search_active = False
        inp = self.query_one("#search-input", Input)
        inp.display = False
        inp.value = ""
        self._show_group(self.group_names[self.current_group_index])

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
        if not self.search_active or event.input.id != "search-input":
            return
        query = event.value
        content = self.query_one("#detail-content", Static)
        header = self.query_one("#detail-header", Static)

        if not query.strip():
            self._show_group(self.group_names[self.current_group_index])
            return

        results = search_flags(self.flags, query, self.lang)
        header.update(f"== 搜索: {query} ({len(results)} 结果) ==")

        lines = []
        for flag in results:
            label = flag.label(self.lang)
            if flag.type == "single" and flag.choices:
                choices_str = ", ".join(c.label_str(self.lang) for c in flag.choices)
                lines.append(f"{flag.flag}  {label}")
                lines.append(f"    选项: {choices_str}")
            elif flag.type == "multi":
                lines.append(f"{flag.flag}  {label}")
            elif flag.type == "value":
                lines.append(f"{flag.flag}  {label}")
                if flag.required_args:
                    lines.append(f"    参数: {flag.required_args[0].label_str(self.lang)}")

        content.update("\n".join(lines) if lines else "未找到匹配参数")

    def action_execute(self) -> None:
        if self.search_active:
            return
        self._do_execute()

    def _do_execute(self) -> None:
        group_name = self.group_names[self.current_group_index]
        group_flags = self.groups.get(group_name, [])
        selected_args = []

        for i, flag in enumerate(group_flags):
            val = self._selected.get(flag.flag)
            checked = self._checkbox_state.get(flag.flag, False)

            if flag.type == "single" and val:
                selected_args.append(SelectedFlag(flag.flag, val))
            elif flag.type == "multi" and checked:
                selected_args.append(SelectedFlag(flag.flag))
            elif flag.type == "value" and val:
                selected_args.append(SelectedFlag(flag.flag, val))

        argv = build_argv(selected_args)
        self.exit()
        os.execvp(argv[0], argv)

    def on_key(self, event) -> None:
        # 数字键 1-9 快速选择参数
        if event.key in [str(i) for i in range(1, 10)]:
            idx = int(event.key) - 1
            if self.search_active:
                return
            group_name = self.group_names[self.current_group_index]
            group_flags = self.groups.get(group_name, [])
            if idx >= len(group_flags):
                return
            flag = group_flags[idx]

            if flag.type == "single" and flag.choices:
                # 循环选择下一个选项
                current = self._selected.get(flag.flag)
                current_idx = next(
                    (i for i, c in enumerate(flag.choices) if c.value == current),
                    -1
                )
                next_idx = (current_idx + 1) % len(flag.choices)
                self._selected[flag.flag] = flag.choices[next_idx].value
            elif flag.type == "multi":
                current = self._checkbox_state.get(flag.flag, False)
                self._checkbox_state[flag.flag] = not current
            elif flag.type == "value":
                # 弹出输入提示（暂时用简单方式）
                pass

            self._show_group(group_name)

        # Space 切换 checkbox 状态
        if event.key == " ":
            if self.search_active:
                return
            group_name = self.group_names[self.current_group_index]
            group_flags = self.groups.get(group_name, [])
            for i, flag in enumerate(group_flags):
                if flag.type == "multi":
                    current = self._checkbox_state.get(flag.flag, False)
                    self._checkbox_state[flag.flag] = not current
            self._show_group(group_name)
