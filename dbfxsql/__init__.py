"""Initialization module for the application"""

import click

from .models.lazy_group import LazyGroup


@click.group(
    cls=LazyGroup,
    import_name="dbfxsql.cli:cli",
    epilog="For more information, visit https://github.com/joelabreurojas/DBFxSQL",
)
def run():
    """
    A CLI tool to manage data between DBF files and SQL databases.

    Check your `~/.config/DBFxSQL/config.toml` to set your preferences.
    """
