"""Database management for the user table"""

from . import sql_connection
from dbfxsql.helpers import file_manager
from dbfxsql.exceptions.source_errors import SourceNotFound


def create_database(engine: str, filepath: str, filename: str) -> None:
    if not _database_exists(engine, filename):
        query: str = file_manager.load_query(engine, command="databases/create")
        query = query.format(database=filename)

        sql_connection.fetch_none(engine, "master", query)


def create_table(engine: str, filepath: str, table: str, fields: str) -> None:
    query: str = file_manager.load_query(engine, command="tables/create")
    query = query.format(table=table, fields=fields)

    sql_connection.fetch_none(engine, filepath, query)


def insert(
    engine: str, filepath: str, table: str, row: dict, fields: tuple[str, str]
) -> None:
    field_names, values = fields

    query: str = file_manager.load_query(engine, command="rows/insert")
    query = query.format(table=table, field_names=field_names, values=values)

    parameters: dict = {**row}

    sql_connection.fetch_none(engine, filepath, query, parameters)


def read(
    engine: str, filepath: str, table: str, condition_: tuple | None = None
) -> list[dict]:
    command: str = "rows/read"

    if not condition_:
        query: str = file_manager.load_query(engine, command)
        query = query.format(table=table)

        return sql_connection.fetch_all(engine, filepath, query)

    field_name, operator, *_ = condition_
    command += "_by_condition" if "row_number" != field_name else "_by_row_number"

    condition: str = "".join(condition_)
    primary_key: str = fetch_primary_key(engine, filepath, table)

    query: str = file_manager.load_query(engine, command)
    query = query.format(table=table, condition=condition, primary_key=primary_key)

    if operator == "=" and field_name in ["row_number", primary_key]:
        return sql_connection.fetch_one(engine, filepath, query)

    return sql_connection.fetch_all(engine, filepath, query)


def update(
    engine: str, filepath: str, table: str, row: dict, fields: str, condition: tuple
) -> None:
    field_name, *_ = condition

    command: str = "rows/update"

    if "row_number" == field_name:
        command += "_by_row_number"

    query: str = file_manager.load_query(engine, command)
    data: dict = {"table": table, "fields": fields, "condition": "".join(condition)}

    if "SQLite" != engine:
        data["primary_key"] = fetch_primary_key(engine, filepath, table)

    query = query.format(**data)

    parameters: dict = {**row}

    sql_connection.fetch_none(engine, filepath, query, parameters)


def delete(engine: str, filepath: str, table: str, condition: tuple) -> None:
    field_name, *_ = condition

    command: str = "rows/delete"

    if "row_number" == field_name:
        command += "_by_row_number"

    query: str = file_manager.load_query(engine, command)
    data: dict = {"table": table, "condition": "".join(condition)}

    if "SQLite" != engine:
        data["primary_key"] = fetch_primary_key(engine, filepath, table)

    query = query.format(**data)

    sql_connection.fetch_none(engine, filepath, query)


def bulk_insert(
    engine: str, filepath: str, table: str, rows: list, fields: tuple[str, str]
) -> None:
    field_name, values = fields

    query: str = file_manager.load_query(engine, command="rows/insert")
    query = query.format(table=table, field_names=field_name, values=values)

    parameters: list[dict] = rows

    sql_connection.fetch_none(engine, filepath, query, parameters, execute_many=True)


def bulk_update(
    engine: str,
    filepath: str,
    table: str,
    rows: list[dict],
    fields: list[tuple],
    conditions: list[tuple],
) -> None:
    queries: list = []

    text: str = file_manager.load_query(engine, command="rows/update_by_row_number")
    data: dict = {"table": table}

    if "SQLite" != engine:
        data["primary_key"] = fetch_primary_key(engine, filepath, table)

    for field, condition in zip(fields, conditions):
        data["fields"] = field
        data["condition"] = "".join(condition)
        query: str = text.format(**data)

        queries.append(query)

    parameters: list[dict] = rows

    sql_connection.fetch_none(engine, filepath, queries, parameters)


def bulk_delete(
    engine: str,
    filepath: str,
    table: str,
    conditions: list[tuple],
) -> None:
    queries: list = []

    text: str = file_manager.load_query(engine, command="rows/delete_by_row_number")
    data: dict = {"table": table}

    if "SQLite" != engine:
        data["primary_key"] = fetch_primary_key(engine, filepath, table)

    for condition in conditions:
        data["condition"] = "".join(condition)
        query: str = text.format(**data)

        queries.append(query)

    sql_connection.fetch_none(engine, filepath, queries)


def drop_database(engine: str, filepath: str, filename: str) -> None:
    if not _database_exists(engine, filename):
        raise SourceNotFound(filepath)

    query: str = file_manager.load_query(engine, command="databases/drop")
    query = query.format(database=filename)

    sql_connection.fetch_none(engine, "master", query)


def fetch_types(engine: str, filepath: str, table: str) -> dict[str, str]:
    query: str = file_manager.load_query(engine, command="tables/fetch_types")
    query = query.format(table=table)

    return sql_connection.fetch_all(engine, filepath, query)


def fetch_primary_key(engine: str, filepath: str, table: str) -> str:
    query: str = file_manager.load_query(engine, command="tables/fetch_primary_key")
    query = query.format(table=table)

    primary_key: list | None = sql_connection.fetch_one(engine, filepath, query)

    return "" if not primary_key else primary_key[0]["name"]


def fetch_row(engine: str, filepath: str, table: str, condition: tuple) -> dict:
    field_name, *_ = condition

    command: str = "rows/fetch"

    if "row_number" == field_name:
        command += "_by_row_number"

    query: str = file_manager.load_query(engine, command)
    data: dict = {"table": table, "condition": "".join(condition)}

    if "SQLite" != engine:
        data["primary_key"] = fetch_primary_key(engine, filepath, table)

    query = query.format(**data)

    return sql_connection.fetch_one(engine, filepath, query)[0]["COUNT(1)"]


def deploy_procedures(engine, filepath):
    procedures: list[str] = file_manager.list_files(engine, folder="procedures")

    for procedure in procedures:
        if not _procedure_exists(engine, filepath, procedure):
            query = file_manager.load_query(engine, command=f"procedures/{procedure}")

            sql_connection.fetch_none(engine, filepath, query)


def deploy_triggers(engine, filepath, database, table):
    triggers: list[str] = file_manager.list_files(engine, folder="triggers")

    for trigger in triggers:
        if not _trigger_exists(engine, filepath, trigger):
            query = file_manager.load_query(engine, command=f"triggers/{trigger}")
            query = query.format(database=database, table=table)

            sql_connection.fetch_none(engine, filepath, query)


def table_exists(engine: str, filepath: str, table: str) -> bool:
    query: str = file_manager.load_query(engine, command="tables/exists")
    query = query.format(table=table)

    return bool(sql_connection.fetch_one(engine, filepath, query)[0]["COUNT(1)"])


def _database_exists(engine: str, filename: str) -> bool:
    query: str = file_manager.load_query(engine, command="databases/exists")
    query = query.format(database=filename)

    return bool(sql_connection.fetch_one(engine, "master", query)[0]["COUNT(1)"])


def _procedure_exists(engine: str, filepath: str, procedure: str) -> bool:
    query: str = file_manager.load_query(engine, command="procedures/exists")
    query = query.format(procedure=procedure)

    return bool(sql_connection.fetch_one(engine, filepath, query)[0]["COUNT(1)"])


def _trigger_exists(engine: str, filepath: str, trigger: str) -> bool:
    query: str = file_manager.load_query(engine, command="triggers/exists")
    query = query.format(trigger=trigger)

    return bool(sql_connection.fetch_one(engine, filepath, query)[0]["COUNT(1)"])
