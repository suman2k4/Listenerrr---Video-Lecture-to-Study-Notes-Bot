from fastapi import FastAPI

from app.api import api_router
from app.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/healthz")
async def healthcheck():
    return {"status": "ok"}
