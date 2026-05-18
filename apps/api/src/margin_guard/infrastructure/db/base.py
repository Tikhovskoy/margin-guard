"""Базовый класс ORM."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Корень моделей SQLAlchemy."""
