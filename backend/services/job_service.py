from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import json

from models.job import Job
from schemas.job import JobCreate, JobUpdate
from logging_config import get_logger

# Create logger for this module
logger = get_logger(__name__)

def get_job(db: Session, job_id: str) -> Optional[Job]:
    """Get job by ID"""
    logger.debug(f"Retrieving job with ID: {job_id}")
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        logger.debug(f"Found job: {job.id}")
    else:
        logger.debug(f"Job not found for ID: {job_id}")
    return job

def get_jobs(db: Session, skip: int = 0, limit: int = 100) -> List[Job]:
    """Get list of jobs"""
    logger.debug(f"Retrieving jobs with skip={skip}, limit={limit}")
    jobs = db.query(Job).offset(skip).limit(limit).all()
    logger.debug(f"Retrieved {len(jobs)} jobs")
    return jobs

def get_active_jobs(db: Session, skip: int = 0, limit: int = 100) -> List[Job]:
    """Get list of active jobs"""
    logger.debug(f"Retrieving active jobs with skip={skip}, limit={limit}")
    jobs = db.query(Job).filter(Job.active == True).offset(skip).limit(limit).all()
    logger.debug(f"Retrieved {len(jobs)} active jobs")
    return jobs

def create_job(db: Session, job: JobCreate) -> Job:
    """Create a new job"""
    logger.info(f"Creating new job with title: {job.title}")
    db_job = Job(
        id=str(uuid.uuid4()),
        title=job.title,
        seniority=job.seniority,
        description=job.description,
        skill_categories=json.dumps(job.skill_categories) if job.skill_categories else "[]",
        active=job.active
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    logger.info(f"Successfully created job with ID: {db_job.id}")
    return db_job

def update_job(db: Session, job_id: str, **kwargs) -> Optional[Job]:
    """Update a job"""
    logger.info(f"Updating job with ID: {job_id}")
    db_job = get_job(db, job_id)
    if db_job:
        for key, value in kwargs.items():
            if key == 'skill_categories' and isinstance(value, list):
                setattr(db_job, key, json.dumps(value))
            else:
                setattr(db_job, key, value)
        db.commit()
        db.refresh(db_job)
        logger.info(f"Successfully updated job: {db_job.id}")
        return db_job
    logger.warning(f"Failed to update job - job not found: {job_id}")
    return None

def delete_job(db: Session, job_id: str) -> bool:
    """Delete a job"""
    logger.info(f"Deleting job with ID: {job_id}")
    db_job = get_job(db, job_id)
    if db_job:
        db.delete(db_job)
        db.commit()
        logger.info(f"Successfully deleted job: {db_job.id}")
        return True
    logger.warning(f"Failed to delete job - job not found: {job_id}")
    return False

def get_job_applicants_count(db: Session, job_id: str) -> int:
    """Get the number of applicants for a job"""
    logger.debug(f"Getting applicant count for job ID: {job_id}")
    # This would require joining with the applications table
    # For now, returning a placeholder
    from models.application import Application
    count = db.query(Application).filter(Application.job_id == job_id).count()
    logger.debug(f"Applicant count for job ID {job_id}: {count}")
    return count