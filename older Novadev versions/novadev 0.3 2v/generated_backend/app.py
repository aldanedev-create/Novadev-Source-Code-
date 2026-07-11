"""Generated NovaDev 0.3 Flask app.

Run with:
    python -m pip install -r requirements.txt
    python app.py

Then open:
    http://127.0.0.1:5000
"""

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from models import (
    API_TABLES,
    TABLES,
    count_rows,
    create_row,
    delete_row,
    get_row,
    primary_key,
    public_row,
    public_rows,
    sum_rows,
    table_for_resource,
)
from routes import ROUTES, handle_declared_route


BACKEND_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = (BACKEND_DIR / '..\\dist').resolve()

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")


@app.get("/")
def index():
    return send_frontend_file("index.html")


@app.get("/<path:asset_path>")
def frontend_asset(asset_path):
    if asset_path.startswith("api/"):
        return jsonify({"error": "API route not found", "path": "/" + asset_path}), 404
    candidate = FRONTEND_DIR / asset_path
    if candidate.is_file():
        return send_frontend_file(asset_path)
    return send_frontend_file("index.html")


def send_frontend_file(name):
    if not FRONTEND_DIR.exists():
        return (
            "Frontend files were not found. Run `python nova.py build-ui examples/business_admin.nova` first.",
            404,
        )
    return send_from_directory(FRONTEND_DIR, name)


@app.route("/api/<path:api_path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def api(api_path):
    path = "/api/" + api_path.strip("/")
    body = request.get_json(silent=True) or {}

    declared = handle_declared_route(request.method, path, body)
    if declared is not None:
        payload, status = declared
        return jsonify(payload), status

    parts = [part for part in api_path.split("/") if part]
    if not parts:
        return jsonify({"error": "missing API resource"}), 400

    table_name = table_for_resource(parts[0])
    if table_name is None:
        return jsonify({"error": "unknown API resource", "resource": parts[0]}), 404

    if len(parts) == 1:
        if request.method == "GET":
            return jsonify({"rows": public_rows(table_name), "table": table_name})
        if request.method == "POST":
            return jsonify({"row": public_row(table_name, create_row(table_name, body)), "table": table_name}), 201
        return jsonify({"error": "method not allowed"}), 405

    if len(parts) == 2 and parts[1] == "count" and request.method == "GET":
        return jsonify({"count": count_rows(table_name), "table": table_name})

    if len(parts) == 3 and parts[1] == "sum" and request.method == "GET":
        return jsonify({"sum": sum_rows(table_name, parts[2]), "table": table_name, "field": parts[2]})

    if len(parts) == 2:
        row_id = parts[1]
        if request.method == "GET":
            row = get_row(table_name, row_id)
            if row is None:
                return jsonify({"error": "row not found"}), 404
            return jsonify({"row": public_row(table_name, row), "table": table_name})
        if request.method in {"PUT", "PATCH"}:
            from models import update_row

            row = update_row(table_name, row_id, body)
            if row is None:
                return jsonify({"error": "row not found"}), 404
            return jsonify({"row": public_row(table_name, row), "table": table_name})
        if request.method == "DELETE":
            row = delete_row(table_name, row_id)
            if row is None:
                return jsonify({"error": "row not found"}), 404
            return jsonify({"deleted": public_row(table_name, row), "table": table_name})

    return jsonify({"error": "unsupported API shape", "path": path}), 404


@app.get("/api/schema")
def schema():
    return jsonify(
        {
            "tables": TABLES,
            "resources": API_TABLES,
            "primaryKeys": {name: primary_key(name) for name in TABLES},
            "routes": ROUTES,
        }
    )


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "frontend": FRONTEND_DIR.exists()})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
