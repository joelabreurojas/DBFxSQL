import types
from dbfxsql.constants import sample_commands
from prettytable import PrettyTable
from watchfiles import Change


def show_table(records: list[dict]) -> None:
    """Displays a list of records in a table format."""

    table = PrettyTable()

    table.field_names = records[0].keys() if records else []

    for record in records:
        table.add_row([record[field] for field in table.field_names])

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


def notify(insert: list, update: list, delete: list, header: dict) -> None:
    for record in insert:
        print(f"Insert in table '{header['table']}': {record}")

    for record in update:
        print(
            f"""
            Update in table '{header['table']}'
            on fields '{header['destiny_fields']}'
            with record: {record}
            """
        )

    for record in delete:
        print(f"Delete in table '{header['table']}' with id: {record['id']}")
