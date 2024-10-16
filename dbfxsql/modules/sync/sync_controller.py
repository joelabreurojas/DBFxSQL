from . import sync_services
from dbfxsql.models.sync_table import SyncTable
from dbfxsql.helpers import file_manager, utils

import logging


def init() -> None:
    logging.getLogger("watchfiles").setLevel(logging.ERROR)

    setup: dict = file_manager.load_toml()
    setup["folders"]: tuple[str] = ("DBF_FOLDERPATH"), ("SQL_FOLDERPATH")

    return setup


async def synchronize(setup: list[list[dict]]) -> None:
    folders: tuple[str] = setup["folders"]
    relations: list[dict] = setup["relations"]

    async for filenames in sync_services.listen(folders):
        for change in sync_services.relevant_changes(filenames, relations):
            origin: SyncTable = change["origin"]

            for index, destiny in enumerate(change["destinies"]):
                # copy with only the correspond fie
                _origin: SyncTable = utils.clone_actor(origin, index)

                insert, update, delete = sync_services.classify(_origin, destiny)

                # data to know where do the changes
                header: dict = _parse_header(_origin, destiny)

                # utils.notify(insert, update, delete, header)

                sync_services.operate(insert, update, delete, header)


def _parse_header(origin: SyncTable, destiny: SyncTable) -> dict:
    return {
        "file": destiny.file,
        "table": destiny.table,
        "origin_fields": origin.fields[0].split(", "),
        "destiny_fields": destiny.fields[0],
    }
