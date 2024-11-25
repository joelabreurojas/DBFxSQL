"""Database management for the user table"""

from . import sql_connection
from dbfxsql.exceptions.table_errors import TableAlreadyExists, TableNotFound


def create(filepath: str, table: str, fields: str) -> None:
    if table_exists(filepath, table):
        raise TableAlreadyExists(table)

    query: str = f"CREATE TABLE IF NOT EXISTS {table} ({fields})"
    sql_connection.fetch_none(filepath, query)


def insert(filepath: str, table: str, row: dict, fields: tuple[str, str]) -> None:
    if not table_exists(filepath, table):
        raise TableNotFound(table)

    field_names, values = fields

    query: str = f"INSERT INTO {table} ({field_names}) VALUES ({values})"
    parameters: dict = {**row}

    sql_connection.fetch_none(filepath, query, parameters)


def read(filepath: str, table: str, condition: tuple | None = None) -> list[dict]:
    if not table_exists(filepath, table):
        raise TableNotFound(table)

    query: str = f"SELECT * FROM {table}"

    if condition:
        query += f" WHERE {"".join(condition)}"

        field_name, operator, *_ = condition
        primary_key: str = fetch_primary_key(filepath, table)

        if "row_number" == field_name:
            query = f"""
            WITH numbered_rows AS (
                SELECT rowid, ROW_NUMBER() OVER (ORDER BY rowid) AS row_number 
                FROM {table}
            )
            SELECT * FROM {table}
            WHERE rowid IN (SELECT rowid FROM numbered_rows WHERE {"".join(condition)})
            """

        if operator == "=" and field_name in [primary_key, "row_number"]:
            return sql_connection.fetch_one(filepath, query)

    return sql_connection.fetch_all(filepath, query)


def update(filepath: str, table: str, row: dict, fields: str, condition: tuple) -> None:
    if not table_exists(filepath, table):
        raise TableNotFound(table)

    query: str = f"UPDATE {table} SET {fields} WHERE {"".join(condition)}"
    parameters: dict = {**row}

    field_name, *_ = condition

    if "row_number" == field_name:
        query = f"""
        WITH numbered_rows AS (
            SELECT rowid, ROW_NUMBER() OVER (ORDER BY rowid) AS row_number 
            FROM {table}
        )
        UPDATE {table}
        SET {fields}
        WHERE rowid IN (SELECT rowid FROM numbered_rows WHERE {"".join(condition)})
        """

    sql_connection.fetch_none(filepath, query, parameters)


def delete(filepath: str, table: str, condition: tuple) -> None:
    if not table_exists(filepath, table):
        raise TableNotFound(table)

    query: str = f"DELETE FROM {table} WHERE {"".join(condition)}"

    field_name, *_ = condition

    if "row_number" == field_name:
        query = f"""
        WITH numbered_rows AS (
            SELECT rowid, ROW_NUMBER() OVER (ORDER BY rowid) AS row_number 
            FROM {table}
        )
        DELETE FROM {table}
        WHERE rowid IN (SELECT rowid FROM numbered_rows WHERE {"".join(condition)})
        """

    sql_connection.fetch_none(filepath, query)


def drop(filepath: str, table: str) -> None:
    if not table_exists(filepath, table):
        raise TableNotFound(table)

    query: str = f"DROP TABLE IF EXISTS {table}"
    sql_connection.fetch_none(filepath, query)


def fetch_types(filepath: str, table: str) -> dict[str, str]:
    query: str = f"SELECT name, type FROM pragma_table_info('{table}')"

    return sql_connection.fetch_all(filepath, query)


def fetch_primary_key(filepath: str, table: str) -> str:
    query: str = f"SELECT name FROM pragma_table_info('{table}') WHERE pk = 1"

    primary_key: list | None = sql_connection.fetch_one(filepath, query)

    return "" if not primary_key else primary_key[0]["name"]


def fetch_row(filepath: str, table: str, condition: tuple) -> dict:
    if not table_exists(filepath, table):
        raise TableNotFound(table)

    query: str = f"SELECT COUNT(1) FROM {table} WHERE {"".join(condition)}"
    field_name, *_ = condition

    if "row_number" == field_name:
        query = f"""
        WITH numbered_rows AS (
            SELECT rowid, ROW_NUMBER() OVER (ORDER BY rowid) AS row_number
            FROM {table}
        )
        SELECT COUNT(1) FROM {table}
        WHERE rowid IN (SELECT rowid FROM numbered_rows WHERE {"".join(condition)})
        """

    return sql_connection.fetch_one(filepath, query)[0]["COUNT(1)"]


def table_exists(filepath: str, table: str) -> bool:
    query = f"SELECT COUNT(1) FROM sqlite_master WHERE type='table' AND name='{table}'"

    return bool(sql_connection.fetch_one(filepath, query)[0]["COUNT(1)"])
