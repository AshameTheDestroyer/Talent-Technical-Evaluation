import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.assessment import Assessment
from models.job import Job
from models.user import User
from models.application import Application
from models.base import Base
from config import settings
from schemas.assessment import AssessmentQuestion, AssessmentQuestionOption
from schemas.enums import QuestionType
from services.ai_service import score_answer
from uuid import uuid4

def test_ai_scoring_functionality():
    """Test the AI scoring functionality"""
    
    print("Testing AI scoring functionality...")
    
    # Create a sample question
    sample_question = AssessmentQuestion(
        id=str(uuid4()),
        text="What is the capital of France?",
        weight=3,
        skill_categories=["geography", "knowledge"],
        type=QuestionType.choose_one,
        options=[
            AssessmentQuestionOption(text="London", value="a"),
            AssessmentQuestionOption(text="Paris", value="b"),
            AssessmentQuestionOption(text="Berlin", value="c")
        ],
        correct_options=["b"]
    )
    
    # Test correct answer
    print("\n1. Testing correct answer...")
    correct_result = score_answer(
        question=sample_question,
        answer_text="",
        selected_options=["b"]
    )
    print(f"   Correct answer score: {correct_result['score']}")
    print(f"   Correct answer rationale: {correct_result['rationale']}")
    print(f"   Is correct: {correct_result['correct']}")
    assert correct_result['score'] == 1.0, f"Expected 1.0, got {correct_result['score']}"
    assert correct_result['correct'] == True, f"Expected True, got {correct_result['correct']}"
    print("   [PASS] Correct answer test passed")
    
    # Test incorrect answer
    print("\n2. Testing incorrect answer...")
    incorrect_result = score_answer(
        question=sample_question,
        answer_text="",
        selected_options=["a"]  # London is wrong
    )
    print(f"   Incorrect answer score: {incorrect_result['score']}")
    print(f"   Incorrect answer rationale: {incorrect_result['rationale']}")
    print(f"   Is correct: {incorrect_result['correct']}")
    assert incorrect_result['score'] == 0.0, f"Expected 0.0, got {incorrect_result['score']}"
    assert incorrect_result['correct'] == False, f"Expected False, got {incorrect_result['correct']}"
    print("   [PASS] Incorrect answer test passed")
    
    # Test text-based question
    print("\n3. Testing text-based question...")
    text_question = AssessmentQuestion(
        id=str(uuid4()),
        text="Explain the importance of renewable energy.",
        weight=5,
        skill_categories=["environment", "science"],
        type=QuestionType.text_based,
        options=[],
        correct_options=[]
    )
    
    text_result = score_answer(
        question=text_question,
        answer_text="Renewable energy is important because it reduces carbon emissions and is sustainable.",
        selected_options=[]
    )
    print(f"   Text answer score: {text_result['score']}")
    print(f"   Text answer rationale: {text_result['rationale']}")
    print(f"   Is correct: {text_result['correct']}")
    # For text-based questions, we expect a partial score (0.5 in the updated mock implementation)
    assert text_result['score'] == 0.5, f"Expected 0.5, got {text_result['score']}"
    # In the mock implementation, any score > 0.5 is considered correct, so 0.5 is not correct
    assert text_result['correct'] == False, f"Expected False (since score is 0.5, not > 0.5), got {text_result['correct']}"
    print("   [PASS] Text-based question test passed")
    
    # Test multiple choice (choose many) question
    print("\n4. Testing choose-many question...")
    multichoice_question = AssessmentQuestion(
        id=str(uuid4()),
        text="Which of the following are programming languages?",
        weight=4,
        skill_categories=["programming", "computer-science"],
        type=QuestionType.choose_many,
        options=[
            AssessmentQuestionOption(text="Python", value="a"),
            AssessmentQuestionOption(text="HTML", value="b"),
            AssessmentQuestionOption(text="Java", value="c"),
            AssessmentQuestionOption(text="CSS", value="d")
        ],
        correct_options=["a", "c"]  # Python and Java are programming languages
    )
    
    correct_multichoice_result = score_answer(
        question=multichoice_question,
        answer_text="",
        selected_options=["a", "c"]  # Correct answers
    )
    print(f"   Correct multichoice score: {correct_multichoice_result['score']}")
    print(f"   Correct multichoice rationale: {correct_multichoice_result['rationale']}")
    print(f"   Is correct: {correct_multichoice_result['correct']}")
    assert correct_multichoice_result['score'] == 1.0, f"Expected 1.0, got {correct_multichoice_result['score']}"
    assert correct_multichoice_result['correct'] == True, f"Expected True, got {correct_multichoice_result['correct']}"
    print("   [PASS] Choose-many correct answer test passed")
    
    incorrect_multichoice_result = score_answer(
        question=multichoice_question,
        answer_text="",
        selected_options=["a", "b"]  # Partially correct (includes HTML which is not a programming language)
    )
    print(f"   Incorrect multichoice score: {incorrect_multichoice_result['score']}")
    print(f"   Incorrect multichoice rationale: {incorrect_multichoice_result['rationale']}")
    print(f"   Is correct: {incorrect_multichoice_result['correct']}")
    assert incorrect_multichoice_result['score'] == 0.0, f"Expected 0.0, got {incorrect_multichoice_result['score']}"
    assert incorrect_multichoice_result['correct'] == False, f"Expected False, got {incorrect_multichoice_result['correct']}"
    print("   [PASS] Choose-many incorrect answer test passed")
    
    print("\n[PASS] All AI scoring functionality tests passed!")


def test_application_scoring():
    """Test the application scoring functionality"""
    
    print("\n\nTesting application scoring functionality...")
    
    # Create a test database session
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create a test session
    db = TestingSessionLocal()
    
    try:
        # Create a test job
        test_job = Job(
            id=str(uuid4()),
            title="Software Engineer",
            seniority="mid",
            description="Test job for assessment",
            skill_categories='["programming", "python", "fastapi"]'
        )
        db.add(test_job)
        db.commit()
        
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
                    {"text": "A programming language", "value": "b"},
                    {"text": "An IDE", "value": "c"}
                ],
                "correct_options": ["b"]
            },
            {
                "id": str(uuid4()),
                "text": "What is 2+2?",
                "weight": 2,
                "skill_categories": ["math"],
                "type": "choose_one",
                "options": [
                    {"text": "3", "value": "a"},
                    {"text": "4", "value": "b"},
                    {"text": "5", "value": "c"}
                ],
                "correct_options": ["b"]
            }
        ]
        
        test_assessment = Assessment(
            id=str(uuid4()),
            job_id=test_job.id,
            title="Programming Skills Assessment",
            passing_score=70,
            questions=json.dumps(test_questions)
        )
        db.add(test_assessment)
        db.commit()
        
        # Create a test user
        test_user = User(
            id=str(uuid4()),
            first_name="John",
            last_name="Doe",
            email=f"test_{str(uuid4())[:8]}@example.com",
            role="applicant"
        )
        test_user.set_password("password123")
        db.add(test_user)
        db.commit()
        
        # Create an application with correct answers
        test_answers = [
            {
                "question_id": test_questions[0]['id'],
                "text": "",
                "options": ["b"]  # Correct answer for question 1
            },
            {
                "question_id": test_questions[1]['id'], 
                "text": "",
                "options": ["b"]  # Correct answer for question 2
            }
        ]
        
        test_application = Application(
            id=str(uuid4()),
            job_id=test_job.id,
            assessment_id=test_assessment.id,
            user_id=test_user.id,
            answers=json.dumps(test_answers)
        )
        db.add(test_application)
        db.commit()
        
        # Test the score calculation
        from services.application_service import calculate_application_score
        calculated_score = calculate_application_score(db, test_application.id)
        print(f"Calculated score for application with all correct answers: {calculated_score}%")
        
        # Since both answers are correct, the score should be 100%
        expected_total_points = 3 + 2  # weights of both questions
        expected_earned_points = 3 + 2  # both answers are correct
        expected_percentage = (expected_earned_points / expected_total_points) * 100
        
        assert calculated_score == expected_percentage, f"Expected {expected_percentage}%, got {calculated_score}%"
        print("   [PASS] Score calculation is correct for all correct answers")
        
        # Create another application with some incorrect answers
        test_answers_partial = [
            {
                "question_id": test_questions[0]['id'],
                "text": "",
                "options": ["a"]  # Wrong answer for question 1
            },
            {
                "question_id": test_questions[1]['id'], 
                "text": "",
                "options": ["b"]  # Correct answer for question 2
            }
        ]
        
        test_application_partial = Application(
            id=str(uuid4()),
            job_id=test_job.id,
            assessment_id=test_assessment.id,
            user_id=test_user.id,
            answers=json.dumps(test_answers_partial)
        )
        db.add(test_application_partial)
        db.commit()
        
        # Test the score calculation for partial correct answers
        calculated_score_partial = calculate_application_score(db, test_application_partial.id)
        print(f"Calculated score for application with partial correct answers: {calculated_score_partial}%")
        
        # Expected: 2 points earned (question 2) out of 5 total points
        expected_partial_percentage = (2 / 5) * 100  # 40%
        
        assert calculated_score_partial == expected_partial_percentage, f"Expected {expected_partial_percentage}%, got {calculated_score_partial}%"
        print("   [PASS] Score calculation is correct for partial correct answers")
        
        print("\n[PASS] Application scoring functionality tests passed!")
        
    finally:
        db.close()


if __name__ == "__main__":
    test_ai_scoring_functionality()
    test_application_scoring()