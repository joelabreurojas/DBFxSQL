PATH: str = "~/.config/DBFxSQL/config.toml"

TEMPLATE: str = """
[[engines.dBase]]
folderpaths = ["."]
extensions = [".dbf", ".DBF"]

[[engines.SQLite]]
folderpaths = ["."]
extensions = [".sql", ".SQL", ".sqlite3", ".SQLite3", ".db", ".DB"]

[[engines.MSSQL]]
# For Windows, change the path to your MSSQL data folder
folderpaths = ["/var/opt/mssql/data/"] 
extensions = [".mdf", ".MDF"]

[[relations]]
sources = ["users.dbf", "company.sql"]
tables = ["", "users"]
fields = [["id", "name"], ["id", "name"]]
"""
