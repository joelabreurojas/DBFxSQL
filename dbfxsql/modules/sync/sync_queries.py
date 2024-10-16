from dbfxsql.helpers import file_manager
from dbfxsql.modules import dbf_controller, sql_controller


def insert(filename: str, table: str, fields: str, values: str) -> None:
    if filename.endswith(".dbf"):
        dbf_controller.insert_record(table, fields, values)
    else:
        database, _ = file_manager.decompose_filename(filename)
        sql_controller.insert_record(database, table, fields, values)


def read(filename: str, table: str) -> dict:
    if filename.endswith(".dbf"):
        return dbf_controller.read_records(table)

    database, _ = file_manager.decompose_filename(filename)
    return sql_controller.read_records(database, table)


def update(filename: str, table: str, fields: str, values: str, condition: str) -> None:
    if filename.endswith(".dbf"):
        dbf_controller.update_records(table, fields, values, condition)
    else:
        database, _ = file_manager.decompose_filename(filename)
        sql_controller.update_records(database, table, fields, values, condition)


def delete(filename: str, table: str, condition: str) -> None:
    if filename.endswith(".dbf"):
        dbf_controller.delete_records(table, condition)
    else:
        database, _ = file_manager.decompose_filename(filename)
        sql_controller.delete_records(database, table, condition)
