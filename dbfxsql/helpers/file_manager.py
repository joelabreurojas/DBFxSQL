import tomllib

from ..constants import config

from pathlib import Path


def add_folderpath(engine: str, source: str) -> str:
    """Adds the folderpath to the source depending on the engine."""
    folderpath: str = load_config()["folderpaths"][engine][0]

    if not folderpath.endswith("/"):
        folderpath += "/"

    return folderpath + source


def load_config() -> dict:
    configpath: Path = Path(config.PATH).expanduser()

    if not configpath.exists():
        _create_default_config(configpath)

    with open(configpath.as_posix(), "rb") as configfile:
        toml_data: dict = tomllib.load(configfile)

    return toml_data


def path_exists(sourcepath: str) -> None:
    return Path(sourcepath).exists()


def new_file(sourcepath: str) -> None:
    Path(sourcepath).touch()


def remove_file(filepath: str) -> None:
    Path(filepath).unlink()


def decompose_filename(file: str) -> tuple[str, str]:
    """Decomposes a filename into its stem and suffix."""

    return Path(file).stem, Path(file).suffix


def _create_default_config(configpath: Path) -> None:
    configpath.parent.mkdir(parents=True, exist_ok=True)
    configpath.touch()

    with open(configpath.as_posix(), "w") as configfile:
        configfile.write(config.TEMPLATE[1:])  # remove the first newline
