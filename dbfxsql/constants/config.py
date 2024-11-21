PATH: str = "~/.config/DBFxSQL/config.toml"

TEMPLATE: str = """
[folderpaths]
DBF = ["."]
SQL = ["."]

[extensions]
DBF = [".dbf", ".DBF"]
SQL = [".sql", ".SQL"]

[[relations]]
sources = ["users.dbf", "company.sql"]
tables = ["", "users"]
fields = [["id", "name"], ["id", "name"]]
"""

VERSION = "0.2.0"
