from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import dbf

from dbfxsql.exceptions.connection_errors import DBFConnectionFailed
from dbfxsql.helpers import formatters


@contextmanager
def get_table(filepath: str) -> Generator[dbf.Table]:
    """Context manager to open and manage a DBF table."""

    # create the table if it doesn't exist
    if not Path(filepath).read_bytes():
        table: dbf.Table = dbf.Table(filepath, "tmp N(1,0)").open(dbf.READ_WRITE)
        table.delete_fields(table.field_names)

    table: dbf.Table = dbf.Table(filepath).open(dbf.READ_WRITE)

    try:
        yield table

    except Exception as error:
        filename: str = formatters.decompose_file(filepath)[0]

        raise DBFConnectionFailed(filename, error)

    finally:
        table.close()
