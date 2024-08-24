# DBF2SQL Sync


### ✨ Overview

This project aims to synchronize data between [DBF](https://en.wikipedia.org/wiki/DBF) (dBase) files and a [SQL](https://en.wikipedia.org/wiki/SQL) database. In order to do so, will provides a bi-directional data transfer mechanism, allowing to migrate data from DBF to SQL and vice versa.

&nbsp;

### 🔌 Installation

1. Clone he repository, `git clone https://github.com/j4breu/dbf2sql-sync.git`
2. Create a virtual environment, `python -m venv .venv`
3. Activate the virtual environment, `source .venv/bin/activate`
4. Install dependencies, `pip install -r requirements.txt`
5. Run the app, `python run.py` or `python -m dbf2sql_sync`

&nbsp;

### 💻 Usage


&nbsp;

### 📝 Roadmap

**Required:**
- [x] Create a CRUD to handle DBF and SQL
- [x] Make a CLI to manage DBF and SQL
- [ ] Transfer data between DBF and SQL
- [ ] Change detection in folders/files
- [ ] Compare DB with replicas to sync specific fields
- [ ] Set up a cron job to sync data

**Desirable:**
- [ ] Upload to Github
- [ ] Write a documentation
- [x] Make some tests to validate the code
- [x] Use parameters in tests
- [ ] Indicate a folder path to find the databases
- [ ] Handle dynamic fields between databases
- [ ] Change arquitecture from MVC to Hexagonal 
- [ ] Apply CQRS patterns
- [ ] Share as a library
- [ ] Create a GUI to manage DBF and SQL

&nbsp;

### 👐 Contribute

> Improvements?

- Don't hesitate to create a PR.

> Problems?

- Feel free to open a new issue!

&nbsp;

### ❤️  Gratitude

Thanks to the following projects developing this project is possible:

- [ethanfurman/dbf](https://github.com/ethanfurman/dbf): pure python dbf reader/writer
