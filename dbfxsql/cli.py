from .constants import config, sample_commands
from .models.order_commands import OrderCommands
from .modules import dbf_controller, sql_controller, sync_controller
from .helpers import utils

import click
import asyncio
from yaspin import yaspin


@click.group(cls=OrderCommands)
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
def cli():
    """This script helps with the initialization of the tool."""


@cli.command()
@click.option(
    "-e",
    "--engine",
    type=click.Choice(["DBF", "SQL"], case_sensitive=False),
    required=True,
)
@click.option(
    "-r",
    "--rdbms",
    type=click.Choice(["SQLite", "SQLServer"], case_sensitive=False),
    default="SQLite",
    show_default=True,
)
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
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def create(
    engine: str, rdbms: str, source: str, table: str | None, fields: tuple
) -> None:
    """Create a DBF/SQL table."""

    # Use cases
    if "DBF" == engine:
        dbf_controller.create_table(engine, source, fields)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table'.")

    elif "SQLite" == rdbms:
        sql_controller.create_table(engine, source, table, fields)

    else:
        raise NotImplementedError


@cli.command()
@click.option(
    "-e",
    "--engine",
    type=click.Choice(["DBF", "SQL"], case_sensitive=False),
    required=True,
)
@click.option(
    "-r",
    "--rdbms",
    default="SQLite",
    show_default=True,
)
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
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def drop(engine: str, rdbms: str, source: str, table: str | None) -> None:
    """Drop a DBF/SQL source or SQL table."""

    # Use cases
    if "DBF" == engine:
        dbf_controller.drop_table(engine, source)

    elif not table and "SQLite" == rdbms:
        sql_controller.drop_database(engine, source)

    elif "SQLite" == rdbms:
        sql_controller.drop_table(engine, source, table)

    else:
        raise NotImplementedError


@cli.command()
@click.option(
    "-e",
    "--engine",
    type=click.Choice(["DBF", "SQL"], case_sensitive=False),
    required=True,
)
@click.option(
    "-r",
    "--rdbms",
    default="SQLite",
    show_default=True,
)
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
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def insert(
    engine: str, rdbms: str, source: str, table: str | None, fields: tuple
) -> None:
    """Insert a record into a DBF/SQL table."""

    # Use cases
    if "DBF" == engine:
        dbf_controller.insert_record(engine, source, fields)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table'.")

    elif "SQLite" == rdbms:
        sql_controller.insert_record(engine, source, table, fields)

    else:
        raise NotImplementedError


@cli.command()
@click.option(
    "-e",
    "--engine",
    type=click.Choice(["DBF", "SQL"], case_sensitive=False),
    required=True,
)
@click.option(
    "-r",
    "--rdbms",
    type=click.Choice(["SQLite", "SQLServer"], case_sensitive=False),
    default="SQLite",
    show_default=True,
)
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
    multiple=True,
    metavar="<TEXT>...",
    default=["*"],
    show_default=True,
)
@click.option(
    "-c",
    "--condition",
    type=(click.Tuple([str, str, str])),
    metavar="TEXT TEXT TEXT",
    help="Field, operator and value.",
)
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def read(
    engine: str,
    rdbms: str,
    source: str,
    table: str | None,
    fields: tuple,
    condition: tuple | None,
) -> None:
    """Read records from a DBF/SQL table."""

    records: list = []

    # Use cases
    if "DBF" == engine:
        records = dbf_controller.read_records(engine, source, fields, condition)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table'.")

    elif "SQLite" == rdbms:
        records = sql_controller.read_records(engine, source, table, fields, condition)

    else:
        raise NotImplementedError

    utils.show_table(records)


@cli.command()
@click.option(
    "-e",
    "--engine",
    type=click.Choice(["DBF", "SQL"], case_sensitive=False),
    required=True,
)
@click.option(
    "-r",
    "--rdbms",
    type=click.Choice(["SQLite", "SQLServer"], case_sensitive=False),
    default="SQLite",
    show_default=True,
)
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
    multiple=True,
    metavar="<TEXT>...",
    default=["*"],
    show_default=True,
)
@click.option(
    "-c",
    "--condition",
    type=(click.Tuple([str, str, str])),
    metavar="TEXT TEXT TEXT",
    help="Field, operator and value.",
)
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def update(
    engine: str,
    rdbms: str,
    source: str,
    table: str | None,
    fields: tuple,
    condition: tuple,
) -> None:
    """Update records from a DBF/SQL table."""

    # Use cases
    if "DBF" != engine:
        dbf_controller.update_records(engine, source, *fields, condition)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table'.")

    elif "SQLite" == rdbms:
        sql_controller.update_records(engine, source, table, *fields, condition)

    else:
        raise NotImplementedError()


@cli.command()
@click.option(
    "-e",
    "--engine",
    type=click.Choice(["DBF", "SQL"], case_sensitive=False),
    required=True,
)
@click.option(
    "-r",
    "--rdbms",
    type=click.Choice(["SQLite", "SQLServer"], case_sensitive=False),
    default="SQLite",
    show_default=True,
)
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
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
@utils.embed_examples
def delete(
    engine: str, rdbms: str, source: str, table: str | None, condition: tuple
) -> None:
    """Delete records from an DBF/SQL table."""

    # Use cases
    if "DBF" != engine:
        dbf_controller.update_records(engine, source, condition)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table'.")

    elif "SQLite" == rdbms:
        sql_controller.update_records(engine, source, table, condition)

    else:
        raise NotImplementedError()


@cli.command()
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
def migrate():
    """
    Migrate data between DBF and SQL databases.

    This read a config.toml file with the necessary information to migrate
    data between DBF and SQL databases.
    """

    raise NotImplementedError()


@cli.command()
@click.version_option(config.VERSION, "-v", "--version")
@click.help_option("-h", "--help")
def sync():
    """
    Synchronize data between DBF and SQL databases.

    This read a config.toml file with the necessary information to sync data
    between DBF and SQL databases.
    """
    with yaspin(color="cyan", timer=True) as spinner:
        try:
            spinner.text = "Initializing..."
            setup: list[list[dict]] = sync_controller.init()

            spinner.text = "Listening..."
            asyncio.run(sync_controller.synchronize(setup))

        except KeyboardInterrupt:
            spinner.ok("END")
