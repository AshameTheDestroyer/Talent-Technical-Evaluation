from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from database.database import get_db
from schemas import JobCreate, JobUpdate, JobResponse, JobListResponse
from services import create_job, get_job, get_active_jobs, update_job, delete_job, get_job_applicants_count
from utils.dependencies import get_current_user
from models.user import User
from logging_config import get_logger

# Create logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("", response_model=JobListResponse)
def get_jobs_list(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    """Get list of jobs"""
    logger.info(f"Retrieving jobs list - page: {page}, limit: {limit}")
    skip = (page - 1) * limit
    jobs = get_active_jobs(db, skip=skip, limit=limit)

    # Calculate total count
    total = len(get_active_jobs(db, skip=0, limit=1000))  # Simplified for demo

    # Convert skill_categories from JSON string to list and add applicants_count
    job_responses = []
    for job in jobs:
        job_dict = job.__dict__
        if job.skill_categories:
            job_dict['skill_categories'] = json.loads(job.skill_categories)
        else:
            job_dict['skill_categories'] = []

        # Add applicants count
        job_dict['applicants_count'] = get_job_applicants_count(db, job.id)
        job_responses.append(JobResponse(**job_dict))

    logger.info(f"Successfully retrieved {len(jobs)} jobs out of total {total}")
    return JobListResponse(
        count=len(jobs),
        total=total,
        data=job_responses
    )

@router.get("/{id}", response_model=JobResponse)
def get_job_details(id: str, db: Session = Depends(get_db)):
    """Get job details by ID"""
    logger.info(f"Retrieving job details for ID: {id}")
    job = get_job(db, id)
    if not job:
        logger.warning(f"Job not found for ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    # Convert skill_categories from JSON string to list and add applicants_count
    job_dict = job.__dict__
    if job.skill_categories:
        job_dict['skill_categories'] = json.loads(job.skill_categories)
    else:
        job_dict['skill_categories'] = []

    job_dict['applicants_count'] = get_job_applicants_count(db, job.id)

    logger.info(f"Successfully retrieved job details for ID: {job.id}")
    return JobResponse(**job_dict)

@router.post("", response_model=dict)  # Returns just id as per requirements
def create_new_job(job: JobCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new job"""
    logger.info(f"Creating new job with title: {job.title} by user: {current_user.id}")
    # Only HR users can create jobs
    if current_user.role != "hr":
        logger.warning(f"Unauthorized attempt to create job by user: {current_user.id} with role: {current_user.role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR users can create jobs"
        )
    db_job = create_job(db, job)
    logger.info(f"Successfully created job with ID: {db_job.id}")
    return {"id": db_job.id}

@router.patch("/{id}")
def update_existing_job(id: str, job_update: JobUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update an existing job"""
    logger.info(f"Updating job with ID: {id} by user: {current_user.id}")
    # Only HR users can update jobs
    if current_user.role != "hr":
        logger.warning(f"Unauthorized attempt to update job by user: {current_user.id} with role: {current_user.role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR users can update jobs"
        )
    updated_job = update_job(db, id, **job_update.dict(exclude_unset=True))
    if not updated_job:
        logger.warning(f"Job not found for update with ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    logger.info(f"Successfully updated job with ID: {updated_job.id}")
    return {}

@router.delete("/{id}")
def delete_existing_job(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a job"""
    logger.info(f"Deleting job with ID: {id} by user: {current_user.id}")
    # Only HR users can delete jobs
    if current_user.role != "hr":
        logger.warning(f"Unauthorized attempt to delete job by user: {current_user.id} with role: {current_user.role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR users can delete jobs"
        )
    success = delete_job(db, id)
    if not success:
        logger.warning(f"Job not found for deletion with ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    logger.info(f"Successfully deleted job with ID: {id}")
    return {}