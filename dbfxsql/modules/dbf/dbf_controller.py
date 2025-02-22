from collections.abc import Iterable

from dbfxsql.exceptions import (
    FieldReserved,
    RowNotFound,
    SourceAlreadyExists,
    SourceNotFound,
)
from dbfxsql.helpers import file_manager, formatters, validators

from . import dbf_queries


def create_table(
    engine: str, filename: str, fields_: Iterable[tuple[str, str]]
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if validators.path_exists(filepath):
        raise SourceAlreadyExists(filename)

    if row_number := validators.field_name_in(fields_, "row_number"):
        raise FieldReserved(row_number)

    fields: str = formatters.fields_to_str(fields_, sep="; ")

    file_manager.new_file(filepath)
    dbf_queries.create(filepath, fields)


def insert_row(engine: str, filename: str, fields: Iterable[tuple[str, str]]) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    types: dict[str, str] = dbf_queries.fetch_types(filepath)
    row: dict = formatters.fields_to_dict(fields)

    row = formatters.assign_types(engine, types, row)

    dbf_queries.insert(filepath, row)


def bulk_insert_rows(engine: str, filename: str, fields_: list[tuple]) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    rows: list[dict] = [formatters.fields_to_dict(fields) for fields in fields_]

    dbf_queries.bulk_insert(filepath, rows)


def read_rows(
    engine: str, filename: str, condition: tuple[str, str, str] | None
) -> list[dict]:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    types: dict[str, str] = dbf_queries.fetch_types(filepath)
    rows: list[dict] = dbf_queries.read(filepath)

    rows = formatters.scourgify_rows(rows)
    rows = [formatters.assign_types(engine, types, row) for row in rows]

    if condition and not (rows := formatters.filter_rows(rows, condition)[0]):
        raise RowNotFound(condition)

    return rows


def update_rows(
    engine: str,
    filename: str,
    fields: Iterable[tuple[str, str]],
    condition: tuple[str, str, str],
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    # assign types to each row's value
    types: dict[str, str] = dbf_queries.fetch_types(filepath)
    row: dict = formatters.fields_to_dict(fields)

    row = formatters.assign_types(engine, types, row)

    # get a sanitized list of rows
    rows: list[dict] = dbf_queries.read(filepath)

    rows = formatters.scourgify_rows(rows)
    rows = [formatters.assign_types(engine, types, row) for row in rows]

    # manual filter of rows by condition
    rows, indexes = formatters.filter_rows(rows, condition)

    if not rows:
        raise RowNotFound(condition)

    # update filtered rows by their index
    if validators.values_are_different(rows, row):
        dbf_queries.update(filepath, row, indexes)


def bulk_update_rows(
    engine: str,
    filename: str,
    fields_: list[tuple],
    conditions: list[tuple[str, str, str]],
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    dict_rows: list[dict] = [formatters.fields_to_dict(fields) for fields in fields_]

    table_rows: list[dict] = dbf_queries.read(filepath)
    table_rows = formatters.scourgify_rows(table_rows)

    update_rows: list = []

    for dict_row, condition in zip(dict_rows, conditions):
        _, indexes = formatters.filter_rows(table_rows, condition)

        update_rows.append((dict_row, indexes))

    dbf_queries.bulk_update(filepath, update_rows)


def delete_rows(engine: str, filename: str, condition: tuple[str, str, str]) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    if not validators.path_exists(filepath):
        raise SourceNotFound(filepath)

    types: dict[str, str] = dbf_queries.fetch_types(filepath)
    rows: list[dict] = dbf_queries.read(filepath)

    rows = formatters.scourgify_rows(rows)
    rows = [formatters.assign_types(engine, types, row) for row in rows]

    rows, indexes = formatters.filter_rows(rows, condition)

    if not rows:
        raise RowNotFound(condition)

    dbf_queries.delete(filepath, indexes)


def bulk_delete_rows(
    engine: str, filename: str, conditions: list[tuple[str, str, str]]
) -> None:
    filepath: str = formatters.add_folderpath(engine, filename)

    table_rows: list[dict] = dbf_queries.read(filepath)
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
