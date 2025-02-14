from collections.abc import Iterable
from datetime import date, datetime
from pathlib import Path

from dbf.data_types import NullType

from ..constants.data_types import DATA_TYPES
from ..exceptions.field_errors import FieldNotFound
from ..exceptions.value_errors import ValueNotValid
from ..models.sync_table import SyncTable
from . import file_manager, validators


def decompose_file(filename: str) -> tuple[str, str]:
    """Decomposes a file into its stem and suffix."""

    return Path(filename).stem, Path(filename).suffix


def add_folderpath(engine: str, filename: str) -> str:
    """Adds the folderpath to the filename depending on the engine."""
    engines: dict[str, dict[str, list[str] | str]] = file_manager.load_config()[
        "engines"
    ]
    folderpath: str = engines[engine]["folderpaths"][0]

    return str(Path(folderpath).resolve() / filename)


def fields_to_str(fields: Iterable[tuple[str, str]], sep: str = ", ") -> str:
    return sep.join([f"{field[0]} {field[1]}" for field in fields])


def fields_to_dict(fields: Iterable[tuple[str, str]]) -> dict:
    return {field[0]: field[1] for field in fields}


def _fields_to_tuple(fields: dict[str, str]) -> tuple[tuple[str, str], ...]:
    return tuple(fields.items())


def assign_types(engine: str, types_: dict[str, str], row: dict[str, str]) -> dict:
    data_type: dict[str, type] = DATA_TYPES[engine]

    field_names: list[str] = [field.lower() for field in row.keys()]
    type_names: list[str] = [type_.lower() for type_ in types_.keys()]

    for field in field_names:
        if field not in type_names:
            raise FieldNotFound(field)

        type_: str = types_[field].upper()
        value: str = row[field]

        try:
            # date case
            if value and data_type[type_] is date:
                if type(value) is str:
                    iso_date: date = date.fromisoformat(value)
                    row[field] = iso_date.strftime("%Y-%m-%d")

            # datetime case
            elif value and data_type[type_] is datetime:
                if type(value) is str:
                    iso_datetime: datetime = datetime.fromisoformat(value)
                    row[field] = iso_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # NullType case
            elif type(value) is NullType:
                row[field] = ""

            # other cases
            elif value:
                row[field] = data_type[type_](value)

        except ValueError:
            raise ValueNotValid(field, value, type_)

    return row


def deglose_fields(row: dict, start: str, end: str) -> tuple[str, str]:
    keys: list[str] = [str(key) for key in row.keys()]

    field_names: str = ", ".join(keys)  # [key]
    values: str = start + f"{end}, {start}".join(keys) + end  # [:key]

    return field_names, values


def merge_fields(row: dict, start: str, end: str) -> str:
    return ", ".join([f"{key} = {start}{key}{end}" for key in row.keys()])


def scourgify_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Convert fields to lowercase and stripping values."""

    lower_fields: list[str] = [key.lower() for key in rows[0].keys()]

    for row in rows:
        for key in row.keys():
            row[key] = row[key].rstrip() if isinstance(row[key], str) else row[key]

    return [dict(zip(lower_fields, row.values())) for row in rows]


def quote_values(
    engine: str, types: dict[str, str], condition: tuple[str, str, str]
) -> tuple[str, str, str]:
    field, operator, value = condition

    if "==" == operator:
        operator = "="

    if field == "row_number":
        return field, operator, value

    if field not in types:
        raise FieldNotFound(field)

    type_: str = types[field].upper()

    # SQL
    if DATA_TYPES[engine][type_] is str:
        value = f"'{value}'"

    return field, operator, value


def filter_rows(
    rows_: list[dict], condition: tuple[str, str, str]
) -> tuple[list[dict], list[int]]:
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
    names: list[str] = [type_["name"] for type_ in types]
    data_structure: list[str] = [type_["type"] for type_ in types]

    return dict(zip(names, data_structure))


def depurate_empty_rows(rows: list[dict]) -> list:
    """Return an empty list if a list of rows only contains empty rows."""

    if not rows:
        return rows

    if all(all(not value for value in row.values()) for row in rows):
        return []

    return rows


def relevant_filenames(
    filenames: list[str], relations: list[dict[str, list[str] | str]]
) -> list[str]:
    relevant_filenames: list = []

    for filename in filenames:
        if filename := _search_filenames(filename, relations):
            relevant_filenames.append(filename)

    return relevant_filenames


def package_changes(
    filenames: list[str], relations: list[dict[str, list[str] | str]]
) -> list[dict[str, SyncTable | list[SyncTable]]]:
    changes: list = []

    for filename in filenames:
        origin_tables: dict = _parse_origin(filename, relations)

        for name in origin_tables.keys():
            origin_data: SyncTable = origin_tables[name]["data"]
            origin_fields: list[str] = origin_tables[name]["fields"]
            destinies: list[SyncTable] = origin_tables[name]["destinies"]

            origin: SyncTable = SyncTable(
                engine=origin_data.engine,
                source=origin_data.source,
                name=origin_data.name,
                fields=origin_fields,
            )

            changes.append({"origin": origin, "destinies": destinies})

    return changes


def _parse_origin(filename: str, relations: list[dict[str, list[str] | str]]) -> dict:
    origin_tables: dict = {}

    for relation in relations:
        if filename in relation["sources"]:
            tables: list[SyncTable] = _parse_tables(relation)
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


def compare_tables(
    origin: SyncTable, destinies: list[SyncTable]
) -> list[tuple[list[dict], list[dict]]]:
    residual_tables: list = []

    for origin_fields, destiny in zip(origin.fields, destinies):
        fields: tuple[list[str], list[str]] = (origin_fields, destiny.fields)

        origin_rows: list[dict] = list(origin.rows)
        destiny_rows: list[dict] = list(destiny.rows)

        residual_origin, residual_destiny = _compare_rows(
            origin_rows, destiny_rows, fields
        )

        for residual in residual_origin:
            residual["fields"] = _depurate_fields(
                residual["fields"], list(origin_fields)
            )
            residual["fields"] = _change_fields(residual["fields"], destiny.fields)

        residual_tables.append((residual_origin, residual_destiny))

    return residual_tables


def _depurate_fields(row: dict, fields: list[str]) -> dict:
    """
    Remove the keys not in the fields
    """

    return {key: row[key] for key in fields}


def _change_fields(row: dict, fields: list[str]) -> dict:
    """
    Change the dict keys to the fields received
    """

    return {key: value for key, value in zip(fields, row.values())}


def filter_filepaths(
    changes: list[list[str]], engines: dict[str, dict[str, list[str] | str]]
) -> list:
    filepaths: list = []

    for change in changes:
        filepath: str = change[-1]

        if isinstance((listened := engines["MSSQL"]["listen"]), str):
            if filepath.endswith(listened):
                filepath = filepath.replace(listened, engines["MSSQL"]["extensions"][0])

            if validators.valid_filepath(filepath, engines):
                filepaths.append(filepath)

    return filepaths


def parse_filenames(filepaths: list[str]) -> list[str]:
    filenames: list = []

    for filepath in filepaths:
        name, extension = decompose_file(filepath)
        filenames.append(f"{name}{extension}")

    return filenames


def classify_operations(
    residual_tables: list[tuple[list[dict], list[dict]]],
) -> list[dict[str, list[dict]]]:
    operations: list = []

    for residual_table in residual_tables:
        origin, destiny = residual_table

        origin_range: int = len(origin)
        destiny_range: int = len(destiny)

        insert: list[dict] = [
            {"fields": row["fields"]} for row in origin[destiny_range:]
        ]

        delete: list[dict] = [
            {"index": row["index"]} for row in destiny[origin_range:][::-1]
        ]

        update: list[dict] = [
            {
                "index": destiny_row["index"],
                "fields": _residual_rows(origin_row["fields"], destiny_row["fields"]),
            }
            for origin_row, destiny_row in zip(origin, destiny)
        ]

        operations.append({"delete": delete, "update": update, "insert": insert})

    return operations


def _residual_rows(destiny_row: dict, origin_row: dict) -> dict:
    return {
        key: value for key, value in destiny_row.items() if value != origin_row[key]
    }


def _compare_rows(
    origin_rows: list, destiny_rows: list, fields_: tuple
) -> tuple[list[dict], list[dict]]:
    residual_origin: list = []
    residual_destiny: list = [
        {"index": index, "fields": fields}
        for index, fields in enumerate(destiny_rows, start=1)
    ]

    origin_range: int = len(origin_rows)
    destiny_range: int = len(destiny_rows)

    origin_index: int = 0

    while origin_index < origin_range:
        destiny_index: int = 0
        origin_row: dict = origin_rows[origin_index]

        if not destiny_range:
            residual_origin.append({"index": origin_index + 1, "fields": origin_row})

        while destiny_index < destiny_range:
            destiny_row: dict = residual_destiny[destiny_index]["fields"]

            if validators.same_rows(origin_row, destiny_row, fields_):
                # New list skipping then existent index

                residual_destiny = (
                    residual_destiny[:destiny_index]
                    + residual_destiny[destiny_index + 1 :]
                )

                destiny_range -= 1
                break

            if destiny_index == destiny_range - 1:
                residual_origin.append(
                    {"index": origin_index + 1, "fields": origin_row}
                )

            destiny_index += 1
        origin_index += 1

    return residual_origin, residual_destiny


def _search_filenames(filename: str, relations: list[dict]) -> str:
    for relation in relations:
        if filename in relation["sources"]:
            return filename

    return ""


def _parse_condition(condition: tuple[str, str, str]) -> tuple:
    field: str = condition[0]
    operator: str = condition[1]
    value: int | str = condition[2]

    if "=" == operator:
        operator = "=="

    try:
        if "row_number" == field.lower():
            value = int(value) - 1

    except ValueError:
        raise ValueNotValid(value, field, "int")

    return field, operator, value


def _parse_tables(relation: dict) -> list:
    tables: list = []

    for index, _ in enumerate(relation["sources"]):
        table: SyncTable = SyncTable(
            engine=validators.check_engine(relation["sources"][index]),
            source=relation["sources"][index],
            name=relation["tables"][index],
            fields=relation["fields"][index],
        )

        tables.append(table)

    return tables


def _define_tables(tables: list[SyncTable], filename: str) -> tuple:
    for table in tables:
        if filename == table.source:
            origin: SyncTable = table
        else:
            destiny: SyncTable = table

    return origin, destiny


def extract_data(name: str, dataset: list[dict], destiny: SyncTable) -> list[dict]:
    values: list = []

    for data in dataset:
        value: dict = {
            "engine": destiny.engine,
            "filename": destiny.source,
            "table": destiny.name,
        }

        if "delete" != name:
            value["fields"] = fields_to_tuple(data["fields"])

        if "insert" != name:
            value["index"] = data["index"]

        values.append(value)

    return values


def get_filenames(
    engines: dict[str, dict[str, list[str] | str]],
    relations: list[dict[str, list[str] | str]],
) -> dict:
    """
    Returns a dict with the filenames based on the engines
    """
    paths: list = []

    for engine in engines.values():
        files: list = []

        for folder in list(set(engine["folderpaths"])):
            for path in Path(folder).iterdir():
                files.append("".join(decompose_file(path)))

        paths.append(files)

    return dict(zip(engines.keys(), paths))


def get_mssql_entities(relations: list[dict]) -> dict:
    entities: dict = {}

    for relation in relations:
        for index, filename in enumerate(relation["sources"]):
            if "MSSQL" == validators.check_engine(filename):
                if filename not in entities.keys():
                    entities[filename] = []

                entities[filename].append(relation["tables"][index])

    return entities


def db_to_tmp(
    engines: dict[str, dict[str, list[str] | str]], databases: list
) -> list[str]:
    extension: str = engines["MSSQL"]["extensions"][0]

    filepaths: list = []

    for database in databases:
        for folderpath in engines["MSSQL"]["folderpaths"]:
            if validators.path_exists(f"{folderpath}{database}"):
                tmp_file: str = database.replace(extension, ".tmp")
                filepaths.append(f"{folderpath}{tmp_file}")

    return filepaths
