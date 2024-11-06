# Warning: Theses tests only works with the default config file.

import os
import subprocess

from dbfxsql.constants import sample_commands
from dbfxsql.helpers import validators


def test_create_table() -> None:
    os.system(sample_commands.DBF["create"])

    assert validators.path_exists("./users.dbf")


def test_insert_row() -> None:
    os.system(sample_commands.DBF["insert"])

    command: str = sample_commands.DBF["read"]

    try:
        output: str = subprocess.check_output(command, shell=True, text=True)
        table: str = "+----+----------+\n| id |   name   |\n+----+----------+\n| 1  | John Doe |\n+----+----------+\n\n"

        assert output == table

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def test_read_rows() -> None:
    command: str = sample_commands.DBF["read"]

    try:
        output: str = subprocess.check_output(command, shell=True, text=True)
        table: str = "+----+----------+\n| id |   name   |\n+----+----------+\n| 1  | John Doe |\n+----+----------+\n\n"

        assert output == table

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def test_update_rows() -> None:
    os.system(sample_commands.DBF["update"])

    command: str = sample_commands.DBF["read"]

    try:
        output: str = subprocess.check_output(command, shell=True, text=True)
        table: str = "+----+----------+\n| id |   name   |\n+----+----------+\n| 1  | Jane Doe |\n+----+----------+\n\n"

        assert output == table

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def test_delete_rows() -> None:
    os.system(sample_commands.DBF["delete"])

    command: str = sample_commands.DBF["read"]

    try:
        command = "dbfxsql read -e DBF -s users.dbf"
        output: str = subprocess.check_output(command, shell=True, text=True)
        table: str = "+----+------+\n| id | name |\n+----+------+\n|    |      |\n+----+------+\n\n"
        assert output == table

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def test_drop_table() -> None:
    os.system(sample_commands.DBF["drop"] + " --yes")

    assert not validators.path_exists("./users.dbf")
