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
- [x] Support interaction between tables with same engine, using their position to migrate.
<details>
  <summary><strong>Desirable:</strong></summary>
  <br>
  <ul>
      <li>[x] Handle 'n' type as 'C' type in DBF.</li>
      <li>[x] Support for date/datetime/None types.</li>
      <li>[ ] Transform temporal file extensions to .mdf during modification events.</li>
      <li>[ ] Equalize rows for indirect table relationships.</li>
      <li>[ ] Implement field target to indirect table relationships.</li>
      <li>[ ] Detect indirect table relationships by their destiny tables.</li>
      <li>[ ] Match the number of rows between indirect table relationships (big over small).</li>
      <li>[ ] Apply synchronization by target fields, if they exist.</li>
      <li>[ ] Automatic creation of temporal files based on configuration (Windows).</li>
      <li>[ ] MSSQL triggers/procedures for table changes.</li>
      <li>[ ] Integrate Store Procedures & Triggers to modify temporal files (Windows).</li>
      <li>[ ] Handle starving connections.</li>
      <li>[ ] Standardize automatic sinchronization tests.</li>
      <li>[ ] Use models to transmit data between shapes.</li>
      <li>[ ] Agrupate entities like exceptions and models.</li>
      <li>[ ] New cli workflow based in stages.</li>
      <li>[ ] Implement more abstraction in controllers.</li>
      <li>[ ] Group origin tables by destiny tables to optimize read queries when migrating.</li>
      <li>[ ] Accept conditions over row_number for DBF.</li>
      <li>[ ] Add FIELDS options for filtering read queries.</li>
      <li>[ ] Configuration commands for upload and edit.</li>
      <li>[ ] Validate the existence of the received field type.</li>
      <li>[ ] Validate KeyErrors for invalid fields.</li>
      <li>[ ] Validate type lengths and names for consistency between DBF and SQL.</li>
      <li>[ ] Validate the data migration to a the same table.</li>
      <li>[ ] Support for relationships between +2 tables in the config file.</li>
      <li>[ ] Public project documentation.</li>
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

