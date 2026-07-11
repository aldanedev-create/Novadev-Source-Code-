"""Generated NovaDev 1.0 Flask app.

Run with:
    python -m pip install -r requirements.txt
    python app.py

Then open:
    http://127.0.0.1:5000
"""

import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from models import (
    API_TABLES,
    TABLES,
    count_rows,
    create_row,
    delete_row,
    get_row,
    list_rows,
    primary_key,
    public_row,
    public_rows,
    sum_rows,
    table_for_resource,
)
from routes import ROUTES, handle_declared_route


BACKEND_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = (BACKEND_DIR / '..\\frontend').resolve()

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


def find_table(*names):
    for wanted in names:
        for table_name in TABLES:
            if table_name.lower() == wanted.lower():
                return table_name
    for wanted in names:
        for table_name in TABLES:
            if wanted.lower() in table_name.lower():
                return table_name
    return None


def find_field(table_name, *names):
    fields = TABLES.get(table_name, [])
    for wanted in names:
        for field in fields:
            if field["name"].lower() == wanted.lower():
                return field["name"]
    for wanted in names:
        for field in fields:
            if wanted.lower() in field["name"].lower():
                return field["name"]
    return None


def set_if_field(payload, table_name, value, *field_names):
    field = find_field(table_name, *field_names)
    if field:
        payload[field] = value


@app.post("/api/checkout")
def checkout():
    body = request.get_json(silent=True) or {}
    cart_table = find_table("CartItem", "CartLine", "Cart")
    product_table = find_table("Product")
    order_table = find_table("Order", "Purchase")
    order_item_table = find_table("OrderItem", "OrderLine")

    if not cart_table or not order_table:
        return jsonify({"error": "checkout needs CartItem and Order tables"}), 400

    cart_rows = list(list_rows(cart_table))
    if not cart_rows:
        return jsonify({"error": "cart is empty"}), 400

    cart_product_id = find_field(cart_table, "productId", "product_id", "product")
    cart_product_name = find_field(cart_table, "productName", "product_name", "name")
    cart_price = find_field(cart_table, "price", "unitPrice", "amount")
    cart_quantity = find_field(cart_table, "quantity", "qty", "count")

    total = sum(float(row.get(cart_price) or 0) * int(row.get(cart_quantity) or 1) for row in cart_rows)

    order_payload = {}
    for key, value in body.items():
        set_if_field(order_payload, order_table, value, key)
    set_if_field(order_payload, order_table, body.get("customerName") or body.get("name") or "", "customerName", "customer", "name")
    set_if_field(order_payload, order_table, body.get("email") or "", "email")
    set_if_field(order_payload, order_table, body.get("address") or "", "address", "shipping")
    set_if_field(order_payload, order_table, total, "total", "amount")
    set_if_field(order_payload, order_table, "Paid", "status", "state")

    order = create_row(order_table, order_payload)
    order_id = order.get(primary_key(order_table))
    created_items = []

    if order_item_table:
        for cart_row in cart_rows:
            item_payload = {}
            set_if_field(item_payload, order_item_table, order_id, "orderId", "order_id", "order")
            set_if_field(item_payload, order_item_table, cart_row.get(cart_product_id), "productId", "product_id", "product")
            set_if_field(item_payload, order_item_table, cart_row.get(cart_product_name), "productName", "product_name", "name")
            set_if_field(item_payload, order_item_table, cart_row.get(cart_price), "price", "unitPrice", "amount")
            set_if_field(item_payload, order_item_table, cart_row.get(cart_quantity), "quantity", "qty", "count")
            created_items.append(create_row(order_item_table, item_payload))

    if product_table and cart_product_id:
        stock_field = find_field(product_table, "stock", "inventory", "quantity")
        if stock_field:
            for cart_row in cart_rows:
                product = get_row(product_table, cart_row.get(cart_product_id))
                if product:
                    product[stock_field] = max(0, int(product.get(stock_field) or 0) - int(cart_row.get(cart_quantity) or 1))

    list_rows(cart_table).clear()
    return jsonify(
        {
            "order": public_row(order_table, order),
            "items": [public_row(order_item_table, item) for item in created_items] if order_item_table else [],
            "total": total,
        }
    ), 201


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
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("DEBUG", "1") != "0"
    app.run(host=host, port=port, debug=debug, use_reloader=False)
