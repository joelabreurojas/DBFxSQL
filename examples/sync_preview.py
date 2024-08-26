from dbfxsql.modules import dbf_controller, sql_controller, sync_controller


def test_dbf_to_sql(db: str, table: str) -> None:
    print("\nRunning DBF -> SQL tests...", end="\n\n")

    # dbf_controller.read_rows("users", "users")

    print("Read DBF Table")
    dbf_controller.read_rows("users")

    print("Read SQL Table")
    sql_controller.read_rows("users", "users")

    print("Syncing...", end="\n\n")

    print("Read DBF Table")
    sync_controller.dbf_to_sql(db, table)

    print("Read SQL Table")
    sql_controller.read_rows("users", "users")

    print("DBF -> SQL test done!")


def test_sql_to_dbf(db: str, table: str) -> None:
    print("\nRunning SQL -> DBF tests...", end="\n\n")

    print("Read SQL Table")
    sql_controller.read_rows("users", "users")

    print("Read DBF Table")
    dbf_controller.read_rows("users")

    print("Syncing...", end="\n\n")

    print("Read SQL Table")
    sync_controller.sql_to_dbf(db, table)

    print("Read DBF Table")
    dbf_controller.read_rows("users")

    print("SQL -> DBF test done!")


if __name__ == "__main__":
    print("\nSelect tests:", end="\n\n")
    choice = input("1. Run DBF->SQL tests\n2. Run SQL->DBF tests\n\n > ")

    # Load data
    dbf_fields = "id N(20,0); name C(20); password C(20)"
    sql_fields = "id integer PRIMARY KEY, name text, password text"

    dbf_parameters = [
        ["users", "id, name, password", "1, j4breu, qwerty"],
        ["users", "id, name, password", "2, JAR-Transmandu, 123456"],
        ["users", "id, name, password", "3, admin, password"],
    ]

    sql_parameters = [
        ["users", "users", "id, name, password", "1, j4breu, qwerty"],
        ["users", "users", "id, name, password", "2, JAR-Transmandu, 123456"],
        ["users", "users", "id, name, password", "3, admin, password"],
    ]

    if choice == "1":
        # Create
        dbf_controller.create_table("users", dbf_fields)
        sql_controller.create_database("users")
        sql_controller.create_table("users", "users", sql_fields)

        # Insert
        for parameter in dbf_parameters:
            dbf_controller.insert_row(*parameter)

        # Test
        test_dbf_to_sql("users", "users")

        # Drop
        dbf_controller.drop_table("users")
        sql_controller.drop_database("users")

    elif choice == "2":
        # Create
        dbf_controller.create_table("users", dbf_fields)
        sql_controller.create_database("users")
        sql_controller.create_table("users", "users", sql_fields)

        # Insert
        for parameter in sql_parameters:
            sql_controller.insert_row(*parameter)

        # Test
        test_sql_to_dbf("users", "users")

        # Drop
        dbf_controller.drop_table("users")
        sql_controller.drop_database("users")

    else:
        print("Invalid choice")
