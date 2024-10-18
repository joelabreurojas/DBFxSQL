from collections.abc import Iterable

from . import sql_queries
from dbfxsql.helpers import file_manager, formatters
from dbfxsql.exceptions.source_errors import SourceNotFound
from dbfxsql.exceptions.row_errors import RowAlreadyExists, RowNotFound


def create_table(engine: str, source: str, table: str, fields: Iterable[tuple]) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if file_manager.path_exists(sourcepath):
        file_manager.new_file(sourcepath)

    _fields: str = formatters.fields_to_str(fields)

    sql_queries.create(sourcepath, table, _fields)


def drop_database(engine: str, source: str) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    file_manager.remove_file(sourcepath)


def drop_table(engine: str, source: str, table: str) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    sql_queries.drop(sourcepath, table)


def insert_row(
    engine: str, source: str, table: str, fields: Iterable[tuple]
) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    types: dict = sql_queries.fetch_types(sourcepath, table)
    types = formatters.scourgify_types(types)

    row: dict = formatters.fields_to_dict(fields)
    row = formatters.assign_types(engine, types, row)

    if formatters.field_id_exists(row):
        condition: str = f"id == {row['id']}"

        if _row_exists(sourcepath, table, condition):
            raise RowAlreadyExists(row["id"])

    _fields: tuple[str, str] = formatters.deglose_fields(row)

    sql_queries.insert(sourcepath, table, row, _fields)


def read_rows(
    engine: str, source: str, table: str, condition: tuple | None
) -> list[dict]:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    if condition and not _row_exists(sourcepath, table, condition):
        raise RowNotFound(condition)

    return sql_queries.read(sourcepath, table, condition)


def update_rows(
    engine: str, source: str, table: str, fields: Iterable[tuple], condition: tuple
) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    # assign types to each row's value
    types: dict = sql_queries.fetch_types(sourcepath, table)
    types = formatters.scourgify_types(types)

    row: dict = formatters.fields_to_dict(fields)
    row = formatters.assign_types(engine, types, row)

    # check if other row have the same received id
    if formatters.field_id_exists(row):
        condition: str = f"id == {row['id']}"

        if _row_exists(sourcepath, table, condition):
            raise RowAlreadyExists(row["id"])

    if not _row_exists(sourcepath, table, condition):
        raise RowNotFound(condition)

    fields: tuple[str, str] = formatters.deglose_fields(row)
    _fields: str = formatters.merge_fields(fields, sep=" = ")

    sql_queries.update(sourcepath, table, row, _fields, condition)


def delete_rows(engine: str, source: str, table: str, condition: tuple) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    if not _row_exists(sourcepath, table, condition):
        raise RowNotFound(condition)

    sql_queries.delete(sourcepath, table, condition)


def _row_exists(sourcepath: str, table: str, condition: tuple) -> bool:
    rows: list[dict] = sql_queries.read(sourcepath, table, condition)

    return bool(formatters.depurate_empty_rows(rows))
