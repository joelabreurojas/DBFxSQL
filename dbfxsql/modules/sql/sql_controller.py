from . import sql_queries
from dbfxsql.helpers import file_manager, formatters
from dbfxsql.exceptions.source_errors import SourceNotFound
from dbfxsql.exceptions.record_errors import RecordAlreadyExists, RecordNotFound


def create_table(engine: str, source: str, table: str, fields: tuple[tuple]) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if file_manager.path_exists(sourcepath):
        file_manager.create_file(sourcepath)

    _fields: str = formatters.fields_to_str(fields)

    sql_queries.create(sourcepath, table, fields)


def drop_database(engine: str, source: str) -> None:
    sourcepath: str = file_manager.add_folderpath(engine, source)

    if not file_manager.path_exists(sourcepath):
        raise SourceNotFound(sourcepath)

    file_manager.remove_file(sourcepath)


def drop_table(db: str, table: str) -> None:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise SourceNotFound(filepath)

    sql_queries.drop(filepath, table)


def insert_record(db: str, table: str, fields: str, values: str) -> None:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise SourceNotFound(filepath)

    types: dict[str, str] = sql_queries.fetch_types(filepath, table, fields)
    record: dict = formatters.format_input(fields, values, types)

    if "id" in fields:
        filter: str = formatters.parse_condition(f"id == {record['id']}")

        if _record_exists(filepath, table, filter):
            raise RecordAlreadyExists(record["id"])

    sql_queries.insert(filepath, table, record)


def read_records(
    db: str, table: str, condition: str | None = None
) -> list[dict]:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise SourceNotFound(filepath)

    if condition:
        filter: str = formatters.parse_condition(condition)

        if not _record_exists(filepath, table, filter):
            raise RecordNotFound(condition)

        records: list[dict] = sql_queries.read(filepath, table, filter)
    else:
        records: list[dict] = sql_queries.read(filepath, table)

    return records


def update_records(
    db: str, table: str, fields: str, values: str, condition: str
) -> None:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise SourceNotFound(filepath)

    types: dict[str, str] = sql_queries.fetch_types(filepath, table, fields)
    record: dict = formatters.format_input(fields, values, types)

    # check if other record have the same id
    if "id" in fields:
        filter: str = formatters.parse_condition(f"id == {record['id']}")

        if _record_exists(filepath, table, filter):
            raise RecordAlreadyExists(record["id"])

    # check if this record exists
    filter: str = formatters.parse_condition(condition)

    if not _record_exists(filepath, table, filter):
        raise RecordNotFound(condition)

    sql_queries.update(filepath, table, record, filter)


def delete_records(db: str, table: str, condition: str) -> None:
    filepath: str = file_manager.generate_filepath(db, database="sql")
    if not file_manager.filepath_exists(filepath):
        raise SourceNotFound(filepath)

    filter: str = formatters.parse_condition(condition)

    if not _record_exists(filepath, table, filter):
        raise RecordNotFound(condition)

    sql_queries.delete(filepath, table, filter)


def _record_exists(filepath: str, table: str, filter: str) -> bool:
    records: list[dict] = sql_queries.read(filepath, table, filter)

    return bool(formatters.depurate_empty_records(records))
