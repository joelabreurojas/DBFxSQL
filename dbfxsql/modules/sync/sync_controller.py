import logging
from collections.abc import AsyncGenerator

from . import sync_connection
from dbfxsql.models.sync_table import SyncTable
from dbfxsql.helpers import file_manager, formatters, utils

from watchfiles import awatch


def init() -> dict:
    logging.getLogger("watchfiles").setLevel(logging.ERROR)

    return file_manager.load_config()


def collect_files(setup: dict, priority: str) -> tuple:
    folders: list[str] = setup["folderpaths"][priority]
    extensions: list[str] = setup["extensions"][priority]

    return file_manager.get_filenames(folders, extensions)


def migrate(filenames: list, relations: dict) -> None:
    origins, destinies = formatters.package_tables(filenames, relations)
    origin, destinies = _depurate_tables(origins, destinies)

    residual_tables: tuple = formatters.compare_tables(origin, destinies)
    operations: list = formatters.classify_operations(residual_tables)

    # Operations to be executed in the correspond source
    # utils.notify(operations, destinies)

    _execute_operations(operations, destinies)


async def synchronize(setup: dict, priority: str) -> None:
    folders: list[str] = setup["folderpaths"][priority]
    relations: list[dict] = setup["relations"]

    async for filenames in _listen(folders):
        migrate(filenames, relations)


def _depurate_tables(origins: list[SyncTable], destinies: list[SyncTable]) -> tuple:
    rows: list[dict] = sync_connection.read(
        origins[0].engine, origins[0].source, origins[0].name
    )
    origin: SyncTable = SyncTable(
        engine=origins[0].engine,
        source=origins[0].source,
        name=origins[0].name,
        fields=[origin.fields for origin in origins],
        rows=formatters.depurate_empty_rows(rows),
    )

    _destinies: list = []

    for destiny in destinies:
        rows = sync_connection.read(destiny.engine, destiny.source, destiny.name)

        destiny: SyncTable = SyncTable(
            engine=destiny.engine,
            source=destiny.source,
            name=destiny.name,
            fields=destiny.fields,
            rows=formatters.depurate_empty_rows(rows),
        )

        _destinies.append(destiny)

    return origin, _destinies


def _execute_operations(operations: list, destinies: list[SyncTable]) -> None:
    for (inserts, updates, deletes), destiny in zip(operations, destinies):
        for insert in inserts:
            sync_connection.insert(
                destiny.engine,
                destiny.source,
                destiny.name,
                formatters.fields_to_tuple(insert["fields"]),
            )

        for update in updates:
            sync_connection.update(
                destiny.engine,
                destiny.source,
                destiny.name,
                formatters.fields_to_tuple(update["fields"]),
                update["index"],
            )

        for delete in deletes[::-1]:
            sync_connection.delete(
                destiny.engine,
                destiny.source,
                destiny.name,
                delete["index"],
            )


async def _listen(folders: tuple[str]) -> AsyncGenerator[tuple, None]:
    """Asynchronously listens for file changes and triggers the runner function."""

    async for changes in awatch(*folders, watch_filter=utils.only_modified):
        yield formatters.parse_filepaths(changes)
