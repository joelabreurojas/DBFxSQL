# Warning: Theses tests only works with the default config file.

import os
import subprocess

from dbfxsql.constants import sample_commands
from dbfxsql.helpers import file_manager


def test_create_table() -> None:
    os.system(sample_commands.DBF["create"])

    assert file_manager.path_exists("./data.dbf")


def test_insert_record() -> None:
    os.system(sample_commands.DBF["insert"])

    command: str = sample_commands.DBF["read"]

    try:
        output: str = subprocess.check_output(command, shell=True, text=True)
        table: str = "+----+----------+\n| id |   name   |\n+----+----------+\n| 1  | John Doe |\n+----+----------+\n\n"

        assert output == table

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def test_read_records() -> None:
    command: str = sample_commands.DBF["read"]

    try:
        output: str = subprocess.check_output(command, shell=True, text=True)
        table: str = "+----+----------+\n| id |   name   |\n+----+----------+\n| 1  | John Doe |\n+----+----------+\n\n"

        assert output == table

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def test_update_records() -> None:
    os.system(sample_commands.DBF["update"])

    command: str = sample_commands.DBF["read"]

    try:
        output: str = subprocess.check_output(command, shell=True, text=True)
        table: str = "+----+----------+\n| id |   name   |\n+----+----------+\n| 1  | Jane Doe |\n+----+----------+\n\n"

        assert output == table

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def test_delete_records() -> None:
    os.system(sample_commands.DBF["delete"])

    command: str = sample_commands.DBF["read"]

    try:
        command = "dbfxsql read -e DBF -s data.dbf"
        output: str = subprocess.check_output(command, shell=True, text=True)
        table: str = "+----+------+\n| id | name |\n+----+------+\n|    |      |\n+----+------+\n\n"
        assert output == table

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def test_drop_table() -> None:
    os.system(sample_commands.DBF["drop"] + " --yes")

    assert not file_manager.path_exists("./data.dbf")


if __name__ == "__main__":
    test_create_table()
    test_insert_record()
    test_read_records()
    test_update_records()
    test_delete_records()
    test_drop_table()
