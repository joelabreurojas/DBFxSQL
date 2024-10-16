from .dbf_connection import get_table

import dbf


def create(sourcepath: str, fields: str) -> None:
    with get_table(sourcepath) as table:
        table.add_fields(fields)


def insert(sourcepath: str, record: dict) -> None:
    with get_table(sourcepath) as table:
        table.append(record)


def read(sourcepath: str) -> list[dict]:
    with get_table(sourcepath) as table:
        field_names: list[str] = [field.lower() for field in table.field_names]

        records: list[dict] = [dict(zip(field_names, record)) for record in table]

    return records if records else [{field: "" for field in field_names}]


def update(sourcepath: str, record: dict, indexes: list[int]) -> None:
    with get_table(sourcepath) as table:
        for index in indexes:
            with table[index] as row:
                for key, value in record.items():
                    setattr(row, key, value)


def delete(sourcepath: str, indexes: list[int]) -> None:
    with get_table(sourcepath) as table:
        for index in indexes:
            with table[index] as row:
                dbf.delete(row)

        table.pack()


def fetch_types(sourcepath) -> dict[str, str]:
    names: list = []
    data_structure: list = []

    with get_table(sourcepath) as table:
        for i in range(table.field_count):
            names.append(table._field_layout(i).lower().split(" ")[0])
            data_structure.append(table._field_layout(i).split(" ")[-1][0])

    return dict(zip(names, data_structure))
