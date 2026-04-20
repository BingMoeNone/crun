# src/claude_run/wizard.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RadioButton, RadioSet, Button, Static
from textual.containers import Container
from claude_run.config import Preferences, save_preferences, CONFIG_DIR


class WizardApp(App):
    CSS = """
    Screen { align: center middle; }
    """

    BINDINGS = [("q", "quit", "退出")]

    def __init__(self, prefs: Preferences):
        super().__init__()
        self.prefs = prefs
        self.step = 0

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(id="content")
        yield Footer()

    def on_mount(self) -> None:
        self._render_step()

    def _render_step(self) -> None:
        container = self.query_one("#content")
        container.remove_children()

        if self.step == 0:
            self._render_welcome(container)
        elif self.step == 1:
            self._render_search_mode(container)
        elif self.step == 2:
            self._render_language(container)
        elif self.step == 3:
            self._render_done(container)

    def _render_welcome(self, container: Container) -> None:
        container.mount(Static("=== 欢迎使用 claude-run ==="))
        container.mount(Static(""))
        container.mount(Static("一个 TUI 工具，帮助你选择 Claude CLI 的启动参数。"))
        container.mount(Static(""))
        container.mount(Button("开始设置", id="start", variant="primary"))

    def _render_search_mode(self, container: Container) -> None:
        container.mount(Static("=== 步骤 1/2：选择搜索模式 ==="))
        container.mount(Static(""))
        container.mount(RadioButton("A - 模糊搜索（输入关键词实时过滤）", value="A", id="rb-a"))
        container.mount(RadioButton("B - 统一搜索（搜索框常驻）", value="B", id="rb-b"))
        container.mount(RadioButton("both - 两者都显示", value="both", id="rb-both"))
        container.mount(Static(""))
        container.mount(Button("下一步", id="next", variant="primary"))

    def _render_language(self, container: Container) -> None:
        container.mount(Static("=== 步骤 2/2：选择界面语言 ==="))
        container.mount(Static(""))
        container.mount(RadioButton("中文", value="zh", id="rb-zh"))
        container.mount(RadioButton("English", value="en", id="rb-en"))
        container.mount(Static(""))
        container.mount(Button("下一步", id="next", variant="primary"))

    def _render_done(self, container: Container) -> None:
        container.mount(Static("设置完成！"))
        container.mount(Static("正在保存配置..."))
        self.set_timer(0.5, self.save_and_exit)

    def save_and_exit(self) -> None:
        rs_a = self.query_one("#rb-a", RadioButton)
        rs_b = self.query_one("#rb-b", RadioButton)
        rs_both = self.query_one("#rb-both", RadioButton)
        if rs_a.checked:
            self.prefs.search_mode = "A"
        elif rs_b.checked:
            self.prefs.search_mode = "B"
        elif rs_both.checked:
            self.prefs.search_mode = "both"

        rb_zh = self.query_one("#rb-zh", RadioButton)
        rb_en = self.query_one("#rb-en", RadioButton)
        if rb_zh.checked:
            self.prefs.language = "zh"
        elif rb_en.checked:
            self.prefs.language = "en"

        self.prefs.first_run = False
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        save_preferences(self.prefs)
        self.exit(self.prefs)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.step = 1
        elif event.button.id == "next":
            if self.step == 1:
                rs = self.query_one("#rb-a", RadioButton)
                rb_b = self.query_one("#rb-b", RadioButton)
                rb_both = self.query_one("#rb-both", RadioButton)
                if not (rs.checked or rb_b.checked or rb_both.checked):
                    return
            elif self.step == 2:
                rb = self.query_one("#rb-zh", RadioButton)
                rb_en = self.query_one("#rb-en", RadioButton)
                if not (rb.checked or rb_en.checked):
                    return
            self.step += 1
        self._render_step()


def run_wizard(prefs: Preferences) -> Preferences:
    app = WizardApp(prefs)
    result = app.run()
    return result if result is not None else prefs
