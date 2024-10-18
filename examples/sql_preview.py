# SQL ORM

from dbfxsql.functionalities import sql_controller
from dbfxsql.common import utils


def create_database(database: str) -> None:
    sql_controller.create_database(database)


def test_create(database: str, table: str, fields: str) -> None:
    print(f"CREATE TABLE {table} ({fields});")
    sql_controller.create_table(database, table, fields)


def test_drop(database: str) -> None:
    print(f"DROP DATABASE {database};", end="\n\n")
    sql_controller.drop_database(database)


def test_insert(database: str, table: str, fields: str, values: str) -> None:
    print(f"INSERT INTO {table} ({fields}) VALUES ({values});")

    sql_controller.insert_row(database, table, fields, values)


def test_read_all(database: str, table: str) -> None:
    utils.show_table(sql_controller.read_rows(database, table))


def test_read_with_condition(database: str, table: str, condition: str) -> None:
    print(f"SELECT * FROM {table} WHERE ({condition});")
    utils.show_table(sql_controller.read_rows(database, table, condition))


def test_update(
    database: str, table: str, fields: str, values: str, condition: str
) -> None:
    print(
        "UPDATE FROM users",
        f"SET ({fields}) = ({values})",
        f"WHERE ({condition});",
    )

    sql_controller.update_rows(database, table, fields, values, condition)


def test_delete(database: str, table: str, condition: str) -> None:
    print(f"DELETE FROM users WHERE ({condition});")

    sql_controller.delete_rows(database, table, condition)


if __name__ == "__main__":
    print("\nRunning SQL tests...", end="\n\n")

    parameters = [
        ["users", "users", "name, password", "j4breu, qwerty"],
        ["users", "users", "name, password", "JAR-Transmandu, 123456"],
        ["users", "users", "name, password", "admin, password"],
    ]

    create_database("users")
    test_create("users", "users", "id integer primary key, name text, password text")
    test_read_all("users", "users")

    for parameter in parameters:
        test_insert(*parameter)
    test_read_all("users", "users")

    test_read_with_condition("users", "users", "name == j4breu")

    test_update("users", "users", "name, password", "JAR, idk", "id == 2")
    test_read_all("users", "users")

    test_delete("users", "users", "id == 1")
    test_read_all("users", "users")

    test_drop("users")

    print("SQL tests done!")
