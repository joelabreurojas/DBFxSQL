DBF: dict[str, str] = {
    "create": "dbfxsql create -e DBF -s data.dbf -f id 'N(20,0)' -f name 'C(20)'",
    "drop": "dbfxsql drop -e DBF -s data.dbf",
    "insert": "dbfxsql insert -e DBF -s data.dbf -f id 1 -f name 'John Doe'",
    "read": "dbfxsql read -e DBF -s data.dbf -c id == 1",
    "update": "dbfxsql update -e DBF -s data.dbf -f name 'Jane Doe' -c id == 1",
    "delete": "dbfxsql delete -e DBF -s data.dbf -c id == 1",
}


SQL: dict[str, str] = {
    "create": "dbfxsql create -e SQL -s data.sql -t users -f id 'integer primary key' -f name text",
    "drop_database": "dbfxsql drop -e SQL -s data.sql",
    "drop_table": "dbfxsql drop -e SQL -s data.sql -t users",
    "insert": "dbfxsql insert -e SQL -s data.sql -t users -f id 1 -f name 'John Doe'",
    "read": "dbfxsql read -e SQL -s data.sql -t users -c id == 1",
    "update": "dbfxsql update -e SQL -s data.sql -t users -f name 'Jane Doe' -c id == 1",
    "delete": "dbfxsql delete -e SQL -s data.sql -t users -c id == 1",
}
