"""Initialization module for the application"""

from .models.lazy_group import LazyGroup

import click


@click.group(
    cls=LazyGroup,
    import_name="dbfxsql.cli:cli",
    epilog="For more information, visit https://github.com/joelabreurojas/dbfxsql",
)
def run():
    """A CLI tool to manage data between DBF files and SQL databases."""
