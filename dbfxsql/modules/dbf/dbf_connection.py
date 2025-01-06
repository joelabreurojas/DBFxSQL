from contextlib import contextmanager
from collections.abc import Generator

import dbf
import logging
from pathlib import Path


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
        logging.error(error)

    finally:
        table.close()
