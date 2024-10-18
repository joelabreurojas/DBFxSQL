PATH: str = "~/.config/dbfxsql/config.toml"

TEMPLATE: str = """
[folderpaths]
DBF = ["."]
SQL = ["."]

[[relations]]
engines = ["DBF", "SQL"]
sources = ["data.dbf", "data.sql"]
tables = ["", "users"]
fields = [["name"], ["name"]]
"""

VERSION = "0.1.0"
