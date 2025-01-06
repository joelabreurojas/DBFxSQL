from collections.abc import Iterable

from . import sql_queries
from dbfxsql.helpers import file_manager, formatters, validators
from dbfxsql.exceptions.source_errors import SourceNotFound
from dbfxsql.exceptions.row_errors import RowAlreadyExists, RowNotFound
from dbfxsql.exceptions.field_errors import FieldReserved
from dbfxsql.exceptions.table_errors import TableAlreadyExists, TableNotFound


def create_database(engine: str, filename: str) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if "SQLite" != engine:
        filename = formatters.decompose_file(filename)[0]
        sql_queries.create_database(engine, filepath, filename)

    elif not validators.path_exists(filepath):
        file_manager.new_file(filepath)


def create_table(
    engine: str, filename: str, table: str, fields_: Iterable[tuple]
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if sql_queries.table_exists(engine, filepath, table):
        raise TableAlreadyExists(table)

    if row_number := validators.field_name_in(fields_, "row_number"):
        raise FieldReserved(row_number)

    fields: str = formatters.fields_to_str(fields_)

    sql_queries.create_table(engine, filepath, table, fields)


def insert_row(
    engine: str, filename: str, table: str, fields_: Iterable[tuple]
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    if not sql_queries.table_exists(engine, filepath, table):
        raise TableNotFound(table)

    types: dict = sql_queries.fetch_types(engine, filepath, table)
    types = formatters.scourgify_types(types)

    row: dict = formatters.fields_to_dict(fields_)
    row = formatters.assign_types(engine, types, row)

    primary_key: str = sql_queries.fetch_primary_key(engine, filepath, table)

    if primary_key := validators.field_name_in(fields_, primary_key):
        condition: str = f"{primary_key} = {row[primary_key]}"

        if _row_exists(engine, filepath, table, condition):
            raise RowAlreadyExists(row[primary_key])

    start, end = (":", "") if "SQLite" == engine else ("%(", ")s")

    fields: tuple[str, str] = formatters.deglose_fields(row, start, end)

    sql_queries.insert(engine, filepath, table, row, fields)


def bulk_insert_rows(
    engine: str, filename: str, table: str, fields_: list[tuple]
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    rows: list[dict] = [formatters.fields_to_dict(field) for field in fields_]

    start, end = (":", "") if "SQLite" == engine else ("%(", ")s")

    fields: tuple[str, str] = formatters.deglose_fields(rows[0], start, end)

    sql_queries.bulk_insert(engine, filepath, table, rows, fields)


def read_rows(
    engine: str, filename: str, table: str, condition: tuple | None
) -> list[dict]:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    if not sql_queries.table_exists(engine, filepath, table):
        raise TableNotFound(table)

    if not condition:
        return sql_queries.read(engine, filepath, table)

    types: dict = sql_queries.fetch_types(engine, filepath, table)
    types = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types, condition)

    rows: list[dict] = sql_queries.read(engine, filepath, table, condition)

    if not formatters.depurate_empty_rows(rows):
        raise RowNotFound(condition)

    return rows


def update_rows(
    engine: str, filename: str, table: str, fields_: Iterable[tuple], condition: tuple
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    if not sql_queries.table_exists(engine, filepath, table):
        raise TableNotFound(table)

    # assign types to each row's value
    types: dict = sql_queries.fetch_types(engine, filepath, table)
    types = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types, condition)

    row: dict = formatters.fields_to_dict(fields_)
    row = formatters.assign_types(engine, types, row)

    # check if other row have the same pk
    primary_key: str = sql_queries.fetch_primary_key(engine, filepath, table)

    if primary_key := validators.field_name_in(fields_, primary_key):
        condition_: str = f"{primary_key} = {row[primary_key]}"

        if _row_exists(engine, filepath, table, condition_):
            raise RowAlreadyExists(row[primary_key])

    if not _row_exists(engine, filepath, table, condition):
        raise RowNotFound(condition)

    start, end = (":", "") if "SQLite" == engine else ("%(", ")s")

    fields: str = formatters.merge_fields(row, start, end)

    sql_queries.update(engine, filepath, table, row, fields, condition)


def bulk_update_rows(
    engine: str, filename: str, table: str, fields: list[tuple], conditions: list[tuple]
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    types: dict = sql_queries.fetch_types(engine, filepath, table)
    types = formatters.scourgify_types(types)

    conditions = [
        formatters.quote_values(engine, types, condition) for condition in conditions
    ]

    rows: list[dict] = [formatters.fields_to_dict(field) for field in fields]

    start, end = (":", "") if "SQLite" == engine else ("%(", ")s")

    fields: list[tuple] = [formatters.merge_fields(row, start, end) for row in rows]

    sql_queries.bulk_update(engine, filepath, table, rows, fields, conditions)


def delete_rows(engine: str, filename: str, table: str, condition: tuple) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    types: dict = sql_queries.fetch_types(engine, filepath, table)
    types = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types, condition)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    if not sql_queries.table_exists(engine, filepath, table):
        raise TableNotFound(table)

    if not _row_exists(engine, filepath, table, condition):
        raise RowNotFound(condition)

    types: dict = sql_queries.fetch_types(engine, filepath, table)
    types = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types, condition)

    sql_queries.delete(engine, filepath, table, condition)


def bulk_delete_rows(
    engine: str, filename: str, table: str, conditions: list[tuple]
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    types: dict = sql_queries.fetch_types(engine, filepath, table)
    types = formatters.scourgify_types(types)

    conditions = [
        formatters.quote_values(engine, types, condition) for condition in conditions
    ]

    sql_queries.bulk_delete(engine, filepath, table, conditions)


def drop_table(engine: str, filename: str, table: str) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    if not sql_queries.table_exists(engine, filepath, table):
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


def _row_exists(engine: str, filepath: str, table: str, condition: tuple) -> list:
    return sql_queries.fetch_row(engine, filepath, table, condition)
