"""Database management for the table"""

from ..database import dbf_connection
from ..models.exceptions import RecordNotFound
from typing import Any


def insert(record: dict[str, Any]) -> None:
    query = "INSERT"
    parameters = {**record}

    dbf_connection.fetch_none(query, parameters)


def list_all() -> list[dict[str, Any]]:
    query = "SELECT *"

    records = dbf_connection.fetch_all(query)

    return records


def detail(record: dict[str, Any]) -> dict[str, Any]:
    query = f"SELECT * WHERE id == {record["id"]}"

    record = dbf_connection.fetch_one(query)

    if not record:
        raise RecordNotFound(f"No record with id: {record["id"]}")

    return record


def update(record: dict[str, Any]) -> None:
    if not __record_exists("id", record["id"]):
        raise RecordNotFound(f"No record with id: {record["id"]}")

    # query = f"SELECT * WHERE id == {record["id"]}"

    raise NotImplementedError


def delete(record: dict[str, Any]) -> None:
    if not __record_exists("id", record["id"]):
        raise RecordNotFound(f"No record with id: {record["id"]}")

    query = "DELETE"
    parameter = f"SELECT * WHERE id == {record["id"]}"

    dbf_connection.fetch_none(query, parameter)


def reset_tables(parameters: str) -> None:
    """Re-create the user table, if it already exists, delete it"""

    dbf_connection.fetch_none("DROP")
    dbf_connection.fetch_none("CREATE", parameters)


def __record_exists(field: str, value: str) -> bool:
    """Check if a parameter exists"""

    query = f"SELECT * WHERE {field}=={value}"

    return bool(dbf_connection.fetch_one(query))
