import datetime
import decimal


DBF: dict = {
    "C": str,
    "D": datetime.date,
    "N": decimal.Decimal,  # Numeric
    "L": bool,
    "M": str,  # Memo (long text)
    "F": float,
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

