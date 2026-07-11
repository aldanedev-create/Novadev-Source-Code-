# Generated NovaDev Flask Backend

This backend serves the generated NovaDev UI and JSON APIs from one Flask app.
It stores table data in `database.db` using SQLite plus SQLAlchemy.

## Setup

```bash
python -m pip install -r requirements.txt
python app.py
```

Open:

```txt
http://127.0.0.1:5000
```

The app expects frontend files at:

```txt
..\..\..\..\frontend
```

Database file:

```txt
backend/database.db
```

The first app start creates SQLite tables from NovaDev `table` declarations and
seeds sample rows when a table is empty.

Build them from the project root with:

```bash
python nova.py build-ui examples/business_admin.nova
```

Useful API endpoints:

```txt
GET  /api/health
GET  /api/schema
GET  /api/<resource>
POST /api/<resource>
GET  /api/<resource>/count
```

Workflow endpoints generated from this project:

```txt
POST /api/workflows/add-to-cart
POST /api/workflows/checkout
```
