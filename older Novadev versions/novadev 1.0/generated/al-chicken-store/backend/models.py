"""Generated NovaDev 0.4 model and data helpers."""

from copy import deepcopy

TABLES = {'Customer': [{'name': 'id', 'type': 'auto', 'attributes': [], 'auto': True, 'secure': False, 'unique': False}, {'name': 'name', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'email', 'type': 'email', 'attributes': ['unique'], 'auto': False, 'secure': False, 'unique': True}, {'name': 'password', 'type': 'password', 'attributes': ['secure'], 'auto': False, 'secure': True, 'unique': False}, {'name': 'role', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}], 'Product': [{'name': 'id', 'type': 'auto', 'attributes': [], 'auto': True, 'secure': False, 'unique': False}, {'name': 'name', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'description', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'category', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'price', 'type': 'money', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'stock', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'active', 'type': 'boolean', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}], 'CartItem': [{'name': 'id', 'type': 'auto', 'attributes': [], 'auto': True, 'secure': False, 'unique': False}, {'name': 'productId', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'name', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'price', 'type': 'money', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'quantity', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}], 'Order': [{'name': 'id', 'type': 'auto', 'attributes': [], 'auto': True, 'secure': False, 'unique': False}, {'name': 'customerName', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'email', 'type': 'email', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'address', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'status', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'total', 'type': 'money', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}], 'OrderItem': [{'name': 'id', 'type': 'auto', 'attributes': [], 'auto': True, 'secure': False, 'unique': False}, {'name': 'orderId', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'productId', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'name', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'quantity', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'price', 'type': 'money', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}]}
API_TABLES = {'customers': 'Customer', 'products': 'Product', 'cart-items': 'CartItem', 'orders': 'Order', 'order-items': 'OrderItem'}
PRIMARY_KEYS = {'Customer': 'id', 'Product': 'id', 'CartItem': 'id', 'Order': 'id', 'OrderItem': 'id'}
DATA = deepcopy({'Customer': [{'id': 1, 'name': 'Name 1', 'email': 'email1@example.com', 'password': 'Password 1', 'role': 'Role 1'}, {'id': 2, 'name': 'Name 2', 'email': 'email2@example.com', 'password': 'Password 2', 'role': 'Role 2'}, {'id': 3, 'name': 'Name 3', 'email': 'email3@example.com', 'password': 'Password 3', 'role': 'Role 3'}], 'Product': [{'id': 1, 'name': 'Aurora Hoodie', 'description': 'Soft heavyweight fleece for everyday wear.', 'category': 'Apparel', 'price': 68, 'stock': 24, 'active': True}, {'id': 2, 'name': 'Orbit Desk Lamp', 'description': 'Adjustable LED lamp with warm and cool modes.', 'category': 'Home', 'price': 89, 'stock': 18, 'active': True}, {'id': 3, 'name': 'Nova Tote', 'description': 'Durable canvas tote for work, gym, and errands.', 'category': 'Accessories', 'price': 32, 'stock': 40, 'active': True}, {'id': 4, 'name': 'Focus Bottle', 'description': 'Insulated stainless bottle that keeps drinks cold.', 'category': 'Drinkware', 'price': 28, 'stock': 35, 'active': True}], 'CartItem': [], 'Order': [], 'OrderItem': []})


def table_for_resource(resource):
    return API_TABLES.get(resource.lower())


def table_schema(table_name):
    return TABLES.get(table_name, [])


def primary_key(table_name):
    return PRIMARY_KEYS.get(table_name, "id")


def list_rows(table_name):
    return DATA.setdefault(table_name, [])


def public_row(table_name, row):
    secure_fields = {field["name"] for field in table_schema(table_name) if field.get("secure")}
    return {name: value for name, value in row.items() if name not in secure_fields}


def public_rows(table_name):
    return [public_row(table_name, row) for row in list_rows(table_name)]


def count_rows(table_name):
    return len(list_rows(table_name))


def sum_rows(table_name, field_name):
    return sum(float(row.get(field_name) or 0) for row in list_rows(table_name))


def get_row(table_name, row_id):
    key = primary_key(table_name)
    for row in list_rows(table_name):
        if str(row.get(key)) == str(row_id):
            return row
    return None


def create_row(table_name, row):
    rows = list_rows(table_name)
    clean = sanitize_row(table_name, row)
    for field in table_schema(table_name):
        if field.get("auto") and field["name"] not in clean:
            clean[field["name"]] = next_id(table_name)
    rows.append(clean)
    return clean


def update_row(table_name, row_id, values):
    row = get_row(table_name, row_id)
    if row is None:
        return None
    row.update(sanitize_row(table_name, values, partial=True))
    return row


def delete_row(table_name, row_id):
    rows = list_rows(table_name)
    key = primary_key(table_name)
    for index, row in enumerate(rows):
        if str(row.get(key)) == str(row_id):
            return rows.pop(index)
    return None


def next_id(table_name):
    key = primary_key(table_name)
    current = [int(row.get(key, 0)) for row in list_rows(table_name) if str(row.get(key, "")).isdigit()]
    return (max(current) if current else 0) + 1


def sanitize_row(table_name, values, partial=False):
    fields = table_schema(table_name)
    allowed = {field["name"]: field for field in fields}
    clean = {}
    for name, value in (values or {}).items():
        if name not in allowed:
            continue
        field = allowed[name]
        if field.get("auto"):
            continue
        clean[name] = coerce_value(value, field.get("type", "text"))

    if not partial:
        for field in fields:
            name = field["name"]
            if field.get("auto") or name in clean:
                continue
            clean[name] = default_value(field.get("type", "text"))
    return clean


def coerce_value(value, field_type):
    lowered = str(field_type).lower()
    if lowered in {"int", "number"}:
        return int(value or 0)
    if lowered in {"money", "currency"}:
        return float(value or 0)
    if lowered in {"bool", "boolean"}:
        if isinstance(value, bool):
            return value
        return str(value).lower() in {"true", "1", "yes", "on"}
    return "" if value is None else value


def default_value(field_type):
    lowered = str(field_type).lower()
    if lowered in {"int", "number", "money", "currency"}:
        return 0
    if lowered in {"bool", "boolean"}:
        return False
    return ""
