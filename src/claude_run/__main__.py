"""CLI 入口点。"""
import os
import sys
import logging
from importlib.metadata import version, PackageNotFoundError

import questionary

from claude_run.config import load_preferences, is_first_run, Preferences, ConfigError
from claude_run.wizard import run_wizard
from claude_run.app import run_app
from claude_run.runner import execute_claude, ExecuteError

try:
    __version__ = version("crun")
except PackageNotFoundError:
    __version__ = "unknown"

log = logging.getLogger(__name__)

_LOGO = r"""
   ____  ____  _  _  ____
  / ___)|  _ \| || ||  _ \
 | |    | |_| | || || |_| |
 | |    |  _ (| || ||  _ <
 | |___ | |_| | \__/ | |_| |
  \____)|____/  \__/ |____/
""".strip("\n")


def setup_logging() -> None:
    if os.environ.get("DEBUG"):
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s %(name)s: %(message)s",
        )
    else:
        logging.basicConfig(
            level=logging.WARNING,
            format="%(levelname)s: %(message)s",
        )


def print_logo() -> None:
    print(_LOGO)
    print("  by.BingMoe")
    print()


def main() -> int:
    """
    主入口，返回退出码。

    0 - 成功执行 claude
    1 - 用户取消 / 正常退出
    2 - 配置错误
    3 - 参数加载错误
    4 - 执行错误
    5 - 其他未知错误
    """
    if "--version" in sys.argv or "-V" in sys.argv:
        print(f"crun {__version__}")
        return 0

    setup_logging()
    print_logo()

    try:
        if is_first_run():
            prefs = run_wizard(Preferences())
        else:
            prefs = load_preferences()

        # Check custom keybinding conflicts
        if prefs.keybindings:
            from claude_run.config import _validate_keybindings
            warnings = _validate_keybindings(prefs.keybindings)
            if warnings:
                print("⚠ Detected custom keybinding conflicts:")
                for w in warnings:
                    print(f"  {w}")
                print()
                confirm = questionary.confirm(
                    "Continue with custom keybindings? (Y/n):",
                    default=True,
                ).ask()
                if not confirm:
                    print("Using default keybindings.")
                    prefs.keybindings = None
                else:
                    print("Custom keybindings applied.")
                print()

        argv = run_app(prefs)

        if isinstance(argv, list) and argv:
            try:
                execute_claude(argv)
            except ExecuteError as e:
                print(f"\n❌ 执行失败: {e}", file=sys.stderr)
                print("请确保 'claude' 命令已安装并可用。", file=sys.stderr)
                return 4

        return 1

    except ConfigError as e:
        print(f"\n❌ 配置错误: {e}", file=sys.stderr)
        print("请检查 ~/.config/crun/ 目录权限。", file=sys.stderr)
        return 2

    except KeyboardInterrupt:
        print("\n用户取消。")
        return 1

    except Exception as e:
        log.exception("未知错误")
        print(f"\n❌ 未知错误: {e}", file=sys.stderr)
        print("请检查日志或联系开发者。", file=sys.stderr)
        return 5


if __name__ == "__main__":
    sys.exit(main())
