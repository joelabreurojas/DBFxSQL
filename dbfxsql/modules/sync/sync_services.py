from collections.abc import AsyncGenerator

from . import sync_queries
from dbfxsql.models.sync_table import SyncTable
from dbfxsql.helpers import formatters, utils

from watchfiles import awatch


async def listen(folders: tuple[str]) -> AsyncGenerator[tuple, None]:
    """Asynchronously listens for file changes and triggers the runner function."""

    async for changes in awatch(*folders, watch_filter=utils.only_modified):
        yield formatters.parse_filepaths(changes)


def classify(origin: SyncTable, destiny: SyncTable) -> tuple[list, list, list]:
    """Classifies changes into insert, update and delete operations."""

    origin_rows: list = formatters.depurate_empty_rows(origin.rows)
    destiny_rows: list = formatters.depurate_empty_rows(destiny.rows)

    insert: list = origin_rows[:]
    update: list = []
    delete: list = destiny_rows[:]

    fields: tuple = formatters.package_fields(origin, destiny)

    for origin_row in origin_rows:
        for destiny_row in destiny_rows:
            if origin_row["id"] == destiny_row["id"]:
                if change := _comparator(origin_row, destiny_row, fields):
                    update.append(change)

                insert.remove(origin_row)
                delete.remove(destiny_row)

    return insert, update, delete


def operate(insert: list, update: list, delete: list, header: dict) -> None:
    """Executes insert, update and delete operations."""
    for row in insert:
        sync_queries.insert(
            header["file"],
            header["table"],
            header["destiny_fields"],
            ", ".join(f"{row[field]}" for field in header["origin_fields"]),
        )

    # avoid RowAlreadyExists error
    header["origin_fields"].remove("id")
    header["destiny_fields"] = header["destiny_fields"].split(", ")
    header["destiny_fields"].remove("id")

    for row in update:
        sync_queries.update(
            header["file"],
            header["table"],
            ", ".join(header["destiny_fields"]),
            ", ".join(f"{row[field]}" for field in header["origin_fields"]),
            f"id == {row['id']}",
        )

    for row in delete:
        sync_queries.delete(header["file"], header["table"], f"id == {row['id']}")


def _comparator(origin: dict, destiny: dict, fields: tuple) -> dict | None:
    for origin_field, destiny_field in fields:
        if origin[origin_field] != destiny[destiny_field]:
            return origin
