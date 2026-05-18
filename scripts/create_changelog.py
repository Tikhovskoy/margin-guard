"""Создать файл changelog для текущей git-ветки из TEMPLATE.md."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOGS_DIR = ROOT / "changelogs"
TEMPLATE = CHANGELOGS_DIR / "TEMPLATE.md"
UNRELEASED = CHANGELOGS_DIR / "unreleased"
SANITIZE_SCRIPT = CHANGELOGS_DIR / "sanitize_filename.py"


def get_branch_name() -> str:
    """Текущая ветка git."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def sanitize_branch_name(branch_name: str) -> str:
    """Нормализация имени ветки."""
    result = subprocess.run(
        [sys.executable, str(SANITIZE_SCRIPT), branch_name],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> None:
    branch = get_branch_name()
    if branch == "dev":
        print("Создание changelog на ветке 'dev' запрещено!")
        sys.exit(1)

    if not TEMPLATE.is_file():
        print(f"Шаблон не найден: {TEMPLATE}")
        sys.exit(1)

    filename = f"{sanitize_branch_name(branch)}.md"
    destination = UNRELEASED / filename

    if destination.exists():
        print(f"Файл уже существует: {destination}")
        sys.exit(1)

    UNRELEASED.mkdir(parents=True, exist_ok=True)
    shutil.copy(TEMPLATE, destination)
    print(f"Создан {destination}")


if __name__ == "__main__":
    main()
