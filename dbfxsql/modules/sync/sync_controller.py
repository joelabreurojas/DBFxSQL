import logging

from . import sync_connection
from dbfxsql.models.sync_table import SyncTable
from dbfxsql.helpers import file_manager, formatters


def init() -> dict:
    logging.getLogger("watchfiles").setLevel(logging.ERROR)

    return file_manager.load_config()


def migrate(priority: str, extensions: tuple, setup: dict) -> None:
    folders: list[str] = setup["folderpaths"][priority]
    filenames: list[str] = file_manager.get_filenames(folders, extensions)

    relations: list[dict] = setup["relations"]
    filenames = formatters.relevant_filenames(filenames, relations)

    origins, destinies = formatters.package_tables(filenames, relations)
    origin, destinies = _depurate_tables(origins, destinies)

    residual_tables: tuple = formatters.compare_tables(origin, destinies)
    operations: list = formatters.classify_operations(residual_tables)

    # Operations to be executed in the correspond source
    # utils.notify(operations, destinies)

    _execute_operations(operations, destinies)


async def synchronize(setup: dict) -> None:
    pass
    # folders: tuple[str] = setup["folders"]
    # relations: list[dict] = setup["relations"]

    # async for filenames in sync_services.listen(folders):
    # for change in sync_services.relevant_changes(filenames, relations):
    # origin: SyncTable = change["origin"]

    # for index, destiny in enumerate(change["destinies"]):
    # copy with only the correspond fie
    # _origin: SyncTable = utils.clone_actor(origin, index)

    # insert, update, delete = sync_services.classify(_origin, destiny)

    # data to know where do the changes

    # header: dict = _parse_header(_origin, destiny)

    # utils.notify(insert, update, delete, header)

    # sync_services.operate(insert, update, delete, header)


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
