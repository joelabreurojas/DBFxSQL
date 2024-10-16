"""Database management for the user table"""

from . import sql_connection
from dbfxsql.exceptions.table_errors import TableAlreadyExists, TableNotFound


def create(sourcepath: str, table: str, fields: str) -> None:
    if _table_exists(sourcepath, table):
        raise TableAlreadyExists(table)

    query: str = f"CREATE TABLE IF NOT EXISTS {table} ({fields})"
    sql_connection.fetch_none(sourcepath, query)


def drop(sourcepath: str, table: str) -> None:
    if not _table_exists(sourcepath, table):
        raise TableNotFound(table)

    query: str = f"DROP TABLE IF EXISTS {table}"
    sql_connection.fetch_none(sourcepath, query)


def insert(sourcepath: str, table: str, record: dict) -> None:
    if not _table_exists(sourcepath, table):
        raise TableNotFound(table)

    # [key] -> [:key]
    fields: str = ", ".join([f"{key.lower()}" for key in record.keys()])
    _fields: str = ", ".join([f":{key.lower()}" for key in record.keys()])

    query: str = f"INSERT INTO {table} ({fields}) VALUES ({_fields})"
    parameters: dict = {**record}

    sql_connection.fetch_none(sourcepath, query, parameters)


def read(sourcepath: str, table: str, filter: str | None = None) -> list[dict]:
    if not _table_exists(sourcepath, table):
        raise TableNotFound(table)

    query: str = f"SELECT * FROM {table}"

    if filter:
        query += f" WHERE {filter}"

        if "id" == filter.field:
            return sql_connection.fetch_one(sourcepath, query)

    return sql_connection.fetch_all(sourcepath, query)


def update(sourcepath: str, table: str, record: dict, filter: str) -> None:
    if not _table_exists(sourcepath, table):
        raise TableNotFound(table)

    # [key] -> [key = :key]
    fields: str = ", ".join([f"{key} = :{key.lower()}" for key in record.keys()])

    query: str = f"UPDATE {table} SET {fields} WHERE {filter}"
    parameters: dict = {**record}

    sql_connection.fetch_none(sourcepath, query, parameters)


def delete(sourcepath: str, table: str, filter: str) -> None:
    if not _table_exists(sourcepath, table):
        raise TableNotFound(table)

    query: str = f"DELETE FROM {table} WHERE {filter}"

    sql_connection.fetch_none(sourcepath, query)


def fetch_types(sourcepath: str, table: str, fields: str) -> list[dict[str, str]]:
    """Fetches the types of specified fields in a SQL table."""

    fields_list = fields.lower().replace(", ", ",").split(",")

    fields = ", ".join([f"'{field}'" for field in fields_list])

    query: str = (
        f"SELECT name, type FROM pragma_table_info('{table}') WHERE name IN ({fields})"
    )

    records = sql_connection.fetch_all(sourcepath, query)

    fields_types: dict[str, str] = dict(
        zip([types["name"] for types in records], [types["type"] for types in records])
    )

    types: list[str] = []

    for field in fields_list:
        types.append(fields_types[field])  # if KeyError -> Invalid field

    return types


def _table_exists(sourcepath: str, table: str) -> bool:
    query = f"SELECT COUNT(1) FROM sqlite_master WHERE type='table' AND name='{table}'"

    return bool(sql_connection.fetch_one(sourcepath, query)[0]["COUNT(1)"])
