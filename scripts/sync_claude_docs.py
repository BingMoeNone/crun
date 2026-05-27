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


def diff_flags(
    official: list[dict],
    crun: list[dict],
) -> dict:
    """Compare official flag set against crun's flags_default.json.

    Returns {"new": [...], "removed": [...], "in_both": [...]}.
    """
    official_names = {f["flag"] for f in official}
    crun_names = {f["flag"] for f in crun}

    new_flags = [f for f in official if f["flag"] not in crun_names]
    removed = sorted(crun_names - official_names)
    in_both = sorted(official_names & crun_names)

    return {
        "new": sorted(new_flags, key=lambda f: f["flag"]),
        "removed": removed,
        "in_both": in_both,
    }


def load_crun_flags(path: Path) -> list[dict]:
    """Load flag definitions from flags_default.json."""
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        data = json.load(f)
    return data.get("flags", [])


def generate_diff_report(diff: dict, official_flags: list[dict]) -> str:
    """Generate markdown diff report from diff dictionary."""
    lines = [
        "# Claude Code Flags Diff Report",
        "",
        f"**Official flags total:** {len(official_flags)}",
        f"**crun flags total:** {len(diff['in_both']) + len(diff['removed'])}",
        f"**New in common:** {len(diff['in_both'])}",
        "",
    ]

    if diff["new"]:
        lines.append("## New in Official (crun missing)")
        lines.append("")
        lines.append("| Flag | Description |")
        lines.append("|------|-------------|")
        for f in diff["new"]:
            desc = f["description"].replace("|", "\\|")
            lines.append(f"| `{f['flag']}` | {desc[:200]} |")
        lines.append("")

    if diff["removed"]:
        lines.append("## Removed from Official (crun has, possibly deprecated)")
        lines.append("")
        for flag in diff["removed"]:
            lines.append(f"- `{flag}`")
        lines.append("")

    if not diff["new"] and not diff["removed"]:
        lines.append("No differences found. crun flags are in sync with official docs.")
        lines.append("")

    return "\n".join(lines)


def write_file(path: Path, content: str) -> None:
    """Write content to path, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Claude Code docs and diff flags")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print diff to stdout, don't write files")
    parser.add_argument("--skip-changelog", action="store_true",
                        help="Skip changelog fetch")
    parser.add_argument("--skip-cli-ref", action="store_true",
                        help="Skip CLI reference fetch")
    args = parser.parse_args()

    # 1. Fetch and save changelog
    if not args.skip_changelog:
        print("Fetching changelog...")
        changelog = fetch_md(CHANGELOG_URL)
        if not args.dry_run:
            write_file(CHANGELOG_OUT, changelog)
            print(f"  -> {CHANGELOG_OUT} ({len(changelog)} bytes)")

    # 2. Fetch and save CLI reference
    if not args.skip_cli_ref:
        print("Fetching CLI reference...")
        cli_ref = fetch_md(CLI_REF_URL)
        if not args.dry_run:
            write_file(CLI_REF_OUT, cli_ref)
            print(f"  -> {CLI_REF_OUT} ({len(cli_ref)} bytes)")

        # 3. Parse flags from CLI reference
        official_flags = parse_flags_from_md(cli_ref)
        if len(official_flags) < 30:
            print(f"WARNING: Only parsed {len(official_flags)} flags, expected 30+. "
                  f"Table format may have changed.", file=sys.stderr)
        print(f"Parsed {len(official_flags)} flags from CLI reference")

        # 4. Load crun flags and diff
        crun_flags = load_crun_flags(FLAGS_DEFAULT)
        diff = diff_flags(official_flags, crun_flags)
        report = generate_diff_report(diff, official_flags)

        if args.dry_run:
            print("\n" + report)
        else:
            write_file(DIFF_OUT, report)
            print(f"  -> {DIFF_OUT}")
            print(f"  New: {len(diff['new'])}, Removed: {len(diff['removed'])}, "
                  f"In both: {len(diff['in_both'])}")

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
