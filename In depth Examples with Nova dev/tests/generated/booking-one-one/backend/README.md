# Generated NovaDev Flask Backend

This backend serves the generated NovaDev UI and JSON APIs from one Flask app.

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
..\frontend
```

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
POST /api/workflows/create-booking
```
