"""可复用 TUI 组件：FlagRow 表单行。"""
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, RadioSet, RadioButton, Checkbox, Input

from claude_run.flags import Flag


class FlagRow(Container):
    """一个参数行：根据 type 渲染 RadioSet / Checkbox / Input。"""

    DEFAULT_CSS = """
    FlagRow {
        height: auto;
        border: tall $panel;
        padding: 0 1;
        margin-bottom: 1;
    }
    FlagRow.sel { border: tall $success; }
    FlagRow .desc { color: $text-muted; }
    FlagRow RadioSet { layout: horizontal; height: auto; }
    FlagRow Input { height: 3; }
    """

    def __init__(self, flag: Flag, lang: str, state: dict):
        super().__init__()
        self.flag = flag
        self.lang = lang
        self.state = state

    def compose(self) -> ComposeResult:
        yield Static(f"[b]{self.flag.flag}[/b]")
        yield Static(self.flag.label(self.lang), classes="desc")
        if self.flag.type == "single" and self.flag.choices:
            cur = self.state.get(self.flag.flag)
            with RadioSet():
                for c in self.flag.choices:
                    yield RadioButton(
                        c.label_str(self.lang),
                        value=(c.value == cur),
                        name=c.value,
                    )
        elif self.flag.type == "multi":
            yield Checkbox(
                self.flag.flag,
                value=bool(self.state.get(self.flag.flag, False)),
            )
        elif self.flag.type == "value":
            ph = (self.flag.required_args[0].placeholder_str(self.lang)
                  if self.flag.required_args else "")
            cur = self.state.get(self.flag.flag, "") or ""
            yield Input(value=cur, placeholder=ph)

    def on_mount(self) -> None:
        self.refresh_border()

    def refresh_border(self) -> None:
        v = self.state.get(self.flag.flag)
        if self.flag.type == "multi":
            selected = bool(v)
        elif self.flag.type == "single":
            selected = isinstance(v, str) and v != ""
        elif self.flag.type == "value":
            selected = isinstance(v, str) and bool(v)
        else:
            selected = False
        self.set_class(selected, "sel")
