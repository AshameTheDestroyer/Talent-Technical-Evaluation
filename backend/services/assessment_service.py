from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import json

from models.assessment import Assessment
from schemas.assessment import AssessmentCreate, AssessmentUpdate
from logging_config import get_logger
from services.ai_service import generate_questions
from integrations.ai_integration.ai_factory import AIProvider

# Create logger for this module
logger = get_logger(__name__)

def get_assessment(db: Session, assessment_id: str) -> Optional[Assessment]:
    """Get assessment by ID"""
    logger.debug(f"Retrieving assessment with ID: {assessment_id}")
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if assessment:
        logger.debug(f"Found assessment: {assessment.id}")
    else:
        logger.debug(f"Assessment not found for ID: {assessment_id}")
    return assessment

def get_assessments_by_job(db: Session, job_id: str, skip: int = 0, limit: int = 100) -> List[Assessment]:
    """Get list of assessments by job ID"""
    logger.debug(f"Retrieving assessments for job ID: {job_id}, skip={skip}, limit={limit}")
    assessments = db.query(Assessment).filter(Assessment.job_id == job_id).offset(skip).limit(limit).all()
    logger.debug(f"Retrieved {len(assessments)} assessments for job ID: {job_id}")
    return assessments

def get_active_assessments_by_job(db: Session, job_id: str, skip: int = 0, limit: int = 100) -> List[Assessment]:
    """Get list of active assessments by job ID"""
    logger.debug(f"Retrieving active assessments for job ID: {job_id}, skip={skip}, limit={limit}")
    assessments = db.query(Assessment).filter(Assessment.job_id == job_id, Assessment.active == True).offset(skip).limit(limit).all()
    logger.debug(f"Retrieved {len(assessments)} active assessments for job ID: {job_id}")
    return assessments

def create_assessment(db: Session, job_id: str, assessment: AssessmentCreate) -> Assessment:
    """Create a new assessment"""
    logger.info(f"Creating new assessment for job ID: {job_id}, title: {assessment.title}")

    # Get the job information to include in the AI request
    from .job_service import get_job
    job = get_job(db, job_id)
    if not job:
        logger.error(f"Job not found for ID: {job_id}")
        raise ValueError(f"Job not found for ID: {job_id}")

    # Prepare job information for the AI service
    import json
    job_info = {
        "title": job.title,
        "seniority": job.seniority,
        "description": job.description,
        "skill_categories": json.loads(job.skill_categories) if job.skill_categories else []
    }

    # Generate questions using the AI service based on the provided question types and job info
    generated_questions = generate_questions(
        title=assessment.title,
        questions_types=[qt.value for qt in assessment.questions_types],  # Convert enum values to strings
        additional_note=assessment.additional_note,
        job_info=job_info
    )

    # Convert the generated questions to JSON
    questions_json = json.dumps([q.model_dump() for q in generated_questions])

    db_assessment = Assessment(
        id=str(uuid.uuid4()),
        job_id=job_id,
        title=assessment.title,
        duration=getattr(assessment, 'duration', None),  # Include duration if available
        passing_score=assessment.passing_score,
        questions=questions_json,  # Store as JSON string
        active=True
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    logger.info(f"Successfully created assessment with ID: {db_assessment.id} for job ID: {job_id}")
    return db_assessment

def update_assessment(db: Session, assessment_id: str, **kwargs) -> Optional[Assessment]:
    """Update an assessment"""
    logger.info(f"Updating assessment with ID: {assessment_id}")
    db_assessment = get_assessment(db, assessment_id)
    if db_assessment:
        for key, value in kwargs.items():
            if key == 'questions':
                if isinstance(value, list):
                    # Value is already a JSON string if coming from regenerate_assessment
                    setattr(db_assessment, key, json.dumps([q.model_dump() if hasattr(q, 'model_dump') else q for q in value]))
                elif isinstance(value, str):
                    # Value is already a JSON string
                    setattr(db_assessment, key, value)
                else:
                    # Handle other cases
                    setattr(db_assessment, key, json.dumps(value))
            else:
                setattr(db_assessment, key, value)
        db.commit()
        db.refresh(db_assessment)
        logger.info(f"Successfully updated assessment: {db_assessment.id}")
        return db_assessment
    logger.warning(f"Failed to update assessment - assessment not found: {assessment_id}")
    return None

def regenerate_assessment(db: Session, assessment_id: str, **kwargs) -> Optional[Assessment]:
    """Regenerate an assessment"""
    logger.info(f"Regenerating assessment with ID: {assessment_id}")

    # Check if questions_types is provided in kwargs to regenerate questions
    if 'questions_types' in kwargs and kwargs['questions_types'] is not None:
        # Get the assessment to access its title and job_id
        assessment = get_assessment(db, assessment_id)
        if not assessment:
            logger.warning(f"Assessment not found for regeneration: {assessment_id}")
            return None

        # Get the job information to include in the AI request
        from .job_service import get_job
        job = get_job(db, assessment.job_id)
        if not job:
            logger.error(f"Job not found for assessment ID: {assessment_id}")
            raise ValueError(f"Job not found for assessment ID: {assessment_id}")

        # Prepare job information for the AI service
        import json
        job_info = {
            "title": job.title,
            "seniority": job.seniority,
            "description": job.description,
            "skill_categories": json.loads(job.skill_categories) if job.skill_categories else []
        }

        # Generate new questions using the AI service
        additional_note = kwargs.get('additional_note', None)
        generated_questions = generate_questions(
            title=assessment.title,
            questions_types=kwargs['questions_types'],
            additional_note=additional_note,
            job_info=job_info
        )

        # Convert the generated questions to JSON
        questions_json = json.dumps([q.model_dump() for q in generated_questions])

        # Update the kwargs to use the generated questions
        kwargs['questions'] = questions_json
        # Remove questions_types from kwargs as it's not a field in the Assessment model
        del kwargs['questions_types']

    # Update the assessment with the new data
    result = update_assessment(db, assessment_id, **kwargs)
    if result:
        logger.info(f"Successfully regenerated assessment: {result.id}")
    else:
        logger.warning(f"Failed to regenerate assessment - assessment not found: {assessment_id}")
    return result

def delete_assessment(db: Session, assessment_id: str) -> bool:
    """Delete an assessment"""
    logger.info(f"Deleting assessment with ID: {assessment_id}")
    db_assessment = get_assessment(db, assessment_id)
    if db_assessment:
        db.delete(db_assessment)
        db.commit()
        logger.info(f"Successfully deleted assessment: {db_assessment.id}")
        return True
    logger.warning(f"Failed to delete assessment - assessment not found: {assessment_id}")
    return False