from .constants import default_config
from .models.order_commands import OrderCommands
from .modules import dbf_controller, sql_controller, sync_controller
from .helpers import utils

import click
import asyncio
from yaspin import yaspin


@click.group(cls=OrderCommands)
@click.version_option(default_config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
def cli():
    """This script helps with the initialization of the tool."""


@cli.command()
@click.option(
    "-s",
    "--source",
    help="Expects a file.",
    required=True,
)
@click.option(
    "-t",
    "--table",
    help="[required for SQL]",
    default="",
)
@click.option(
    "-f",
    "--fields",
    type=(str, str),
    multiple=True,
    help="Fields with their types.",
    required=True,
)
@click.version_option(default_config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def create(source: str, table: str | None, fields: tuple) -> None:
    """Create a DBF file/SQL file and table."""

    # Use cases
    if not (engine := utils.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}' source.")

    if "dBase" == engine:
        dbf_controller.create_table(engine, source, fields)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table' for SQL.")

    else:
        sql_controller.create_table(engine, source, table, fields)


@cli.command()
@click.option(
    "-s",
    "--source",
    help="Expects a file.",
    required=True,
)
@click.option(
    "-t",
    "--table",
    help="[required for SQL]",
    default="",
)
@click.option(
    "-f",
    "--fields",
    type=(str, str),
    multiple=True,
    help="Fields with their values.",
    required=True,
)
@click.version_option(default_config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def insert(source: str, table: str | None, fields: tuple) -> None:
    """Insert a row into a DBF file/SQL table."""

    # Use cases
    if not (engine := utils.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}' source.")

    if "dBase" == engine:
        dbf_controller.insert_row(engine, source, fields)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table' for SQL.")

    else:
        sql_controller.insert_row(engine, source, table, fields)


@cli.command()
@click.option(
    "-s",
    "--source",
    help="Expects a file.",
    required=True,
)
@click.option(
    "-t",
    "--table",
    help="[required for SQL]",
    default="",
)
@click.option(
    "-c",
    "--condition",
    type=(click.Tuple([str, str, str])),
    metavar="TEXT TEXT TEXT",
    help="Field, operator and value.",
)
@click.version_option(default_config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def read(
    source: str,
    table: str | None,
    condition: tuple | None,
) -> None:
    """Read rows from a DBF file/SQL table."""

    # Use cases
    if not (engine := utils.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}' source.")

    rows: list = []

    if "dBase" == engine:
        rows = dbf_controller.read_rows(engine, source, condition)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table' for SQL.")

    else:
        rows = sql_controller.read_rows(engine, source, table, condition)

    utils.show_table(rows)


@cli.command()
@click.option(
    "-s",
    "--source",
    help="Expects a file.",
    required=True,
)
@click.option(
    "-t",
    "--table",
    help="[required for SQL]",
    default="",
)
@click.option(
    "-f",
    "--fields",
    type=(str, str),
    multiple=True,
    help="Fields with their values.",
    required=True,
)
@click.option(
    "-c",
    "--condition",
    type=(click.Tuple([str, str, str])),
    metavar="TEXT TEXT TEXT",
    help="Field, operator and value.",
    required=True,
)
@click.version_option(default_config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def update(
    source: str,
    table: str | None,
    fields: tuple,
    condition: tuple,
) -> None:
    """Update rows from a DBF file/SQL table."""

    # Use cases
    if not (engine := utils.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}' source.")

    if "dBase" == engine:
        dbf_controller.update_rows(engine, source, fields, condition)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table' for SQL.")

    else:
        sql_controller.update_rows(engine, source, table, fields, condition)


@cli.command()
@click.option(
    "-s",
    "--source",
    help="Expects a file.",
    required=True,
)
@click.option(
    "-t",
    "--table",
    help="[required for SQL]",
    default="",
)
@click.option(
    "-c",
    "--condition",
    type=(click.Tuple([str, str, str])),
    metavar="TEXT TEXT TEXT",
    help="Field, operator and value.",
    required=True,
)
@click.version_option(default_config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def delete(source: str, table: str | None, condition: tuple) -> None:
    """Delete rows from an DBF file/SQL table."""

    # Use cases
    if not (engine := utils.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}' source.")

    if "dBase" == engine:
        dbf_controller.delete_rows(engine, source, condition)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table' for SQL.")

    else:
        sql_controller.delete_rows(engine, source, table, condition)


@cli.command()
@click.option(
    "-s",
    "--source",
    help="Expects a file.",
    required=True,
)
@click.option(
    "-t",
    "--table",
    default="",
)
@click.confirmation_option(
    prompt="Are you sure you want to drop?", help="Confirm the operation."
)
@click.version_option(default_config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def drop(source: str, table: str | None) -> None:
    """Drop a DBF file/SQL file/SQL table."""

    # Use cases
    if not (engine := utils.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}' source.")

    if "dBase" == engine:
        dbf_controller.drop_table(engine, source)

    elif not table:
        sql_controller.drop_database(engine, source)

    else:
        sql_controller.drop_table(engine, source, table)


@cli.command()
@click.option(
    "-e",
    "--engine",
    type=click.Choice(["dBase", "SQLite", "MSSQL"], case_sensitive=False),
    default="dBase",
    show_default=True,
)
@click.version_option(default_config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def migrate(engine: str) -> None:
    """
    Migrate data between DBF and SQL files.

    Based on an engine, selects the appropriate files for migration according
    to the relationships described in the configuration.
    """

    with yaspin(color="cyan", timer=True) as spinner:
        try:
            spinner.text = "Initializing..."
            setup: dict = sync_controller.init()
            relations: list = setup["relations"]
            filenames: list = sync_controller.collect_files(setup, engine)

            spinner.text = "Migrating..."
            sync_controller.migrate(filenames, relations)

            spinner.ok("DONE")

        except KeyboardInterrupt:
            spinner.ok("END")


@cli.command()
@click.option(
    "-e",
    "--engine",
    type=click.Choice(["dBase", "SQLite", "MSSQL"], case_sensitive=False),
    default="dBase",
    show_default=True,
)
@click.version_option(default_config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
def sync(engine: str) -> None:
    """
    Synchronize data between DBF and SQL files.

    Listens to the folders described in the configuration and performs database
    migrations when changes occur. It performs an initial migration based on a
    engine to align the databases before synchronisation.
    """
    with yaspin(color="cyan", timer=True) as spinner:
        try:
            spinner.text = "Initializing..."
            setup: dict = sync_controller.init()
            relations: list = setup["relations"]
            filenames: list = sync_controller.collect_files(setup, engine)

            # Database data alignment
            spinner.text = "Migrating..."
            sync_controller.migrate(filenames, relations)

            spinner.text = "Listening..."
            asyncio.run(sync_controller.synchronize(setup))

        except KeyboardInterrupt:
            spinner.ok("END")
