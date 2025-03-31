import itertools
import json
import logging
import os

from dbfxsql.helpers import file_manager, formatters, utils, validators
from dbfxsql.helpers.alias import TablesDict
from dbfxsql.models import Config, Engine, Relation, SyncTable

from . import sync_connection


def init() -> tuple:
    # Disable watchfiles logging
    logging.getLogger("watchfiles").setLevel(logging.ERROR)

    config: Config = file_manager.load_config()
    engines: dict[str, Engine] = {k: Engine(**v) for k, v in config.engines.items()}
    relations: list[Relation] = [Relation(**r) for r in config.relations]

    filenames: list[str] = formatters.prioritized_files(engines, relations)

    # MSSQL edge cases
    engines["MSSQL"] = Engine(**config.engines["MSSQL"])
    to_convert: str = "_log.ldf"

    if os.name != "posix":  # For Windows cache
        entities: TablesDict = formatters.get_mssql_entities(relations)
        databases: list[str] = list(entities.keys())
        filepaths: list[str] = formatters.db_to_tmp(engines, databases)

        sync_connection.deploy_sql_statements(entities, databases)
        utils.generate_tmp_files(filepaths)

        to_convert = ".tmp"

    engines["MSSQL"].convert_to_extension.append(to_convert)

    return engines, relations, filenames


def migrate(filenames: list, relations: list[Relation]) -> None:
    changes: list[dict] = formatters.package_changes(filenames, relations)

    for tables in changes:
        origin: SyncTable = _assing_rows([tables["origin"]])[0]  # SyncTable
        destinies: list[SyncTable] = _assing_rows(
            tables["destinies"]  # list[SyncTable]
        )

        residual_tables: list = formatters.compare_tables(origin, destinies)
        operations: list = formatters.classify_operations(residual_tables)

        # Operations to be executed in the correspond source
        # utils.notify(operations, destinies)

        _execute_operations(operations, destinies)


async def synchronize(engines: dict[str, Engine], relations: list[Relation]) -> None:
    folders: tuple = tuple(engine.folderpaths for engine in engines.values())
    folders = tuple(set(itertools.chain.from_iterable(folders)))

    await utils.arun_signal_safe(
        _listen,
        *folders,
        watch_filter=validators.only_modified,
        args=(folders, relations, engines),
    )


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
    operation_functions = {
        "insert": sync_connection.insert,
        "update": sync_connection.update,
        "delete": sync_connection.delete,
        "bulk_insert": sync_connection.bulk_insert,
        "bulk_update": sync_connection.bulk_update,
        "bulk_delete": sync_connection.bulk_delete,
    }

    for operation, destiny in zip(operations, destinies):
        for name, dataset in operation.items():
            values: list[dict] = formatters.extract_data(name, dataset, destiny)

            # Bulk operations
            if 1 < len(dataset):
                name = "bulk_" + name

            if values:
                operation_functions[name](values)


def _listen(
    folders: tuple, relations: list[Relation], engines: dict[str, Engine]
) -> None:
    if changes := json.loads(str(os.getenv("WATCHFILES_CHANGES"))):
        changes = formatters.filter_filepaths(changes, engines)

        filenames: list = formatters.parse_filenames(changes)

        migrate(filenames, relations)
