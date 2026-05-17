#!/usr/bin/env python3
"""Собирает changelog/unreleased/*.md в CHANGELOG.md для версии релиза."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNRELEASED_DIR = ROOT / "changelog" / "unreleased"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
RELEASE_NOTES_PATH = ROOT / "changelog" / "RELEASE_NOTES.md"

CATEGORIES = ("Added", "Changed", "Fixed", "Removed")
UNRELEASED_STUB = (
    "## [Unreleased]\n\n"
    "### Added\n\n"
    "### Changed\n\n"
    "### Fixed\n\n"
    "### Removed\n\n"
)


def parse_fragment(text: str) -> dict[str, list[str]]:
    """Парсит ### Category и bullet-строки."""
    buckets: dict[str, list[str]] = {c: [] for c in CATEGORIES}
    current: str | None = None
    for line in text.splitlines():
        header = re.match(r"^###\s+(\w+)\s*$", line.strip())
        if header and header.group(1) in buckets:
            current = header.group(1)
            continue
        if current and line.strip().startswith("-"):
            item = line.strip().removeprefix("-").strip()
            if item:
                buckets[current].append(item)
    return buckets


def merge_buckets(target: dict[str, list[str]], source: dict[str, list[str]]) -> None:
    for cat in CATEGORIES:
        for item in source[cat]:
            if item not in target[cat]:
                target[cat].append(item)


def format_version_block(version: str, release_date: str, buckets: dict[str, list[str]]) -> str:
    lines = [f"## [{version}] - {release_date}", ""]
    for cat in CATEGORIES:
        if not buckets[cat]:
            continue
        lines.append(f"### {cat}")
        lines.append("")
        for item in buckets[cat]:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def load_fragments() -> dict[str, list[str]]:
    merged: dict[str, list[str]] = {c: [] for c in CATEGORIES}
    if not UNRELEASED_DIR.is_dir():
        return merged
    for path in sorted(UNRELEASED_DIR.glob("*.md")):
        merge_buckets(merged, parse_fragment(path.read_text(encoding="utf-8")))
    return merged


def update_changelog_file(version_block: str) -> None:
    content = (
        CHANGELOG_PATH.read_text(encoding="utf-8")
        if CHANGELOG_PATH.exists()
        else "# Changelog\n\n"
    )
    if "## [Unreleased]" in content:
        content = re.sub(
            r"## \[Unreleased\][\s\S]*?(?=## \[)",
            UNRELEASED_STUB,
            content,
            count=1,
        )
    else:
        content = content.replace("# Changelog\n\n", f"# Changelog\n\n{UNRELEASED_STUB}", 1)
    content = content.replace(UNRELEASED_STUB, UNRELEASED_STUB + version_block, 1)
    CHANGELOG_PATH.write_text(content, encoding="utf-8")


def clear_fragments() -> None:
    if not UNRELEASED_DIR.is_dir():
        return
    for path in UNRELEASED_DIR.glob("*.md"):
        path.unlink()


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: changelog_release.py <version> [YYYY-MM-DD]")

    version = sys.argv[1].lstrip("v")
    release_date = sys.argv[2] if len(sys.argv) > 2 else date.today().isoformat()

    buckets = load_fragments()
    if not any(buckets[c] for c in CATEGORIES):
        raise SystemExit("No unreleased changelog entries in changelog/unreleased/")

    version_block = format_version_block(version, release_date, buckets)
    RELEASE_NOTES_PATH.parent.mkdir(parents=True, exist_ok=True)
    RELEASE_NOTES_PATH.write_text(version_block, encoding="utf-8")
    update_changelog_file(version_block)
    clear_fragments()
    print(f"CHANGELOG updated for v{version}")


if __name__ == "__main__":
    main()
