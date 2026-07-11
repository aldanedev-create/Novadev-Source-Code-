"""Generated NovaDev 0.3 declared route handlers."""

from models import count_rows, public_rows, sum_rows

ROUTES = [{'method': 'GET', 'path': '/api/products', 'handler': 'route_0', 'requires_auth': False, 'required_role': None}, {'method': 'GET', 'path': '/api/orders', 'handler': 'route_1', 'requires_auth': False, 'required_role': None}, {'method': 'GET', 'path': '/api/cart-items', 'handler': 'route_2', 'requires_auth': False, 'required_role': None}, {'method': 'GET', 'path': '/api/orders/count', 'handler': 'route_3', 'requires_auth': False, 'required_role': None}]


def handle_declared_route(method, path, body=None):
    for route in ROUTES:
        if route["method"] == method and route["path"] == path:
            return globals()[route["handler"]](body or {})
    return None

def route_0(body):
    return public_rows("Product"), 200

def route_1(body):
    return public_rows("Order"), 200

def route_2(body):
    return public_rows("CartItem"), 200

def route_3(body):
    return {"count": count_rows("Order")}, 200

