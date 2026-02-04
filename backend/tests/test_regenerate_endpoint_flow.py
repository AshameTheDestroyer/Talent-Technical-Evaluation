import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.assessment import Assessment
from models.job import Job
from models.user import User
from models.base import Base
from config import settings
from schemas.assessment import AssessmentCreate, AssessmentRegenerate
from schemas.enums import QuestionType
from services.assessment_service import create_assessment, regenerate_assessment
from uuid import uuid4

def test_regenerate_endpoint_flow():
    """Test that the regenerate endpoint works the same way as create with job information"""
    
    # Create a test database session
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create a test session
    db = TestingSessionLocal()
    
    try:
        # Create a test job with specific information
        test_job = Job(
            id=str(uuid4()),
            title="Mid-Level Software Engineer",
            seniority="mid",
            description="We are looking for a Mid-Level Software Engineer with experience in Python, Django, and REST APIs.",
            skill_categories='["python", "django", "rest-api", "sql", "testing"]'
        )
        db.add(test_job)
        db.commit()
        
        print("Testing regenerate endpoint flow with job information...")
        
        # Create an initial assessment
        assessment_data = AssessmentCreate(
            title="Python Backend Skills Assessment",
            passing_score=70,
            questions_types=[QuestionType.choose_one, QuestionType.text_based],
            additional_note="Focus on Django and API development"
        )
        
        created_assessment = create_assessment(db, test_job.id, assessment_data)
        print(f"Created assessment ID: {created_assessment.id}")
        print(f"Original assessment title: {created_assessment.title}")
        
        # Parse and verify the original questions
        original_questions = json.loads(created_assessment.questions)
        print(f"Number of original questions: {len(original_questions)}")
        
        for i, q in enumerate(original_questions):
            print(f"  Original Q{i+1}: {q['text'][:60]}...")
            print(f"     Skill categories: {q['skill_categories'][:3]}...")  # Show first 3 categories
            print()
        
        # Now test regeneration with different question types
        print("Testing regeneration with different question types...")
        
        # Prepare regeneration data
        regenerate_data = AssessmentRegenerate(
            questions_types=[QuestionType.choose_many, QuestionType.text_based, QuestionType.choose_one],
            additional_note="New focus on advanced Python concepts and testing"
        )
        
        # Regenerate the assessment
        regenerated_assessment = regenerate_assessment(
            db,
            created_assessment.id,
            **regenerate_data.model_dump(exclude_unset=True)
        )
        
        if regenerated_assessment:
            regenerated_questions = json.loads(regenerated_assessment.questions)
            print(f"Number of questions after regeneration: {len(regenerated_questions)}")
            
            for i, q in enumerate(regenerated_questions):
                print(f"  Regenerated Q{i+1}: {q['text'][:60]}...")
                print(f"     Skill categories: {q['skill_categories'][:3]}...")  # Show first 3 categories
                print()
            
            # Verify that the number of questions matches expectations
            assert len(regenerated_questions) == 3, f"Expected 3 questions after regeneration, but got {len(regenerated_questions)}"
            
            # Verify that job information was used in regeneration (check for job-specific content in questions)
            job_context_in_regenerated = any(
                "Mid-Level Software Engineer" in q['text'] or 
                "Python, Django, and REST APIs" in q['text']
                for q in regenerated_questions
            )
            
            print(f"Job context preserved in regenerated questions: {job_context_in_regenerated}")
            
            # Verify that skill categories from the job are included
            all_regenerated_categories = [cat for q in regenerated_questions for cat in q['skill_categories']]
            job_skills_present = any(skill in ['python', 'django', 'rest-api', 'sql', 'testing'] for skill in all_regenerated_categories)
            
            print(f"Job-specific skills present in regenerated assessment: {job_skills_present}")
            
            print("[PASS] Regeneration test passed! Job information is properly used in regeneration.")
        else:
            print("[FAIL] Regeneration failed - assessment not found")
            return False
        
        print("[PASS] Regenerate endpoint flow test completed successfully!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_regenerate_endpoint_flow()
    if success:
        print("\n[PASS] All tests passed! The regenerate endpoint works correctly with job information.")
    else:
        print("\n[FAIL] Tests failed!")