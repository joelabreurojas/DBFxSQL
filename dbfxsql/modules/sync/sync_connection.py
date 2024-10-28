from dbfxsql.modules import dbf_controller, sql_controller


def insert(engine: str, source: str, table: str, fields: tuple) -> None:
    if "DBF" == engine.upper():
        dbf_controller.insert_row(engine, source, fields)

    else:
        sql_controller.insert_row(engine, source, table, fields)


def read(engine: str, source: str, table: str) -> dict:
    if "DBF" == engine.upper():
        return dbf_controller.read_rows(engine, source, condition=None)

    return sql_controller.read_rows(engine, source, table, condition=None)


def update(engine: str, source: str, table: str, fields: tuple, index: int) -> None:
    condition: tuple = ("row_number", "==", f"{index + 1}")

    if "DBF" == engine.upper():
        dbf_controller.update_rows(engine, source, fields, condition)

    else:
        sql_controller.update_rows(engine, source, table, fields, condition)


def delete(engine: str, source: str, table: str, index: int) -> None:
    condition: tuple = ("row_number", "==", f"{index + 1}")

    if "DBF" == engine.upper():
        dbf_controller.delete_rows(engine, source, condition)

    else:
        sql_controller.delete_rows(engine, source, table, condition)
