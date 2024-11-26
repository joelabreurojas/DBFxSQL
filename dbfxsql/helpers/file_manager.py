import tomllib

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


def get_filenames(paths: list[str], extensions: tuple[str]) -> list[str]:
    return [
        file.as_posix()
        for path in paths
        for file in Path(path).iterdir()
        if file.suffix in extensions
    ]


def _create_default_config(configpath: Path) -> None:
    configpath.parent.mkdir(parents=True, exist_ok=True)
    configpath.touch()

    with open(configpath.as_posix(), "w") as configfile:
        configfile.write(default_config.TEMPLATE[1:])  # remove the first newline
