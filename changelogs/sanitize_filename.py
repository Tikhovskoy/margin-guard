"""Нормализация имени ветки для имени файла changelog."""

import re
import sys


def sanitize_branch_name(branch_name: str) -> str:
    """Заменяет недопустимые символы на подчёркивание."""
    return re.sub(r'[\\/:*?"<>|]', "_", branch_name)


if __name__ == "__main__":
    print(sanitize_branch_name(sys.argv[1]))
