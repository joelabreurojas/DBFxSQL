from collections.abc import Iterable

from . import sql_queries
from dbfxsql.helpers import file_manager, formatters, validators
from dbfxsql.exceptions.source_errors import SourceNotFound
from dbfxsql.exceptions.row_errors import RowAlreadyExists, RowNotFound
from dbfxsql.exceptions.field_errors import FieldReserved


def create_table(
    engine: str, filename: str, table: str, fields: Iterable[tuple]
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if validators.path_exists(filepath):
        file_manager.new_file(filepath)

    if row_number := validators.field_name_in(fields, "row_number"):
        raise FieldReserved(row_number)

    _fields: str = formatters.fields_to_str(fields)

    sql_queries.create(filepath, table, _fields)


def insert_row(engine: str, filename: str, table: str, fields: Iterable[tuple]) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    types: dict = sql_queries.fetch_types(filepath, table)
    types = formatters.scourgify_types(types)

    row: dict = formatters.fields_to_dict(fields)
    row = formatters.assign_types(engine, types, row)

    primary_key: str = sql_queries.fetch_primary_key(filepath, table)

    if primary_key := validators.field_name_in(fields, primary_key):
        condition: str = f"{primary_key} = {row[primary_key]}"

        if _row_exists(filepath, table, condition):
            raise RowAlreadyExists(row[primary_key])

    _fields: tuple[str, str] = formatters.deglose_fields(row)

    sql_queries.insert(filepath, table, row, _fields)


def read_rows(
    engine: str, filename: str, table: str, condition: tuple | None
) -> list[dict]:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    if not condition:
        return sql_queries.read(filepath, table)

    types: dict = sql_queries.fetch_types(filepath, table)
    types = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types, condition)

    rows: list[dict] = sql_queries.read(filepath, table, condition)

    if not formatters.depurate_empty_rows(rows):
        raise RowNotFound(condition)

    return rows


def update_rows(
    engine: str, filename: str, table: str, fields: Iterable[tuple], condition: tuple
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    # assign types to each row's value
    types: dict = sql_queries.fetch_types(filepath, table)
    types = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types, condition)

    row: dict = formatters.fields_to_dict(fields)
    row = formatters.assign_types(engine, types, row)

    # check if other row have the same pk
    primary_key: str = sql_queries.fetch_primary_key(filepath, table)

    if primary_key := validators.field_name_in(fields, primary_key):
        _condition: str = f"{primary_key} = {row[primary_key]}"

        if _row_exists(filepath, table, _condition):
            raise RowAlreadyExists(row[primary_key])

    if not _row_exists(filepath, table, condition):
        raise RowNotFound(condition)

    _fields: str = formatters.merge_fields(row)

    sql_queries.update(filepath, table, row, _fields, condition)


def delete_rows(engine: str, filename: str, table: str, condition: tuple) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    if not _row_exists(filepath, table, condition):
        raise RowNotFound(condition)

    types: dict = sql_queries.fetch_types(filepath, table)
    types = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types, condition)

    sql_queries.delete(filepath, table, condition)


def drop_table(engine: str, filename: str, table: str) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    sql_queries.drop(filepath, table)


def drop_database(engine: str, filename: str) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    file_manager.remove_file(filepath)


def _row_exists(filepath: str, table: str, condition: tuple) -> list:
    return sql_queries.fetch_row(filepath, table, condition)
