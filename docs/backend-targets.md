# Backend Targets

NovaDev 1.0 can generate backend starters from the same table and route
declarations.

```nova
project {
    backend Flask
}
```

Targets:

- `Flask`: most complete target, includes SQLite persistence through
  SQLAlchemy, REST routes, health endpoint, and optional frontend serving.
- `FastAPI`: starter API with generated resources.
- `Express`: starter Node API.
- `Django`: starter Django files.

Build a backend:

```bash
python nova.py build-backend examples/apps/webshield --target Flask
```

Build frontend and backend together:

```bash
python nova.py build-fullstack examples/apps/webshield
```

For `database SQLite`, generated Flask projects write data to:

```txt
backend/database.db
```

The generated `models.py` uses Python's built-in `sqlite3` module for SQLite
setup and SQLAlchemy for table creation, CRUD helpers, counts, sums, and seeded
sample rows.
