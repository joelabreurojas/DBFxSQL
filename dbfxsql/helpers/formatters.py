import decimal
from collections.abc import Iterable

from . import file_manager, validators, utils
from ..constants.data_types import DATA_TYPES
from ..models.sync_table import SyncTable
from ..exceptions.field_errors import FieldNotFound
from ..exceptions.value_errors import ValueNotValid

from pathlib import Path


def decompose_file(filename: str) -> tuple[str, str]:
    """Decomposes a file into its stem and suffix."""

    return Path(filename).stem, Path(filename).suffix


def add_folderpath(engine: str, filename: str) -> str:
    """Adds the folderpath to the filename depending on the engine."""
    engines: str = file_manager.load_config()["engines"]
    folderpath: str = engines[engine]["folderpaths"][0]

    if not folderpath.endswith("/"):
        folderpath += "/"

    return folderpath + filename


def fields_to_str(fields: Iterable[tuple[str, str]], sep: str = ", ") -> str:
    return sep.join([f"{field[0]} {field[1]}" for field in fields])


def fields_to_dict(fields: Iterable[tuple[str, str]]) -> dict:
    return {field[0]: field[1] for field in fields}


def fields_to_tuple(fields: dict) -> tuple:
    return tuple(fields.items())


def assign_types(engine: str, types_: dict[str, str], row: dict[str, str]) -> dict:
    data_type: dict = DATA_TYPES[engine]

    field_names: list[str] = [field.lower() for field in row.keys()]
    type_names: list[str] = [type_.lower() for type_ in types_.keys()]

    for field in field_names:
        if field not in type_names:
            raise FieldNotFound(field)

        type_: str = types_[field].upper()
        value: str = _apply_type_cases(field, row[field], type_)

        try:
            row[field] = data_type[type_](value)

        except (ValueError, AttributeError, KeyError, decimal.InvalidOperation):
            raise ValueNotValid(field, value, type_)

    return row


def deglose_fields(row: dict, start: str, end: str) -> tuple:
    keys: list = [str(key) for key in row.keys()]

    field_names: str = ", ".join(keys)  # [key]
    values: str = start + f"{end}, {start}".join(keys) + end  # [:key]

    return field_names, values


def merge_fields(row: dict, start: str, end: str) -> str:
    return ", ".join([f"{key} = {start}{key}{end}" for key in row.keys()])


def scourgify_rows(rows: list[dict]) -> list[dict]:
    """Convert fields to lowercase and stripping values."""

    lower_fields: list[str] = [key.lower() for key in rows[0].keys()]

    for row in rows:
        for key in row.keys():
            row[key] = row[key].rstrip() if isinstance(row[key], str) else row[key]

    return [dict(zip(lower_fields, row.values())) for row in rows]


def quote_values(engine: str, types: dict[str, str], condition: tuple) -> tuple:
    field, operator, value = condition

    if field == "row_number":
        return field, operator, value

    if field not in types:
        raise FieldNotFound(field)

    if "==" == operator:
        operator = "="

    type_: str = types[field].upper()

    # SQL
    if DATA_TYPES[engine][type_] is str:
        value = f"'{value}'"

    return field, operator, value


def filter_rows(rows_: list, condition: tuple) -> tuple[list, list]:
    filter: str = ""
    rows: list = []
    indexes: list = []

    field, operator, value = _parse_condition(condition)

    if "==" == operator and "row_number" == field:
        return [rows_[value]], [value]

    for index, row in enumerate(rows_):
        if isinstance(row[field], str):
            filter = f"'{row[field]}'{operator}'{value}'"
        else:
            filter = f"{row[field]}{operator}{value}"

        if eval(filter):
            rows.append(row)
            indexes.append(index)

    return rows, indexes


def scourgify_types(types: list[dict[str, str]]) -> dict[str, str]:
    names: list = [type_["name"] for type_ in types]
    data_structure: list = [type_["type"] for type_ in types]

    return dict(zip(names, data_structure))


def depurate_empty_rows(rows: list[dict]) -> list:
    """Return an empty list if a list of rows only contains empty rows."""

    if not rows:
        return rows

    if [{""}] == [{row for row in rows.values()} for rows in rows]:
        return []

    return rows


def relevant_filenames(filenames: list[str], relations: list[dict]) -> list[str]:
    relevant_filenames: list = []

    for filename in filenames:
        if filename := _search_filenames(filename, relations):
            relevant_filenames.append(filename)

    return relevant_filenames


def package_changes(filenames: list[str], relations: list[dict]) -> list[dict]:
    changes: list = []

    for filename in filenames:
        origin_tables: dict = _parse_origin(filename, relations)

        for name in origin_tables.keys():
            origin_data: SyncTable = origin_tables[name]["data"]
            origin_fields: list = origin_tables[name]["fields"]
            destinies: list = origin_tables[name]["destinies"]

            origin: SyncTable = SyncTable(
                engine=origin_data.engine,
                source=origin_data.source,
                name=origin_data.name,
                fields=origin_fields,
            )

            changes.append({"origin": origin, "destinies": destinies})

    return changes


def _parse_origin(filename: str, relations: list[dict]) -> dict:
    origin_tables: dict = {}

    for relation in relations:
        if filename in relation["sources"]:
            tables: list[SyncTable, SyncTable] = _parse_tables(relation)
            origin, destiny = _define_tables(tables, filename)

            if not destiny:
                continue

            if origin.name in origin_tables.keys():
                origin_tables[origin.name]["fields"].append(origin.fields)
                origin_tables[origin.name]["destinies"].append(destiny)
            else:
                origin_tables[origin.name] = {
                    "data": origin,
                    "fields": [origin.fields],
                    "destinies": [destiny],
                }

    return origin_tables


def compare_tables(origin: SyncTable, destinies: list[SyncTable]) -> list:
    residual_tables: list = []

    for origin_fields, destiny in zip(origin.fields, destinies):
        fields: tuple = (origin_fields, destiny.fields)
        rows: tuple = (origin.rows, destiny.rows)

        residual_origin, residual_destiny = _compare_rows(*rows, fields)

        for residual in residual_origin:
            residual["fields"] = _depurate_fields(residual["fields"], origin_fields)
            residual["fields"] = _change_fields(residual["fields"], destiny.fields)

        residual_tables.append((residual_origin, residual_destiny))

    return residual_tables


def _depurate_fields(row: list, fields: list) -> list[dict]:
    return {key: value for key, value in row.items() if key in fields}


def _change_fields(row: list, fields: list) -> list[dict]:
    return {key: value for key, value in zip(fields, row.values())}


def parse_filepaths(changes: list[set]) -> list:
    """Retrieves the modified file from the environment variables."""

    filenames: list = []

    for change in changes:
        filepath: str = change[-1]
        name, extension = decompose_file(filepath)
        filenames.append(f"{name}{extension}")

    return filenames


def classify_operations(residual_tables: tuple) -> list:
    operations: list = []

    for residual_table in residual_tables:
        origin, destiny = residual_table

        origin_range: int = len(origin)
        destiny_range: int = len(destiny)

        insert: list = [{"fields": row["fields"]} for row in origin[destiny_range:]]

        delete: list = [{"index": row["index"]} for row in destiny[origin_range:]]

        update: list = [
            {"index": destiny_row["index"], "fields": origin_row["fields"]}
            for origin_row, destiny_row in zip(origin, destiny)
        ]

        operations.append({"insert": insert, "update": update, "delete": delete})

    return operations


def _compare_rows(origin_rows: list, destiny_rows: list, fields: tuple) -> tuple:
    residual_origin: list = []
    residual_destiny: list = [
        {"index": index, "fields": fields} for index, fields in enumerate(destiny_rows)
    ]

    origin_range: int = len(origin_rows)
    destiny_range: int = len(destiny_rows)

    origin_index: int = 0

    while origin_index < origin_range:
        destiny_index: int = 0
        origin_row: dict = origin_rows[origin_index]

        if not destiny_range:
            residual_origin.append({"index": origin_index, "fields": origin_row})

        while destiny_index < destiny_range:
            destiny_row: dict = residual_destiny[destiny_index]["fields"]

            if validators.same_rows(origin_row, destiny_row, fields):
                # New list skipping then existent index

                residual_destiny = (
                    residual_destiny[:destiny_index]
                    + residual_destiny[destiny_index + 1 :]
                )

                destiny_range -= 1
                break

            if destiny_index == destiny_range - 1:
                residual_origin.append({"index": origin_index, "fields": origin_row})

            destiny_index += 1
        origin_index += 1

    return residual_origin, residual_destiny


def _search_filenames(filename: str, relations: list[dict]) -> str | None:
    for relation in relations:
        if filename in relation["sources"]:
            return filename


def _apply_type_cases(field: str, value: str, type_: str) -> str:
    # Logical case
    if "N" == type_ and value is None:
        value = "0"

    if "L" == type_ and ("True" != value != "False"):
        raise ValueNotValid(value, field, "bool")

    # Date/Datetime case
    if "D" == type_ or "@" == type_:
        value.replace("/", "-")

    return value


def _parse_condition(condition: tuple[str, str, str]) -> tuple:
    field, operator, value = condition

    if "=" == operator:
        operator = "=="

    try:
        if "row_number" == field.lower():
            value = int(value) - 1

    except ValueError:
        raise ValueNotValid(value, field, "int")

    return field, operator, value


def _parse_tables(relation: dict) -> list[SyncTable, SyncTable]:
    tables: list = []

    for index, _ in enumerate(relation["sources"]):
        table: SyncTable = SyncTable(
            engine=utils.check_engine(relation["sources"][index]),
            source=relation["sources"][index],
            name=relation["tables"][index],
            fields=relation["fields"][index],
        )

        tables.append(table)

    return tables


def _define_tables(tables: list[SyncTable], filename: str) -> tuple:
    origin: SyncTable = None
    destiny: SyncTable = None

    for table in tables:
        if filename == table.source:
            origin = table
        else:
            destiny = table

    return origin, destiny


def _insert_rows(origin: list[dict], destiny: list[dict]) -> list:
    return origin[len(destiny) :]


def _delete_rows(origin: list[dict], destiny: list[dict], limit: int = 0) -> tuple:
    return origin[len(destiny) :], origin[:limit]


def _update_rows(origin: list[dict], destiny: list[dict]) -> list:
    return origin
