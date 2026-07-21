"""Тесты команды demo-запуска."""

from pathlib import Path

from run_demo import configure_console_encoding, get_api_port, make_multipart_file


class FakeConsole:
    def __init__(self, encoding: str | None) -> None:
        self.encoding = encoding
        self.configured_encoding: str | None = None

    def reconfigure(self, *, encoding: str) -> None:
        self.configured_encoding = encoding


def test_get_api_port_uses_value_from_env(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("APP_ENV=local\nAPI_PORT=8010\n", encoding="utf-8")

    assert get_api_port(env_file) == 8010


def test_get_api_port_defaults_to_8000(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("APP_ENV=local\n", encoding="utf-8")

    assert get_api_port(env_file) == 8000


def test_make_multipart_file_contains_csv(tmp_path: Path) -> None:
    csv_file = tmp_path / "cost-prices.csv"
    csv_file.write_text("marketplace,sku,cost_price\n", encoding="utf-8")

    body, content_type = make_multipart_file(csv_file)

    assert b'filename="cost-prices.csv"' in body
    assert b"marketplace,sku,cost_price" in body
    assert content_type.startswith("multipart/form-data; boundary=margin-guard-")


def test_configure_console_encoding_uses_utf8_for_legacy_console() -> None:
    stream = FakeConsole("cp1251")

    configure_console_encoding(stream)  # type: ignore[arg-type]

    assert stream.configured_encoding == "utf-8"


def test_configure_console_encoding_keeps_utf8_stream() -> None:
    stream = FakeConsole("utf-8")

    configure_console_encoding(stream)  # type: ignore[arg-type]

    assert stream.configured_encoding is None
