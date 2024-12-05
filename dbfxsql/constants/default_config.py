PATH: str = "~/.config/DBFxSQL/config.toml"

TEMPLATE: str = """
[engines.dBase]
folderpaths = ["."]
extensions = [".dbf", ".DBF"]

[engines.SQLite]
folderpaths = ["."]
extensions = [".sql", ".SQL", ".sqlite3", ".SQLite3", ".db", ".DB"]

[engines.MSSQL]
# For Windows, change the path to your MSSQL data folder
folderpaths = ["/var/opt/mssql/data/"] 
extensions = [".mdf", ".MDF"]
db_server = "YOUR_MSSQL_SERVER"
db_user = "YOUR_MSSQL_USER"
db_password = "YOUR_MSSQL_PASSWORD"

[[relations]]
sources = ["users.dbf", "company.sql"]
tables = ["", "users"]
fields = [["id", "name"], ["id", "name"]]
"""
