"""Communications with the SQL database"""

from collections.abc import Generator
from contextlib import contextmanager
from dbfxsql.constants.sql_libraries import SQL
from dbfxsql.helpers import formatters

from decouple import config


def fetch_all(engine: str, filepath: str, query: str) -> list[dict]:
    """Executes a query returning all rows in the found set"""

    with _get_cursor(engine, filepath) as cursor:
        cursor.execute(query)

        fields: list[str] = [description[0] for description in cursor.description]

        rows: list[dict] = [dict(zip(fields, row)) for row in cursor.fetchall()]

    return rows if rows else [{field: "" for field in fields}]


def fetch_one(engine: str, filepath: str, query: str) -> list[dict] | None:
    """Executes a query and returns the first row as a dictionary (or None)."""

    with _get_cursor(engine, filepath) as cursor:
        cursor.execute(query)

        fields: list[str] = [description[0] for description in cursor.description]

        if row := cursor.fetchone():
            return [dict(zip(fields, row))]


def fetch_none(
    engine: str, filepath: str, query: str, parameters: dict | None = None
) -> None:
    """Executes a query that doesn't return values."""

    with _get_cursor(engine, filepath) as cursor:
        cursor.execute(query, parameters) if parameters else cursor.execute(query)


@contextmanager
def _get_cursor(engine: str, filepath: str) -> Generator:
    """Provides a context manager for establishing and closing a database connection."""

    if "SQLite" == engine:
        connection: SQL[engine].Connection = SQL[engine].connect(filepath)
    else:
        filename: str = formatters.decompose_file(filepath)[0]

        connection: SQL[engine].Connection = SQL[engine].connect(
            server=config("DB_SERVER"),
            user=config("DB_USER"),
            password=config("DB_PASSWORD"),
            database=filename,
            autocommit=True,
        )

    cursor: SQL[engine].Cursor = connection.cursor()

    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()
