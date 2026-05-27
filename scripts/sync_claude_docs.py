#!/usr/bin/env python3
"""Sync Claude Code official docs: changelog, CLI reference, and flag diff report."""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib import request
from urllib.error import URLError

CHANGELOG_URL = "https://code.claude.com/docs/en/changelog.md"
CLI_REF_URL = "https://code.claude.com/docs/en/cli-reference.md"
FLAGS_DEFAULT = Path("data/flags_default.json")
OUTPUT_DIR = Path("docs/officaldocs")

CHANGELOG_OUT = OUTPUT_DIR / "CLAUDE_CHANGELOG.md"
CLI_REF_OUT = OUTPUT_DIR / "CLAUDE_CLI_REFERENCE.md"
DIFF_OUT = OUTPUT_DIR / "FLAGS_DIFF.md"


def fetch_md(url: str) -> str:
    """Fetch a markdown document from url, returning its text content."""
    req = request.Request(url, headers={"User-Agent": "crun-sync-docs/1.0"})
    try:
        with request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except URLError as e:
        print(f"ERROR: Failed to fetch {url}: {e}", file=sys.stderr)
        sys.exit(1)


_FLAG_ROW_RE = re.compile(
    r"\|\s*`--([^`]+)`[^|]*\|\s*(.+?)\s*\|"
)


def parse_flags_from_md(text: str) -> list[dict]:
    """Parse CLI reference markdown table rows, returning list of {flag, description}."""
    flags: list[dict] = []
    seen: set[str] = set()

    for line in text.split("\n"):
        m = _FLAG_ROW_RE.match(line)
        if not m:
            continue
        name = "--" + m.group(1)
        desc = m.group(2).strip()
        # Strip inline HTML like <br /> from description
        desc = re.sub(r"<[^>]+>", " ", desc)
        # Collapse whitespace
        desc = re.sub(r"\s+", " ", desc)
        if name not in seen:
            seen.add(name)
            flags.append({"flag": name, "description": desc})
    return flags


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Claude Code docs and diff flags")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print diff to stdout, don't write files")
    parser.add_argument("--skip-changelog", action="store_true",
                        help="Skip changelog fetch")
    parser.add_argument("--skip-cli-ref", action="store_true",
                        help="Skip CLI reference fetch")
    args = parser.parse_args()

    return 0


if __name__ == "__main__":
    sys.exit(main())
