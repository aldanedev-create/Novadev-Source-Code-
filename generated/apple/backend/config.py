"""Generated NovaDev 1.1 Flask backend config."""

import os
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BACKEND_DIR / "database.db"
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///" + DATABASE_PATH.as_posix())
FRONTEND_RELATIVE = '..\\..\\..\\..\\frontend'
API_PREFIX = "/api"
