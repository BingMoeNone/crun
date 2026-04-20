"""首次运行引导：选择搜索模式 + 语言。"""
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Header, Footer, Button, Static, RadioSet, RadioButton

from claude_run.config import Preferences, save_preferences, CONFIG_DIR, ConfigError


class WizardApp(App):
    """两步引导 — 配色同主应用：$accent + $success。"""

    CSS = """
    Screen { align: center middle; background: $surface; }
    #content {
        width: auto;
        max-width: 72;
        height: auto;
        padding: 2 4;
        border: tall $accent;
        background: $panel;
    }
    Static.title { text-style: bold; color: $accent; }
    Static.error { color: $error; text-style: bold; }
    RadioSet { margin: 1 0; }
    Button { margin-top: 1; }
    """

    TITLE = "claude-run · 初次设置"

    BINDINGS = [
        Binding("q,ctrl+c", "quit", "退出", priority=True),
        Binding("escape", "quit", "退出"),
    ]

    def __init__(self, prefs: Preferences):
        super().__init__()
        self.prefs = prefs
        self.step = 0

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Container(id="content")
        yield Footer()

    def on_mount(self) -> None:
        self._render_step()

    def _render_step(self) -> None:
        c = self.query_one("#content", Container)
        c.remove_children()
        if self.step == 0:
            c.mount(Static("欢迎使用 claude-run", classes="title"))
            c.mount(Static(""))
            c.mount(Static("一个帮你选择 Claude CLI 启动参数的 TUI 工具。"))
            c.mount(Static(""))
            c.mount(Button("开始设置 →", id="start", variant="primary"))
        elif self.step == 1:
            c.mount(Static("步骤 1 / 2 · 搜索模式", classes="title"))
            rs = RadioSet(id="rs-search")
            c.mount(rs)
            rs.mount(RadioButton("A · 模糊搜索（按 / 激活临时搜索框）",
                                 value=True, name="A"))
            rs.mount(RadioButton("B · 统一搜索（搜索框常驻顶部）", name="B"))
            rs.mount(RadioButton("Both · 两者都启用", name="both"))
            c.mount(Button("下一步 →", id="next", variant="primary"))
        elif self.step == 2:
            c.mount(Static("步骤 2 / 2 · 界面语言", classes="title"))
            rs = RadioSet(id="rs-lang")
            c.mount(rs)
            rs.mount(RadioButton("中文", value=True, name="zh"))
            rs.mount(RadioButton("English", name="en"))
            c.mount(Button("完成 ✓", id="finish", variant="success"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id
        if bid == "start":
            self.step = 1
            self._render_step()
        elif bid == "next":
            rs = self.query_one("#rs-search", RadioSet)
            if rs.pressed_button and rs.pressed_button.name:
                self.prefs.search_mode = rs.pressed_button.name
            self.step = 2
            self._render_step()
        elif bid == "finish":
            rs = self.query_one("#rs-lang", RadioSet)
            if rs.pressed_button and rs.pressed_button.name:
                self.prefs.language = rs.pressed_button.name
            self.prefs.first_run = False
            try:
                CONFIG_DIR.mkdir(parents=True, exist_ok=True)
                save_preferences(self.prefs)
            except ConfigError as e:
                c = self.query_one("#content", Container)
                c.mount(Static(""))
                c.mount(Static(f"❌ 保存配置失败: {e}", classes="error"))
                c.mount(Button("重试", id="retry", variant="warning"))
                return
            self.exit(self.prefs)
        elif bid == "retry":
            try:
                CONFIG_DIR.mkdir(parents=True, exist_ok=True)
                save_preferences(self.prefs)
                self.exit(self.prefs)
            except ConfigError as e:
                c = self.query_one("#content", Container)
                c.remove_children()
                c.mount(Static("❌ 仍然失败", classes="error"))
                c.mount(Static(f"错误: {e}"))
                c.mount(Static("请检查 ~/.config/claude-run/ 权限"))
                c.mount(Button("退出", id="quit", variant="error"))
        elif bid == "quit":
            self.exit(self.prefs)


def run_wizard(prefs: Preferences) -> Preferences:
    app = WizardApp(prefs)
    result = app.run()
    return result if result is not None else prefs
