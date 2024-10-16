# Warning: Theses tests only works with the default config file.

import os
import subprocess

from dbfxsql.constants import sample_commands
from dbfxsql.helpers import file_manager


def test_create_table() -> None:
    os.system(sample_commands.SQL["create"])

    assert file_manager.path_exists("./data.sql") is True
