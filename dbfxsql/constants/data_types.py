import datetime
import decimal


DBF: dict = {
    "0": None,
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

SQL: dict = {
    "NULL": None,
    "INTEGER": int,
    "REAL": float,
    "TEXT": str,
    "BLOB": bytes,  # Binary data
}

DATA_TYPES: dict[str, dict] = {"DBF": DBF, "SQL": SQL}
