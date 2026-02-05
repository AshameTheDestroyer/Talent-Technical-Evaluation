from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.assessment import Assessment
from models.job import Job
from models.user import User
from models.base import Base
from config import settings
from schemas.assessment import AssessmentCreate, AssessmentQuestion, AssessmentQuestionOption
from services.assessment_service import create_assessment
from uuid import uuid4

# Create a test database session
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_create_assessment_with_questions():
    """
    Test creating an assessment with questions
    """
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create a test job
    db = TestingSessionLocal()
    
    # Create a sample job for testing
    test_job = Job(
        id=str(uuid4()),
        title="Software Engineer",
        seniority="mid",
        description="Test job for assessment",
        skill_categories='["programming", "python", "fastapi"]'
    )
    db.add(test_job)
    db.commit()
    
    # Define sample questions
    sample_questions = [
        AssessmentQuestion(
            id=str(uuid4()),
            text="What is Python?",
            weight=3,
            skill_categories=["programming", "python"],
            type="choose_one",
            options=[
                AssessmentQuestionOption(text="A snake", value="a"),
                AssessmentQuestionOption(text="A programming language", value="b"),
                AssessmentQuestionOption(text="An IDE", value="c")
            ],
            correct_options=["b"]
        ),
        AssessmentQuestion(
            id=str(uuid4()),
            text="What is FastAPI?",
            weight=4,
            skill_categories=["web development", "python"],
            type="text_based",
            options=[],
            correct_options=[]
        )
    ]
    
    # Create assessment with questions
    assessment_data = AssessmentCreate(
        title="Python Programming Skills Assessment",
        passing_score=70,
        questions=sample_questions,
        additional_note="This is a test assessment"
    )
    
    # Create the assessment
    created_assessment = create_assessment(db, test_job.id, assessment_data)
    
    # Verify the assessment was created with questions
    print(f"Created assessment ID: {created_assessment.id}")
    print(f"Assessment title: {created_assessment.title}")
    print(f"Assessment passing score: {created_assessment.passing_score}")
    print(f"Questions stored: {created_assessment.questions}")
    
    # Close the session
    db.close()
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_create_assessment_with_questions()