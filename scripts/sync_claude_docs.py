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
