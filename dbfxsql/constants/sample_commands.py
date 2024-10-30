DBF: dict[str, str] = {
    "create": "dbfxsql create -s data.dbf -f id 'N(20,0)' -f name 'C(20)'",
    "drop": "dbfxsql drop -s data.dbf",
    "insert": "dbfxsql insert -s data.dbf -f id 1 -f name 'John Doe'",
    "read": "dbfxsql read -s data.dbf -c id == 1",
    "update": "dbfxsql update -s data.dbf -f name 'Jane Doe' -c id == 1",
    "delete": "dbfxsql delete -s data.dbf -c id == 1",
    "migrate": "dbfxsql migrate -p SQL",
}


SQL: dict[str, str] = {
    "create": "dbfxsql create -s data.sql -t users -f id 'integer primary key' -f name text",
    "drop_database": "dbfxsql drop -s data.sql",
    "drop_table": "dbfxsql drop -s data.sql -t users",
    "insert": "dbfxsql insert -s data.sql -t users -f id 1 -f name 'John Doe'",
    "read": "dbfxsql read -s data.sql -t users -c id == 1",
    "update": "dbfxsql update -s data.sql -t users -f name 'Jane Doe' -c id == 1",
    "delete": "dbfxsql delete -s data.sql -t users -c id == 1",
    "migrate": "dbfxsql migrate -p SQL",
}
