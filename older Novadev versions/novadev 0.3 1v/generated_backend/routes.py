"""Generated NovaDev 0.3 route registry."""

from models import list_rows

ROUTES = [{'method': 'GET', 'path': '/api/products', 'handler': 'route_0'}, {'method': 'GET', 'path': '/api/orders/count', 'handler': 'route_1'}]


def handle_route(method, path, body=None):
    for route in ROUTES:
        if route["method"] == method and route["path"] == path:
            return globals()[route["handler"]](body or {})
    return {"error": "route not found", "method": method, "path": path}, 404

def route_0(body):
    return list_rows("Product"), 200

def route_1(body):
    return {"count": len(list_rows("Order"))}, 200

