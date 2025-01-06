from collections.abc import Iterable

from . import dbf_queries
from dbfxsql.helpers import file_manager, formatters, validators
from dbfxsql.exceptions.source_errors import SourceAlreadyExists, SourceNotFound
from dbfxsql.exceptions.field_errors import FieldReserved
from dbfxsql.exceptions.row_errors import RowNotFound


def create_table(engine: str, filename: str, fields_: Iterable[tuple]) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if validators.path_exists(filepath):
        raise SourceAlreadyExists(filename)

    if row_number := validators.field_name_in(fields_, "row_number"):
        raise FieldReserved(row_number)

    fields: str = formatters.fields_to_str(fields_, sep="; ")

    file_manager.new_file(filepath)
    dbf_queries.create(filepath, fields)


def insert_row(engine: str, filename: str, fields: Iterable[tuple]) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    types: dict = dbf_queries.fetch_types(filepath)
    row: dict = formatters.fields_to_dict(fields)

    row = formatters.assign_types(engine, types, row)

    dbf_queries.insert(filepath, row)


def bulk_insert_rows(engine: str, filename: str, fields: list[tuple]) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    types: dict = dbf_queries.fetch_types(filepath)
    rows: list[dict] = [formatters.fields_to_dict(field) for field in fields]

    rows = [formatters.assign_types(engine, types, row) for row in rows]

    dbf_queries.bulk_insert(filepath, rows)


def read_rows(engine: str, filename: str, condition: tuple | None) -> list[dict]:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    rows: list[dict] = dbf_queries.read(filepath)
    rows = formatters.scourgify_rows(rows)

    if condition:
        rows, _ = formatters.filter_rows(rows, condition)

    if not rows:
        raise RowNotFound(condition)

    return rows


def update_rows(
    engine: str, filename: str, fields: Iterable[tuple], condition: tuple
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    # assign types to each row's value
    types: dict = dbf_queries.fetch_types(filepath)
    row: dict = formatters.fields_to_dict(fields)

    row = formatters.assign_types(engine, types, row)

    # get a sanitized list of rows
    rows: list[dict] = dbf_queries.read(filepath)
    rows = formatters.scourgify_rows(rows)

    # manual filter of rows by condition
    rows, indexes = formatters.filter_rows(rows, condition)

    if not rows:
        raise RowNotFound(condition)

    # update filtered rows by their index
    if validators.values_are_different(rows, row):
        dbf_queries.update(filepath, row, indexes)


def bulk_update_rows(
    engine: str, filename: str, fields: list[tuple], conditions: list[tuple]
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    types: dict = dbf_queries.fetch_types(filepath)
    dict_rows: list[dict] = [formatters.fields_to_dict(field) for field in fields]

    dict_rows = [formatters.assign_types(engine, types, row) for row in dict_rows]

    table_rows = dbf_queries.read(filepath)
    table_rows = formatters.scourgify_rows(table_rows)

    update_rows: list = []

    for dict_row, condition in zip(dict_rows, conditions):
        _, indexes = formatters.filter_rows(table_rows, condition)

        update_rows.append((dict_row, indexes))

    dbf_queries.bulk_update(filepath, update_rows)


def delete_rows(engine: str, filename: str, condition: tuple) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    rows: list[dict] = dbf_queries.read(filepath)
    rows = formatters.scourgify_rows(rows)

    rows, indexes = formatters.filter_rows(rows, condition)

    if not rows:
        raise RowNotFound(condition)

    dbf_queries.delete(filepath, indexes)


def bulk_delete_rows(engine: str, filename: str, conditions: list[tuple]) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    table_rows = dbf_queries.read(filepath)
    table_rows = formatters.scourgify_rows(table_rows)

    delete_indexes: list = []

    for condition in conditions:
        _, indexes = formatters.filter_rows(table_rows, condition)

        delete_indexes.append(indexes)

    dbf_queries.bulk_delete(filepath, delete_indexes)


def drop_table(engine: str, filename: str) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    file_manager.remove_file(filepath)
