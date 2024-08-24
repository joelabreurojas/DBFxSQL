"""Database management for the user table"""

from dataclasses import asdict

from ..database import sql_connection
from ..models.entities import User


def reset_tables() -> None:
    """Re-create the user table, if it already exists, delete it"""

    query = "DROP TABLE IF EXISTS users"
    sql_connection.fetch_none(query)

    # Re-create the table
    fields = "(name text, password text)"
    query = f"CREATE TABLE IF NOT EXISTS users {fields}"
    sql_connection.fetch_none(query)

    # Add some data
    parameters = asdict(User(name="j4breu", password="qwerty"))
    query = """
        INSERT INTO users
        VALUES (:name, :password)
        """

    sql_connection.fetch_none(query, parameters)


def __user_exists(field: str, value: str) -> bool:
    """Check if a parameter exists"""

    query = f"SELECT oid, name from password WHERE {field}=?"
    parameters = value

    record = sql_connection.fetch_one(query, parameters)

    return bool(record)


def __package_users(records: list[str]) -> list[str]:
    """Receives a list of data and returns it in a list of objects"""

    users: list[User] = list()

    for record in records:
        user = User(
            id=record[0],
            name=record[1],
            password=record[2],
        )
        users.append(user)

    return users
