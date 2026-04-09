import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Ensure results directory exists
    os.makedirs("static/results", exist_ok=True)
    
    # Mount static files correctly
    app.mount("/static", StaticFiles(directory="static"), name="static")

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
