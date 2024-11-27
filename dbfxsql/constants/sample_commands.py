DBF: dict[str, str] = {
    "create": 'dbfxsql create -s users.dbf -f id "N(20,0)" -f name "C(20)"',
    "drop": "dbfxsql drop -s users.dbf",
    "insert": 'dbfxsql insert -s users.dbf -f id 1 -f name "John Doe"',
    "read": "dbfxsql read -s users.dbf -c id == 1",
    "update": 'dbfxsql update -s users.dbf -f name "Jane Doe" -c id == 1',
    "delete": "dbfxsql delete -s users.dbf -c id == 1",
    "migrate": "dbfxsql migrate -e dBase",
}


SQL: dict[str, str] = {
    "create": 'dbfxsql create -s company.sql -t users -f id "integer primary key" -f name text',
    "drop_database": "dbfxsql drop -s company.sql",
    "drop_table": "dbfxsql drop -s company.sql -t users",
    "insert": 'dbfxsql insert -s company.sql -t users -f id 1 -f name "John Doe"',
    "read": "dbfxsql read -s company.sql -t users -c id == 1",
    "update": 'dbfxsql update -s company.sql -t users -f name "Jane Doe" -c id == 1',
    "delete": "dbfxsql delete -s company.sql -t users -c id == 1",
    "migrate": "dbfxsql migrate -e SQLite",
}
