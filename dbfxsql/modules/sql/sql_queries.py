"""Database management for the user table"""

from dbfxsql.exceptions import SourceNotFound
from dbfxsql.helpers import file_manager
from dbfxsql.helpers.alias import TypesList
from dbfxsql.models import Condition

from . import sql_connection


def create_database(engine: str, filepath: str, database: str) -> None:
    if not statement_exists(engine, filepath, database, statement="databases"):
        query: str = file_manager.load_query(engine, command="databases/create")
        query = query.format(database=database)

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
    engine: str, filepath: str, table: str, condition: Condition | None = None
) -> list[dict]:
    command: str = "rows/read"

    if not condition:
        query: str = file_manager.load_query(engine, command)
        query = query.format(table=table)

        return sql_connection.fetch_all(engine, filepath, query)

    command += "_by_condition" if "row_number" != condition.field else "_by_row_number"

    primary_key: str = fetch_primary_key(engine, filepath, table)

    query = file_manager.load_query(engine, command)
    query = query.format(table=table, condition=str(condition), primary_key=primary_key)

    if condition.operator == "=" and condition.field in ["row_number", primary_key]:
        return sql_connection.fetch_one(engine, filepath, query)

    return sql_connection.fetch_all(engine, filepath, query)


def bulk_insert(
    engine: str, filepath: str, table: str, rows: list, fields: tuple[str, str]
) -> None:
    field_name, values = fields

    query: str = file_manager.load_query(engine, command="rows/insert")
    query = query.format(table=table, field_names=field_name, values=values)

    parameters: list[dict] = rows

    sql_connection.fetch_none(engine, filepath, query, parameters, execute_many=True)


def update(
    engine: str, filepath: str, table: str, row: dict, fields: str, condition: Condition
) -> None:
    command: str = "rows/update"

    if "row_number" == condition.field:
        command += "_by_row_number"

    query: str = file_manager.load_query(engine, command)
    data: dict = {"table": table, "fields": fields, "condition": str(condition)}

    if "SQLite" != engine:
        data["primary_key"] = fetch_primary_key(engine, filepath, table)

    query = query.format(**data)

    parameters: dict = {**row}

    sql_connection.fetch_none(engine, filepath, query, parameters)


def bulk_update(
    engine: str,
    filepath: str,
    table: str,
    rows: list[dict],
    fields_: list[str],
    conditions: list[Condition],
) -> None:
    queries: list = []

    text: str = file_manager.load_query(engine, command="rows/update_by_row_number")
    data: dict = {"table": table}

    if "SQLite" != engine:
        data["primary_key"] = fetch_primary_key(engine, filepath, table)

    for fields, condition in zip(fields_, conditions):
        data["fields"] = fields
        data["condition"] = str(condition)
        query: str = text.format(**data)

        queries.append(query)

    parameters: list[dict] = rows

    sql_connection.fetch_none(engine, filepath, queries, parameters)


def delete(engine: str, filepath: str, table: str, condition: Condition) -> None:
    command: str = "rows/delete"

    if "row_number" == condition.field:
        command += "_by_row_number"

    query: str = file_manager.load_query(engine, command)
    data: dict = {"table": table, "condition": str(condition)}

    if "SQLite" != engine:
        data["primary_key"] = fetch_primary_key(engine, filepath, table)

    query = query.format(**data)

    sql_connection.fetch_none(engine, filepath, query)


def bulk_delete(
    engine: str,
    filepath: str,
    table: str,
    conditions: list[Condition],
) -> None:
    queries: list = []

    text: str = file_manager.load_query(engine, command="rows/delete_by_row_number")
    data: dict = {"table": table}

    if "SQLite" != engine:
        data["primary_key"] = fetch_primary_key(engine, filepath, table)

    for condition in conditions:
        data["condition"] = str(condition)
        query: str = text.format(**data)

        queries.append(query)

    sql_connection.fetch_none(engine, filepath, queries)


def drop_table(engine: str, filepath: str, table: str) -> None:
    query: str = file_manager.load_query(engine, command="table/drop")
    query = query.format(table=table)

    sql_connection.fetch_none(engine, filepath, query)


def drop_database(engine: str, filepath: str, database: str) -> None:
    if not statement_exists(engine, filepath, database, statement="databases"):
        raise SourceNotFound(filepath)

    query: str = file_manager.load_query(engine, command="databases/drop")
    query = query.format(database=database)

    sql_connection.fetch_none(engine, "master", query)


def deploy_procedures(engine: str, filepath: str) -> None:
    procedures: list[str] = file_manager.list_files(engine, folder="procedures")

    for procedure in procedures:
        if not statement_exists(engine, filepath, procedure, statement="procedures"):
            query = file_manager.load_query(engine, command=f"procedures/{procedure}")

            sql_connection.fetch_none(engine, filepath, query)


def deploy_triggers(engine: str, filepath: str, database: str, table: str) -> None:
    triggers: list[str] = file_manager.list_files(engine, folder="triggers")

    for trigger in triggers:
        trigger_: str = f"{table}_{trigger.split('_')[1].upper()}"

        if not statement_exists(engine, filepath, trigger_, statement="triggers"):
            query: str = file_manager.load_query(engine, command=f"triggers/{trigger}")
            query = query.format(table=table, filepath=filepath, data=trigger)

            sql_connection.fetch_none(engine, filepath, query)


def fetch_primary_key(engine: str, filepath: str, table: str) -> str:
    query: str = file_manager.load_query(engine, command="tables/fetch_primary_key")
    query = query.format(table=table)

    primary_key: list[dict] = sql_connection.fetch_one(engine, filepath, query)

    return "" if not primary_key else primary_key[0]["name"]


def fetch_row(engine: str, filepath: str, table: str, condition: Condition) -> dict:
    command: str = "rows/fetch"

    if "row_number" == condition.field:
        command += "_by_row_number"

    query: str = file_manager.load_query(engine, command)
    data: dict = {"table": table, "condition": str(condition)}

    if "SQLite" != engine:
        data["primary_key"] = fetch_primary_key(engine, filepath, table)

    query = query.format(**data)

    row: list[dict] = sql_connection.fetch_one(engine, filepath, query)

    return row[0]["COUNT(1)"]


def fetch_types(engine: str, filepath: str, table: str) -> TypesList:
    query: str = file_manager.load_query(engine, command="tables/fetch_types")
    query = query.format(table=table)

    return sql_connection.fetch_all(engine, filepath, query)


def statement_exists(engine: str, filepath: str, value: str, statement: str) -> bool:
    query: str = file_manager.load_query(engine, command=f"{statement}/exists")
    query = query.format(value=value)

    return bool(sql_connection.fetch_one(engine, filepath, query)[0]["COUNT(1)"])
