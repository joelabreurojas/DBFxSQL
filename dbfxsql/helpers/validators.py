from collections.abc import Iterable
from pathlib import Path

from watchfiles import Change

from ..helpers import file_manager, formatters


def path_exists(filepath: str) -> bool:
    path: Path = Path(filepath)

    return path.exists()


def field_name_in(fields: Iterable[tuple[str, str]], field_name_: str) -> str:
    for field in fields:
        field_name: str = field[0]

        if field_name_.lower() == field_name.lower():
            return field_name

    return ""


def same_rows(
    origin_row: dict, destiny_row: dict, fields: tuple[list[str], list[str]]
) -> bool:
    for origin_field, destiny_field in zip(*fields):
        if origin_row[origin_field] != destiny_row[destiny_field]:
            return False

    return True


def only_modified(change: Change, path: str) -> bool:
    return change == Change.modified


def values_are_different(rows: list[dict], row_: dict) -> bool:
    """Checks if a list of rows are different from a given row."""

    for row in rows:
        for key, value in row_.items():
            if value != row[key]:
                return True

    return False


def valid_filepath(
    filepath_: str, engines: dict[str, dict[str, list[str] | str]]
) -> bool:
    filepath = Path(filepath_)

    extension: str = filepath.suffix
    folderpath: str = str(filepath.resolve().parent)

    for engine in engines.values():
        folderpaths: list[str] = [str(Path(f).resolve()) for f in engine["folderpaths"]]

        if extension in engine["extensions"]:
            if folderpath in folderpaths:
                return True

    return False


def check_engine(filename: str) -> str:
    extension: str = formatters.decompose_file(filename)[1]
    engines: dict[str, dict[str, list[str] | str]] = file_manager.load_config()[
        "engines"
    ]

    for engine_name, engine_config in engines.items():
        if extension in engine_config["extensions"]:
            return engine_name

    return ""
