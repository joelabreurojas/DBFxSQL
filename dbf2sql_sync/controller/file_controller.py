from ..database import dbf_queries, sql_queries
from ..helpers import util
from ..models.entities import User
from typing import List


def update(user: User) -> None:
    dbf_queries.update(user)


def details(user: User) -> User:
    return dbf_queries.detail(user)


def lists() -> List[User]:
    return dbf_queries.list_all()


def reset() -> None:
    """Delete the database and the local storage to create them again"""

    util.reset_databases()
    dbf_queries.reset_tables()
    sql_queries.reset_tables()
