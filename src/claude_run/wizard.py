# src/claude_run/wizard.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RadioButton, RadioSet, Button, Static
from textual.containers import Container
from claude_run.config import Preferences, save_preferences, CONFIG_DIR

class WizardApp(App):
    CSS = """
    Screen { align: center middle; }
    #title { text-style: bold; margin-bottom: 1; }
    .desc { margin-bottom: 2; }
    #buttons { margin-top: 2; }
    """

    BINDINGS = [("q", "quit", "退出")]

    def __init__(self, prefs: Preferences):
        super().__init__()
        self.prefs = prefs
        self.step = 0  # 0=Welcome, 1=SearchMode, 2=Language, 3=Done

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
        container.mount(Static("欢迎使用 claude-run", id="title"))
        container.mount(Static("一个 TUI 工具，帮助你选择 Claude CLI 的启动参数。", classes="desc"))
        container.mount(Button("开始设置", id="start", variant="primary"))

    def _render_search_mode(self, container: Container) -> None:
        container.mount(Static("选择搜索模式", id="title"))
        rs = RadioSet(id="search_mode")
        rs.mount(RadioButton("模糊搜索（A 模式）", value="A"))
        rs.mount(RadioButton("统一搜索（B 模式）", value="B"))
        rs.mount(RadioButton("两者都显示", value="both"))
        container.mount(rs)
        container.mount(Button("下一步", id="next", variant="primary"))

    def _render_language(self, container: Container) -> None:
        container.mount(Static("选择界面语言", id="title"))
        rs = RadioSet(id="language")
        rs.mount(RadioButton("中文", value="zh"))
        rs.mount(RadioButton("English", value="en"))
        container.mount(rs)
        container.mount(Button("下一步", id="next", variant="primary"))

    def _render_done(self, container: Container) -> None:
        container.mount(Static("设置完成！", id="title"))
        container.mount(Static("正在进入主界面...", classes="desc"))
        # Auto-save and exit after a short delay
        self.set_timer(1.0, self.save_and_exit)

    def save_and_exit(self) -> None:
        rs = self.query_one("#search_mode", RadioSet)
        if rs.selected:
            self.prefs.search_mode = rs.selected
        lang = self.query_one("#language", RadioSet)
        if lang.selected:
            self.prefs.language = lang.selected
        self.prefs.first_run = False
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        save_preferences(self.prefs)
        self.exit(self.prefs)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.step = 1
        elif event.button.id == "next":
            if self.step == 1:
                rs = self.query_one("#search_mode", RadioSet)
                if not rs.selected:
                    return  # Don't advance without selection
            elif self.step == 2:
                rs = self.query_one("#language", RadioSet)
                if not rs.selected:
                    return
            self.step += 1
        self._render_step()

def run_wizard(prefs: Preferences) -> Preferences:
    """Run the first-run wizard. Returns the configured Preferences."""
    app = WizardApp(prefs)
    result = app.run()
    return result if result is not None else prefs
