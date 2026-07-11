"""Generated NovaDev 0.5 FastAPI routes."""

from fastapi import APIRouter, HTTPException

from models import DATA

router = APIRouter(prefix="/api")
RESOURCES = {'incidents': 'Incident'}


@router.get("/health")
def health():
    return {"ok": True, "backend": "FastAPI"}


@router.get("/{resource}")
def list_rows(resource: str):
    table = RESOURCES.get(resource)
    if not table:
        raise HTTPException(status_code=404, detail="Unknown resource")
    return {"rows": DATA.get(table, [])}
