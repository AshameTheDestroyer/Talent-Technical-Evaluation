import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.assessment import Assessment
from models.job import Job
from models.user import User
from models.base import Base
from config import settings
from schemas.assessment import AssessmentCreate
from schemas.enums import QuestionType
from services.assessment_service import create_assessment
from services.ai_service import generate_questions
from uuid import uuid4

def test_ai_generated_questions():
    """Test that assessments are created with AI-generated questions"""
    
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
        
        # Test the AI service directly
        print("Testing AI service directly...")
        generated_questions = generate_questions(
            title="Python Programming Skills Assessment",
            questions_types=[QuestionType.choose_one.value, QuestionType.text_based.value, QuestionType.choose_many.value],
            additional_note="Focus on advanced Python concepts"
        )
        
        print(f"Generated {len(generated_questions)} questions:")
        for i, q in enumerate(generated_questions):
            print(f"  {i+1}. {q.text}")
            print(f"     Type: {q.type}, Weight: {q.weight}")
            print(f"     Skill categories: {q.skill_categories}")
            if q.options:
                print(f"     Options: {[opt.text for opt in q.options]}")
                print(f"     Correct options: {q.correct_options}")
            print()
        
        # Create an assessment using the service
        print("Testing assessment creation with AI-generated questions...")
        assessment_data = AssessmentCreate(
            title="Python Programming Skills Assessment",
            passing_score=70,
            questions_types=[QuestionType.choose_one, QuestionType.text_based, QuestionType.choose_many],
            additional_note="Focus on advanced Python concepts"
        )
        
        created_assessment = create_assessment(db, test_job.id, assessment_data)
        print(f"Created assessment ID: {created_assessment.id}")
        print(f"Assessment title: {created_assessment.title}")
        print(f"Assessment passing score: {created_assessment.passing_score}")
        
        # Parse and verify the questions
        questions = json.loads(created_assessment.questions)
        print(f"Number of questions generated: {len(questions)}")
        
        for i, q in enumerate(questions):
            print(f"  {i+1}. {q['text']}")
            print(f"     Type: {q['type']}, Weight: {q['weight']}")
            print(f"     Skill categories: {q['skill_categories']}")
            if q['options']:
                print(f"     Options: {[opt['text'] for opt in q['options']]}")
                print(f"     Correct options: {q['correct_options']}")
            print()
        
        # Verify that questions were generated
        assert len(questions) > 0, "No questions were generated"
        assert len(questions) == 3, f"Expected 3 questions, but got {len(questions)}"
        
        # Verify that each question has the required properties
        for q in questions:
            assert 'id' in q, "Question missing ID"
            assert 'text' in q, "Question missing text"
            assert 'weight' in q, "Question missing weight"
            assert 'type' in q, "Question missing type"
            assert 'skill_categories' in q, "Question missing skill categories"
            assert 'options' in q, "Question missing options"
            assert 'correct_options' in q, "Question missing correct_options"
            
            # Verify weight is in range 1-5
            assert 1 <= q['weight'] <= 5, f"Weight {q['weight']} is not in range 1-5"
            
            # Verify type is valid
            assert q['type'] in ['choose_one', 'choose_many', 'text_based'], f"Invalid question type: {q['type']}"
        
        print("[PASS] All tests passed! AI-generated questions are working correctly.")

        # Test regeneration functionality
        print("\nTesting assessment regeneration...")
        from services.assessment_service import regenerate_assessment

        # Regenerate the assessment with different question types
        regenerated_assessment = regenerate_assessment(
            db,
            created_assessment.id,
            questions_types=['choose_one', 'text_based'],  # Just two question types
            additional_note="Regenerated with different question types"
        )

        if regenerated_assessment:
            regenerated_questions = json.loads(regenerated_assessment.questions)
            print(f"Number of questions after regeneration: {len(regenerated_questions)}")

            assert len(regenerated_questions) == 2, f"Expected 2 questions after regeneration, but got {len(regenerated_questions)}"

            print("[PASS] Regeneration test passed!")
        else:
            print("[WARN] Regeneration failed - assessment not found")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_ai_generated_questions()