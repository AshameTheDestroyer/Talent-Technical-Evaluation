from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from database.database import get_db
from schemas import AssessmentCreate, AssessmentUpdate, AssessmentRegenerate, AssessmentResponse, AssessmentListResponse, AssessmentDetailedResponse
from services import create_assessment, get_assessment, get_assessments_by_job, update_assessment, regenerate_assessment, delete_assessment
from utils.dependencies import get_current_user
from models.user import User
from logging_config import get_logger

# Create logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/assessments", tags=["assessments"])

@router.get("/jobs/{jid}", response_model=AssessmentListResponse)
def get_assessments_list(jid: str, page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    """Get list of assessments for a job"""
    logger.info(f"Retrieving assessments list for job ID: {jid}, page: {page}, limit: {limit}")
    skip = (page - 1) * limit
    assessments = get_assessments_by_job(db, jid, skip=skip, limit=limit)

    # Calculate total count
    total = len(get_assessments_by_job(db, jid, skip=0, limit=1000))  # Simplified for demo

    # Convert questions from JSON string to list and add questions_count
    assessment_responses = []
    for assessment in assessments:
        assessment_dict = assessment.__dict__
        if assessment.questions:
            assessment_dict['questions'] = json.loads(assessment.questions)
        else:
            assessment_dict['questions'] = []

        # Add questions count
        assessment_dict['questions_count'] = len(assessment_dict['questions'])
        assessment_responses.append(AssessmentResponse(**assessment_dict))

    logger.info(f"Successfully retrieved {len(assessments)} assessments out of total {total} for job ID: {jid}")
    return AssessmentListResponse(
        count=len(assessments),
        total=total,
        data=assessment_responses
    )

@router.get("/jobs/{jid}/{aid}", response_model=AssessmentDetailedResponse)
def get_assessment_details(jid: str, aid: str, db: Session = Depends(get_db)):
    """Get assessment details"""
    logger.info(f"Retrieving assessment details for job ID: {jid}, assessment ID: {aid}")
    assessment = get_assessment(db, aid)
    if not assessment or assessment.job_id != jid:
        logger.warning(f"Assessment not found for job ID: {jid}, assessment ID: {aid}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found for this job"
        )

    # Convert questions from JSON string to list and add questions_count
    assessment_dict = assessment.__dict__
    if assessment.questions:
        assessment_dict['questions'] = json.loads(assessment.questions)
    else:
        assessment_dict['questions'] = []

    assessment_dict['questions_count'] = len(assessment_dict['questions'])

    logger.info(f"Successfully retrieved assessment details for job ID: {jid}, assessment ID: {assessment.id}")
    return AssessmentDetailedResponse(**assessment_dict)

@router.post("/jobs/{id}", response_model=dict)  # Returns just id as per requirements
def create_new_assessment(id: str, assessment: AssessmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new assessment for a job"""
    logger.info(f"Creating new assessment for job ID: {id}, title: {assessment.title} by user: {current_user.id}")
    # Only HR users can create assessments
    if current_user.role != "hr":
        logger.warning(f"Unauthorized attempt to create assessment by user: {current_user.id} with role: {current_user.role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR users can create assessments"
        )
    db_assessment = create_assessment(db, id, assessment)
    logger.info(f"Successfully created assessment with ID: {db_assessment.id} for job ID: {id}")
    return {"id": db_assessment.id}

@router.patch("/jobs/{jid}/{aid}/regenerate")
def regenerate_assessment_route(jid: str, aid: str, regenerate_data: AssessmentRegenerate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Regenerate an assessment"""
    logger.info(f"Regenerating assessment for job ID: {jid}, assessment ID: {aid} by user: {current_user.id}")
    # Only HR users can regenerate assessments
    if current_user.role != "hr":
        logger.warning(f"Unauthorized attempt to regenerate assessment by user: {current_user.id} with role: {current_user.role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR users can regenerate assessments"
        )
    # Extract parameters from the request data using dict() to maintain consistency with other routes
    regenerate_params = regenerate_data.dict(exclude_unset=True)

    # Call the service function with the extracted parameters
    updated_assessment = regenerate_assessment(db, aid, **regenerate_params)
    if not updated_assessment:
        logger.warning(f"Assessment not found for regeneration with job ID: {jid}, assessment ID: {aid}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    logger.info(f"Successfully regenerated assessment with ID: {updated_assessment.id} for job ID: {jid}")
    return {}

@router.patch("/jobs/{jid}/{aid}")
def update_existing_assessment(jid: str, aid: str, assessment_update: AssessmentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update an existing assessment"""
    logger.info(f"Updating assessment for job ID: {jid}, assessment ID: {aid} by user: {current_user.id}")
    # Only HR users can update assessments
    if current_user.role != "hr":
        logger.warning(f"Unauthorized attempt to update assessment by user: {current_user.id} with role: {current_user.role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR users can update assessments"
        )
    updated_assessment = update_assessment(db, aid, **assessment_update.dict(exclude_unset=True))
    if not updated_assessment:
        logger.warning(f"Assessment not found for update with job ID: {jid}, assessment ID: {aid}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    logger.info(f"Successfully updated assessment with ID: {updated_assessment.id} for job ID: {jid}")
    return {}

@router.delete("/jobs/{jid}/{aid}")
def delete_existing_assessment(jid: str, aid: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete an assessment"""
    logger.info(f"Deleting assessment for job ID: {jid}, assessment ID: {aid} by user: {current_user.id}")
    # Only HR users can delete assessments
    if current_user.role != "hr":
        logger.warning(f"Unauthorized attempt to delete assessment by user: {current_user.id} with role: {current_user.role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR users can delete assessments"
        )
    success = delete_assessment(db, aid)
    if not success:
        logger.warning(f"Assessment not found for deletion with job ID: {jid}, assessment ID: {aid}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    logger.info(f"Successfully deleted assessment with ID: {aid} for job ID: {jid}")
    return {}