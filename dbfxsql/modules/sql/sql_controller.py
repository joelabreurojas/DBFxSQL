from collections.abc import Iterable

from . import sql_queries
from dbfxsql.helpers import file_manager, formatters, validators
from dbfxsql.exceptions.source_errors import SourceNotFound
from dbfxsql.exceptions.row_errors import RowAlreadyExists, RowNotFound
from dbfxsql.exceptions.field_errors import FieldReserved


def create_table(engine: str, source: str, table: str, fields: Iterable[tuple]) -> None:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if validators.path_exists(sourcepath):
        file_manager.new_file(sourcepath)

    if row_number := validators.field_name_in(fields, "row_number"):
        raise FieldReserved(row_number)

    _fields: str = formatters.fields_to_str(fields)

    sql_queries.create(sourcepath, table, _fields)


def insert_row(engine: str, source: str, table: str, fields: Iterable[tuple]) -> None:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if not validators.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    types: dict = sql_queries.fetch_types(sourcepath, table)
    types = formatters.scourgify_types(types)

    row: dict = formatters.fields_to_dict(fields)
    row = formatters.assign_types(engine, types, row)

    primary_key: str = sql_queries.fetch_primary_key(sourcepath, table)

    if primary_key := validators.field_name_in(fields, primary_key):
        condition: str = f"{primary_key} = {row[primary_key]}"

        if _row_exists(sourcepath, table, condition):
            raise RowAlreadyExists(row[primary_key])

    _fields: tuple[str, str] = formatters.deglose_fields(row)

    sql_queries.insert(sourcepath, table, row, _fields)


def read_rows(
    engine: str, source: str, table: str, condition: tuple | None
) -> list[dict]:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if not validators.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    if not condition:
        return sql_queries.read(sourcepath, table)

    types: dict = sql_queries.fetch_types(sourcepath, table)
    types = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types, condition)

    rows: list[dict] = sql_queries.read(sourcepath, table, condition)

    if not formatters.depurate_empty_rows(rows):
        raise RowNotFound(condition)

    return rows


def update_rows(
    engine: str, source: str, table: str, fields: Iterable[tuple], condition: tuple
) -> None:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if not validators.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    # assign types to each row's value
    types: dict = sql_queries.fetch_types(sourcepath, table)
    types = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types, condition)

    row: dict = formatters.fields_to_dict(fields)
    row = formatters.assign_types(engine, types, row)

    # check if other row have the same pk
    primary_key: str = sql_queries.fetch_primary_key(sourcepath, table)

    if primary_key := validators.field_name_in(fields, primary_key):
        _condition: str = f"{primary_key} = {row[primary_key]}"

        if _row_exists(sourcepath, table, _condition):
            raise RowAlreadyExists(row[primary_key])

    if not _row_exists(sourcepath, table, condition):
        raise RowNotFound(condition)

    _fields: str = formatters.merge_fields(row)

    sql_queries.update(sourcepath, table, row, _fields, condition)


def delete_rows(engine: str, source: str, table: str, condition: tuple) -> None:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if not validators.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    if not _row_exists(sourcepath, table, condition):
        raise RowNotFound(condition)

    types: dict = sql_queries.fetch_types(sourcepath, table)
    types = formatters.scourgify_types(types)

    condition = formatters.quote_values(engine, types, condition)

    sql_queries.delete(sourcepath, table, condition)


def drop_table(engine: str, source: str, table: str) -> None:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if not validators.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    sql_queries.drop(sourcepath, table)


def drop_database(engine: str, source: str) -> None:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if not validators.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    file_manager.remove_file(sourcepath)


def _row_exists(sourcepath: str, table: str, condition: tuple) -> list:
    return sql_queries.fetch_row(sourcepath, table, condition)
