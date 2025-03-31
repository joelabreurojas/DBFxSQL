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
<details>
  <summary><strong>Desirable:</strong></summary>
  <br>
  <ul>
      <li>[ ] Omit os.kill from watch_files (Windows issues).</li>
      <li>[ ] Rename triggers.</li>
      <li>[ ] Improve store procedure write_file (use CLR procedures).</li>
      <li>[ ] Option to initialize triggers/procedures.</li>
      <li>[ ] Fix timetuple issues in DBF by using a string as a date.</li>
      <li>[ ] Add loading bar during migration.</li>
      <li>[ ] Create a changelog.</li>
      <li>[ ] Specify temporary files to listen on in configuration.</li>
      <li>[ ] Specify migration order into the configuration.</li>
      <li>[ ] Add CDC to SQL.</li>
      <li>[ ] Balance rows for indirect table relationships.</li>
      <li>[ ] Implement field target for indirect table relationships.</li>
      <li>[ ] Recognize indirect table relationships by their target tables.</li>
      <li>[ ] Balance the number of rows between indirect table relationships (large over small).</li>
      <li>[ ] Apply synchronization by target fields when they exist.</li>
      <li>[ ] Standardize automatic synchronization checks.</li>
      <li>[ ] New incremental cli workflow.</li>
      <li>[ ] Implement more abstraction in controllers.</li>
      <li>[ ] Group origin tables by destiny tables to optimize read queries during migration.</li>
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

