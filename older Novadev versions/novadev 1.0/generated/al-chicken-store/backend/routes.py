"""Generated NovaDev 0.4 declared route handlers."""

from models import count_rows, public_rows, sum_rows

ROUTES = [{'method': 'GET', 'path': '/api/health', 'handler': 'route_0', 'requires_auth': False, 'required_role': None}]


def handle_declared_route(method, path, body=None):
    for route in ROUTES:
        if route["method"] == method and route["path"] == path:
            return globals()[route["handler"]](body or {})
    return None

def route_0(body):
    return {"result": '"ALChickenStore is running"'}, 200

