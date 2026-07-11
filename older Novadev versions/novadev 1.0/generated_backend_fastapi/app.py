"""Generated NovaDev 0.5 FastAPI app."""

from fastapi import FastAPI

from routes import router

app = FastAPI(title="NovaDev FastAPI Backend")
app.include_router(router)
