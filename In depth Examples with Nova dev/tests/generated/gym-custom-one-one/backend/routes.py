"""Generated NovaDev 1.1 declared route handlers."""

from models import count_rows, create_row, public_row, public_rows, sum_rows, table_schema

ROUTES = []


def handle_declared_route(method, path, body=None):
    for route in ROUTES:
        if route["method"] == method and route["path"] == path:
            return globals()[route["handler"]](body or {})
    return None




# NovaDev 1.1 workflow routes generated from ProjectIR
def ensure_backend_path():
    import sys
    from pathlib import Path

    backend_dir = str(Path(__file__).resolve().parent)
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)


def load_backend_module(module_name):
    import importlib.util
    from pathlib import Path

    ensure_backend_path()
    module_path = Path(__file__).resolve().parent / "modules" / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(f"_novadev_generated_{module_name}", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def workflow_payload(table_name, body, module_result=None):
    payload = dict(body) if isinstance(body, dict) else {}
    field_names = {field["name"] for field in table_schema(table_name)}
    if module_result is not None:
        if isinstance(module_result, str):
            for text_field in ("message", "content", "text"):
                if text_field in field_names:
                    payload[text_field] = module_result
                    break
        for result_field in ("amount", "total", "value", "result", "score"):
            if result_field in field_names and result_field not in payload:
                payload[result_field] = module_result
                break
    if "leadName" in field_names and "leadName" not in payload:
        payload["leadName"] = payload.get("name") or payload.get("customerName") or ""
    if "customerName" in field_names and "customerName" not in payload:
        payload["customerName"] = payload.get("name") or ""
    if "status" in field_names and not payload.get("status"):
        payload["status"] = "Created"
    return payload

ROUTES.append({"method": "POST", "path": "/api/workflows/member-check-in", "handler": "workflow_member_check_in", "requires_auth": False, "required_role": None})
def workflow_member_check_in(body):
    module_gym_tools = load_backend_module('gym_tools')
    module_result = module_gym_tools.status(**body) if isinstance(body, dict) else module_gym_tools.status(body)
    result = {"workflow": 'MemberCheckIn', "result": module_result, "body": body}

    payload_check_in = workflow_payload('CheckIn', body, module_result)
    created_check_in = create_row('CheckIn', payload_check_in)
    result['CheckIn'] = public_row('CheckIn', created_check_in)
    return result, 200

