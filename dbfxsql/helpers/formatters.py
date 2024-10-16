import decimal

from . import file_manager
from ..constants.data_types import DATA_TYPES
from ..models.sync_table import SyncTable
from ..exceptions.value_errors import ValueNotFound, ValueNotValid


def fields_to_str(fields: tuple[tuple], sep: str = ", ") -> str:
    return sep.join([f"{field[0]} {field[1]}" for field in fields])


def fields_to_dict(fields: tuple[tuple]) -> dict:
    return {field[0]: field[1] for field in fields}


def assign_types(engine: str, _types: dict[str, str], record: dict[str, str]) -> dict:
    data_type: dict = DATA_TYPES[engine]

    field_names: list[str] = [field.lower() for field in record.keys()]
    type_names: list[str] = [_type.lower() for _type in _types.keys()]

    for field in field_names:
        if field not in type_names:
            raise ValueNotFound(field)

        _type: str = _types[field]
        value: str = _apply_type_cases(field, record[field], _type)

        try:
            record[field] = data_type[_type](value)

        except (ValueError, AttributeError, decimal.InvalidOperation):
            raise ValueNotValid(field, value, _type)

    return record


def _apply_type_cases(field: str, value: str, _type: str) -> str:
    # Logical case
    if "L" == _type and ("True" != value != "False"):
        raise ValueNotValid(value, field, "bool")

    # Date/Datetime case
    if "D" == _type or "@" == _type:
        value.replace("/", "-")

    return value


def scourgify_records(records: list[dict]) -> list[dict]:
    """Convert fields to lowercase and stripping values."""

    lower_fields: list[str] = [key.lower() for key in records[0].keys()]

    for record in records:
        for key in record.keys():
            record[key] = (
                record[key].rstrip() if isinstance(record[key], str) else record[key]
            )

    return [dict(zip(lower_fields, record.values())) for record in records]


def filter_records(_records: list, condition: tuple) -> tuple[list, list]:
    filter: str = ""
    records: list = []
    indexes: list = []

    field, condition, value = _parse_condition(condition)

    for index, record in enumerate(_records):
        if isinstance(record[field], str):
            filter = f"'{record[field]}'{condition}'{value}'"
        else:
            filter = f"{record[field]}{condition}{value}"

        if eval(filter):
            records.append(record)
            indexes.append(index)

    return records, indexes


def _parse_condition(condition: tuple[str, str, str]) -> tuple:
    field, operator, value = condition

    if "=" == operator:
        operator = "=="

    return field, operator, value


def values_are_different(records: list[dict], record: dict) -> bool:
    """Checks if a list of records are different from a given record."""

    for _record in records:
        for key, value in record.items():
            if value != _record[key]:
                return True

    return False


def depurate_empty_records(records: list[dict]) -> list:
    """Return an empty list if a list of records only contains empty records."""

    if not records:
        return records

    if [{""}] == [{record for record in records.values()} for records in records]:
        return []

    return records


def parse_filepaths(changes: list[set]) -> list:
    """Retrieves the modified file from the environment variables."""

    filenames: list = []

    for change in changes:
        filepath: str = change[-1]
        name, extension = file_manager.decompose_filename(filepath)
        filenames.append(name + extension)

    return filenames


def package_fields(origin: SyncTable, destiny: SyncTable) -> tuple[str, str]:
    """Returns a tuple of fields to be compared."""

    return zip(origin.fields[0].split(", "), destiny.fields[0].split(", "))


def copy_with_indexed_field(table: SyncTable, index: int) -> SyncTable:
    return SyncTable(
        name=table.name,
        source=table.source,
        fields=[table.fields[index]],
        records=table.records[:],
    )


def parse_extensions(relations: list[dict]) -> list[str]:
    """Returns a list of extensions from a list of relations."""
    extensions: list = []

    for relation in relations:
        extensions.append(file_manager.decompose_filename(relation["source"])[1])

    print(extensions)
