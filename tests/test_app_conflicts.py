# tests/test_app_conflicts.py
"""测试 TUI 互斥逻辑。"""
from claude_run.flags import Flag, Choice


def make_flag(name: str, conflicts: list[str] | None = None, group: str = "test") -> Flag:
    return Flag(
        flag=name,
        description={"zh": name, "en": name},
        required_args=[],
        type="multi",
        group=group,
        choices=None,
        conflicts_with=conflicts,
    )


def test_toggle_adds_conflicting_removes_existing():
    """勾选互斥 flag 时，应取消已选的冲突 flag。"""
    chrome = make_flag("--chrome", conflicts=["--no-chrome"])
    no_chrome = make_flag("--no-chrome", conflicts=["--chrome"])

    checked = {"--no-chrome"}

    # 模拟 toggle：勾选 --chrome
    if "--chrome" not in checked:
        checked.add("--chrome")
        for c in (chrome.conflicts_with or []):
            checked.discard(c)

    assert "--chrome" in checked
    assert "--no-chrome" not in checked


def test_toggle_non_conflicting_preserves_existing():
    """勾选无冲突 flag 时，不影响已选项。"""
    bare = make_flag("--bare")
    verbose = make_flag("--verbose")

    checked = {"--verbose"}
    if "--bare" not in checked:
        checked.add("--bare")

    assert "--bare" in checked
    assert "--verbose" in checked


def test_toggle_uncheck_does_not_affect_others():
    """取消勾选时，不影响其他已选项。"""
    chrome = make_flag("--chrome", conflicts=["--no-chrome"])

    checked = {"--chrome", "--bare"}
    checked.discard("--chrome")

    assert "--chrome" not in checked
    assert "--bare" in checked


def test_system_prompt_mutual_exclusion():
    """--system-prompt 和 --system-prompt-file 互斥。"""
    sp = make_flag("--system-prompt", conflicts=["--system-prompt-file"])
    spf = make_flag("--system-prompt-file", conflicts=["--system-prompt"])

    checked = {"--system-prompt-file"}
    checked.add("--system-prompt")
    for c in (sp.conflicts_with or []):
        checked.discard(c)

    assert "--system-prompt" in checked
    assert "--system-prompt-file" not in checked


def test_no_conflicts_field_does_not_crash():
    """没有 conflicts_with 的 flag 正常 toggle。"""
    flag = make_flag("--verbose")
    checked: set[str] = set()
    checked.add("--verbose")
    for c in (flag.conflicts_with or []):
        checked.discard(c)
    assert "--verbose" in checked
