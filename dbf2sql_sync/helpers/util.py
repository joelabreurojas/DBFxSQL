"""Auxiliary tasks of the application"""

from pathlib import Path

DBF_DATABASE = str(Path.cwd() / "dbf2sql_sync" / "database" / "users.dbf")
SQL_DATABASE = str(Path.cwd() / "dbf2sql_sync" / "database" / "users.sql")


def reset_databases() -> None:
    """Delete the database and storage to create them again"""

    if DBF_DATABASE.exists() or SQL_DATABASE.exists():
        SQL_DATABASE.unlink()
        DBF_DATABASE.unlink()

    DBF_DATABASE.touch()
    SQL_DATABASE.touch()
