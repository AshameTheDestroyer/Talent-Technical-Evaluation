from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import json

from models.application import Application
from schemas.application import ApplicationCreate, ApplicationUpdate
from logging_config import get_logger

# Create logger for this module
logger = get_logger(__name__)

def get_application(db: Session, application_id: str) -> Optional[Application]:
    """Get application by ID"""
    logger.debug(f"Retrieving application with ID: {application_id}")
    application = db.query(Application).filter(Application.id == application_id).first()
    if application:
        logger.debug(f"Found application: {application.id}")
    else:
        logger.debug(f"Application not found for ID: {application_id}")
    return application

def get_applications_by_job_and_assessment(db: Session, job_id: str, assessment_id: str, skip: int = 0, limit: int = 100) -> List[Application]:
    """Get list of applications by job and assessment IDs"""
    logger.debug(f"Retrieving applications for job ID: {job_id}, assessment ID: {assessment_id}, skip={skip}, limit={limit}")
    applications = db.query(Application).filter(
        Application.job_id == job_id,
        Application.assessment_id == assessment_id
    ).offset(skip).limit(limit).all()
    logger.debug(f"Retrieved {len(applications)} applications for job ID: {job_id}, assessment ID: {assessment_id}")
    return applications

def get_applications_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Application]:
    """Get list of applications by user ID"""
    logger.debug(f"Retrieving applications for user ID: {user_id}, skip={skip}, limit={limit}")
    applications = db.query(Application).filter(Application.user_id == user_id).offset(skip).limit(limit).all()
    logger.debug(f"Retrieved {len(applications)} applications for user ID: {user_id}")
    return applications

def create_application(db: Session, application: ApplicationCreate) -> Application:
    """Create a new application"""
    logger.info(f"Creating new application for job ID: {application.job_id}, assessment ID: {application.assessment_id}, user ID: {application.user_id}")
    db_application = Application(
        id=str(uuid.uuid4()),
        job_id=application.job_id,
        assessment_id=application.assessment_id,
        user_id=application.user_id,
        answers=json.dumps([ans.dict() for ans in application.answers])  # Store as JSON string
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    logger.info(f"Successfully created application with ID: {db_application.id}")
    return db_application

def update_application(db: Session, application_id: str, **kwargs) -> Optional[Application]:
    """Update an application"""
    logger.info(f"Updating application with ID: {application_id}")
    db_application = get_application(db, application_id)
    if db_application:
        for key, value in kwargs.items():
            if key == 'answers' and isinstance(value, list):
                setattr(db_application, key, json.dumps([ans.dict() if hasattr(ans, 'dict') else ans for ans in value]))
            else:
                setattr(db_application, key, value)
        db.commit()
        db.refresh(db_application)
        logger.info(f"Successfully updated application: {db_application.id}")
        return db_application
    logger.warning(f"Failed to update application - application not found: {application_id}")
    return None

def delete_application(db: Session, application_id: str) -> bool:
    """Delete an application"""
    logger.info(f"Deleting application with ID: {application_id}")
    db_application = get_application(db, application_id)
    if db_application:
        db.delete(db_application)
        db.commit()
        logger.info(f"Successfully deleted application: {db_application.id}")
        return True
    logger.warning(f"Failed to delete application - application not found: {application_id}")
    return False

def calculate_application_score(db: Session, application_id: str) -> float:
    """Calculate the score for an application"""
    logger.debug(f"Calculating score for application ID: {application_id}")

    # Get the application
    application = get_application(db, application_id)
    if not application:
        logger.warning(f"Application not found for ID: {application_id}")
        return 0.0

    # Get the associated assessment to compare answers with correct answers
    from models.assessment import Assessment
    assessment = db.query(Assessment).filter(Assessment.id == application.assessment_id).first()
    if not assessment:
        logger.warning(f"Assessment not found for application ID: {application_id}")
        return 0.0

    # Parse the answers and questions
    import json
    try:
        answers = json.loads(application.answers) if application.answers else []
        questions = json.loads(assessment.questions) if assessment.questions else []
    except json.JSONDecodeError:
        logger.error(f"Failed to parse answers or questions for application ID: {application_id}")
        return 0.0

    # Create a mapping of question_id to question for easy lookup
    question_map = {q['id']: q for q in questions}

    # Calculate the score
    total_points = 0
    earned_points = 0

    for answer in answers:
        question_id = answer.get('question_id')
        if not question_id or question_id not in question_map:
            continue

        question_data = question_map[question_id]

        # Calculate weighted score
        question_weight = question_data.get('weight', 1)  # Default weight is 1
        total_points += question_weight

        # For multiple choice questions, score directly without AI
        if question_data['type'] in ['choose_one', 'choose_many']:
            correct_options = set(question_data.get('correct_options', []))
            selected_options = set(answer.get('options', []))

            # Check if the selected options match the correct options exactly
            if selected_options == correct_options:
                earned_points += question_weight  # Full points for correct answer
            # Otherwise, 0 points for incorrect answer (no partial credit for multiple choice)

        # For text-based questions, use AI to evaluate the answer
        elif question_data['type'] == 'text_based':
            # Convert the question data to an AssessmentQuestion object
            from schemas.assessment import AssessmentQuestion, AssessmentQuestionOption
            from schemas.enums import QuestionType
            question_obj = AssessmentQuestion(
                id=question_data['id'],
                text=question_data['text'],
                weight=question_data['weight'],
                skill_categories=question_data['skill_categories'],
                type=QuestionType(question_data['type']),
                options=[AssessmentQuestionOption(text=opt['text'], value=opt['value']) for opt in question_data.get('options', [])],
                correct_options=question_data.get('correct_options', [])
            )

            # Use AI service to score the text-based answer
            from services.ai_service import score_answer
            score_result = score_answer(
                question=question_obj,
                answer_text=answer.get('text', ''),
                selected_options=answer.get('options', [])
            )

            earned_points += score_result['score'] * question_weight

    # Calculate percentage score
    if total_points > 0:
        score = (earned_points / total_points) * 100
    else:
        score = 0.0

    logger.debug(f"Calculated score for application ID {application_id}: {score}% ({earned_points}/{total_points} points)")
    return round(score, 2)