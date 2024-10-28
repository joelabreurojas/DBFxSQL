# dbfxsql


### ✨ Overview

A tool that enables bi-directional data synchronization between [DBF](https://en.wikipedia.org/wiki/DBF) (dBase) files and a [SQL](https://en.wikipedia.org/wiki/SQL) databases. It facilitates seamless data migration from DBF to SQL and vice versa.

&nbsp;

### 🔌 Installation

1. Check your Python version, we use `python` > `3.11`:

```bash
python --version
```

2. Clone the repository:

```bash
git clone https://github.com/joelabreurojas/dbfxsql.git
```

3. Install Poetry (if not alredy installed)

```bash
pip install poetry
```

4. Set up the environment:

```bash
cd dbfxsql
poetry shell
poetry install
```

5. Run the tool:

```bash
python run.py # python -m dbfxsql
```

<details>
  <summary><strong>As a library:</strong></summary>
  <br>
  <ol>

1. Clone the repository:

```bash
git clone https://github.com/j4breu/dbfxsql.git
```

2. Install the project as a Python library:

```bash
cd dbfxsql
pip install .
````

3. Run the tool:

```bash
dbfxsql
```
  </ol>
</details>
&nbsp;

### 💻 Usage

**Detailed Usage Instructions Coming Soon!**

Comprehensive documentation with usage instructions and code examples will be available in a separate file shortly. Stay tuned!

**Early Code Example:**

This early version of the code demonstrates a basic interaction with the tool.

[Link to Asciinema code example](https://asciinema.org/a/675516)

&nbsp;

### 📝 To do

**Required:**
- [x] CRUD operations for both DBF and SQL databases.
- [x] Bi-directional data transfer between DBF and SQL.
- [x] Command-Line Interface (CLI) for managing DBF and SQL tasks.
- [x] Detect changes in folder paths.
- [x] Asynchronous file watcher for automatic change sync.
- [x] Configuration file for specifying relations to compare.
- [ ] Perform table migration before initial data synchronization.
<details>
  <summary><strong>Desirable:</strong></summary>
  <br>
  <ul>
      <li>[x] Dynamic input parameters and database fields handling</li>
      <li>[x] Automatic data type assignment for input values.</li>
      <li>[x] <s>DBF field addition and incremental ID support</s>.</li>
      <li>[x] Retrieve database folder paths from a `.env` file.</li>
      <li>[x] Share a project overview video.</li>
      <li>[x] Detect changes in folder paths.</li>
      <li>[x] Merge DBF/SQL commands into a more friendly CLI format.</li>
      <li>[x] Explain each single command in the CLI documentation.</li>
      <li>[x] Get the rows of all relations in the config file.</li>
      <li>[x] Optimize read queries saving origin rows for future comparations.</li>
      <li>[x] Filtering rows for optimized data changesets.</li>
      <li>[x] Refactor update query to ignore DBF rows that haven't changed.</li>
      <li>[x] Force SQL -> DBF "synchronization" (read all tables).</li>
      <li>[x] Replace dictionaries with classes during synchronization.</li>
      <li>[x] Automatic SQL database creation during SQL table creation.</li>
      <li>[x] Refactor project structure with data structures as inputs.</li>
      <li>[x] Unit tests for code validation.</li>
      <li>[x] Validate dynamic primary key and row_number fields.</li>
      <li>[x] Operate over the databases through their row number.</li>
      <li>[x] Row-based sync implementation.</li>
      <li>[ ] Additional RDBMS support (MSQL Server).</li>
      <li>[ ] SQL triggers/procedures for table changes.</li>
      <li>[ ] Error and exception logging.</li>
      <li>[ ] Decorator for listening command.</li>
      <li>[ ] Replace controller with commands during the sync</li>
      <li>[ ] Add FIELDS options for filtering read queries.</li>
      <li>[ ] Configuration commands for upload and edit.</li>
      <li>[ ] Validate the existence of the received field type.</li>
      <li>[ ] Validate KeyErrors for invalid fields.</li>
      <li>[ ] Validate type lengths and names for consistency between DBF and SQL.</li>
      <li>[ ] Support for relationships between +2 tables in the config file.</li>
      <li>[ ] Comprehensive project documentation.</li>
      <li>[ ] Implementation of CQRS (Command Query Responsibility Segregation) patterns.</li>
      <li>[ ] Sharing as a Python library.</li>
      <li>[ ] Development of a GUI for managing DBF and SQL.</li>
  </ul>
</details>

&nbsp;

### 👐 Contribute

> Improvements?

- Don't hesitate to create a PR.

> Problems?

- Feel free to open a new issue!

&nbsp;

### ❤️  Gratitude

Special thanks to the following projects for making this tool possible:

- [Flask Boilerplate](https://www.youtube.com/watch?v=TTYdcZ4aYz8&feature=youtu.be) - Python Structure Guide by [Ezequiel L. Castaño](https://github.com/ELC)
- [DBF library](https://github.com/ethanfurman/dbf/tree/master/dbf) - Pure Python DBF reader/writer by [Ethan Furman](https://github.com/ethanfurman)
- [Watchfiles library](https://watchfiles.helpmanual.io) - Simple, modern and fast file watching and code reload in Python by [Samuel Colvin](https://github.com/samuelcolvin)
- [Click library](https://click.palletsprojects.com/en/) - A Python command line interface toolkit by [Pallets Organization](https://github.com/pallets)
