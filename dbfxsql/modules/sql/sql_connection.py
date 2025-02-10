"""Communications with the SQL database"""

from collections.abc import Generator
from contextlib import contextmanager

from dbfxsql.constants.sql_libraries import SQL
from dbfxsql.helpers import formatters, file_manager
from dbfxsql.exceptions.connection_errors import SQLConnectionFailed


def fetch_all(engine: str, filepath: str, query: str) -> list[dict]:
    """Executes a query returning all rows in the found set"""

    with _get_cursor(engine, filepath) as cursor:
        cursor.execute(query)

        fields: list[str] = [description[0] for description in cursor.description]

        rows: list = []

        for row in cursor.fetchall():
            rows.append(
                [field.rstrip() if isinstance(field, str) else field for field in row]
            )

        rows: list[dict] = [dict(zip(fields, row)) for row in rows]

    return rows if rows else [{field: "" for field in fields}]


def fetch_one(engine: str, filepath: str, query: str) -> list[dict] | None:
    """Executes a query and returns the first row as a dictionary (or None)."""

    with _get_cursor(engine, filepath) as cursor:
        cursor.execute(query)

        fields: list[str] = [description[0] for description in cursor.description]

        row: list = []

        for field in cursor.fetchone():
            row.append(field.rstrip() if isinstance(field, str) else field)

        return [dict(zip(fields, row))]


def fetch_none(
    engine: str,
    filepath: str,
    query: str | list,
    parameters: dict | list | None = None,
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


@contextmanager
def _get_cursor(engine: str, filepath: str) -> Generator:
    """Provides a context manager for establishing and closing a database connection."""

    if "SQLite" == engine:
        connection: SQL[engine].Connection = SQL[engine].connect(filepath)
    else:
        config: dict = file_manager.load_config()["engines"][engine]
        filename: str = formatters.decompose_file(filepath)[0]

        connection: SQL[engine].Connection = SQL[engine].connect(
            server=config["db_server"],
            user=config["db_user"],
            password=config["db_password"],
            database=filename,
            autocommit=True,
            tds_version="7.0",
        )

    cursor: SQL[engine].Cursor = connection.cursor()

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
