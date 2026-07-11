"""Generated NovaDev 1.1 model and data helpers."""

from copy import deepcopy

TABLES = {'Service': [{'name': 'id', 'type': 'auto', 'attributes': [], 'auto': True, 'secure': False, 'unique': False}, {'name': 'name', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'duration', 'type': 'int', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}], 'Customer': [{'name': 'id', 'type': 'auto', 'attributes': [], 'auto': True, 'secure': False, 'unique': False}, {'name': 'name', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'email', 'type': 'email', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}], 'Booking': [{'name': 'id', 'type': 'auto', 'attributes': [], 'auto': True, 'secure': False, 'unique': False}, {'name': 'customerName', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'serviceName', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'status', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}]}
API_TABLES = {'services': 'Service', 'customers': 'Customer', 'bookings': 'Booking'}
PRIMARY_KEYS = {'Service': 'id', 'Customer': 'id', 'Booking': 'id'}
DATA = deepcopy({'Service': [{'id': 1, 'name': 'Name 1', 'duration': 10}, {'id': 2, 'name': 'Name 2', 'duration': 20}, {'id': 3, 'name': 'Name 3', 'duration': 30}], 'Customer': [{'id': 1, 'name': 'Name 1', 'email': 'email1@example.com'}, {'id': 2, 'name': 'Name 2', 'email': 'email2@example.com'}, {'id': 3, 'name': 'Name 3', 'email': 'email3@example.com'}], 'Booking': [{'id': 1, 'customerName': 'Customername 1', 'serviceName': 'Servicename 1', 'status': 'new'}, {'id': 2, 'customerName': 'Customername 2', 'serviceName': 'Servicename 2', 'status': 'active'}, {'id': 3, 'customerName': 'Customername 3', 'serviceName': 'Servicename 3', 'status': 'review'}]})


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
