import dbf
from contextlib import contextmanager
from typing import Any, Iterator

from ..helpers import util


def fetch_none(query: str, parameters: dict[str, Any] | str | None = None) -> None:
    """Executes a query without returning values"""

    command: dict[str, Any] = {
        "CREATE": __create_table,
        "INSERT": __insert_record,
        "UPDATE": __update_record,
        "DELETE": __delete_record,
        "DROP": __drop_table,
    }

    with __get_table() as table:
        command[query](table, parameters) if parameters else command[query](table)


def fetch_one(query: str) -> dict[str, Any]:
    """Executes a query returning one row in the found set"""

    with __get_table() as table:
        # Save field names in a list
        fields = [field for field in table.field_names]

        # Save data in a list
        values = table.query(query)[0]

        # Save fields and data in a dictionary
        record = dict(zip(fields, values))

        return record


def fetch_all(query: str) -> list[dict[str, Any]]:
    """Executes a query returning all rows in the found set"""

    with __get_table() as table:
        # Save field names in a list
        fields = [field for field in table.field_names]

        # Save data of each record in a list
        values = [value for value in table.query(query)]

        if not values:
            return [{field: None for field in fields}]

        # Save fields and data in a dictionary for each record
        records = [dict(zip(fields, value)) for value in values]

        return records


def __create_table(table: dbf.Table, parameters: str) -> None:
    table.add_fields(parameters)


def __insert_record(table: dbf.Table, parameters: dict[str, Any]) -> None:
    table.append(parameters)


def __update_record(table: dbf.Table, parameters: dict[str, Any]) -> None:
    raise NotImplementedError


def __delete_record(table: dbf.Table, parameters: str) -> None:
    with table.query(parameters)[0] as record:
        dbf.delete(record)

    table.pack()


def __drop_table(table: dbf.Table) -> None:
    table.zap()
    table.delete_fields(table.field_names)


@contextmanager
def __get_table() -> Iterator[dbf.Table]:
    """Allows working with database table"""

    table: dbf.Table = dbf.Table(util.DBF_DATABASE).open(dbf.READ_WRITE)
    try:
        yield table
    finally:
        table.close()
