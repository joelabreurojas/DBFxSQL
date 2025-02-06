import tomllib

from . import validators, formatters
from ..constants import default_config

from pathlib import Path


def load_config() -> dict:
    configpath: Path = Path(default_config.PATH).expanduser()

    if not configpath.exists():
        _create_default_config(configpath)

    with open(configpath.as_posix(), "rb") as configfile:
        toml_data: dict = tomllib.load(configfile)

    return toml_data


def load_query(engine: str, command: str) -> str:
    sql_path: str = Path(__file__).resolve().parents[1] / "modules/sql"

    with open(f"{sql_path}/{engine.lower()}_queries/{command}") as sqlfile:
        sql_query: str = sqlfile.read()

    return sql_query


def new_file(filepath: str) -> None:
    Path(filepath).touch()


def remove_file(filepath: str) -> None:
    Path(filepath).unlink()


def prioritized_files(engines, relations) -> list[str]:
    files: dict = formatters.get_filenames(engines, relations)

    filenames: list = []

    for relation in relations:
        if filename := relation.get("priority"):
            engine: str = validators.check_engine(filename)

            if filename in files[engine]:
                filenames.append(filename)

    return filenames


def list_files(engine: str, folder: str) -> list[str]:
    sql_path: str = Path(__file__).resolve().parents[1] / "modules/sql"
    query_folder: str = f"{engine.lower()}_queries/{folder}"
    files: list = []

    for file in Path(sql_path / query_folder).iterdir():
        if "exists" != file.name:
            files.append(file.name)

    return files


def _create_default_config(configpath: Path) -> None:
    configpath.parent.mkdir(parents=True, exist_ok=True)
    configpath.touch()

    with open(configpath.as_posix(), "w") as configfile:
        configfile.write(default_config.TEMPLATE[1:])  # remove the first newline
