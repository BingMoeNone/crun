"""命令构建与执行。"""
import os
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


def validate_argv(argv: list[str]) -> tuple[bool, str]:
    """
    验证 argv 是否可执行。
    返回 (是否有效, 错误信息)。
    """
    if not argv:
        return False, "参数列表为空"

    exe = argv[0]

    # 检查 claude 命令是否存在
    if exe == "claude":
        # 检查 PATH 中是否有 claude
        from shutil import which
        if which("claude") is None:
            return False, "claude 命令未安装或不在 PATH 中"
    else:
        # 非 claude 命令，检查是否存在
        from shutil import which
        if which(exe) is None:
            return False, f"命令 '{exe}' 未安装或不在 PATH 中"

    return True, ""


def execute_claude(argv: list[str]) -> None:
    """
    执行 claude 命令，使用 execvp 替换当前进程。

    注意：此函数不返回（成功时进程被替换），
    失败时抛出 ExecuteError。
    """
    # 验证命令
    valid, err_msg = validate_argv(argv)
    if not valid:
        raise ExecuteError(err_msg)

    exe = argv[0]

    try:
        os.execvp(exe, argv)
    except FileNotFoundError as e:
        raise ExecuteError(f"命令 '{exe}' 不存在: {e}")
    except PermissionError as e:
        raise ExecuteError(f"无法执行 '{exe}': 权限不足")
    except OSError as e:
        raise ExecuteError(f"执行 '{exe}' 失败: {e}")