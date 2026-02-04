from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from database.database import get_db
from schemas import ApplicationCreate, ApplicationUpdate, ApplicationResponse, ApplicationListResponse, ApplicationDetailedResponse, ApplicationDetailedListResponse
from services import create_application, get_application, get_applications_by_job_and_assessment, calculate_application_score
from services.assessment_service import get_assessment
from utils.dependencies import get_current_user
from models.user import User
from logging_config import get_logger

# Create logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/applications", tags=["applications"])

@router.get("/jobs/{jid}/assessments/{aid}", response_model=ApplicationDetailedListResponse)
def get_applications_list(jid: str, aid: str, page: int = 1, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get list of applications for an assessment"""
    logger.info(f"Retrieving applications list for job ID: {jid}, assessment ID: {aid}, page: {page}, limit: {limit} by user: {current_user.id}")
    # Only HR users can view applications
    if current_user.role != "hr":
        logger.warning(f"Unauthorized attempt to view applications by user: {current_user.id} with role: {current_user.role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR users can view applications"
        )
    skip = (page - 1) * limit
    applications = get_applications_by_job_and_assessment(db, jid, aid, skip=skip, limit=limit)

    # Calculate total count
    total = len(get_applications_by_job_and_assessment(db, jid, aid, skip=0, limit=1000))  # Simplified for demo

    # Convert answers from JSON string to list and calculate scores
    application_responses = []
    for application in applications:
        application_dict = application.__dict__
        if application.answers:
            application_dict['answers'] = json.loads(application.answers)
        else:
            application_dict['answers'] = []

        # Calculate score (placeholder)
        application_dict['score'] = calculate_application_score(db, application.id)
        application_dict['passing_score'] = 0.0  # Placeholder

        application_responses.append(ApplicationResponse(**application_dict))

    logger.info(f"Successfully retrieved {len(applications)} applications out of total {total} for job ID: {jid}, assessment ID: {aid}")
    return ApplicationDetailedListResponse(
        count=len(applications),
        total=total,
        data=application_responses
    )

@router.post("/jobs/{jid}/assessments/{aid}", response_model=dict)  # Returns just id as per requirements
def create_new_application(jid: str, aid: str, application: ApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new application for an assessment"""
    logger.info(f"Creating new application for job ID: {jid}, assessment ID: {aid}, user ID: {application.user_id} by user: {current_user.id}")
    # Only applicant users can create applications
    if current_user.role != "applicant":
        logger.warning(f"Unauthorized attempt to create application by user: {current_user.id} with role: {current_user.role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only applicant users can submit applications"
        )
    # Ensure the user submitting the application is the same as the one in the request
    if current_user.id != application.user_id:
        logger.warning(f"User {current_user.id} attempted to submit application for user {application.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot submit application for another user"
        )

    # Validate that the job and assessment exist and match
    assessment_obj = get_assessment(db, aid)
    if not assessment_obj or assessment_obj.job_id != jid:
        logger.warning(f"Assessment not found for job ID: {jid}, assessment ID: {aid}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found for this job"
        )

    db_application = create_application(db, application)
    logger.info(f"Successfully created application with ID: {db_application.id} for job ID: {jid}, assessment ID: {aid}")
    return {"id": db_application.id}