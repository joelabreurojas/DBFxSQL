# Warning: Theses tests only works with the default config file.

import os
import subprocess

from dbfxsql.constants import sample_commands
from dbfxsql.helpers import formatters, validators
from dbfxsql.modules.sql import sql_queries
from dbfxsql.helpers.utils import check_engine


def test_create_table() -> None:
    os.system(sample_commands.SQL["create"])

    assert validators.path_exists("./company.sql")


def test_insert_row() -> None:
    os.system(sample_commands.SQL["insert"])

    command: str = sample_commands.SQL["read"]

    try:
        output: str = subprocess.check_output(command, shell=True, text=True)
        table: str = "+----+----------+\n| id |   name   |\n+----+----------+\n| 1  | John Doe |\n+----+----------+\n\n"

        assert output == table

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def test_read_rows() -> None:
    command: str = sample_commands.SQL["read"]

    try:
        output: str = subprocess.check_output(command, shell=True, text=True)
        table: str = "+----+----------+\n| id |   name   |\n+----+----------+\n| 1  | John Doe |\n+----+----------+\n\n"

        assert output == table

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def test_update_rows() -> None:
    os.system(sample_commands.SQL["update"])

    command: str = sample_commands.SQL["read"]

    try:
        output: str = subprocess.check_output(command, shell=True, text=True)
        table: str = "+----+----------+\n| id |   name   |\n+----+----------+\n| 1  | Jane Doe |\n+----+----------+\n\n"

        assert output == table

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def test_delete_rows() -> None:
    os.system(sample_commands.SQL["delete"])

    command: str = sample_commands.SQL["read"]

    try:
        output: str = subprocess.check_output(command, shell=True, text=True)
        table: str = "+----+------+\n| id | name |\n+----+------+\n|    |      |\n+----+------+\n\n"
        assert output == table

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def test_drop_table() -> None:
    os.system(sample_commands.SQL["drop_table"] + " --yes")

    filename: str = "company.sql"
    engine: str = check_engine(filename)
    filepath: str = formatters.add_folderpath(engine, filename)

    assert not sql_queries.table_exists(engine, filepath, table="users")


def test_drop_database() -> None:
    os.system(sample_commands.SQL["drop_database"] + " --yes")

    assert not validators.path_exists("./company.sql")
