from contextlib import contextmanager
from collections.abc import Generator

import dbf
from pathlib import Path


@contextmanager
def get_table(sourcepath: str) -> Generator[dbf.Table]:
    """Context manager to open and manage a DBF table."""

    # create the table if it doesn't exist
    if not Path(sourcepath).read_bytes():
        table: dbf.Table = dbf.Table(sourcepath, "tmp N(1,0)").open(dbf.READ_WRITE)
        table.delete_fields(table.field_names)

    table: dbf.Table = dbf.Table(sourcepath).open(dbf.READ_WRITE)

    try:
        yield table

    finally:
        table.close()
