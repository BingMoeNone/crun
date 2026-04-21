# tests/test_runner.py
from claude_run.runner import SelectedFlag, build_argv

def test_build_argv_empty():
    args = build_argv([])
    assert args == ["claude"]

def test_build_argv_single_flag():
    args = build_argv([SelectedFlag("--model", "opus")])
    assert args == ["claude", "--model", "opus"]

def test_build_argv_no_value_flag():
    args = build_argv([SelectedFlag("--bare")])
    assert args == ["claude", "--bare"]

def test_build_argv_with_value():
    args = build_argv([SelectedFlag("--mcp-config", "/path/to/mcp.json")])
    assert args == ["claude", "--mcp-config", "/path/to/mcp.json"]

def test_build_argv_multiple_flags():
    args = build_argv([SelectedFlag("--model", "sonnet"), SelectedFlag("--bare")])
    assert args == ["claude", "--model", "sonnet", "--bare"]

def test_selected_flag_to_argv():
    sf = SelectedFlag("--debug", "api,hooks")
    assert sf.to_argv() == ["--debug", "api,hooks"]

def test_selected_flag_no_value():
    sf = SelectedFlag("--bare")
    assert sf.to_argv() == ["--bare"]
