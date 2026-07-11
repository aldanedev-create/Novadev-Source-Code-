"""Generated NovaDev 1.1 SQLAlchemy model and data helpers."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    delete,
    event,
    func,
    insert,
    select,
    update,
)

from config import DATABASE_URL

TABLES = {'CartItem': [{'name': 'id', 'type': 'auto', 'attributes': [], 'auto': True, 'secure': False, 'unique': False}, {'name': 'productName', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'quantity', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'price', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}], 'Order': [{'name': 'id', 'type': 'auto', 'attributes': [], 'auto': True, 'secure': False, 'unique': False}, {'name': 'customerName', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'email', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'address', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'total', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'status', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}], 'Product': [{'name': 'id', 'type': 'auto', 'attributes': [], 'auto': True, 'secure': False, 'unique': False}, {'name': 'name', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'category', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'price', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'oldPrice', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'image', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'rating', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'stock', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'description', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'badge', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}], 'Review': [{'name': 'id', 'type': 'auto', 'attributes': [], 'auto': True, 'secure': False, 'unique': False}, {'name': 'customer', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'product', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'rating', 'type': 'number', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}, {'name': 'comment', 'type': 'text', 'attributes': [], 'auto': False, 'secure': False, 'unique': False}]}
API_TABLES = {'cart-items': 'CartItem', 'orders': 'Order', 'products': 'Product', 'reviews': 'Review'}
PRIMARY_KEYS = {'CartItem': 'id', 'Order': 'id', 'Product': 'id', 'Review': 'id'}
SEED_DATA = {'CartItem': [], 'Order': [], 'Product': [{'id': 1, 'name': 'Aurora Hoodie', 'category': 'Apparel', 'price': 68, 'oldPrice': 68, 'image': 'Image 1', 'rating': 10, 'stock': 24, 'description': 'Soft heavyweight fleece for everyday wear.', 'badge': 'Badge 1'}, {'id': 2, 'name': 'Orbit Desk Lamp', 'category': 'Home', 'price': 89, 'oldPrice': 89, 'image': 'Image 2', 'rating': 20, 'stock': 18, 'description': 'Adjustable LED lamp with warm and cool modes.', 'badge': 'Badge 2'}, {'id': 3, 'name': 'Nova Tote', 'category': 'Accessories', 'price': 32, 'oldPrice': 32, 'image': 'Image 3', 'rating': 30, 'stock': 40, 'description': 'Durable canvas tote for work, gym, and errands.', 'badge': 'Badge 3'}, {'id': 4, 'name': 'Focus Bottle', 'category': 'Drinkware', 'price': 28, 'oldPrice': 28, 'image': 'Image 4', 'rating': 40, 'stock': 35, 'description': 'Insulated stainless bottle that keeps drinks cold.', 'badge': 'Badge 4'}], 'Review': [{'id': 1, 'customer': 'Customer 1', 'product': 'Product 1', 'rating': 10, 'comment': 'Comment 1'}, {'id': 2, 'customer': 'Customer 2', 'product': 'Product 2', 'rating': 20, 'comment': 'Comment 2'}, {'id': 3, 'customer': 'Customer 3', 'product': 'Product 3', 'rating': 30, 'comment': 'Comment 3'}]}


def table_for_resource(resource):
    return API_TABLES.get(resource.lower())


def table_schema(table_name):
    return TABLES.get(table_name, [])


def primary_key(table_name):
    return PRIMARY_KEYS.get(table_name, "id")


def sqlite_database_path():
    if not DATABASE_URL.startswith("sqlite:///"):
        return None
    raw_path = DATABASE_URL.replace("sqlite:///", "", 1)
    if raw_path in {"", ":memory:"}:
        return None
    database_path = Path(raw_path)
    if not database_path.is_absolute():
        database_path = Path(__file__).resolve().parent / raw_path
    return database_path


def prepare_sqlite_database():
    database_path = sqlite_database_path()
    if database_path is None:
        return
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")


def sql_type_for_field(field):
    lowered = str(field.get("type", "text")).lower()
    if field.get("auto"):
        return Integer
    if lowered in {"int", "integer"}:
        return Integer
    if lowered in {"number", "float", "double", "money", "currency", "decimal"}:
        return Float
    if lowered in {"bool", "boolean"}:
        return Boolean
    if lowered in {"string", "varchar", "email"}:
        return String(255)
    return Text


def column_for_field(field, key_name):
    name = field["name"]
    is_primary = name == key_name or bool(field.get("auto"))
    kwargs = {
        "primary_key": is_primary,
        "nullable": False if is_primary or "required" in field.get("attributes", []) else True,
    }
    if field.get("auto"):
        kwargs["autoincrement"] = True
    if field.get("unique"):
        kwargs["unique"] = True
    return Column(name, sql_type_for_field(field), **kwargs)


def build_sql_tables():
    sql_tables = {}
    for table_name, fields in TABLES.items():
        key_name = primary_key(table_name)
        columns = [column_for_field(field, key_name) for field in fields]
        if not columns:
            columns.append(Column("id", Integer, primary_key=True, autoincrement=True))
        sql_tables[table_name] = Table(table_name, metadata, *columns)
    return sql_tables


prepare_sqlite_database()
engine = create_engine(
    DATABASE_URL,
    future=True,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.close()


metadata = MetaData()
SQL_TABLES = build_sql_tables()


def sql_table(table_name):
    table = SQL_TABLES.get(table_name)
    if table is None:
        raise KeyError(f"Unknown table: {table_name}")
    return table


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)


def list_rows(table_name):
    table = sql_table(table_name)
    with engine.connect() as connection:
        rows = connection.execute(select(table)).mappings().all()
    return [row_to_dict(row) for row in rows]


def public_row(table_name, row):
    if row is None:
        return None
    secure_fields = {field["name"] for field in table_schema(table_name) if field.get("secure")}
    return {name: value for name, value in row.items() if name not in secure_fields}


def public_rows(table_name):
    return [public_row(table_name, row) for row in list_rows(table_name)]


def count_rows(table_name):
    table = sql_table(table_name)
    with engine.connect() as connection:
        return int(connection.execute(select(func.count()).select_from(table)).scalar_one())


def sum_rows(table_name, field_name):
    table = sql_table(table_name)
    if field_name not in table.c.keys():
        return 0
    with engine.connect() as connection:
        value = connection.execute(select(func.coalesce(func.sum(table.c[field_name]), 0))).scalar_one()
    return float(value or 0)


def get_row(table_name, row_id):
    table = sql_table(table_name)
    key = primary_key(table_name)
    if key not in table.c.keys():
        return None
    with engine.connect() as connection:
        row = connection.execute(select(table).where(table.c[key] == row_id)).mappings().first()
    return row_to_dict(row)


def create_row(table_name, row):
    table = sql_table(table_name)
    clean = sanitize_row(table_name, row)
    with engine.begin() as connection:
        result = connection.execute(insert(table).values(**clean))
        inserted_key = result.inserted_primary_key[0] if result.inserted_primary_key else None
    key = primary_key(table_name)
    if inserted_key is not None:
        created = get_row(table_name, inserted_key)
        if created is not None:
            return created
    if key in clean:
        created = get_row(table_name, clean[key])
        if created is not None:
            return created
    return clean


def update_row(table_name, row_id, values):
    table = sql_table(table_name)
    key = primary_key(table_name)
    if key not in table.c.keys():
        return None
    clean = sanitize_row(table_name, values, partial=True)
    if clean:
        with engine.begin() as connection:
            connection.execute(update(table).where(table.c[key] == row_id).values(**clean))
    return get_row(table_name, row_id)


def delete_row(table_name, row_id):
    table = sql_table(table_name)
    key = primary_key(table_name)
    existing = get_row(table_name, row_id)
    if existing is None or key not in table.c.keys():
        return None
    with engine.begin() as connection:
        connection.execute(delete(table).where(table.c[key] == row_id))
    return existing


def clear_rows(table_name):
    table = sql_table(table_name)
    with engine.begin() as connection:
        connection.execute(delete(table))


def next_id(table_name):
    table = sql_table(table_name)
    key = primary_key(table_name)
    if key not in table.c.keys():
        return 1
    with engine.connect() as connection:
        value = connection.execute(select(func.max(table.c[key]))).scalar_one()
    return int(value or 0) + 1


def sanitize_row(table_name, values, partial=False, include_auto=False):
    fields = table_schema(table_name)
    allowed = {field["name"]: field for field in fields}
    clean = {}
    for name, value in (values or {}).items():
        if name not in allowed:
            continue
        field = allowed[name]
        if field.get("auto") and not include_auto:
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
    if lowered in {"int", "integer", "auto"}:
        try:
            return int(float(value or 0))
        except (TypeError, ValueError):
            return 0
    if lowered in {"number", "float", "double", "money", "currency", "decimal"}:
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return 0.0
    if lowered in {"bool", "boolean"}:
        if isinstance(value, bool):
            return value
        return str(value).lower() in {"true", "1", "yes", "on"}
    return "" if value is None else value


def default_value(field_type):
    lowered = str(field_type).lower()
    if lowered in {"int", "integer", "auto"}:
        return 0
    if lowered in {"number", "float", "double", "money", "currency", "decimal"}:
        return 0.0
    if lowered in {"bool", "boolean"}:
        return False
    return ""


def seed_database():
    for table_name, rows in SEED_DATA.items():
        if not rows or count_rows(table_name) > 0:
            continue
        table = sql_table(table_name)
        with engine.begin() as connection:
            for row in rows:
                connection.execute(insert(table).values(**sanitize_row(table_name, row, include_auto=True)))


def init_db():
    metadata.create_all(engine)
    seed_database()


def database_status():
    database_path = sqlite_database_path()
    return {
        "url": DATABASE_URL,
        "path": str(database_path) if database_path else "",
        "tables": list(SQL_TABLES.keys()),
    }


init_db()
