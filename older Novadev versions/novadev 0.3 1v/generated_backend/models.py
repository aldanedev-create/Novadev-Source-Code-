"""Generated NovaDev 0.3 model registry."""

TABLES = {'User': [{'name': 'id', 'type': 'auto', 'attributes': []}, {'name': 'name', 'type': 'text', 'attributes': []}, {'name': 'email', 'type': 'email', 'attributes': ['unique']}, {'name': 'role', 'type': 'text', 'attributes': []}, {'name': 'password', 'type': 'secure', 'attributes': []}], 'Product': [{'name': 'id', 'type': 'auto', 'attributes': []}, {'name': 'name', 'type': 'text', 'attributes': []}, {'name': 'price', 'type': 'money', 'attributes': []}, {'name': 'stock', 'type': 'int', 'attributes': []}, {'name': 'active', 'type': 'boolean', 'attributes': []}], 'Order': [{'name': 'id', 'type': 'auto', 'attributes': []}, {'name': 'customer', 'type': 'text', 'attributes': []}, {'name': 'total', 'type': 'money', 'attributes': []}, {'name': 'status', 'type': 'text', 'attributes': []}]}
DATA = {name: [] for name in TABLES}


def list_rows(table_name):
    return DATA.setdefault(table_name, [])


def create_row(table_name, row):
    rows = DATA.setdefault(table_name, [])
    fields = TABLES.get(table_name, [])
    for field in fields:
        if field["type"] == "auto" and field["name"] not in row:
            row[field["name"]] = len(rows) + 1
    rows.append(row)
    return row
