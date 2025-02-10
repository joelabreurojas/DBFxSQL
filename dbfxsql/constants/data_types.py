import datetime
import decimal
import uuid

DBASE: dict[str, type] = {
    "0": type(None),
    "C": str,
    "Y": float,
    "D": datetime.date,
    "T": datetime.datetime,
    "B": float,
    "F": float,
    "G": str,
    "I": int,
    "L": bool,
    "M": str,
    "N": decimal.Decimal,
    "P": str,
    "@": datetime.datetime,
}

SQLITE: dict[str, type] = {
    "NULL": type(None),
    "INTEGER": int,
    "REAL": float,
    "TEXT": str,
    "BLOB": bytes,  # Binary data
}

MSSQL: dict[str, type] = {
    "NULL": type(None),
    "BIT": bool,
    "TINYINT": int,
    "SMALLINT": int,
    "INT": int,
    "BIGINT": int,
    "DECIMAL": decimal.Decimal,
    "NUMERIC": decimal.Decimal,
    "FLOAT": float,
    "REAL": float,
    "MONEY": decimal.Decimal,
    "SMALLMONEY": decimal.Decimal,
    "DATETIME": datetime.datetime,
    "SMALLDATETIME": datetime.datetime,
    "DATE": datetime.date,
    "TIME": datetime.time,
    "CHAR": str,
    "NCHAR": str,
    "VARCHAR": str,
    "NVARCHAR": str,
    "TEXT": str,
    "NTEXT": str,
    "BINARY": bytes,
    "VARBINARY": bytes,
    "IMAGE": bytes,
    "UNIQUEIDENTIFIER": uuid.UUID,
}

DATA_TYPES: dict[str, dict] = {"dBase": DBASE, "SQLite": SQLITE, "MSSQL": MSSQL}
