from pathlib import Path

from watchfiles import Change

from ..helpers import file_manager, formatters
from ..models import Config, Engine, Relation
from .alias import FieldsIterable, FieldsTuple, FilesDict


def check_engine(filename: str) -> str | None:
    extension: str = formatters.decompose_file(filename)[1]
    config: Config = file_manager.load_config()
    engines: dict[str, Engine] = {k: Engine(**v) for k, v in config.engines.items()}

    for name, engine in engines.items():
        if extension in engine.extensions:
            return name

    return None


def field_name_in(fields: FieldsIterable, field_name_: str) -> str | None:
    for field in fields:
        field_name: str = field[0]

        if field_name_.lower() == field_name.lower():
            return field_name

    return None


def only_modified(change: Change, path: str) -> bool:
    return change == Change.modified


def path_exists(filepath: str) -> bool:
    path: Path = Path(filepath)

    return path.exists()


def same_rows(origin_row: dict, destiny_row: dict, fields: FieldsTuple) -> bool:
    for origin_field, destiny_field in zip(*fields):
        if origin_row[origin_field] != destiny_row[destiny_field]:
            return False

    return True


def should_add_filename(relation: Relation, files: FilesDict) -> bool:
    if filename := relation.priority:
        if engine := check_engine(filename):
            if filename in files[engine]:
                return True

    return False


def valid_filepath(filepath_: str, engines: dict[str, Engine]) -> bool:
    filepath = Path(filepath_)

    extension: str = filepath.suffix
    folderpath: str = str(filepath.resolve().parent)

    for engine in engines.values():
        folderpaths: list[str] = [str(Path(f).resolve()) for f in engine.folderpaths]

        if extension in engine.extensions:
            if folderpath in folderpaths:
                return True

    return False


def values_are_different(rows: list[dict], row_: dict) -> bool:
    """Checks if a list of rows are different from a given row."""

    for row in rows:
        for key, value in row_.items():
            if value != row[key]:
                return True

    return False
