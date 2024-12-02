import logging
import itertools
import json

from . import sync_connection
from dbfxsql.models.sync_table import SyncTable
from dbfxsql.helpers import file_manager, formatters, validators

from decouple import config
from watchfiles import arun_process


def init(engine) -> tuple:
    logging.getLogger("watchfiles").setLevel(logging.ERROR)

    setup: dict = file_manager.load_config()

    engines: dict = setup["engines"]
    relations: list = setup["relations"]
    filenames: list = file_manager.get_filenames(engines[engine])

    return engines, relations, filenames


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
    folders: tuple = tuple(engine["folderpaths"] for engine in engines.values())
    folders = tuple(set(itertools.chain.from_iterable(folders)))

    try:
        await arun_process(
            *folders,
            watch_filter=validators.only_modified,
            target=_listen,
            args=(folders, relations, engines),
        )
    except Exception as e:
        logging.error(f"Synchronization error: {str(e)}")


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


def _listen(folders: tuple, relations: dict, engines: dict) -> None:
    if changes := json.loads(config("WATCHFILES_CHANGES")):
        changes = formatters.filter_filepaths(changes, engines)

        filenames: list = formatters.parse_filenames(changes)

        migrate(filenames, relations)
