"""Поднять локальный demo-контур и загрузить тестовую себестоимость."""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"
ENV_TEMPLATE = ROOT / ".env.example"
SEED_FILE = ROOT / "demo" / "cost-prices.csv"


def get_api_port(env_file: Path) -> int:
    """Прочитать внешний порт API из локального env-файла."""
    for line in env_file.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        if separator and key.strip() == "API_PORT":
            return int(value.strip())
    return 8000


def make_multipart_file(file_path: Path) -> tuple[bytes, str]:
    """Собрать multipart-тело для загрузки CSV без внешних зависимостей."""
    boundary = f"margin-guard-{uuid.uuid4().hex}"
    body = b"\r\n".join(
        [
            f"--{boundary}".encode(),
            (
                'Content-Disposition: form-data; name="file"; '
                f'filename="{file_path.name}"'
            ).encode(),
            b"Content-Type: text/csv",
            b"",
            file_path.read_bytes(),
            f"--{boundary}--".encode(),
            b"",
        ],
    )
    return body, f"multipart/form-data; boundary={boundary}"


def run_command(command: list[str]) -> None:
    """Запустить команду и сразу прервать demo при ошибке."""
    print("$", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def upload_seed(port: int) -> str:
    """Загрузить seed CSV с повторными попытками, пока API запускается."""
    body, content_type = make_multipart_file(SEED_FILE)
    request = Request(
        f"http://localhost:{port}/api/v1/cost-prices/upload",
        data=body,
        headers={"Content-Type": content_type},
        method="POST",
    )
    for attempt in range(10):
        try:
            with urlopen(request, timeout=5) as response:  # noqa: S310
                return response.read().decode("utf-8")
        except (OSError, URLError):
            if attempt == 9:
                raise
            time.sleep(1)
    raise RuntimeError("API не запустился")


def get_preview(port: int) -> str:
    """Получить итог demo-расчёта маржи."""
    url = f"http://localhost:{port}/api/v1/margins/preview"
    with urlopen(url, timeout=5) as response:  # noqa: S310
        return response.read().decode("utf-8")


def ensure_env_file() -> None:
    """Создать локальную конфигурацию из шаблона при первом запуске."""
    if ENV_FILE.exists():
        return
    shutil.copy(ENV_TEMPLATE, ENV_FILE)
    print("Создан .env из .env.example")


def main() -> None:
    """Запустить полный демонстрационный сценарий."""
    ensure_env_file()
    port = get_api_port(ENV_FILE)
    run_command(["docker", "compose", "up", "-d", "--build"])
    run_command(
        [
            "docker",
            "compose",
            "exec",
            "-T",
            "api",
            "alembic",
            "-c",
            "alembic.ini",
            "upgrade",
            "head",
        ],
    )
    print("Загружена себестоимость:", upload_seed(port))
    print("Preview маржи:", get_preview(port))


if __name__ == "__main__":
    try:
        main()
    except (OSError, subprocess.CalledProcessError, URLError) as error:
        print(f"Demo не запущен: {error}", file=sys.stderr)
        sys.exit(1)
