import sqlite3
from types import ModuleType

import pymssql

SQL: dict[str, ModuleType] = {
    "MSSQL": pymssql,
    "SQLite": sqlite3,
}
