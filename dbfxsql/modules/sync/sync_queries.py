from dbfxsql.helpers import file_manager
from dbfxsql.modules import dbf_controller, sql_controller


def insert(filename: str, table: str, fields: str, values: str) -> None:
    if filename.endswith(".dbf"):
        dbf_controller.insert_row(table, fields, values)
    else:
        database, _ = file_manager.decompose_filename(filename)
        sql_controller.insert_row(database, table, fields, values)


def read(engine: str, source: str, table: str) -> dict:
    if "DBF" == engine.upper():
        return dbf_controller.read_rows(engine, source, condition=None)

    return sql_controller.read_rows(engine, source, table, condition=None)


def update(filename: str, table: str, fields: str, values: str, condition: str) -> None:
    if filename.endswith(".dbf"):
        dbf_controller.update_rows(table, fields, values, condition)
    else:
        database, _ = file_manager.decompose_filename(filename)
        sql_controller.update_rows(database, table, fields, values, condition)


def delete(filename: str, table: str, condition: str) -> None:
    if filename.endswith(".dbf"):
        dbf_controller.delete_rows(table, condition)
    else:
        database, _ = file_manager.decompose_filename(filename)
        sql_controller.delete_rows(database, table, condition)
