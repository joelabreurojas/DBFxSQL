from collections.abc import Iterable

from . import dbf_queries
from dbfxsql.helpers import file_manager, formatters
from dbfxsql.exceptions.source_errors import SourceAlreadyExists, SourceNotFound
from dbfxsql.exceptions.record_errors import RecordNotFound


def create_table(engine: str, source: str, fields: Iterable[tuple]) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if file_manager.path_exists(sourcepath):
        raise SourceAlreadyExists(source)

    _fields: str = formatters.fields_to_str(fields, sep="; ")

    file_manager.new_file(sourcepath)
    dbf_queries.create(sourcepath, _fields)


def drop_table(engine: str, source: str) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    file_manager.remove_file(sourcepath)


def insert_record(engine: str, source: str, fields: Iterable[tuple]) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    types: dict = dbf_queries.fetch_types(sourcepath)
    record: dict = formatters.fields_to_dict(fields)

    record = formatters.assign_types(engine, types, record)

    dbf_queries.insert(sourcepath, record)


def read_records(engine: str, source: str, condition: tuple | None) -> list[dict]:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    records: list[dict] = dbf_queries.read(sourcepath)
    records = formatters.scourgify_records(records)

    if condition:
        records, _ = formatters.filter_records(records, condition)

    if not records:
        raise RecordNotFound(condition)

    # utils.show_table(records)
    return records


def update_records(
    engine: str, source: str, fields: Iterable[tuple], condition: tuple
) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    # assign types to each record's value
    types: dict = dbf_queries.fetch_types(sourcepath)
    record: dict = formatters.fields_to_dict(fields)

    record = formatters.assign_types(engine, types, record)

    # get a sanitized list of records
    records: list[dict] = dbf_queries.read(sourcepath)
    records = formatters.scourgify_records(records)

    # manual filter of records by condition
    records, indexes = formatters.filter_records(records, condition)

    if not records:
        raise RecordNotFound(condition)

    # update filtered records by their index
    if formatters.values_are_different(records, record):
        dbf_queries.update(sourcepath, record, indexes)


def delete_records(engine: str, source: str, condition: tuple) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    records: list[dict] = dbf_queries.read(sourcepath)
    records = formatters.scourgify_records(records)

    records, indexes = formatters.filter_records(records, condition)

    if not records:
        raise RecordNotFound(condition)

    dbf_queries.delete(sourcepath, indexes)
