"""命令构建与执行。"""
import os
import platform
import subprocess
import logging
from typing import Sequence

log = logging.getLogger(__name__)


class ExecuteError(Exception):
    """执行 claude 失败时的错误。"""
    pass


class SelectedFlag:
    """已选参数。"""
    def __init__(self, flag: str, value: str | None = None):
        self.flag = flag
        self.value = value

    def to_argv(self) -> list[str]:
        argv = [self.flag]
        if self.value is not None:
            argv.append(self.value)
        return argv


def build_argv(selected: Sequence[SelectedFlag]) -> list[str]:
    """构建 claude 命令参数列表。"""
    argv = ["claude"]
    for sel in selected:
        argv.extend(sel.to_argv())
    return argv


def _resolve_exe(exe: str) -> str | None:
    """Resolve an executable path, handling Windows PATHEXT (.cmd/.bat wrappers)."""
    from shutil import which
    resolved = which(exe)
    if resolved is None and platform.system() == "Windows":
        for ext in os.environ.get("PATHEXT", ".EXE;.CMD;.BAT").split(";"):
            resolved = which(exe + ext)
            if resolved:
                break
    return resolved


def validate_argv(argv: list[str]) -> tuple[bool, str]:
    """
    验证 argv 是否可执行。
    返回 (是否有效, 错误信息)。
    """
    if not argv:
        return False, "参数列表为空"

    if _resolve_exe(argv[0]) is None:
        return False, f"命令 '{argv[0]}' 未安装或不在 PATH 中"

    return True, ""


def execute_claude(argv: list[str]) -> None:
    """
    执行 claude 命令，替换当前进程。

    注意：此函数不返回（成功时进程被替换），
    失败时抛出 ExecuteError。
    """
    # 验证命令
    valid, err_msg = validate_argv(argv)
    if not valid:
        raise ExecuteError(err_msg)

    exe = argv[0]

    if platform.system() == "Windows":
        resolved = _resolve_exe(exe)
        if resolved:
            argv[0] = resolved
        try:
            result = subprocess.run(argv)
            os._exit(result.returncode)
        except FileNotFoundError:
            raise ExecuteError(f"命令 '{exe}' 不存在")
        except PermissionError:
            raise ExecuteError(f"无法执行 '{exe}': 权限不足")
        except OSError as e:
            raise ExecuteError(f"执行 '{exe}' 失败: {e}")
    else:
        try:
            os.execvp(exe, argv)
        except FileNotFoundError as e:
            raise ExecuteError(f"命令 '{exe}' 不存在: {e}")
        except PermissionError as e:
            raise ExecuteError(f"无法执行 '{exe}': 权限不足")
        except OSError as e:
            raise ExecuteError(f"执行 '{exe}' 失败: {e}")