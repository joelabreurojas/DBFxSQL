from typing import Callable

from prettytable import PrettyTable

from ..constants import sample_commands
from ..models.sync_table import SyncTable
from . import file_manager, validators


def embed_examples(func: Callable) -> Callable:
    """Decorator to add docstrings to a function."""
    examples: str = """
    \n
    \b
    Examples:
    ---------
    """

    for command in sample_commands.DBF.keys():
        if func.__name__ in command:
            examples += f"- {sample_commands.DBF[command]}"

    for command in sample_commands.SQL.keys():
        if func.__name__ in command:
            examples += f"\n    - {sample_commands.SQL[command]}"

    if func.__doc__ is None:
        func.__doc__ = examples
    else:
        func.__doc__ += examples

    return func


def generate_tmp_files(filepaths: list[str]) -> None:
    for filepath in filepaths:
        if not validators.path_exists(filepath):
            file_manager.new_file(filepath)


def notify(operations: list[dict[str, list[dict]]], tables: list[SyncTable]) -> None:
    for operation, table in zip(operations, tables):
        if operation["insert"] or operation["update"] or operation["delete"]:
            message: str = f"\nMake changes in: {table.source}"
            print(message if not table.name else message + f" > {table.name}")

            for row in operation["insert"]:
                print(f"Insert row: {row['fields']}")

            for row in operation["update"]:
                print(f"Update row: {row['fields']} with row_number {row['index']}")

            for row in operation["delete"]:
                print(f"Delete row with row_number {row['index']}")


def show_table(rows: list[dict]) -> None:
    """Displays a list of rows in a table format."""

    table = PrettyTable()

    table.field_names = rows[0].keys() if rows else []

    for row in rows:
        table.add_row([row[field] for field in table.field_names])

    print(table, end="\n\n")
