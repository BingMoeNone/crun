"""? 键打开的帮助弹窗。"""
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Static, Button


HELP_TEXT = """[b]claude-run · 快捷键[/b]

[b]导航[/b]
  ↑/k, ↓/j         上/下一个分组
  ←/h, →/l         回到分组 / 进入参数列表
  Tab / Shift+Tab  在输入控件间切换焦点

[b]选择[/b]
  Space            勾选 / 取消勾选
  Enter            在分组列表上按 = 执行
  直接键入         value 类型参数输入值

[b]搜索[/b]
  /  或  Ctrl+S    模糊搜索（底部临时搜索框）
  Ctrl+U           统一搜索（顶部常驻搜索框）
  Esc              关闭搜索

[b]执行 / 退出[/b]
  F5 / Ctrl+R      执行 claude <选中参数>
  q / Ctrl+C       退出
  ?                显示本帮助
"""


class HelpScreen(ModalScreen):
    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }
    #help-box {
        width: auto;
        max-width: 70;
        height: auto;
        padding: 1 2;
        border: tall $accent;
        background: $surface;
    }
    #help-box Button { margin-top: 1; }
    """

    BINDINGS = [
        ("escape", "dismiss_help", "关闭"),
        ("q", "dismiss_help", "关闭"),
        ("question_mark", "dismiss_help", "关闭"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="help-box"):
            yield Static(HELP_TEXT)
            yield Button("关闭 (Esc)", id="close-help", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close-help":
            self.dismiss()

    def action_dismiss_help(self) -> None:
        self.dismiss()
