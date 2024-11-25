"""Communications with the SQL database"""

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager


def fetch_all(filepath: str, query: str) -> list[dict]:
    """Executes a query returning all rows in the found set"""

    with _get_cursor(filepath) as cursor:
        cursor.execute(query)

        fields: list[str] = [description[0] for description in cursor.description]

        rows: list[dict] = [dict(zip(fields, row)) for row in cursor.fetchall()]

    return rows if rows else [{field: "" for field in fields}]


def fetch_one(filepath: str, query: str) -> list[dict] | None:
    """Executes a query and returns the first row as a dictionary (or None)."""

    with _get_cursor(filepath) as cursor:
        cursor.execute(query)

        fields: list[str] = [description[0] for description in cursor.description]

        if row := cursor.fetchone():
            return [dict(zip(fields, row))]


def fetch_none(filepath: str, query: str, parameters: dict | None = None) -> None:
    """Executes a query that doesn't return values."""

    with _get_cursor(filepath) as cursor:
        cursor.execute(query, parameters) if parameters else cursor.execute(query)


@contextmanager
def _get_cursor(filepath: str) -> Generator[sqlite3.Cursor]:
    """Provides a context manager for establishing and closing a database connection."""

    connection: sqlite3.Connection = sqlite3.connect(filepath)
    cursor: sqlite3.Cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()
