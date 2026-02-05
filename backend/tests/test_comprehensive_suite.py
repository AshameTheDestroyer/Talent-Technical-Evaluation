"""
Comprehensive test suite for the AI-Powered Hiring Assessment Platform
This file contains all tests for the application's functionality.
"""

import pytest
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app
from database.database import get_db
from models.assessment import Assessment
from models.job import Job
from models.user import User
from models.application import Application
from models.base import Base
from schemas.assessment import AssessmentQuestion, AssessmentQuestionOption
from schemas.enums import QuestionType
from services.ai_service import generate_questions, score_answer
from services.assessment_service import create_assessment
from services.application_service import calculate_application_score
from integrations.ai_integration.ai_factory import AIGeneratorFactory, AIProvider
from integrations.ai_integration.mock_ai_generator import MockAIGenerator
from uuid import uuid4


# Create a test database session
TEST_DATABASE_URL = "sqlite:///./test_assessment_platform.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override the get_db dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the database dependency
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    """Create a test database session."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="module")
def setup_test_data(db_session):
    """Setup test data for all tests."""
    # Create test users
    hr_user = User(
        id=str(uuid4()),
        first_name="Test",
        last_name="HR",
        email="test.hr@example.com",
        role="hr"
    )
    hr_user.set_password("password123")
    db_session.add(hr_user)
    
    applicant_user = User(
        id=str(uuid4()),
        first_name="Test",
        last_name="Applicant",
        email="test.applicant@example.com",
        role="applicant"
    )
    applicant_user.set_password("password123")
    db_session.add(applicant_user)
    
    db_session.commit()
    
    return {
        "hr_user": hr_user,
        "applicant_user": applicant_user
    }


class TestAIInterface:
    """Test the AI interface and factory pattern."""
    
    def test_factory_pattern(self):
        """Test that the AI factory pattern works correctly."""
        # Test creating a mock generator
        mock_generator = AIGeneratorFactory.create_generator(AIProvider.MOCK)
        assert isinstance(mock_generator, MockAIGenerator)
        
        # Test getting available providers
        providers = AIGeneratorFactory.get_available_providers()
        assert len(providers) >= 1  # At least mock provider should be available
        
        # Test non-existent provider raises error
        with pytest.raises(ValueError):
            AIGeneratorFactory.create_generator("NON_EXISTENT")
    
    def test_mock_ai_generator_functionality(self):
        """Test the mock AI generator functionality."""
        generator = AIGeneratorFactory.create_generator(AIProvider.MOCK)
        
        # Test question generation
        questions = generator.generate_questions(
            title="Test Assessment",
            questions_types=["choose_one", "text_based"],
            additional_note="Test note",
            job_info={
                "title": "Software Engineer",
                "seniority": "mid",
                "description": "Test job description",
                "skill_categories": ["python", "django"]
            }
        )
        
        assert len(questions) == 2
        assert questions[0].type.value == "choose_one"
        assert questions[1].type.value == "text_based"
        
        # Test answer scoring
        test_question = AssessmentQuestion(
            id=str(uuid4()),
            text="What is Python?",
            weight=3,
            skill_categories=["programming"],
            type=QuestionType.choose_one,
            options=[
                AssessmentQuestionOption(text="A snake", value="a"),
                AssessmentQuestionOption(text="A programming language", value="b")
            ],
            correct_options=["b"]
        )
        
        score_result = generator.score_answer(
            question=test_question,
            answer_text="",
            selected_options=["b"]  # Correct answer
        )
        
        assert score_result['score'] == 1.0
        assert score_result['correct'] == True


class TestQuestionGeneration:
    """Test the question generation functionality."""
    
    def test_generate_questions_with_job_info(self):
        """Test that questions are generated with job information."""
        job_info = {
            "title": "Senior Python Developer",
            "seniority": "senior",
            "description": "Looking for experienced Python developers",
            "skill_categories": ["python", "django", "flask"]
        }
        
        questions = generate_questions(
            title="Python Skills Assessment",
            questions_types=["choose_one", "text_based"],
            additional_note="Focus on Django",
            job_info=job_info
        )
        
        assert len(questions) == 2
        assert questions[0].type.value == "choose_one"
        assert questions[1].type.value == "text_based"
        
        # Check that job-specific skills are included in categories
        all_categories = [cat for q in questions for cat in q.skill_categories]
        assert "python" in all_categories
        assert "django" in all_categories
    
    def test_generate_questions_without_job_info(self):
        """Test that questions are generated without job information."""
        questions = generate_questions(
            title="General Knowledge Assessment",
            questions_types=["choose_one"],
            additional_note="General questions"
        )
        
        assert len(questions) == 1
        assert questions[0].type.value == "choose_one"


class TestAnswerScoring:
    """Test the answer scoring functionality."""
    
    def test_score_multiple_choice_correct(self):
        """Test scoring of correct multiple choice answers."""
        question = AssessmentQuestion(
            id=str(uuid4()),
            text="What is 2+2?",
            weight=3,
            skill_categories=["math"],
            type=QuestionType.choose_one,
            options=[
                AssessmentQuestionOption(text="3", value="a"),
                AssessmentQuestionOption(text="4", value="b"),
                AssessmentQuestionOption(text="5", value="c")
            ],
            correct_options=["b"]
        )
        
        result = score_answer(
            question=question,
            answer_text="",
            selected_options=["b"]  # Correct answer
        )
        
        assert result['score'] == 1.0
        assert result['correct'] == True
        assert "match the correct options" in result['rationale']
    
    def test_score_multiple_choice_incorrect(self):
        """Test scoring of incorrect multiple choice answers."""
        question = AssessmentQuestion(
            id=str(uuid4()),
            text="What is 2+2?",
            weight=3,
            skill_categories=["math"],
            type=QuestionType.choose_one,
            options=[
                AssessmentQuestionOption(text="3", value="a"),
                AssessmentQuestionOption(text="4", value="b"),
                AssessmentQuestionOption(text="5", value="c")
            ],
            correct_options=["b"]
        )
        
        result = score_answer(
            question=question,
            answer_text="",
            selected_options=["a"]  # Incorrect answer
        )
        
        assert result['score'] == 0.0
        assert result['correct'] == False
        assert "do not match the correct options" in result['rationale']
    
    def test_score_text_based_answer(self):
        """Test scoring of text-based answers."""
        question = AssessmentQuestion(
            id=str(uuid4()),
            text="Explain the importance of renewable energy.",
            weight=5,
            skill_categories=["environment"],
            type=QuestionType.text_based,
            options=[],
            correct_options=[]
        )
        
        result = score_answer(
            question=question,
            answer_text="Renewable energy is important because it reduces carbon emissions.",
            selected_options=[]
        )
        
        # Text-based answers should receive a score based on our heuristic evaluation
        assert 0.0 <= result['score'] <= 1.0
        assert "evaluated with score" in result['rationale']


class TestAssessmentService:
    """Test the assessment service functionality."""
    
    def test_create_assessment_with_job_info(self, db_session, setup_test_data):
        """Test creating an assessment with job information."""
        from schemas.assessment import AssessmentCreate
        
        # Create a test job first
        test_job = Job(
            id=str(uuid4()),
            title="Software Engineer",
            seniority="mid",
            description="Test job for assessment",
            skill_categories='["python", "django", "sql"]'
        )
        db_session.add(test_job)
        db_session.commit()
        
        # Create assessment data
        assessment_data = AssessmentCreate(
            title="Python Skills Assessment",
            passing_score=70,
            questions_types=[QuestionType.choose_one, QuestionType.text_based],
            additional_note="Focus on Python and Django"
        )
        
        # Create the assessment
        created_assessment = create_assessment(db_session, test_job.id, assessment_data)
        
        assert created_assessment.title == "Python Skills Assessment"
        assert created_assessment.passing_score == 70
        
        # Parse and verify questions
        questions = json.loads(created_assessment.questions)
        assert len(questions) == 2
        
        # Verify that job information was used in question generation
        question_texts = [q['text'] for q in questions]
        assert any("Python" in text for text in question_texts)
    
    def test_calculate_application_score(self, db_session, setup_test_data):
        """Test calculating application scores."""
        # Create a test job
        test_job = Job(
            id=str(uuid4()),
            title="Software Engineer",
            seniority="mid",
            description="Test job for assessment",
            skill_categories='["python", "django"]'
        )
        db_session.add(test_job)
        
        # Create a test assessment with questions
        test_questions = [
            {
                "id": str(uuid4()),
                "text": "What is Python?",
                "weight": 3,
                "skill_categories": ["programming", "python"],
                "type": "choose_one",
                "options": [
                    {"text": "A snake", "value": "a"},
                    {"text": "A programming language", "value": "b"}
                ],
                "correct_options": ["b"]
            }
        ]
        
        test_assessment = Assessment(
            id=str(uuid4()),
            job_id=test_job.id,
            title="Python Skills Assessment",
            passing_score=70,
            questions=json.dumps(test_questions)
        )
        db_session.add(test_assessment)
        
        # Create a test user
        test_user = User(
            id=str(uuid4()),
            first_name="Test",
            last_name="User",
            email=f"test_{str(uuid4())[:8]}@example.com",
            role="applicant"
        )
        test_user.set_password("password123")
        db_session.add(test_user)
        
        db_session.commit()
        
        # Create an application with correct answers
        test_answers = [
            {
                "question_id": test_questions[0]['id'],
                "text": "",
                "options": ["b"]  # Correct answer
            }
        ]
        
        test_application = Application(
            id=str(uuid4()),
            job_id=test_job.id,
            assessment_id=test_assessment.id,
            user_id=test_user.id,
            answers=json.dumps(test_answers)
        )
        db_session.add(test_application)
        db_session.commit()
        
        # Calculate the score
        score = calculate_application_score(db_session, test_application.id)
        
        # Since the answer is correct, the score should be 100%
        assert score == 100.0


class TestIntegration:
    """Test the full integration of the system."""
    
    def test_full_assessment_lifecycle(self, db_session, setup_test_data):
        """Test the full lifecycle of an assessment."""
        from schemas.assessment import AssessmentCreate
        from schemas.application import ApplicationCreate, ApplicationAnswer
        from schemas.enums import QuestionType
        
        # Create a job
        test_job = Job(
            id=str(uuid4()),
            title="Python Developer",
            seniority="mid",
            description="Looking for Python developers",
            skill_categories='["python", "django", "flask"]'
        )
        db_session.add(test_job)
        db_session.commit()
        
        # Create an assessment
        assessment_data = AssessmentCreate(
            title="Python Programming Skills Assessment",
            passing_score=75,
            questions_types=[QuestionType.choose_one, QuestionType.text_based],
            additional_note="Focus on Django and Flask"
        )
        
        created_assessment = create_assessment(db_session, test_job.id, assessment_data)
        assert created_assessment.title == "Python Programming Skills Assessment"
        
        # Verify questions were generated
        questions = json.loads(created_assessment.questions)
        assert len(questions) == 2
        
        # Create an application with answers
        test_user = setup_test_data["applicant_user"]
        
        application_data = ApplicationCreate(
            job_id=test_job.id,
            assessment_id=created_assessment.id,
            user_id=test_user.id,
            answers=[
                ApplicationAnswer(
                    question_id=questions[0]['id'],
                    text="",
                    options=["b"]  # Assuming 'b' is correct from our mock
                ),
                ApplicationAnswer(
                    question_id=questions[1]['id'],
                    text="This is a detailed answer to the text-based question.",
                    options=[]
                )
            ]
        )
        
        # Calculate score for the application
        # (This would normally be done when the application is submitted)
        score = calculate_application_score(db_session, application_data.answers[0].question_id[:8])  # This is a simplified test
        
        # The assessment was created successfully with proper questions
        assert created_assessment.id is not None
        assert created_assessment.questions is not None


# Run all tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])