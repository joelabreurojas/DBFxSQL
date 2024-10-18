from dbfxsql.modules import dbf_controller
from dbfxsql import utils


def test_create(table: str, fields: str) -> None:
    print(f"CREATE TABLE {table} ({fields});")
    dbf_controller.create_table(table, fields)


def test_drop(table: str) -> None:
    print(f"DROP TABLE {table};", end="\n\n")
    dbf_controller.drop_table(table)


def test_add_fields(table: str, fields: str, increment: str) -> None:
    autoincrement = " AUTOINCREMENT" if "True" == increment else ""
    _fields = fields.replace(";", ",")

    print(f"ALTER TABLE {table} ADD ({_fields}){autoincrement};")
    dbf_controller.add_fields(table, fields, increment)


def test_insert(table: str, fields: str, values: str) -> None:
    print(f"INSERT INTO {table} ({fields}) VALUES ({values});")

    dbf_controller.insert_row(table, fields, values)


def test_read_all(table: str) -> None:
    utils.show_table(dbf_controller.read_rows(table))


def test_read_with_condition(table: str, condition: str) -> None:
    print(f"SELECT * FROM {table} WHERE ({condition});")
    utils.show_table(dbf_controller.read_rows(table, condition))


def test_update(table: str, fields: str, values: str, condition: str) -> None:
    print(
        "UPDATE FROM users",
        f"SET ({fields}) = ({values})",
        f"WHERE ({condition});",
    )

    dbf_controller.update_rows(table, fields, values, condition)


def test_delete(table: str, condition: str) -> None:
    print(f"DELETE FROM users WHERE ({condition});")

    dbf_controller.delete_rows(table, condition)


if __name__ == "__main__":
    print("\nRunning DBF tests...", end="\n\n")

    parameters = [
        ["users", "name, password", "j4breu, qwerty"],
        ["users", "name, password", "JAR-Transmandu, 123456"],
        ["users", "name, password", "admin, password"],
    ]

    test_create("users", "name C(20); password C(20)")
    test_read_all("users")

    for parameter in parameters:
        test_insert("users", "name, password", "j4breu, qwerty")
    test_read_all("users")

    test_add_fields("users", "id N(20,0); address C(20)", increment="True")
    test_read_all("users")

    test_read_with_condition("users", "name == j4breu")

    test_update("users", "name, password", "JAR, idk", "id == 2")
    test_read_all("users")

    test_delete("users", "id == 1")
    test_read_all("users")

    test_drop("users")

    print("DBF tests done!")
