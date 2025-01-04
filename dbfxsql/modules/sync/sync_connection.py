from dbfxsql.modules import dbf_controller, sql_controller


def insert(values: list[dict]) -> None:
    engine: str = values[0]["engine"]
    filename: str = values[0]["filename"]
    table: str = values[0]["table"]
    fields: tuple = tuple(values[0]["fields"])

    if "dBase" == engine:
        dbf_controller.insert_row(engine, filename, fields)

    else:
        sql_controller.insert_row(engine, filename, table, fields)


def read(engine: str, filename: str, table: str) -> dict:
    if "dBase" == engine:
        return dbf_controller.read_rows(engine, filename, condition=None)

    return sql_controller.read_rows(engine, filename, table, condition=None)


def update(values: list[dict]) -> None:
    engine: str = values[0]["engine"]
    filename: str = values[0]["filename"]
    table: str = values[0]["table"]
    fields: tuple = tuple(values[0]["fields"])
    condition: tuple = ("row_number", "==", f"{values[0]["index"]}")

    if "dBase" == engine:
        dbf_controller.update_rows(engine, filename, fields, condition)

    else:
        sql_controller.update_rows(engine, filename, table, fields, condition)


def delete(values: list[dict]) -> None:
    engine: str = values[0]["engine"]
    filename: str = values[0]["filename"]
    table: str = values[0]["table"]
    condition: tuple = ("row_number", "==", f"{values[0]["index"]}")

    if "dBase" == engine:
        dbf_controller.delete_rows(engine, filename, condition)

    else:
        sql_controller.delete_rows(engine, filename, table, condition)
