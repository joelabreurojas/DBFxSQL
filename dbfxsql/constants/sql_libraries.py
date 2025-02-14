import sqlite3
from types import ModuleType

import pymssql

SQL: dict[str, ModuleType] = {
    "SQLite": sqlite3,
    "MSSQL": pymssql,
}
