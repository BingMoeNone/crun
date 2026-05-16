# tests/test_integration.py
"""pexpect integration tests -- requires crun in PATH or uv run crun."""
import subprocess
import sys
import os
import pytest


def _crun_cmd():
    """Return the command to run crun."""
    # Prefer uv run crun
    try:
        subprocess.run(["uv", "run", "crun", "--version"], capture_output=True, timeout=5)
        return ["uv", "run", "crun"]
    except Exception:
        pass
    return ["crun"]


@pytest.mark.integration
def test_crun_version():
    """crun --version outputs correctly."""
    cmd = _crun_cmd() + ["--version"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    assert result.returncode == 0
    assert "crun" in result.stdout


@pytest.mark.integration
def test_pexpect_startup_and_quit():
    """pexpect: start crun -> see UI -> Esc to quit."""
    pexpect = pytest.importorskip("pexpect")
    child = pexpect.spawn(" ".join(_crun_cmd()), encoding="utf-8", timeout=10)
    try:
        child.expect(["crun", "search", "搜索"], timeout=5)
        child.send("\x1b")  # Esc to quit
        child.expect(pexpect.EOF, timeout=5)
        if child.isalive():
            child.wait()
        assert child.exitstatus in (0, 1)
    finally:
        child.terminate(force=True)


@pytest.mark.integration
def test_pexpect_search_and_toggle():
    """pexpect: search 'model' -> see results -> exit."""
    pexpect = pytest.importorskip("pexpect")
    child = pexpect.spawn(" ".join(_crun_cmd()), encoding="utf-8", timeout=10)
    try:
        child.expect(["crun", "search", "搜索"], timeout=5)
        child.send("/")
        child.send("model")
        child.expect("--model", timeout=5)
        child.send("\x1b")  # Esc exit search
        child.send("\x1b")  # Esc exit program
        child.expect(pexpect.EOF, timeout=5)
    finally:
        child.terminate(force=True)


@pytest.mark.integration
def test_pexpect_help():
    """crun --help works."""
    cmd = _crun_cmd() + ["--help"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    assert result.returncode == 0
