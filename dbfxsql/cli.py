import asyncio

import click
from yaspin import yaspin

from .helpers import utils, validators
from .helpers.alias import FieldsIterable
from .models import Condition, OrderCommands
from .modules import dbf_controller, sql_controller, sync_controller


@click.group(cls=OrderCommands)
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
@click.help_option("-h", "--help")
@utils.embed_examples
def create(source: str, table: str | None, fields: FieldsIterable) -> None:
    """Create a DBF file/SQL file and table."""

    # Use cases
    if not (engine := validators.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}' source.")

    if "dBase" == engine:
        if table:
            raise click.UsageError("No such option '-t' / '--table' for DBF.")

        dbf_controller.create_table(engine, source, fields)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table' for SQL.")

    else:
        sql_controller.create_database(engine, source)
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
@click.help_option("-h", "--help")
@utils.embed_examples
def insert(source: str, table: str | None, fields: FieldsIterable) -> None:
    """Insert a row into a DBF file/SQL table."""

    # Use cases
    if not (engine := validators.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}' source.")

    if "dBase" == engine:
        if table:
            raise click.UsageError("No such option '-t' / '--table' for DBF.")

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
@click.help_option("-h", "--help")
@utils.embed_examples
def read(
    source: str,
    table: str | None,
    condition: tuple[str, str, str] | None,
) -> None:
    """Read rows from a DBF file/SQL table."""

    # Use cases
    if not (engine := validators.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}' source.")

    rows: list = []
    condition_: Condition | None = Condition(*condition) if condition else None

    if "dBase" == engine:
        if table:
            raise click.UsageError("No such option '-t' / '--table' for DBF.")

        rows = dbf_controller.read_rows(engine, source, condition_)

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table' for SQL.")

    else:
        rows = sql_controller.read_rows(engine, source, table, condition_)

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
@click.help_option("-h", "--help")
@utils.embed_examples
def update(
    source: str,
    table: str | None,
    fields: FieldsIterable,
    condition: tuple[str, str, str],
) -> None:
    """Update rows from a DBF file/SQL table."""

    # Use cases
    if not (engine := validators.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}' source.")

    if "dBase" == engine:
        if table:
            raise click.UsageError("No such option '-t' / '--table' for DBF.")

        dbf_controller.update_rows(engine, source, fields, Condition(*condition))

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table' for SQL.")

    else:
        sql_controller.update_rows(engine, source, table, fields, Condition(*condition))


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
@click.help_option("-h", "--help")
@utils.embed_examples
def delete(source: str, table: str | None, condition: tuple[str, str, str]) -> None:
    """Delete rows from an DBF file/SQL table."""

    # Use cases
    if not (engine := validators.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}' source.")

    if "dBase" == engine:
        if table:
            raise click.UsageError("No such option '-t' / '--table' for DBF.")

        dbf_controller.delete_rows(engine, source, Condition(*condition))

    elif not table:
        raise click.UsageError("Missing option '-t' / '--table' for SQL.")

    else:
        sql_controller.delete_rows(engine, source, table, Condition(*condition))


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
@click.help_option("-h", "--help")
@utils.embed_examples
def drop(source: str, table: str | None) -> None:
    """Drop a DBF file/SQL file/SQL table."""

    # Use cases
    if not (engine := validators.check_engine(source)):
        raise click.UsageError(f"Unknown extension for '{source}' source.")

    if "dBase" == engine:
        if table:
            raise click.UsageError("No such option '-t' / '--table' for DBF.")

        dbf_controller.drop_table(engine, source)

    elif not table:
        sql_controller.drop_database(engine, source)

    else:
        sql_controller.drop_table(engine, source, table)


@cli.command()
@click.option(
    "-n",
    "--notify",
    help="Notify the changes.",
    is_flag=True,
)
@click.help_option("-h", "--help")
def migrate(notify: bool) -> None:
    """
    Migrate data between DBF and SQL files.

    Transfers data from the files that have priority in the relations defined
    in the configuration.
    """

    with yaspin(color="cyan", timer=True) as spinner:
        try:
            spinner.text = "Initializing..."

            _, relations, filenames = sync_controller.init()

            spinner.text = "Migrating..."

            sync_controller.migrate(filenames, relations, notify)

            spinner.ok("DONE")

        except KeyboardInterrupt:
            spinner.ok("END")


@cli.command()
@click.option(
    "-n",
    "--notify",
    help="Notify the changes.",
    is_flag=True,
)
@click.help_option("-h", "--help")
def sync(notify: bool) -> None:
    """
    Synchronize data between DBF and SQL files.

    Listens to the folders described in the configuration and performs database
    migrations when changes occur. It performs an initial migration based on the
    source priority defined (from the relation) to align the databases before
    synchronisation.
    """
    with yaspin(color="cyan", timer=True) as spinner:
        try:
            spinner.text = "Initializing..."

            engines, relations, filenames = sync_controller.init()

            spinner.text = "Migrating..."

            sync_controller.migrate(filenames, relations, notify)

            spinner.text = "Listening..."

            asyncio.run(sync_controller.synchronize(engines, relations, notify))

        except KeyboardInterrupt:
            spinner.ok("END")
