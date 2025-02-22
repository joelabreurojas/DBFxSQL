import dbf

from dbfxsql.helpers.alias import IndexesList, RowIndexesTuple

from .dbf_connection import get_table


def create(filepath: str, fields: str) -> None:
    with get_table(filepath) as table:
        table.add_fields(fields)


def insert(filepath: str, row: dict) -> None:
    with get_table(filepath) as table:
        table.append(row)


def bulk_insert(filepath: str, rows: list[dict]) -> None:
    with get_table(filepath) as table:
        for row in rows:
            table.append(row)


def read(filepath: str) -> list[dict]:
    with get_table(filepath) as table:
        field_names: list[str] = [field.lower() for field in table.field_names]

        rows: list[dict] = [dict(zip(field_names, row)) for row in table]

    return rows if rows else [{field: "" for field in field_names}]


def update(filepath: str, row_: dict, indexes: list[int]) -> None:
    with get_table(filepath) as table:
        for index in indexes:
            with table[index] as row:
                for key, value in row_.items():
                    setattr(row, key, value)


def bulk_update(filepath: str, filtered_rows: list[RowIndexesTuple]) -> None:
    with get_table(filepath) as table:
        for row_, indexes in filtered_rows:
            for index in indexes:
                with table[index] as row:
                    for key, value in row_.items():
                        setattr(row, key, value)


def delete(filepath: str, indexes: list[int]) -> None:
    with get_table(filepath) as table:
        for index in indexes:
            with table[index] as row:
                dbf.delete(row)

        table.pack()


def bulk_delete(filepath: str, indexes: IndexesList) -> None:
    with get_table(filepath) as table:
        for indexes_ in indexes:
            for index in indexes_:
                with table[index] as row:
                    dbf.delete(row)

        table.pack()


def fetch_types(filepath) -> dict[str, str]:
    names: list = []
    data_structure: list = []

    with get_table(filepath) as table:
        for i in range(table.field_count):
            names.append(table._field_layout(i).lower().split(" ")[0])

            data_type: str = table._field_layout(i).split(" ")[-1][0]
            data_structure.append(data_type if data_type != "n" else "C")

    return dict(zip(names, data_structure))
