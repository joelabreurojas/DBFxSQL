import logging
import itertools
from collections.abc import AsyncGenerator

from . import sync_connection
from dbfxsql.models.sync_table import SyncTable
from dbfxsql.helpers import file_manager, formatters, validators

from watchfiles import awatch


def init(engine) -> tuple:
    logging.getLogger("watchfiles").setLevel(logging.ERROR)

    setup: dict = file_manager.load_config()

    engines: dict = setup["engines"]
    relations: list = setup["relations"]
    filenames: list = file_manager.get_filenames(engines[engine])

    return engines, relations, filenames


def _collect_files(engine_data: dict) -> tuple:
    folders: list[str] = list(set(engine_data["folderpaths"]))
    extensions: list[str] = list(set(engine_data["extensions"]))

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


async def synchronize(engines: dict, relations: dict) -> None:
    # Get all folders and extensions
    folders: tuple = tuple(engine["folderpaths"] for engine in engines.values())
    extensions: tuple = tuple(engine["extensions"] for engine in engines.values())

    # Remove duplicates
    folders = tuple(set(itertools.chain.from_iterable(folders)))
    extensions = tuple(set(itertools.chain.from_iterable(extensions)))

    async for filenames in _listen(folders, engines):
        migrate(filenames, relations)


def _assing_rows(tables_: list[SyncTable]) -> list[SyncTable]:
    tables: list = []

    for table in tables_:
        rows: list[dict] = sync_connection.read(table.engine, table.source, table.name)

        destiny: SyncTable = SyncTable(
            engine=table.engine,
            source=table.source,
            name=table.name,
            fields=table.fields,
            rows=formatters.depurate_empty_rows(rows),
        )

        tables.append(destiny)

    return tables


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


async def _listen(folders: tuple[str], engines: dict) -> AsyncGenerator:
    """Asynchronously listens for file changes and triggers the runner function."""

    async for changes in awatch(*folders, watch_filter=validators.only_modified):
        yield formatters.filter_filepaths(changes, engines)
