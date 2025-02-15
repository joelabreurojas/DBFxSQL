"""Communications with the SQL database"""

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager

import pymssql

from dbfxsql.constants.sql_libraries import SQL
from dbfxsql.exceptions.connection_errors import SQLConnectionFailed
from dbfxsql.helpers import file_manager, formatters


def fetch_none(
    engine: str,
    filepath: str,
    query: str | list,
    parameters: dict[str, str] | list = [],
    execute_many: bool = False,
) -> None:
    """Executes a query that doesn't return values."""

    with _get_cursor(engine, filepath) as cursor:
        if execute_many:
            for parameter in parameters:
                cursor.execute(query, parameter)

            # Triggers don't detect executemany changes
            # cursor.executemany(query, parameters)

        elif isinstance(query, list):
            if parameters:
                for query_, parameter in zip(query, parameters):
                    cursor.execute(query_, parameter)
            else:
                for query_ in query:
                    cursor.execute(query_)

        else:
            cursor.execute(query, parameters) if parameters else cursor.execute(query)


def fetch_one(engine: str, filepath: str, query: str) -> list[dict]:
    """Executes a query and returns the first row as a dictionary."""

    with _get_cursor(engine, filepath) as cursor:
        cursor.execute(query)

        fields: list[str] = [description[0] for description in cursor.description]

        row: list = []

        for field in cursor.fetchone():
            row.append(field.rstrip() if isinstance(field, str) else field)

        return [dict(zip(fields, row))]


def fetch_all(engine: str, filepath: str, query: str) -> list[dict]:
    """Executes a query returning all rows in the found set"""

    with _get_cursor(engine, filepath) as cursor:
        cursor.execute(query)

        fields: list[str] = [description[0] for description in cursor.description]

        rows: list = [
            [field.rstrip() if isinstance(field, str) else field for field in row]
            for row in cursor.fetchall()
        ]

        rows = [dict(zip(fields, row)) for row in rows]

    return rows if rows else [{field: "" for field in fields}]


@contextmanager
def _get_cursor(engine: str, filepath: str) -> Generator:
    """Provides a context manager for establishing and closing a database connection."""
    connection: sqlite3.Connection | pymssql.Connection

    if "SQLite" == engine:
        connection = SQL[engine].connect(filepath)
    else:
        config: dict = file_manager.load_config()["engines"][engine]
        database: str = formatters.decompose_file(filepath)[0]

        connection = SQL[engine].connect(
            server=config["db_server"],
            user=config["db_user"],
            password=config["db_password"],
            database=database,
            autocommit=True,
            tds_version="7.0",
        )

    cursor = connection.cursor()

    try:
        yield cursor
        connection.commit()

    except Exception as error:
        connection.rollback()

        filename: str = formatters.decompose_file(filepath)[0]

        raise SQLConnectionFailed(engine, filename, error)

    finally:
        cursor.close()
        connection.close()
