"""CLI 入口点。"""
import os
import platform
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


def print_help() -> None:
    _HELP = (
        f"crun {__version__}\n"
        "A TUI tool for selecting Claude Code startup flags.\n"
        "\n"
        "USAGE:\n"
        "  crun                    Launch the TUI parameter selector\n"
        "  crun --version, -V      Show version and exit\n"
        "  crun --help, -h         Show this help and exit\n"
        "\n"
        "For more information, visit:\n"
        "  https://github.com/BingNgeee/crun\n"
    )
    print(_HELP)


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
    print(f"  v{__version__}")
    print("  by.BingMoe")
    print()


def _check_windows_terminal() -> None:
    """On Windows, enable VT processing and UTF-8 on classic conhost.

    crun's TUI needs ANSI/VT escape sequences. conhost on Win10 1511+
    supports them but may need VT mode enabled and code page set to UTF-8.
    Falls back to a clear error if the console is too old.
    """
    if platform.system() != "Windows":
        return
    if os.environ.get("WT_SESSION") or os.environ.get("TERM_PROGRAM"):
        return

    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32

        # Enable ANSI/VT processing on Windows 10 1511+
        STD_OUTPUT_HANDLE = -11
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
            kernel32.SetConsoleMode(handle, mode)

        # Set UTF-8 I/O so Unicode box-drawing and CJK render correctly
        CP_UTF8 = 65001
        kernel32.SetConsoleOutputCP(CP_UTF8)
        kernel32.SetConsoleCP(CP_UTF8)
        return
    except Exception:
        pass

    print("=" * 60)
    print("  ERROR: Unsupported terminal")
    print()
    print("  crun could not enable ANSI/VT processing on this console.")
    print("  Windows Terminal is required for the full TUI experience.")
    print()
    print("  Install: winget install Microsoft.WindowsTerminal")
    print("  https://aka.ms/terminal")
    print("  Then run: wt crun")
    print("=" * 60)
    sys.exit(6)


def _validate_upgrade_configs() -> None:
    """Validate existing configs after upgrade, report stale entries.

    Runs at startup to detect and clean stale history/presets entries
    that reference flags no longer available (e.g. after version bump).
    """
    from claude_run.config import (
        load_history, load_presets, save_history_entry, save_preset,
        HISTORY_PATH, PRESETS_PATH,
    )
    from claude_run.flags import load_flags as _load_flags

    try:
        valid_flags = {f.flag for f in _load_flags()}
    except Exception:
        return  # can't validate without flags

    # Validate history
    history = load_history()
    if history:
        stale_count = 0
        for entry in history:
            for item in entry.get("selected", []):
                if item.get("flag") and item["flag"] not in valid_flags:
                    stale_count += 1
                    break
        if stale_count > 0:
            log.info(
                "History: %d/%d entries reference stale flags (auto-cleaned on use)",
                stale_count, len(history),
            )

    # Validate presets
    presets = load_presets()
    if presets:
        stale_presets = []
        for name, pdata in presets.items():
            for item in pdata.get("selected", []):
                if item.get("flag") and item["flag"] not in valid_flags:
                    stale_presets.append(name)
                    break
        if stale_presets:
            log.info(
                "Presets: %d/%d presets reference stale flags: %s",
                len(stale_presets), len(presets), ", ".join(stale_presets),
            )


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

    if "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        return 0

    setup_logging()
    print_logo()

    _check_windows_terminal()

    _validate_upgrade_configs()

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
