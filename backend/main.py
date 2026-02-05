from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import from our modules
from models import Base
from database.database import engine
from api.routes import router as root_router
from api.user_routes import router as user_router
from api.job_routes import router as job_router
from api.assessment_routes import router as assessment_router
from api.application_routes import router as application_router
from config import settings
from logging_config import get_logger

# Create logger for this module
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Database URL: {settings.database_url}")
    logger.info("Application started successfully")
    yield
    # Shutdown
    logger.info("Application shutting down")

# Initialize FastAPI app with settings
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan
)

# Configure CORS for frontend dev server(s)
# Default to allowing the common Vite port and localhost:3000 for React dev
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(root_router)
app.include_router(user_router)
app.include_router(job_router)
app.include_router(assessment_router)
app.include_router(application_router)

logger.info("Application routes registered")

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
    )