from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from dbf.data_types import NullType

from ..constants.data_types import DATA_TYPES
from ..exceptions import FieldNotFound, FolderPathNotProvided, ValueNotValid
from ..models import Condition, Config, Engine, Relation, SyncTable
from . import file_manager, validators
from .alias import (
    ChangeDict,
    ChangesList,
    FieldsIterable,
    FieldsTuple,
    FilesDict,
    OperationsList,
    RowsIndexesTuple,
    SyncTableDict,
    TablesDict,
    TablesTuple,
    TypesList,
    VariableFieldsTuple,
)


def add_folderpath(engine_: str, filename: str) -> str:
    """Adds the folderpath to the filename depending on the engine."""
    config: Config = file_manager.load_config()
    engine: Engine = Engine(**config.engines[engine_])
    folderpath: str = engine.folderpaths[0]

    if not folderpath:
        raise FolderPathNotProvided(engine_)

    return str(Path(folderpath).resolve() / filename)


def assign_types(engine: str, types: dict[str, str], row: dict[str, Any]) -> dict:
    data_type: dict[str, type] = DATA_TYPES[engine]

    field_names: list[str] = [field.lower() for field in row.keys()]
    type_names: list[str] = [type_.lower() for type_ in types.keys()]

    for field in field_names:
        if field not in type_names:
            raise FieldNotFound(field)

        type_: str = types[field].upper()
        value: Any = row[field]

        try:
            # date case
            if value and data_type[type_] is date:
                if type(value) is str:
                    row[field] = date.fromisoformat(value)

            # datetime case
            elif value and data_type[type_] is datetime:
                if type(value) is str:
                    row[field] = datetime.fromisoformat(value)

            # Decimal case
            elif value and data_type[type_] is Decimal:
                row[field] = data_type[type_](str(value))

            # NullType case
            elif type(value) is NullType:
                row[field] = ""

            # other cases
            elif value:
                row[field] = data_type[type_](value)

        except ValueError:
            raise ValueNotValid(field, value, type_)

    return row


def classify_operations(residual_tables: list[TablesTuple]) -> OperationsList:
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


def compare_tables(origin: SyncTable, destinies: list[SyncTable]) -> list[TablesTuple]:
    residual_tables: list = []

    for origin_fields, destiny in zip(origin.fields, destinies):
        fields: FieldsTuple = (origin_fields, destiny.fields)

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


def db_to_tmp(engines: dict[str, Engine], databases: list[str]) -> list[str]:
    engine: Engine = engines["MSSQL"]
    extension: str = engine.extensions[0]

    filepaths: list = []

    for database in databases:
        for folderpath in engine.folderpaths:
            if validators.path_exists(f"{folderpath}{database}"):
                tmp_file: str = database.replace(extension, ".tmp")
                filepaths.append(f"{folderpath}{tmp_file}")

    return filepaths


def decompose_file(filename: str) -> tuple[str, str]:
    """Decomposes a file into its stem and suffix."""

    return Path(filename).stem, Path(filename).suffix


def deglose_fields(row: dict, start: str, end: str) -> tuple[str, str]:
    keys: list[str] = [str(key) for key in row.keys()]

    field_names: str = ", ".join(keys)  # [key]
    values: str = start + f"{end}, {start}".join(keys) + end  # [:key]

    return field_names, values


def depurate_empty_rows(rows: list[dict]) -> list:
    """Return an empty list if a list of rows only contains empty rows."""

    if all(all(not value for value in row.values()) for row in rows):
        return []

    return rows


def extract_data(name: str, dataset: list[dict], destiny: SyncTable) -> list[dict]:
    values: list = []

    for data in dataset:
        value: dict = {
            "engine": destiny.engine,
            "filename": destiny.source,
            "table": destiny.name,
        }

        if "delete" != name:
            value["fields"] = _fields_to_tuple(data["fields"])

        if "insert" != name:
            value["index"] = data["index"]

        values.append(value)

    return values


def fields_to_dict(fields: FieldsIterable) -> dict:
    return {field[0]: field[1] for field in fields}


def fields_to_str(fields: FieldsIterable, sep: str = ", ") -> str:
    return sep.join([f"{field[0]} {field[1]}" for field in fields])


def filter_filepaths(changes: ChangesList, engines: dict[str, Engine]) -> list:
    filepaths: list = []

    for change in changes:
        filepath: str = change[-1]

        engine: Engine = engines["MSSQL"]
        to_convert: list = engine.convert_to_extension

        for suffix in to_convert:
            if filepath.endswith(suffix):
                filepath = filepath.replace(suffix, engine.extensions[0])

            if validators.valid_filepath(filepath, engines):
                filepaths.append(filepath)

    return filepaths


def filter_rows(rows_: list[dict], condition: Condition) -> RowsIndexesTuple:
    rows: list = []
    indexes: list = []

    for index, row in enumerate(rows_):
        if condition.compare(row, index):
            rows.append(row)
            indexes.append(index)

    return rows, indexes


def get_mssql_entities(relations: list[Relation]) -> TablesDict:
    entities: dict = {}

    for relation in relations:
        for index, filename in enumerate(relation.sources):
            if "MSSQL" == validators.check_engine(filename):
                if filename not in entities.keys():
                    entities[filename] = []

                entities[filename].append(relation.tables[index])

    return entities


def merge_fields(row: dict, start: str, end: str) -> str:
    return ", ".join([f"{key} = {start}{key}{end}" for key in row.keys()])


def normalize_row(row: dict) -> dict:
    """Convert empty values to None"""

    return {key: None if value == "" else value for key, value in row.items()}


def package_changes(
    filenames: list[str], relations: list[Relation]
) -> list[ChangeDict]:
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


def parse_filenames(filepaths: list[str]) -> list:
    filenames: list = []

    for filepath in filepaths:
        name, extension = decompose_file(filepath)
        filenames.append(f"{name}{extension}")

    return filenames


def prioritized_files(
    engines: dict[str, Engine], relations: list[Relation]
) -> list[str]:
    files: FilesDict = _get_filenames(engines, relations)

    filenames: list = []

    for relation in relations:
        if validators.should_add_filename(relation, files):
            filenames.append(relation.priority)

    return filenames


def quote_values(engine: str, types: dict[str, str], condition: Condition) -> Condition:
    if "row_number" == condition.field:
        return condition

    if condition.field not in types:
        raise FieldNotFound(condition.field)

    type_: str = types[condition.field].upper()
    data_type: type = DATA_TYPES[engine][type_]

    # SQL
    value: Any = f"'{condition.value}'" if data_type is str else condition.value

    return Condition(condition.field, condition.operator, value)


def relevant_filenames(filenames: list[str], relations: list[Relation]) -> list[str]:
    relevant_filenames: list = []

    for filename_ in filenames:
        if filename := _search_filenames(filename_, relations):
            relevant_filenames.append(filename)

    return relevant_filenames


def scourgify_rows(rows: list[dict]) -> list[dict]:
    """Convert fields to lowercase and stripping values."""

    lower_fields: list[str] = [key.lower() for key in rows[0].keys()]

    for row in rows:
        for key in row.keys():
            row[key] = row[key].rstrip() if isinstance(row[key], str) else row[key]

    return [dict(zip(lower_fields, row.values())) for row in rows]


def scourgify_types(types: TypesList) -> dict[str, str]:
    names: list[str] = [type_["name"] for type_ in types]
    data_structure: list[str] = [type_["type"] for type_ in types]

    return dict(zip(names, data_structure))


def _change_fields(row: dict, fields: list[str]) -> dict:
    """
    Change the dict keys to the fields received
    """

    return {key: value for key, value in zip(fields, row.values())}


def _compare_rows(
    origin_rows: list[dict], destiny_rows: list[dict], fields_: FieldsTuple
) -> TablesTuple:
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


def _define_tables(
    tables: list[SyncTable], filename: str
) -> tuple[SyncTable, SyncTable]:
    for table in tables:
        if filename == table.source:
            origin: SyncTable = table
        else:
            destiny: SyncTable = table

    return origin, destiny


def _depurate_fields(row: dict, fields: list[str]) -> dict:
    """
    Remove the keys not in the fields
    """

    return {key: row[key] for key in fields}


def _fields_to_tuple(fields: dict[str, str]) -> VariableFieldsTuple:
    return tuple(fields.items())


def _get_filenames(engines: dict[str, Engine], relations: list[Relation]) -> FilesDict:
    """
    Returns a dict with the filenames based on the engines
    """
    paths: list = []

    for engine in engines.values():
        files: list = []

        for folder in list(set(engine.folderpaths)):
            for path in Path(folder).iterdir():
                files.append("".join(decompose_file(path.as_posix())))

        paths.append(files)

    return dict(zip(engines.keys(), paths))


def _parse_origin(filename: str, relations: list[Relation]) -> SyncTableDict:
    origin_tables: dict = {}

    for relation in relations:
        if filename in relation.sources:
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


def _parse_tables(relation: Relation) -> list[SyncTable]:
    tables: list = []

    for index, _ in enumerate(relation.sources):
        if engine := validators.check_engine(relation.sources[index]):
            table: SyncTable = SyncTable(
                engine=engine,
                source=relation.sources[index],
                name=relation.tables[index],
                fields=relation.fields[index],
            )

        tables.append(table)

    return tables


def _residual_rows(origin_row: dict, destiny_row: dict) -> dict:
    return {
        key: value for key, value in origin_row.items() if value != destiny_row[key]
    }


def _search_filenames(filename: str, relations: list[Relation]) -> str | None:
    for relation in relations:
        if filename in relation.sources:
            return filename

    return None
