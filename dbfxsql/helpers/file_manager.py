import tomllib

from ..constants import config

from pathlib import Path


def load_config() -> dict:
    configpath: Path = Path(config.PATH).expanduser()

    if not configpath.exists():
        _create_default_config(configpath)

    with open(configpath.as_posix(), "rb") as configfile:
        toml_data: dict = tomllib.load(configfile)

    return toml_data


def new_file(sourcepath: str) -> None:
    Path(sourcepath).touch()


def remove_file(filepath: str) -> None:
    Path(filepath).unlink()


def get_filenames(paths: list[str], extensions: tuple[str]) -> list[str]:
    return [
        file.name
        for path in paths
        for file in Path(path).iterdir()
        if file.suffix in extensions
    ]


def _create_default_config(configpath: Path) -> None:
    configpath.parent.mkdir(parents=True, exist_ok=True)
    configpath.touch()

    with open(configpath.as_posix(), "w") as configfile:
        configfile.write(config.TEMPLATE[1:])  # remove the first newline
