from __future__ import annotations

"""Starter backend generator for NovaDev 0.3.

The generated backend uses only the Python standard library. It is intentionally
small: enough to show how route and table declarations can become real files.
"""

from pathlib import Path
from typing import List

from .ast_nodes import Program, expression_to_source
from .runtime import Runtime


class BackendGenerator:
    def generate(self, program: Program, output_dir: Path | str = "generated_backend") -> List[Path]:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        runtime = Runtime()
        runtime.load_declarations(program)

        files = {
            output_path / "models.py": self.models_py(runtime),
            output_path / "routes.py": self.routes_py(runtime),
            output_path / "app.py": self.app_py(),
        }
        for path, content in files.items():
            path.write_text(content, encoding="utf-8")
        return list(files.keys())

    def models_py(self, runtime: Runtime) -> str:
        tables = {
            name: [{"name": field.name, "type": field.field_type, "attributes": field.attributes} for field in table.fields]
            for name, table in runtime.tables.items()
        }
        return f'''"""Generated NovaDev 0.3 model registry."""

TABLES = {tables!r}
DATA = {{name: [] for name in TABLES}}


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
'''

    def routes_py(self, runtime: Runtime) -> str:
        route_entries = []
        handlers = []
        for index, route in enumerate(runtime.routes):
            handler = f"route_{index}"
            route_entries.append({"method": route.method, "path": route.path, "handler": handler})
            handlers.append(self.handler_py(handler, route.return_expr))
        return f'''"""Generated NovaDev 0.3 route registry."""

from models import list_rows

ROUTES = {route_entries!r}


def handle_route(method, path, body=None):
    for route in ROUTES:
        if route["method"] == method and route["path"] == path:
            return globals()[route["handler"]](body or {{}})
    return {{"error": "route not found", "method": method, "path": path}}, 404

{chr(10).join(handlers)}
'''

    def handler_py(self, name: str, expression) -> str:
        source = expression_to_source(expression)
        if source.endswith(".all()"):
            table = source[:-6]
            body = f'return list_rows("{table}"), 200'
        elif source.endswith(".count()"):
            table = source[:-8]
            body = f'return {{"count": len(list_rows("{table}"))}}, 200'
        elif source:
            body = f'return {{"result": {source!r}}}, 200'
        else:
            body = 'return {"ok": True}, 200'
        return f"""def {name}(body):
    {body}
"""

    def app_py(self) -> str:
        return '''"""Generated NovaDev 0.3 backend app.

Run with:
    python app.py
Then open http://127.0.0.1:8000/api/products or another generated route.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from routes import handle_route


class NovaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond("GET")

    def do_POST(self):
        self.respond("POST")

    def respond(self, method):
        path = urlparse(self.path).path
        result, status = handle_route(method, path)
        payload = json.dumps(result).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), NovaHandler)
    print("NovaDev backend running at http://127.0.0.1:8000")
    server.serve_forever()
'''
