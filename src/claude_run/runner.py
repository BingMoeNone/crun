# src/claude_run/runner.py
import os
from typing import Sequence

class SelectedFlag:
    def __init__(self, flag: str, value: str | None = None):
        self.flag = flag
        self.value = value

    def to_argv(self) -> list[str]:
        argv = [self.flag]
        if self.value is not None:
            argv.append(self.value)
        return argv

def build_argv(selected: Sequence[SelectedFlag]) -> list[str]:
    """Build the claude command argument list."""
    argv = ["claude"]
    for sel in selected:
        argv.extend(sel.to_argv())
    return argv

def execute_claude(argv: list[str]):
    """Execute claude with the given arguments using execvp."""
    os.execvp(argv[0], argv)
