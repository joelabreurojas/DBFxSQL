import decimal
from collections.abc import Iterable

from . import file_manager
from ..constants.data_types import DATA_TYPES
from ..models.sync_table import SyncTable
from ..exceptions.field_errors import FieldNotFound
from ..exceptions.value_errors import ValueNotValid

from pathlib import Path


def decompose_filename(file: str) -> tuple[str, str]:
    """Decomposes a filename into its stem and suffix."""

    return Path(file).stem, Path(file).suffix


def add_folderpath(engine: str, source: str) -> str:
    """Adds the folderpath to the source depending on the engine."""
    folderpath: str = file_manager.load_config()["folderpaths"][engine][0]

    if not folderpath.endswith("/"):
        folderpath += "/"

    return folderpath + source


def fields_to_str(fields: Iterable[tuple[str, str]], sep: str = ", ") -> str:
    return sep.join([f"{field[0]} {field[1]}" for field in fields])


def fields_to_dict(fields: Iterable[tuple[str, str]]) -> dict:
    return {field[0]: field[1] for field in fields}


def assign_types(engine: str, _types: dict[str, str], row: dict[str, str]) -> dict:
    data_type: dict = DATA_TYPES[engine]

    field_names: list[str] = [field.lower() for field in row.keys()]
    type_names: list[str] = [_type.lower() for _type in _types.keys()]

    for field in field_names:
        if field not in type_names:
            raise FieldNotFound(field)

        _type: str = _types[field]
        value: str = _apply_type_cases(field, row[field], _type)

        try:
            row[field] = data_type[_type](value)

        except (ValueError, AttributeError, decimal.InvalidOperation):
            raise ValueNotValid(field, value, _type)

    return row


def deglose_fields(row: dict) -> tuple:
    keys: list = [str(key) for key in row.keys()]

    field_names: str = ", ".join(keys)  # [key]
    values: str = ":" + ", :".join(keys)  # [:key]

    return field_names, values


def merge_fields(fields: tuple[str, str], sep: str) -> str:
    field_names, values = fields

    return sep.join([field_names, values])


def scourgify_rows(rows: list[dict]) -> list[dict]:
    """Convert fields to lowercase and stripping values."""

    lower_fields: list[str] = [key.lower() for key in rows[0].keys()]

    for row in rows:
        for key in row.keys():
            row[key] = row[key].rstrip() if isinstance(row[key], str) else row[key]

    return [dict(zip(lower_fields, row.values())) for row in rows]


def filter_rows(rows: list, condition: tuple) -> tuple[list, list]:
    filter: str = ""
    _rows: list = []
    indexes: list = []

    field, operator, value = _parse_condition(condition)

    if "==" == operator and "row_number" == field:
        return [rows[value]], [value]

    for index, row in enumerate(rows):
        if isinstance(row[field], str):
            filter = f"'{row[field]}'{operator}'{value}'"
        else:
            filter = f"{row[field]}{operator}{value}"

        if eval(filter):
            _rows.append(row)
            indexes.append(index)

    return _rows, indexes


def scourgify_types(types: list[dict[str, str]]) -> dict[str, str]:
    names: list = [type["name"] for type in types]
    data_structure: list = [type["type"] for type in types]

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


def package_tables(filenames: list[str], relations: list[dict]) -> list[dict]:
    origins: list = []
    destinies: list = []

    origin: SyncTable = None
    destiny: SyncTable = None

    for filename in filenames:
        for relation in relations:
            if filename in relation["sources"]:
                tables = _parse_tables(relation, filename)
                origin, destiny = _define_tables(tables, filename)

                origins.append(origin)
                destinies.append(destiny)

    return origins, destinies


def compare_tables(origin: SyncTable, destinies: list[SyncTable]) -> tuple:
    residual_tables: list = []

    if not origin.rows:
        return residual_tables

    for index, destiny in enumerate(destinies):
        if not destiny.rows:
            continue

        _origin: SyncTable = SyncTable(
            engine=origin.engine,
            source=origin.source,
            name=origin.name,
            fields=origin.fields[index],
            rows=origin.rows,
        )

        residual_tables.append(_compare_rows(_origin, destiny))

    return residual_tables


def classify_operations(residual_tables: list) -> tuple:
    return (None,)


def _compare_rows(origin: SyncTable, destiny: SyncTable) -> tuple:
    fields: tuple = (origin.fields, destiny.fields)
    residual_destiny: list = []
    destiny_indexes: list = []

    residual_origin: list = []
    origin_indexes: list = []

    for origin_index, origin_row in enumerate(origin.rows):
        for destiny_index, destiny_row in enumerate(destiny.rows):
            if not __same_rows(origin_row, destiny_row, fields):
                residual_destiny.append(destiny_row)
                destiny_indexes.append(destiny_index)

        residual_origin.append(origin_row)
        origin_indexes.append(origin_index)

    _origin: SyncTable = SyncTable(
        engine=origin.engine,
        source=origin.source,
        name=origin.name,
        fields=origin.fields,
        rows=residual_origin,
        indexes=origin_indexes,
    )

    _destiny: SyncTable = SyncTable(
        engine=destiny.engine,
        source=destiny.source,
        name=destiny.name,
        fields=destiny.fields,
        rows=residual_destiny,
        indexes=destiny_indexes,
    )

    return _origin, _destiny


def __same_rows(origin_row: dict, destiny_row: dict, fields: tuple) -> bool:
    for origin_field, destiny_field in zip(*fields):
        if origin_row[origin_field] != destiny_row[destiny_field]:
            return False

    return True


def _search_filenames(filename: str, relations: list[dict]) -> str | None:
    for relation in relations:
        if filename in relation["sources"]:
            return filename


def _apply_type_cases(field: str, value: str, _type: str) -> str:
    # Logical case
    if "L" == _type and ("True" != value != "False"):
        raise ValueNotValid(value, field, "bool")

    # Date/Datetime case
    if "D" == _type or "@" == _type:
        value.replace("/", "-")

    return value


def _parse_condition(condition: tuple[str, str, str]) -> tuple:
    field, operator, value = condition

    if "=" == operator:
        operator = "=="

    try:
        if "rowid" == field.lower() or "row_number" == field.lower():
            value = int(value) - 1

    except ValueError:
        raise ValueNotValid(value, field, "int")

    return field, operator, value


def _parse_tables(relation: dict, filename: str) -> list[SyncTable, SyncTable]:
    tables: list[SyncTable] = []

    for index, _ in enumerate(relation["sources"]):
        table: SyncTable = SyncTable(
            engine=relation["engines"][index],
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
