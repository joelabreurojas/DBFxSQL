from dbfxsql.exceptions import (
    FieldReserved,
    RowAlreadyExists,
    RowNotFound,
    SourceNotFound,
    TableAlreadyExists,
    TableNotFound,
)
from dbfxsql.helpers import file_manager, formatters, validators
from dbfxsql.helpers.alias import FieldsIterable, TypesList
from dbfxsql.models.condition import Condition

from . import sql_queries


def create_database(engine: str, filename: str) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if "SQLite" != engine:
        filename = formatters.decompose_file(filename)[0]
        sql_queries.create_database(engine, filepath, filename)

    elif not validators.path_exists(filepath):
        file_manager.new_file(filepath)


def create_table(
    engine: str, filename: str, table: str, fields_: FieldsIterable
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if sql_queries.statement_exists(engine, filepath, table, statement="tables"):
        raise TableAlreadyExists(table)

    if row_number := validators.field_name_in(fields_, "row_number"):
        raise FieldReserved(row_number)

    fields: str = formatters.fields_to_str(fields_)

    sql_queries.create_table(engine, filepath, table, fields)


def insert_row(engine: str, filename: str, table: str, fields_: FieldsIterable) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    if not sql_queries.statement_exists(engine, filepath, table, statement="tables"):
        raise TableNotFound(table)

    types: TypesList = sql_queries.fetch_types(engine, filepath, table)
    types_map: dict[str, str] = formatters.scourgify_types(types)

    row: dict = formatters.fields_to_dict(fields_)
    row = formatters.empty_str_to_none(row)
    row = formatters.assign_types(engine, types_map, row)

    primary_key_: str = sql_queries.fetch_primary_key(engine, filepath, table)

    if primary_key := validators.field_name_in(fields_, primary_key_):
        condition: Condition = Condition(primary_key, "=", row[primary_key])

        if _row_exists(engine, filepath, table, condition):
            raise RowAlreadyExists(row[primary_key])

    start, end = (":", "") if "SQLite" == engine else ("%(", ")s")

    fields: tuple[str, str] = formatters.deglose_fields(row, start, end)

    sql_queries.insert(engine, filepath, table, row, fields)


def bulk_insert_rows(
    engine: str, filename: str, table: str, fields_: list[FieldsIterable]
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    rows: list[dict] = [formatters.fields_to_dict(fields) for fields in fields_]

    start, end = (":", "") if "SQLite" == engine else ("%(", ")s")

    fields: tuple[str, str] = formatters.deglose_fields(rows[0], start, end)

    sql_queries.bulk_insert(engine, filepath, table, rows, fields)


def read_rows(
    engine: str, filename: str, table: str, condition: Condition | None
) -> list[dict]:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    if not sql_queries.statement_exists(engine, filepath, table, statement="tables"):
        raise TableNotFound(table)

    if not condition:
        return sql_queries.read(engine, filepath, table)

    types: TypesList = sql_queries.fetch_types(engine, filepath, table)
    types_map: dict[str, str] = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types_map, condition)

    rows: list[dict] = sql_queries.read(engine, filepath, table, condition)
    rows = [formatters.empty_str_to_none(row) for row in rows]

    if not formatters.depurate_empty_rows(rows):
        raise RowNotFound(str(condition))

    return [formatters.assign_types(engine, types_map, row) for row in rows]


def update_rows(
    engine: str,
    filename: str,
    table: str,
    fields_: FieldsIterable,
    condition: Condition,
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    if not sql_queries.statement_exists(engine, filepath, table, statement="tables"):
        raise TableNotFound(table)

    # assign types to each row's value
    types: TypesList = sql_queries.fetch_types(engine, filepath, table)
    types_map: dict[str, str] = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types_map, condition)

    row: dict = formatters.fields_to_dict(fields_)
    row = formatters.empty_str_to_none(row)
    row = formatters.assign_types(engine, types_map, row)

    # check if other row have the same pk
    primary_key_: str = sql_queries.fetch_primary_key(engine, filepath, table)

    if primary_key := validators.field_name_in(fields_, primary_key_):
        condition_: Condition = Condition(primary_key, "=", row[primary_key])

        if _row_exists(engine, filepath, table, condition_):
            raise RowAlreadyExists(row[primary_key])

    if not _row_exists(engine, filepath, table, condition):
        raise RowNotFound(str(condition))

    start, end = (":", "") if "SQLite" == engine else ("%(", ")s")

    fields: str = formatters.merge_fields(row, start, end)

    sql_queries.update(engine, filepath, table, row, fields, condition)


def bulk_update_rows(
    engine: str,
    filename: str,
    table: str,
    fields_: list[FieldsIterable],
    conditions: list[Condition],
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    types: TypesList = sql_queries.fetch_types(engine, filepath, table)
    types_map: dict[str, str] = formatters.scourgify_types(types)

    conditions = [
        formatters.quote_values(engine, types_map, condition)
        for condition in conditions
    ]

    rows: list[dict] = [formatters.fields_to_dict(fields) for fields in fields_]

    start, end = (":", "") if "SQLite" == engine else ("%(", ")s")

    fields: list[str] = [formatters.merge_fields(row, start, end) for row in rows]

    sql_queries.bulk_update(engine, filepath, table, rows, fields, conditions)


def delete_rows(engine: str, filename: str, table: str, condition: Condition) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    types: TypesList = sql_queries.fetch_types(engine, filepath, table)
    types_map: dict[str, str] = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types_map, condition)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    if not sql_queries.statement_exists(engine, filepath, table, statement="tables"):
        raise TableNotFound(table)

    if not _row_exists(engine, filepath, table, condition):
        raise RowNotFound(str(condition))

    sql_queries.delete(engine, filepath, table, condition)


def bulk_delete_rows(
    engine: str, filename: str, table: str, conditions: list[Condition]
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    types: TypesList = sql_queries.fetch_types(engine, filepath, table)
    types_map: dict[str, str] = formatters.scourgify_types(types)

    conditions = [
        formatters.quote_values(engine, types_map, condition)
        for condition in conditions
    ]

    sql_queries.bulk_delete(engine, filepath, table, conditions)


def drop_table(engine: str, filename: str, table: str) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    if not sql_queries.statement_exists(engine, filepath, table, statement="tables"):
        raise TableNotFound(table)

    sql_queries.drop_table(engine, filepath, table)


def drop_database(engine: str, filename: str) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if "SQLite" != engine:
        filename = formatters.decompose_file(filename)[0]
        sql_queries.drop_database(engine, filepath, filename)

    elif not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    else:
        file_manager.remove_file(filepath)


def deploy_statements(entities: dict, databases: list[str], engine: str) -> None:
    for database in databases:
        filepath: str = formatters.add_folderpath(engine, database)

        sql_queries.deploy_procedures(engine, filepath)

        for table in entities[database]:
            sql_queries.deploy_triggers(engine, filepath, database, table)


def _row_exists(engine: str, filepath: str, table: str, condition: Condition) -> dict:
    return sql_queries.fetch_row(engine, filepath, table, condition)
