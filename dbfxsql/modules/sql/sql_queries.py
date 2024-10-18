"""Database management for the user table"""

from . import sql_connection
from dbfxsql.exceptions.table_errors import TableAlreadyExists, TableNotFound


def create(sourcepath: str, table: str, fields: str) -> None:
    if table_exists(sourcepath, table):
        raise TableAlreadyExists(table)

    query: str = f"CREATE TABLE IF NOT EXISTS {table} ({fields})"
    sql_connection.fetch_none(sourcepath, query)


def drop(sourcepath: str, table: str) -> None:
    if not table_exists(sourcepath, table):
        raise TableNotFound(table)

    query: str = f"DROP TABLE IF EXISTS {table}"
    sql_connection.fetch_none(sourcepath, query)


def insert(sourcepath: str, table: str, record: dict, fields: tuple[str, str]) -> None:
    if not table_exists(sourcepath, table):
        raise TableNotFound(table)

    field_names, values = fields

    query: str = f"INSERT INTO {table} ({field_names}) VALUES ({values})"
    parameters: dict = {**record}

    sql_connection.fetch_none(sourcepath, query, parameters)


def read(sourcepath: str, table: str, condition: tuple | None) -> list[dict]:
    if not table_exists(sourcepath, table):
        raise TableNotFound(table)

    query: str = f"SELECT * FROM {table}"

    if condition:
        query += f" WHERE {"".join(condition)}"
        field: str = condition[0]

        if "id" == field.lower():
            return sql_connection.fetch_one(sourcepath, query)

    return sql_connection.fetch_all(sourcepath, query)


def update(
    sourcepath: str, table: str, record: dict, fields: str, condition: tuple
) -> None:
    if not table_exists(sourcepath, table):
        raise TableNotFound(table)

    query: str = f"UPDATE {table} SET {fields} WHERE {"".join(condition)}"
    parameters: dict = {**record}

    sql_connection.fetch_none(sourcepath, query, parameters)


def delete(sourcepath: str, table: str, condition: tuple) -> None:
    if not table_exists(sourcepath, table):
        raise TableNotFound(table)

    query: str = f"DELETE FROM {table} WHERE {"".join(condition)}"

    sql_connection.fetch_none(sourcepath, query)


def fetch_types(sourcepath: str, table: str) -> dict[str, str]:
    query: str = f"SELECT name, type FROM pragma_table_info('{table}')"

    return sql_connection.fetch_all(sourcepath, query)


def table_exists(sourcepath: str, table: str) -> bool:
    query = f"SELECT COUNT(1) FROM sqlite_master WHERE type='table' AND name='{table}'"

    return bool(sql_connection.fetch_one(sourcepath, query)[0]["COUNT(1)"])
