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
    changes: list[dict] = formatters.package_changes(filenames, relations)

    for tables in changes:
        origin: SyncTable = _assing_rows([tables["origin"]])[0]
        destinies: list[SyncTable] = _assing_rows(tables["destinies"])

        residual_tables: list = formatters.compare_tables(origin, destinies)
        operations: list = formatters.classify_operations(residual_tables)

        # Operations to be executed in the correspond source
        # utils.notify(operations, destinies)

        _execute_operations(operations, destinies)


async def synchronize(setup: dict, priority: str) -> None:
    folders: list[str] = setup["folderpaths"][priority]
    relations: list[dict] = setup["relations"]

    async for filenames in _listen(folders):
        migrate(filenames, relations)


def _assing_rows(tables: list[SyncTable]) -> list[SyncTable]:
    _table: list = []

    for table in tables:
        rows: list[dict] = sync_connection.read(table.engine, table.source, table.name)

        destiny: SyncTable = SyncTable(
            engine=table.engine,
            source=table.source,
            name=table.name,
            fields=table.fields,
            rows=formatters.depurate_empty_rows(rows),
        )

        _table.append(destiny)

    return _table


def _execute_operations(operations: list, destinies: list[SyncTable]) -> None:
    for operation, destiny in zip(operations, destinies):
        for insert in operation["insert"]:
            sync_connection.insert(
                destiny.engine,
                destiny.source,
                destiny.name,
                formatters.fields_to_tuple(insert["fields"]),
            )

        for update in operation["update"]:
            sync_connection.update(
                destiny.engine,
                destiny.source,
                destiny.name,
                formatters.fields_to_tuple(update["fields"]),
                update["index"],
            )

        for delete in operation["delete"][::-1]:
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
