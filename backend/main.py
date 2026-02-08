from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
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

# Read environment variables (HF Spaces will set PORT=7860)
HOST = os.getenv("HOST", settings.host)
PORT = int(os.getenv("PORT", settings.port))  # Default to config port for local dev
DEBUG = os.getenv("DEBUG", str(settings.debug)).lower() == "true"

# Initialize FastAPI app with settings
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

# Initialize database tables on startup
@app.on_event("startup")
def startup_event():
    from models import Base
    from database.database import engine
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")

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

api_router = APIRouter(prefix="/api")
# Include API routes
api_router.include_router(root_router)
api_router.include_router(user_router)
api_router.include_router(job_router)
api_router.include_router(assessment_router)
api_router.include_router(application_router)

app.include_router(api_router)

# Mount static files directory (serves React build output)
# MUST come AFTER API routes to avoid conflicts
app.mount("/static", StaticFiles(directory="static"), name="static")

logger.info("Application routes registered")

# SPA fallback handler - serves index.html for all non-API routes
# MUST be the last route defined
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    static_dir = Path("static")
    client_dir = static_dir / "client"
    target = static_dir / full_path
    
    # First check if the requested path exists in the static root
    if target.exists() and not target.is_dir():
        return FileResponse(target)
    
    # Then check if it exists in the client directory (for React assets)
    client_target = client_dir / full_path
    if client_target.exists() and not client_target.is_dir():
        return FileResponse(client_target)

    # Fallback to index.html for client-side routing
    index_path = client_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)

    raise HTTPException(status_code=404, detail="Page not found")


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        app,
        host=HOST,  # Use the environment-configured host
        port=PORT,  # Use the environment-configured port
    )