"""Tests for sync_claude_docs.py."""
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from sync_claude_docs import fetch_md


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
