# DBFxSQL


### ✨ Overview

A tool that enables bi-directional data synchronization between [DBF](https://en.wikipedia.org/wiki/DBF) (dBase) files and a [SQL](https://en.wikipedia.org/wiki/SQL) databases. It facilitates seamless data migration from DBF to SQL and vice versa.

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

3. Install Poetry (if not alredy installed)

```bash
pip install poetry
```

4. Set up the environment:

```bash
cd DBFxSQL
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
git clone https://github.com/joelabreurojas/DBFxSQL.git
```

2. Install the project as a Python library:

```bash
cd DBFxSQL
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
- [x] Detect OS to migrate.
- [x] Handle temp files for MSSQL in Windows.
- [x] Create Store Procedures & Triggers for MSSQL in Windows.
<details>
  <summary><strong>Desirable:</strong></summary>
  <br>
  <ul>
      <li>[x] Automate creation of temp files for any MSSQL source in Windows.</li>
      <li>[x] Treat temporary files as MSSQL sources.</li>
      <li>[x] Create save procedure (write_file) to update temporary files in Windows.</li>
      <li>[x] Create insert/update/delete triggers for any MSSQL table in Windows.</li>
      <li>[x] Handle bulk insert by single executions to detect MSSQL changes.</li>
      <li>[x] Handle migration priority in configuration.</li>
      <li>[x] Fix date format issues.</li>
      <li>[x] Specify None type for engine data types.</li>
      <li>[x] Handle db connection errors.</li>
      <li>[ ] Treat dbf.data_types.NullType as empty string.</li>
      <li>[ ] Order library imports.</li>
      <li>[ ] Specify types that are used throughout the project.</li>
      <li>[ ] Order functions by encapsulation level.</li>
      <li>[ ] Use alias to mitigate long types.</li>
      <li>[ ] Remove comparison for bluk operations.</li>
      <li>[ ] Create a changelog.</li>
      <li>[ ] Raise an error if an empty string is returned.</li>
      <li>[ ] Specify temporary files to listen on in configuration.</li>
      <li>[ ] Specify migration order into the configuration.</li>
      <li>[ ] Add CDC to SQL.</li>
      <li>[ ] Balance rows for indirect table relationships.</li>
      <li>[ ] Implement field target for indirect table relationships.</li>
      <li>[ ] Recognize indirect table relationships by their target tables.</li>
      <li>[ ] Balance the number of rows between indirect table relationships (large over small).</li>
      <li>[ ] Apply synchronization by target fields when they exist.</li>
      <li>[ ] Standardize automatic synchronization checks.</li>
      <li>[ ] Use models to pass data between forms.</li>
      <li>[ ] Aggregate entities like exceptions and models.</li>
      <li>[ ] New incremental cli workflow.</li>
      <li>[ ] Implement more abstraction in controllers.</li>
      <li>[ ] Group origin tables by destiny tables to optimize read queries during migration.</li>
      <li>[ ] Accept row_number conditions for DBF.</li>
      <li>[ ] Add FIELDS options to filter read requests.</li>
      <li>[ ] Configuration commands for uploading and editing.</li>
      <li>[ ] Validate existence of received field type.</li>
      <li>[ ] Validate KeyErrors for invalid fields.</li>
      <li>[ ] Validate type lengths and names for consistency between DBF and SQL.</li>
      <li>[ ] Public project documentation.</li>
      <li>[ ] Command Query Responsibility Segregation (CQRS) pattern implementation.</li>
      <li>[ ] Released as a Python library.</li>
      <li>[ ] Development of a GUI to manage DBF and SQL.</li>
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

