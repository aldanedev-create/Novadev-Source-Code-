"""Generated NovaDev 0.5 declared route handlers."""

from models import count_rows, create_row, public_row, public_rows, sum_rows

ROUTES = []


def handle_declared_route(method, path, body=None):
    for route in ROUTES:
        if route["method"] == method and route["path"] == path:
            return globals()[route["handler"]](body or {})
    return None


