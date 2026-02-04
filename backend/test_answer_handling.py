import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.application import Application
from models.assessment import Assessment
from models.job import Job
from models.user import User
from models.base import Base
from config import settings
from services.application_service import calculate_application_score
from uuid import uuid4

def test_answer_handling():
    """Test that answers are handled correctly without being treated as separate models"""
    
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
                "id": "q1",
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
                "id": "q2",
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
        
        # Create a test application with answers
        test_answers = [
            {
                "question_id": "q1",
                "text": "",
                "options": ["b"]  # Correct answer for question 1
            },
            {
                "question_id": "q2", 
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
        calculated_score = calculate_application_score(db, test_application.id)
        print(f"Calculated score for application: {calculated_score}%")
        
        # Since both answers are correct, the score should be 100%
        expected_total_points = 3 + 2  # weights of both questions
        expected_earned_points = 3 + 2  # both answers are correct
        expected_percentage = (expected_earned_points / expected_total_points) * 100
        
        assert calculated_score == expected_percentage, f"Expected {expected_percentage}%, got {calculated_score}%"
        print("[PASS] Score calculation is correct for all correct answers")

        # Create another application with some incorrect answers
        test_answers_partial = [
            {
                "question_id": "q1",
                "text": "",
                "options": ["a"]  # Wrong answer for question 1
            },
            {
                "question_id": "q2",
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
        print(f"Calculated score for partial application: {calculated_score_partial}%")

        # Expected: 2 points earned (question 2) out of 5 total points
        expected_partial_percentage = (2 / 5) * 100  # 40%

        assert calculated_score_partial == expected_partial_percentage, f"Expected {expected_partial_percentage}%, got {calculated_score_partial}%"
        print("[PASS] Score calculation is correct for partial correct answers")

        # Test with a text-based question
        text_question = [
            {
                "id": "q3",
                "text": "Describe the difference between list and tuple in Python.",
                "weight": 5,
                "skill_categories": ["python"],
                "type": "text_based",
                "options": [],
                "correct_options": []
            }
        ]

        # Update the assessment with the text question
        all_questions = test_questions + text_question
        test_assessment.questions = json.dumps(all_questions)
        db.commit()

        # Create an application with a text answer
        text_answers = [
            {
                "question_id": "q1",
                "text": "",
                "options": ["b"]  # Correct answer
            },
            {
                "question_id": "q2",
                "text": "",
                "options": ["b"]  # Correct answer
            },
            {
                "question_id": "q3",
                "text": "A list is mutable while a tuple is immutable.",
                "options": []
            }
        ]

        test_application_text = Application(
            id=str(uuid4()),
            job_id=test_job.id,
            assessment_id=test_assessment.id,
            user_id=test_user.id,
            answers=json.dumps(text_answers)
        )
        db.add(test_application_text)
        db.commit()

        # Test the score calculation with text answer
        calculated_score_text = calculate_application_score(db, test_application_text.id)
        print(f"Calculated score for application with text answer: {calculated_score_text}%")

        # For text-based questions, we consider them correct if there's text content
        # So this should be 100% (5 points from correct MCQs + 5 points from text answer out of 10 total)
        expected_text_percentage = ((3 + 2 + 5) / (3 + 2 + 5)) * 100  # 100%

        assert calculated_score_text == expected_text_percentage, f"Expected {expected_text_percentage}%, got {calculated_score_text}%"
        print("[PASS] Score calculation is correct for application with text answer")

        print("\nAll tests passed! Answers are correctly handled without being treated as separate models.")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_answer_handling()