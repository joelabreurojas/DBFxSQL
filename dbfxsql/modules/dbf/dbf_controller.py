from collections.abc import Iterable

from . import dbf_queries
from dbfxsql.helpers import file_manager, formatters, validators
from dbfxsql.exceptions.source_errors import SourceAlreadyExists, SourceNotFound
from dbfxsql.exceptions.field_errors import FieldReserved
from dbfxsql.exceptions.row_errors import RowNotFound


def create_table(engine: str, source: str, fields: Iterable[tuple]) -> None:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if validators.path_exists(sourcepath):
        raise SourceAlreadyExists(source)

    if row_number := validators.field_name_in(fields, "row_number"):
        raise FieldReserved(row_number)

    _fields: str = formatters.fields_to_str(fields, sep="; ")

    file_manager.new_file(sourcepath)
    dbf_queries.create(sourcepath, _fields)


def insert_row(engine: str, source: str, fields: Iterable[tuple]) -> None:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if not validators.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    types: dict = dbf_queries.fetch_types(sourcepath)
    row: dict = formatters.fields_to_dict(fields)

    row = formatters.assign_types(engine, types, row)

    dbf_queries.insert(sourcepath, row)


def read_rows(engine: str, source: str, condition: tuple | None) -> list[dict]:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if not validators.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    rows: list[dict] = dbf_queries.read(sourcepath)
    rows = formatters.scourgify_rows(rows)

    if condition:
        rows, _ = formatters.filter_rows(rows, condition)

    if not rows:
        raise RowNotFound(condition)

    return rows


def update_rows(
    engine: str, source: str, fields: Iterable[tuple], condition: tuple
) -> None:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if not validators.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    # assign types to each row's value
    types: dict = dbf_queries.fetch_types(sourcepath)
    row: dict = formatters.fields_to_dict(fields)

    row = formatters.assign_types(engine, types, row)

    # get a sanitized list of rows
    rows: list[dict] = dbf_queries.read(sourcepath)
    rows = formatters.scourgify_rows(rows)

    # manual filter of rows by condition
    rows, indexes = formatters.filter_rows(rows, condition)

    if not rows:
        raise RowNotFound(condition)

    # update filtered rows by their index
    if validators.values_are_different(rows, row):
        dbf_queries.update(sourcepath, row, indexes)


def delete_rows(engine: str, source: str, condition: tuple) -> None:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if not validators.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    rows: list[dict] = dbf_queries.read(sourcepath)
    rows = formatters.scourgify_rows(rows)

    rows, indexes = formatters.filter_rows(rows, condition)

    if not rows:
        raise RowNotFound(condition)

    dbf_queries.delete(sourcepath, indexes)


def drop_table(engine: str, source: str) -> None:
    sourcepath: str = formatters.add_folderpath(engine, source)

    if not validators.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    file_manager.remove_file(sourcepath)
