#!/usr/bin/env python3
"""Извлекает секцию Changelog из текста PR."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def extract_changelog(body: str) -> str:
    """Возвращает содержимое секции ## Changelog до следующего ##."""
    match = re.search(
        r"^##\s+Changelog\s*$([\s\S]*?)(?=^##\s|\Z)",
        body,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    if not match:
        return ""
    return match.group(1).strip()


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/dev/stdin")
    body = source.read_text(encoding="utf-8")
    result = extract_changelog(body)
    sys.stdout.write(result)


if __name__ == "__main__":
    main()
