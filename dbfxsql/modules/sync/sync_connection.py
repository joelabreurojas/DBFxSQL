from dbfxsql.modules import dbf_controller, sql_controller


def insert(values: list[dict]) -> None:
    engine: str = values[0]["engine"]
    filename: str = values[0]["filename"]
    table: str = values[0]["table"]
    fields: tuple[tuple[str, str]] = tuple(values[0]["fields"])

    if "dBase" == engine:
        dbf_controller.insert_row(engine, filename, fields)

    else:
        sql_controller.insert_row(engine, filename, table, fields)


def bulk_insert(values: list[dict]) -> None:
    engine: str = values[0]["engine"]
    filename: str = values[0]["filename"]
    table: str = values[0]["table"]
    fields: list[tuple[str, str]] = [value["fields"] for value in values]

    if "dBase" == engine:
        dbf_controller.bulk_insert_rows(engine, filename, fields)

    else:
        sql_controller.bulk_insert_rows(engine, filename, table, fields)


def read(engine: str, filename: str, table: str) -> list[dict]:
    if "dBase" == engine:
        return dbf_controller.read_rows(engine, filename, condition=None)

    return sql_controller.read_rows(engine, filename, table, condition=None)


def update(values: list[dict]) -> None:
    engine: str = values[0]["engine"]
    filename: str = values[0]["filename"]
    table: str = values[0]["table"]
    fields: tuple[tuple[str, str]] = tuple(values[0]["fields"])
    condition: tuple[str, str, str] = ("row_number", "==", f"{values[0]['index']}")

    if "dBase" == engine:
        dbf_controller.update_rows(engine, filename, fields, condition)

    else:
        sql_controller.update_rows(engine, filename, table, fields, condition)


def bulk_update(values: list[dict]) -> None:
    engine: str = values[0]["engine"]
    filename: str = values[0]["filename"]
    table: str = values[0]["table"]
    fields: list[tuple[str, str]] = [value["fields"] for value in values]
    conditions: list[tuple[str, str, str]] = [
        ("row_number", "==", f"{value['index']}") for value in values
    ]

    if "dBase" == engine:
        dbf_controller.bulk_update_rows(engine, filename, fields, conditions)

    else:
        sql_controller.bulk_update_rows(engine, filename, table, fields, conditions)


def delete(values: list[dict]) -> None:
    engine: str = values[0]["engine"]
    filename: str = values[0]["filename"]
    table: str = values[0]["table"]
    condition: tuple[str, str, str] = ("row_number", "==", f"{values[0]['index']}")

    if "dBase" == engine:
        dbf_controller.delete_rows(engine, filename, condition)

    else:
        sql_controller.delete_rows(engine, filename, table, condition)


def bulk_delete(values: list[dict]) -> None:
    engine: str = values[0]["engine"]
    filename: str = values[0]["filename"]
    table: str = values[0]["table"]
    conditions: list[tuple[str, str, str]] = [
        ("row_number", "==", f"{value['index']}") for value in values
    ]

    if "dBase" == engine:
        dbf_controller.bulk_delete_rows(engine, filename, conditions)

    else:
        sql_controller.bulk_delete_rows(engine, filename, table, conditions)


def deploy_sql_statements(entities: dict, databases: list[str]) -> None:
    sql_controller.deploy_statements(entities, databases, engine="MSSQL")
