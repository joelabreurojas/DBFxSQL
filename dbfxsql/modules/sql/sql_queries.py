"""Database management for the user table"""

from . import sql_connection
from dbfxsql.helpers.file_manager import load_query


def create(engine: str, filepath: str, table: str, fields: str) -> None:
    query: str = load_query(engine, command="create")
    query = query.format(table=table, fields=fields)

    sql_connection.fetch_none(engine, filepath, query)


def insert(
    engine: str, filepath: str, table: str, row: dict, fields: tuple[str, str]
) -> None:
    field_names, values = fields

    query: str = load_query(engine, command="insert")
    query = query.format(table=table, field_names=field_names, values=values)

    parameters: dict = {**row}

    sql_connection.fetch_none(engine, filepath, query, parameters)


def read(
    engine: str, filepath: str, table: str, condition_: tuple | None = None
) -> list[dict]:
    command: str = "read"

    if not condition_:
        query: str = load_query(engine, command)
        query = query.format(table=table)

        return sql_connection.fetch_all(engine, filepath, query)

    field_name, operator, *_ = condition_
    command += "_by_condition" if "row_number" != field_name else "_by_row_number"

    condition: str = "".join(condition_)
    primary_key: str = fetch_primary_key(engine, filepath, table)

    query: str = load_query(engine, command)
    query = query.format(table=table, condition=condition, primary_key=primary_key)

    if operator == "=" and field_name in ["row_number", primary_key]:
        return sql_connection.fetch_one(engine, filepath, query)

    return sql_connection.fetch_all(engine, filepath, query)


def update(
    engine: str, filepath: str, table: str, row: dict, fields: str, condition: tuple
) -> None:
    field_name, *_ = condition

    command: str = "update" if "row_number" != field_name else "update_by_row_number"

    query: str = load_query(engine, command)
    query = query.format(table=table, fields=fields, condition="".join(condition))

    parameters: dict = {**row}

    sql_connection.fetch_none(engine, filepath, query, parameters)


def delete(engine: str, filepath: str, table: str, condition: tuple) -> None:
    field_name, *_ = condition

    command: str = "delete" if "row_number" != field_name else "delete_by_row_number"

    query: str = load_query(engine, command)
    query = query.format(table=table, condition="".join(condition))

    sql_connection.fetch_none(engine, filepath, query)


def drop(engine: str, filepath: str, table: str) -> None:
    query: str = load_query(engine, command="drop")
    query = query.format(table=table)

    sql_connection.fetch_none(engine, filepath, query)


def fetch_types(engine: str, filepath: str, table: str) -> dict[str, str]:
    query: str = load_query(engine, command="fetch_types")
    query = query.format(table=table)

    return sql_connection.fetch_all(engine, filepath, query)


def fetch_primary_key(engine: str, filepath: str, table: str) -> str:
    query: str = load_query(engine, command="fetch_primary_key")
    query = query.format(table=table)

    primary_key: list | None = sql_connection.fetch_one(engine, filepath, query)

    return "" if not primary_key else primary_key[0]["name"]


def fetch_row(engine: str, filepath: str, table: str, condition: tuple) -> dict:
    field, *_ = condition

    command: str = "fetch_row" if "row_number" != field else "fetch_row_by_row_number"

    query: str = load_query(engine, command)
    query = query.format(table=table, condition="".join(condition))

    return sql_connection.fetch_one(engine, filepath, query)[0]["COUNT(1)"]


def table_exists(engine: str, filepath: str, table: str) -> bool:
    query: str = load_query(engine, command="table_exists")
    query = query.format(table=table)

    return bool(sql_connection.fetch_one(engine, filepath, query)[0]["COUNT(1)"])
