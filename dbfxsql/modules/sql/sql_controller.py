from collections.abc import Iterable

from . import sql_queries
from dbfxsql.helpers import file_manager, formatters
from dbfxsql.exceptions.source_errors import SourceNotFound
from dbfxsql.exceptions.record_errors import RecordAlreadyExists, RecordNotFound


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


def insert_record(
    engine: str, source: str, table: str, fields: Iterable[tuple]
) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    types: dict = sql_queries.fetch_types(sourcepath, table)
    types = formatters.scourgify_types(types)

    record: dict = formatters.fields_to_dict(fields)
    record = formatters.assign_types(engine, types, record)

    if "id" in fields:
        condition: str = f"id == {record['id']}"

        if _record_exists(sourcepath, table, condition):
            raise RecordAlreadyExists(record["id"])

    fields: tuple[str, str] = formatters.deglose_fields(record)

    sql_queries.insert(sourcepath, table, record, fields)


def read_records(
    engine: str, source: str, table: str, condition: tuple | None
) -> list[dict]:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    if condition and not _record_exists(sourcepath, table, condition):
        raise RecordNotFound(condition)

    return sql_queries.read(sourcepath, table, condition)


def update_records(
    engine: str, source: str, table: str, fields: Iterable[tuple], condition: tuple
) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    # assign types to each record's value
    types: dict = sql_queries.fetch_types(sourcepath, table)
    types = formatters.scourgify_types(types)

    record: dict = formatters.fields_to_dict(fields)
    record = formatters.assign_types(engine, types, record)

    # check if other record have the same received id
    if "id" in fields:
        condition: str = f"id == {record['id']}"

        if _record_exists(sourcepath, table, condition):
            raise RecordAlreadyExists(record["id"])

    if not _record_exists(sourcepath, table, condition):
        raise RecordNotFound(condition)

    fields: tuple[str, str] = formatters.deglose_fields(record)
    _fields: str = formatters.merge_fields(fields, sep=" = ")

    sql_queries.update(sourcepath, table, record, _fields, condition)


def delete_records(engine: str, source: str, table: str, condition: tuple) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    if not _record_exists(sourcepath, table, condition):
        raise RecordNotFound(condition)

    sql_queries.delete(sourcepath, table, condition)


def _record_exists(sourcepath: str, table: str, condition: tuple) -> bool:
    records: list[dict] = sql_queries.read(sourcepath, table, condition)

    return bool(formatters.depurate_empty_records(records))
