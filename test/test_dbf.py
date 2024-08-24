# DBF ORM

from prettytable import PrettyTable
from dbf2sql_sync.database import dbf_queries
from typing import Any


def test_insert(record: dict[str, Any]) -> None:
    record_fields: str = ""

    for field in record.values():
        record_fields += f"'{field}'," if isinstance(field, str) else f"{str(field)}, "

    record_fields = record_fields[:-1]  # Remove last comma

    print(f"INSERT INTO users VALUES ({record_fields});")

    dbf_queries.insert(record)


def test_details(record: dict[str, Any]) -> None:
    print(f"Select * FROM users WHERE id = {record["id"]};")

    user = dbf_queries.detail(record)

    __show_table([user])


def test_lists() -> None:
    users = dbf_queries.list_all()

    __show_table(users)


def test_update(record: dict[str, Any]) -> None:
    # dbf_queries.update(User(id=1, name="JAR-TRANSMANDU", password="qwerty"))
    raise NotImplementedError


def test_delete(record: dict[str, Any]) -> None:
    print(f"DELETE FROM users WHERE id = {record["id"]};")

    dbf_queries.delete(record)


def test_reset(fields: str) -> None:
    print("DROP TABLE users;", end="\n")
    print(f"CREATE TABLE users ({fields});")

    dbf_queries.reset_tables(fields)


def __show_table(records: list[dict[str, Any]]) -> None:
    table = PrettyTable()
    table.field_names = records[0].keys() if records else []

    for record in records:
        table.add_row(
            [
                record[field] if isinstance(record[field], str) else str(record[field])
                for field in table.field_names
            ]
        )

    print(table, end="\n\n")


if __name__ == "__main__":
    print("\nRunning tests...", end="\n\n")

    users_dict = [
        {"id": 1, "name": "j4breu", "password": "qwerty"},
        {"id": 2, "name": "JAR-Transmandu", "password": "123456"},
        {"id": 3, "name": "admin", "password": "password"},
    ]

    # print("\nSelect * from users WHERE id = 1;", end="\n")
    # test_details()

    test_reset("ID N(20,0); name C(20); password C(20)")
    test_lists()

    for user in users_dict:
        test_insert(user)
    test_lists()

    test_details({**users_dict[0]})

    test_delete({**users_dict[0]})
    test_lists()

    print("Done!")
