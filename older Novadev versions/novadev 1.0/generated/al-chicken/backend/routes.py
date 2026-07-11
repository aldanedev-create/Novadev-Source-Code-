"""Generated NovaDev 0.5 declared route handlers."""

from models import count_rows, create_row, public_row, public_rows, sum_rows

ROUTES = [{'method': 'GET', 'path': '/api/products', 'handler': 'route_0', 'requires_auth': False, 'required_role': None}, {'method': 'POST', 'path': '/api/products', 'handler': 'route_1', 'requires_auth': True, 'required_role': 'Admin'}]


def handle_declared_route(method, path, body=None):
    for route in ROUTES:
        if route["method"] == method and route["path"] == path:
            return globals()[route["handler"]](body or {})
    return None

def route_0(body):
    return public_rows("Product"), 200

def route_1(body):
    return public_row("Product", create_row("Product", body)), 201

