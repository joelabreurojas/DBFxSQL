from pathlib import Path

import tomllib

from ..constants import default_config
from ..models import Config


def list_files(engine: str, folder: str) -> list[str]:
    sql_path: Path = Path(__file__).resolve().parents[1] / "modules/sql"
    query_folder: str = f"{engine.lower()}_queries/{folder}"

    files: list = []

    for file in Path(sql_path / query_folder).iterdir():
        if "exists" != file.name:
            files.append(file.name)

    return files


def load_config() -> Config:
    configpath: Path = Path(default_config.PATH).expanduser()

    if not configpath.exists():
        _create_default_config(configpath)

    with open(configpath.as_posix(), "rb") as configfile:
        toml_data: dict = tomllib.load(configfile)

    return Config(**toml_data)


def load_query(engine: str, command: str) -> str:
    sql_path: Path = Path(__file__).resolve().parents[1] / "modules/sql"

    with open(f"{sql_path}/{engine.lower()}_queries/{command}") as sqlfile:
        sql_query: str = sqlfile.read()

    return sql_query


def new_file(filepath: str) -> None:
    Path(filepath).touch()


def prioritized_files(
    engines: dict[str, dict[str, list[str] | str]],
    relations: list[dict[str, list[str] | str]],
) -> list[str]:
    files: dict[str, list[str]] = formatters.get_filenames(engines, relations)

    filenames: list = []

    for relation in relations:
        if isinstance(filename := relation.get("priority"), str):
            engine: str = validators.check_engine(filename)

            if filename in files[engine]:
                filenames.append(filename)

    return filenames


def remove_file(filepath: str) -> None:
    Path(filepath).unlink()


def _create_default_config(configpath: Path) -> None:
    configpath.parent.mkdir(parents=True, exist_ok=True)
    configpath.touch()

    with open(configpath.as_posix(), "w") as configfile:
        configfile.write(default_config.TEMPLATE[1:])  # remove the first newline
