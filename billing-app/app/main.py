"""FastAPI application initialization and configuration."""

import io
import logging
import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.endpoints import router
from app.core.config import settings
from app.core.database import engine, get_db
from app.models.models import Base

# Fix UTF-8 encoding for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8"
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding="utf-8"
    )

# Auto-create logs directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)
logger.info("Application started successfully")

# Create tables
Base.metadata.create_all(bind=engine)

# Create Jinja2 templates instance
templates = Jinja2Templates(directory="app/templates")

# Initialize FastAPI app
app = FastAPI(
    title="Billing System - Mallow Technologies",
    description="Production-ready billing application",
    version="1.0.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API routes
app.include_router(router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "detail": "Internal server error",
        },
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("Health check passed")
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("FastAPI startup event")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("FastAPI shutdown event")


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Uvicorn server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
