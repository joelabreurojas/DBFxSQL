import types

from dbfxsql.constants import sample_commands
from dbfxsql.helpers import file_manager, formatters

from prettytable import PrettyTable
from watchfiles import Change


def show_table(rows: list[dict]) -> None:
    """Displays a list of rows in a table format."""

    table = PrettyTable()

    table.field_names = rows[0].keys() if rows else []

    for row in rows:
        table.add_row([row[field] for field in table.field_names])

    print(table, end="\n\n")


def embed_examples(func: types.FunctionType) -> types.FunctionType:
    """Decorator to add docstrings to a function."""
    examples: str = """
    \n
    \b
    Examples:
    ---------
    """

    for command in sample_commands.DBF.keys():
        if func.__name__ in command:
            examples += "- " + sample_commands.DBF[command]

    for command in sample_commands.SQL.keys():
        if func.__name__ in command:
            examples += "\n    "
            examples += "- " + sample_commands.SQL[command]

    func.__doc__ += examples

    return func


def only_modified(change: Change, path: str) -> bool:
    allowed_extensions: tuple[str] = (".dbf", ".sql")

    return change == Change.modified and path.endswith(allowed_extensions)


def notify(operations: list, tables: list) -> None:
    for operation, table in zip(operations, tables):
        message: str = f"\nMake changes in: {table.source}"
        print(message if not table.name else message + f" > {table.name}")

        for row in operation["insert"]:
            print(f"Insert row: {row["fields"]}")

        for row in operation["update"]:
            print(f"Update row: {row["fields"]} with row_number {row["index"]}")

        for row in operation["delete"]:
            print(f"Delete row with row_number {row["index"]}")


def check_engine(source: str) -> str:
    engine: str = ""
    extension: str = formatters.decompose_filename(source)[1]

    extensions: dict = file_manager.load_config()["extensions"]

    if extension in extensions["DBF"]:
        engine = "DBF"

    elif extension in extensions["SQL"]:
        engine = "SQL"

    return engine
