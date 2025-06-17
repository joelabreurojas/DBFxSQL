<h1 align='center'>
    DBFxSQL
</h1>

<p align='center'>
    <em>Configure once, sync automatically!</em>
</p>

<h6 align='center'>
    <a href="https://github.com/joelabreurojas/DBFxSQL/blob/main/LICENSE">
        <img alt='MIT License' src='https://img.shields.io/static/v1.svg?label=License&message=MIT&logoColor=d9e0ee&colorA=302d41&colorB=blue'/>
    </a>
    <a href="https://github.com/joelabreurojas/DBFxSQL/blob/main/dbfxsql/constants/data_types.py">
        <img alt='Supports dBase, SQLite & MSSQL' src='https://img.shields.io/static/v1.svg?label=Support&message=dBase/SQLite/MSSQL&logoColor=d9e0ee&colorA=302d41&colorB=blue'/>
    </a>
     <a href="https://deepwiki.com/joelabreurojas/DBFxSQL">
        <img alt='Ask DeepWiki' src='https://img.shields.io/static/v1.svg?label=Ask&message=DeepWiki&logoColor=d9e0ee&colorA=302d41&colorB=blue'/>
    </a>
</h6>

&nbsp;

### ✨ Overview

DBFxSQL enables seamless data consistency between legacy DBF (dBase) files and modern SQL databases during migration projects. Instead of managing two separate data systems manually, DBFxSQL automatically synchronizes changes in both directions, eliminating data reconciliation headaches.

Suitable for:

- Organizations migrating from DBF to SQL while maintaining production systems.
- Development teams building new SQL systems alongside existing DBF infrastructure.
- One-time clean migrations without ongoing DBF dependencies.

&nbsp;

### 🔌 Installation

1. Check your Python version, we use `python = "^3.12"`:

```bash
python --version
```

2. Clone the repository:

```bash
git clone https://github.com/joelabreurojas/DBFxSQL.git
```

3. Create and activate a virtual environment.

4. Install the source code:

```bash
pip install DBFxSQL/
```

5. Run the tool:

```bash
dbfxsql
```

&nbsp;

### 💻 Usage

1. Create a DBF file:

```bash
dbfxsql create -s users.dbf -f id "N(20,0)" -f name "C(20)"
```

2. Insert data into DBF:

```bash
dbfxsql insert -s users.dbf -f id 1 -f name "John Doe"
```

3. Create SQL database and table:

```bash
dbfxsql create -s company.sql -t users -f id 'integer primary key' -f name text
```

4. One-time migration:

```bash
dbfxsql migrate --notify
```

5. Continuous synchronization:

```bash
dbfxsql sync --notify
```

<br>

> [!TIP]
> Use the `--help` flag to see all available commands and options.
>
> Example: `dbfxsql <command> --help`

&nbsp;

### ⚙️ Configuration

DBFxSQL uses TOML configuration files to define:

- Database engines and their file extensions.
- Folder paths to monitor.
- Table relationships and synchronization priorities.
- Field mappings between DBF and SQL schemas.

The tool automatically creates a default configuration on the first run at `~/.config/DBFxSQL/config.toml`.

&nbsp;

### 📌 Disclaimer

Before using, create backups of your DBF files and SQL databases.

Known limitations:

- Requires local file system access.
- MSSQL connection issues in database manipulation commands.
- Some advanced features are still under development.

Use at your own risk and _carefully_ verify data integrity after operations.

&nbsp;

### 📝 To do

**Required:**

- [ ] Fix connection in DB manipulation commands for MSSQL.
<details>
  <summary><strong>Desirable:</strong></summary>
  <br>
  <ul>
      <li>[ ] Add a changelog.</li>
      <li>[ ] Add loading bar during migration.</li>
      <li>[ ] Add option to initialize triggers/procedures in cli.</li>
      <li>[ ] Add option to listen alternative files in config.</li>
      <li>[ ] Add option to specify migration/sync order in config.</li>
      <li>[ ] Add errors for wrong config.</li>
      <li>[ ] Add FIELDS option to filter read requests.</li>
      <li>[ ] Add option to specify field target for indirect table relations in config.</li>
      <li>[ ] Balance the number of rows between indirect table relationships (large over small).</li>
      <li>[ ] Add CDC into SQL layers.</li>
      <li>[ ] Add Command Query Responsibility Segregation (CQRS) pattern.</li>
      <li>[ ] Refactor store procedure write_file (use CLR procedures).</li>
      <li>[ ] Refactor read queries by group origin tables by destiny tables for migration/sync optimizations.</li>
      <li>[ ] Validate existence of received field type.</li>
      <li>[ ] Validate KeyErrors for invalid fields.</li>
      <li>[ ] Validate type lengths and names for consistency between DBF and SQL.</li>
      <li>[ ] Validate existence of target fields during sync.</li>
      <li>[ ] Release as a Python library.</li>
  </ul>
</details>

&nbsp;

### 👐 Contribute

> Improvements?

- Don't hesitate to create a PR.

> Problems?

- Feel free to open a new [issue](https://github.com/joelabreurojas/DBFxSQL/issues/new)!

&nbsp;

### ❤️ Gratitude

Special thanks to the following projects for making this tool possible:

- [Flask Boilerplate](https://www.youtube.com/watch?v=TTYdcZ4aYz8&feature=youtu.be) - Python Structure Guide by [Ezequiel L. Castaño](https://github.com/ELC).
- [DBF library](https://github.com/ethanfurman/dbf/tree/master/dbf) - Pure Python DBF reader/writer by [Ethan Furman](https://github.com/ethanfurman).
- [Watchfiles library](https://watchfiles.helpmanual.io) - Simple, modern and fast file watching and code reload in Python by [Samuel Colvin](https://github.com/samuelcolvin).
- [Click library](https://click.palletsprojects.com/en/) - A Python command line interface toolkit by [Pallets Organization](https://github.com/pallets).
