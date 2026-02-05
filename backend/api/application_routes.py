from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from database.database import get_db
from schemas import ApplicationCreate, ApplicationUpdate, ApplicationResponse, ApplicationListResponse, ApplicationDetailedResponse, ApplicationDetailedListResponse, MyApplicationsListResponse, MyApplicationResponse, MyApplicationsJob, MyApplicationsAssessment, ApplicationAssessment
from services import create_application, get_application, get_applications_by_job_and_assessment, calculate_application_score, get_applications_by_user
from services.assessment_service import get_assessment
from services.job_service import get_job
from utils.dependencies import get_current_user
from models.user import User
from logging_config import get_logger

# Create logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/applications", tags=["applications"])

@router.get("/jobs/{jid}/assessments/{aid}")
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

    # Get the assessment to retrieve the passing score
    assessment = get_assessment(db, aid)
    if not assessment:
        logger.error(f"Assessment not found for ID: {aid}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    # Calculate scores and create responses
    application_responses = []
    for application in applications:
        # Calculate score
        score = calculate_application_score(db, application.id)

        # Get user information
        from services.user_service import get_user
        user = get_user(db, application.user_id)

        # Create response object that matches technical requirements exactly
        application_response = {
            'id': application.id,
            'job_id': application.job_id,
            'assessment_id': application.assessment_id,
            'user_id': application.user_id,
            'answers': [],  # Not including answers in the list view for performance
            'score': score,
            'passing_score': assessment.passing_score,
            'assessment_details': {
                'id': assessment.id,
                'title': assessment.title,
                'passing_score': assessment.passing_score,
                'created_at': None  # Assessment model doesn't have created_at field
            },
            'user': {
                'id': user.id if user else None,
                'first_name': user.first_name if user else None,
                'last_name': user.last_name if user else None,
                'email': user.email if user else None
            } if user else None
        }

        application_responses.append(application_response)

    logger.info(f"Successfully retrieved {len(applications)} applications out of total {total} for job ID: {jid}, assessment ID: {aid}")
    return {
        'count': len(applications),
        'total': total,
        'data': application_responses
    }

@router.get("/jobs/{jid}/assessment_id/{aid}/applications/{id}", response_model=ApplicationDetailedResponse)
def get_application_detail(jid: str, aid: str, id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get detailed application information including answers"""
    logger.info(f"Retrieving application detail for job ID: {jid}, assessment ID: {aid}, application ID: {id} by user: {current_user.id}")

    # Get the application
    application = get_application(db, id)
    if not application or application.job_id != jid or application.assessment_id != aid:
        logger.warning(f"Application not found for job ID: {jid}, assessment ID: {aid}, application ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found for this job and assessment"
        )

    # Authorization: Allow HR users or the applicant who owns the application
    if current_user.role != "hr" and current_user.id != application.user_id:
        logger.warning(f"Unauthorized attempt to view application detail by user: {current_user.id} with role: {current_user.role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR users or the applicant who submitted the application can view application details"
        )

    # Get the assessment to retrieve the passing score
    assessment = get_assessment(db, aid)
    if not assessment:
        logger.error(f"Assessment not found for ID: {aid}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    # Calculate score
    score = calculate_application_score(db, application.id)

    # Get user information
    from services.user_service import get_user
    user = get_user(db, application.user_id)

    # Parse answers from JSON string
    import json
    answers = json.loads(application.answers) if application.answers else []

    # Get the assessment questions to enrich the answers with question details
    assessment_questions = json.loads(assessment.questions) if assessment.questions else []
    question_map = {q['id']: q for q in assessment_questions}

    # Enrich answers with question details and rationales
    enriched_answers = []
    for answer in answers:
        question_id = answer.get('question_id')
        question_data = question_map.get(question_id, {})

        # For text-based questions, we might want to add rationale from AI scoring
        rationale = 'No rationale available'
        if question_data.get('type') == 'text_based':
            # Use AI service to get rationale for text-based answers
            from schemas.assessment import AssessmentQuestion, AssessmentQuestionOption
            from schemas.enums import QuestionType

            # Create a temporary question object for AI scoring
            temp_question = AssessmentQuestion(
                id=question_data['id'],
                text=question_data['text'],
                weight=question_data['weight'],
                skill_categories=question_data['skill_categories'],
                type=QuestionType(question_data['type']),
                options=[AssessmentQuestionOption(text=opt['text'], value=opt['value']) for opt in question_data.get('options', [])],
                correct_options=question_data.get('correct_options', [])
            )

            from services.ai_service import score_answer
            try:
                score_result = score_answer(
                    question=temp_question,
                    answer_text=answer.get('text', ''),
                    selected_options=answer.get('options', [])
                )
                rationale = score_result.get('rationale', 'No rationale provided') or 'No rationale provided'
            except Exception:
                rationale = 'Unable to generate rationale'

        # Create an ApplicationAnswerWithQuestion object with proper field assignments
        # The 'options' field in the parent class refers to selected options (List[str])
        # The 'question_options' field in the child class refers to question options (List[dict])
        from schemas.application import ApplicationAnswerWithQuestion
        from schemas.enums import QuestionType
        enriched_answer = ApplicationAnswerWithQuestion(
            question_id=answer.get('question_id'),
            text=answer.get('text'),
            options=answer.get('options', []),  # Selected options from the applicant (List[str])
            question_text=question_data.get('text', ''),
            weight=question_data.get('weight', 1),
            skill_categories=question_data.get('skill_categories', []),
            type=QuestionType(question_data.get('type', 'text_based')),  # Convert to enum
            question_options=question_data.get('options', []),  # Question's possible options (List[dict])
            correct_options=question_data.get('correct_options', []),
            rationale=rationale
        )

        # Add the selected options as an additional attribute if needed
        # But for now, we'll rely on the schema as defined
        enriched_answers.append(enriched_answer)

    # Create the detailed response
    assessment_details_obj = None
    if assessment:
        try:
            assessment_details_obj = ApplicationAssessment(
                id=assessment.id,
                title=assessment.title,
                passing_score=assessment.passing_score,
                created_at=None  # Assessment model doesn't have created_at field
            )
        except Exception as e:
            logger.error(f"Error creating assessment details: {str(e)}")
            assessment_details_obj = None

    application_detail = ApplicationDetailedResponse(
        id=application.id,
        job_id=application.job_id,
        assessment_id=application.assessment_id,
        user_id=application.user_id,
        answers=enriched_answers,
        score=score,
        passing_score=assessment.passing_score,
        assessment_details=assessment_details_obj,
        user={
            'id': user.id if user else None,
            'first_name': user.first_name if user else None,
            'last_name': user.last_name if user else None,
            'email': user.email if user else None
        } if user else None
    )

    logger.info(f"Successfully retrieved application detail for job ID: {jid}, assessment ID: {aid}, application ID: {id}")
    return application_detail


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


@router.get("/my-applications", response_model=MyApplicationsListResponse)
def get_my_applications(page: int = 1, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get list of applications for the current logged-in user"""
    logger.info(f"Retrieving applications for user ID: {current_user.id}, page: {page}, limit: {limit}")

    skip = (page - 1) * limit
    applications = get_applications_by_user(db, current_user.id, skip=skip, limit=limit)

    # Calculate total count
    total = len(get_applications_by_user(db, current_user.id, skip=0, limit=1000))  # Simplified for demo

    # Create responses with job and assessment details
    application_responses = []
    for application in applications:
        # Calculate score
        score = calculate_application_score(db, application.id)

        # Get assessment to retrieve passing score
        assessment = get_assessment(db, application.assessment_id)

        # Get job details
        job = get_job(db, application.job_id)

        # Create response object that matches technical requirements exactly
        application_response = MyApplicationResponse(
            id=application.id,
            job=MyApplicationsJob(
                id=job.id if job else "",
                title=job.title if job else "",
                seniority=job.seniority if job else "",
                description=job.description if job else ""
            ) if job else None,
            assessment=MyApplicationsAssessment(
                id=assessment.id if assessment else "",
                title=assessment.title if assessment else "",
                passing_score=assessment.passing_score if assessment else 0.0
            ) if assessment else None,
            score=score,
            created_at=application.created_at.isoformat() if application.created_at else None
        )

        application_responses.append(application_response)

    logger.info(f"Successfully retrieved {len(applications)} applications out of total {total} for user ID: {current_user.id}")
    return MyApplicationsListResponse(
        count=len(applications),
        total=total,
        data=application_responses
    )
