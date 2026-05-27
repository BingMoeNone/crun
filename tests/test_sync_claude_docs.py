"""Tests for sync_claude_docs.py."""
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from sync_claude_docs import diff_flags, fetch_md, parse_flags_from_md


SAMPLE_TABLE = """## CLI flags

| Flag | Description | Example |
|------|-------------|---------|
| `--add-dir` | Add additional working directories | `claude --add-dir ../apps` |
| `--agent` | Specify an agent for the current session | `claude --agent my-agent` |
| `--continue`, `-c` | Load the most recent conversation | `claude --continue` |
| `--no-chrome` | Disable Chrome integration | `claude --no-chrome` |
"""


def test_parse_flags_from_md():
    flags = parse_flags_from_md(SAMPLE_TABLE)
    names = {f["flag"] for f in flags}
    assert "--add-dir" in names
    assert "--agent" in names
    assert "--continue" in names
    assert "-c" in names
    assert "--no-chrome" in names
    assert len(flags) == 5


def test_parse_flags_strips_angle_brackets():
    text = "| `--debug-file <path>` | Write debug logs | `claude --debug-file /tmp/log` |"
    flags = parse_flags_from_md(text)
    names = {f["flag"] for f in flags}
    assert "--debug-file" in names
    assert "--debug-file <path>" not in names


def test_parse_flags_skips_commands():
    """CLI commands table (e.g. `claude`, `claude update`) should not be parsed as flags."""
    text = "| `claude` | Start interactive session | `claude` |"
    flags = parse_flags_from_md(text)
    names = {f["flag"] for f in flags}
    assert "claude" not in names
    assert len(flags) == 0


def test_parse_flags_empty():
    assert parse_flags_from_md("No table here.") == []


def test_parse_flags_includes_descriptions():
    flags = parse_flags_from_md(SAMPLE_TABLE)
    flag_map = {f["flag"]: f["description"] for f in flags}
    assert "Add additional working directories" in flag_map["--add-dir"]
    assert "Chrome integration" in flag_map["--no-chrome"]


def test_fetch_md_success():
    fake_html = "# Changelog\n\n## v1.0.0\n\n* Stuff changed"
    with patch("sync_claude_docs.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value.read.return_value = (
            fake_html.encode("utf-8")
        )
        result = fetch_md("https://example.com/changelog.md")
        assert result == fake_html


def test_fetch_md_network_error():
    with patch("sync_claude_docs.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = URLError("Connection refused")
        try:
            fetch_md("https://example.com/broken.md")
            assert False, "Should have raised"
        except SystemExit as e:
            assert e.code == 1


def test_diff_flags_new_and_removed():
    official = [
        {"flag": "--add-dir", "description": "Add dirs"},
        {"flag": "--agent", "description": "Specify agent"},
        {"flag": "--new-flag", "description": "Brand new flag"},
    ]
    crun = [
        {"flag": "--add-dir"},
        {"flag": "--agent"},
        {"flag": "--old-flag"},
    ]
    result = diff_flags(official, crun)
    assert result["new"] == [{"flag": "--new-flag", "description": "Brand new flag"}]
    assert result["removed"] == ["--old-flag"]
    assert set(result["in_both"]) == {"--add-dir", "--agent"}


def test_diff_flags_no_diff():
    official = [{"flag": "--add-dir", "description": "Add dirs"}]
    crun = [{"flag": "--add-dir"}]
    result = diff_flags(official, crun)
    assert result["new"] == []
    assert result["removed"] == []
    assert result["in_both"] == ["--add-dir"]
