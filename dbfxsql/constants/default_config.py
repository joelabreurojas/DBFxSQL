PATH: str = "~/.config/DBFxSQL/config.toml"

TEMPLATE: str = """
[engines.dBase]
folderpaths = ["."]
extensions = [".dbf", ".DBF"]

[engines.SQLite]
folderpaths = ["."]
extensions = [".sql", ".SQL", ".sqlite3", ".SQLite3", ".db", ".DB"]

[engines.MSSQL]
# Linux Folderpath
folderpaths = ["/var/opt/mssql/data/"]
# Windows Folderpath (via WSL)
# folderpaths = ["/mnt/c/Program Files/Microsoft SQL Server/VERSION?/MSSQL/DATA/"]
extensions = [".mdf", ".MDF"]
db_server = "MSSQL_SERVER?\\\\MSSQL_INSTANCE?"
db_user = "MSSQL_USER?"
db_password = "MSSQL_PASSWORD?"

[[relations]]
sources = ["users.dbf", "company.sql"]
tables = ["", "users"]
fields = [["id", "name"], ["id", "name"]]
"""
