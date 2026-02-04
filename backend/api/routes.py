from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from database.database import get_db

router = APIRouter()

# Health check endpoint
@router.get("/", response_model=dict)
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to AI-Powered Hiring Assessment Platform API"}

@router.get("/health", status_code=200)
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify API is running and database is accessible"""
    try:
        # Test database connection using SQLAlchemy
        # Execute a simple query to test the connection
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2026-02-02T00:00:00"  # Placeholder timestamp
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")