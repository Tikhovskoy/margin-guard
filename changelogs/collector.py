# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pydantic>=2.11.7,<3",
# ]
# ///
"""Сборка CHANGELOG.md из файлов changelogs/unreleased/."""

import argparse
import os
import re
from collections import defaultdict
from collections.abc import Generator, Iterable
from datetime import datetime
from pathlib import Path, PosixPath
from typing import Self, cast

from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal


class ChangelogContent(BaseModel):
    """Содержимое changelog по категориям Keep a Changelog."""

    added: str | None = None
    changed: str | None = None
    deprecated: str | None = None
    removed: str | None = None
    fixed: str | None = None
    security: str | None = None

    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_pascal),
    )

    @classmethod
    def parse_changelog(cls, changelog_lines: Iterable[str]) -> Self:
        """Парсит markdown-файлы из unreleased."""
        changelog_content: defaultdict[str, str] = defaultdict(str)
        required_categories = cls.model_fields.keys()
        current_category = ""
        for line in changelog_lines:
            if not line.strip("\n"):
                continue

            possible_category = line.lstrip("#").strip().lower()
            if possible_category.startswith("[mr]"):
                current_category = ""
            elif possible_category in required_categories:
                current_category = possible_category
            elif current_category:
                changelog_content[current_category] += line

        return cls.model_validate(changelog_content)


class ChangelogCollector:
    """Переносит unreleased в CHANGELOG.md и архивирует в changelogs/<version>/."""

    VERSION_PATTERN = r"\d+\.\d+\.\d+"

    def __init__(self, version: str) -> None:
        if not re.match(self.VERSION_PATTERN, version):
            msg = "Неверный формат версии. Ожидается `1.0.0`"
            raise ValueError(msg)

        self.version = version

        current_path = Path(__file__).resolve().parent
        self.main_changelog = current_path.parent / "CHANGELOG.md"
        self.unreleased_path = current_path / "unreleased"
        self.new_release_path = current_path / self.version

    def run(self) -> None:
        """Собрать релиз и очистить unreleased."""
        new_changelog_block = self._render_new_changelog_block()
        self.main_changelog.write_text(
            self._render_main_changelog(new_changelog_block),
            encoding="utf-8",
        )
        gitkeep_file = self.unreleased_path / ".gitkeep"
        if gitkeep_file.exists():
            os.remove(gitkeep_file)
        self.unreleased_path.rename(self.new_release_path)
        self.unreleased_path.mkdir()
        gitkeep_file.touch()

    def _render_main_changelog(self, new_changelog_block: str) -> str:
        self.main_changelog.touch(exist_ok=True)

        changelog_lines = self.main_changelog.read_text(encoding="utf-8").splitlines()
        old_changelog_block_start_index: int | None = None
        for line_index, line in enumerate(changelog_lines):
            if re.match(rf"## \[{self.VERSION_PATTERN}]", line):
                old_changelog_block_start_index = line_index
                break

        if old_changelog_block_start_index is None:
            header = changelog_lines
            old_changelog_block: list[str] = []
        else:
            header = changelog_lines[:old_changelog_block_start_index]
            old_changelog_block = changelog_lines[old_changelog_block_start_index:]

        sections = [
            "\n".join(header).rstrip(),
            new_changelog_block.rstrip(),
            "\n".join(old_changelog_block).rstrip(),
        ]
        return "\n\n".join(section for section in sections if section) + "\n"

    def _render_new_changelog_block(self) -> str:
        changelog_content = ChangelogContent.parse_changelog(
            self._read_all_unreleased(),
        )

        changelog_categories = changelog_content.model_dump(
            exclude_none=True,
            by_alias=True,
        )
        template = "### {category}\n\n{content}\n\n"
        today = datetime.today().strftime("%Y-%m-%d")
        result = f"## [{self.version}] - {today}\n\n"
        for category, content in changelog_categories.items():
            result += template.format(category=category, content=content)

        return result

    def _read_all_unreleased(self) -> Generator[str, None, None]:
        if not self.unreleased_path.exists() or not self.unreleased_path.is_dir():
            return

        for file in sorted(self.unreleased_path.iterdir()):
            file = cast(PosixPath, file)
            if not file.is_file() or file.suffix != ".md":
                continue
            with file.open(encoding="utf-8") as handle:
                yield from handle


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("version")
    args = parser.parse_args()

    ChangelogCollector(args.version).run()


if __name__ == "__main__":
    main()
