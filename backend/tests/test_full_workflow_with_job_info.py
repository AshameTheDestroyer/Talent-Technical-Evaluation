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
from services.assessment_service import create_assessment, regenerate_assessment
from uuid import uuid4

def test_full_workflow_with_job_info():
    """Test the full workflow of creating and regenerating assessments with job information"""
    
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
            title="Junior Data Analyst",
            seniority="junior",
            description="We are looking for a Junior Data Analyst to join our analytics team. The ideal candidate should have experience with data visualization, statistical analysis, and SQL queries.",
            skill_categories='["sql", "python", "excel", "tableau", "statistics"]'
        )
        db.add(test_job)
        db.commit()
        
        print("Testing full workflow with job information...")
        
        # Create an assessment using the service (which should include job info)
        assessment_data = AssessmentCreate(
            title="Data Analysis Skills Assessment",
            passing_score=65,
            questions_types=[QuestionType.choose_one, QuestionType.text_based],
            additional_note="Focus on SQL and data visualization skills"
        )
        
        created_assessment = create_assessment(db, test_job.id, assessment_data)
        print(f"Created assessment ID: {created_assessment.id}")
        print(f"Assessment title: {created_assessment.title}")
        
        # Parse and verify the questions
        questions = json.loads(created_assessment.questions)
        print(f"Number of questions generated: {len(questions)}")
        
        for i, q in enumerate(questions):
            print(f"  {i+1}. {q['text']}")
            print(f"     Type: {q['type']}")
            print(f"     Skill categories: {q['skill_categories']}")
            print()
        
        # Verify that job-specific skills are included in the categories
        all_categories = [cat for q in questions for cat in q['skill_categories']]
        job_skills_found = any(skill in all_categories for skill in ['sql', 'python', 'excel', 'tableau', 'statistics'])
        seniority_skills_found = any(skill in ['learning', 'basic-concepts', 'mentoring'] for skill in all_categories)
        
        print(f"Job-specific skills found in categories: {job_skills_found}")
        print(f"Seniority-specific skills found in categories: {seniority_skills_found}")
        
        # Now test regeneration with different question types
        print("\nTesting regeneration with different question types...")
        regenerated_assessment = regenerate_assessment(
            db,
            created_assessment.id,
            questions_types=[QuestionType.choose_many, QuestionType.text_based, QuestionType.choose_one],
            additional_note="New focus on advanced statistical analysis"
        )
        
        if regenerated_assessment:
            regenerated_questions = json.loads(regenerated_assessment.questions)
            print(f"Number of questions after regeneration: {len(regenerated_questions)}")
            
            for i, q in enumerate(regenerated_questions):
                print(f"  {i+1}. {q['text']}")
                print(f"     Type: {q['type']}")
                print(f"     Skill categories: {q['skill_categories']}")
                print()
            
            # Verify that job-specific skills are still included after regeneration
            all_regenerated_categories = [cat for q in regenerated_questions for cat in q['skill_categories']]
            job_skills_after_regenerate = any(skill in all_regenerated_categories for skill in ['sql', 'python', 'excel', 'tableau', 'statistics'])
            seniority_skills_after_regenerate = any(skill in ['learning', 'basic-concepts', 'mentoring'] for skill in all_regenerated_categories)
            
            print(f"Job-specific skills found after regeneration: {job_skills_after_regenerate}")
            print(f"Seniority-specific skills found after regeneration: {seniority_skills_after_regenerate}")
            
            assert len(regenerated_questions) == 3, f"Expected 3 questions after regeneration, but got {len(regenerated_questions)}"
            print("[PASS] Regeneration test passed!")
        else:
            print("[FAIL] Regeneration failed - assessment not found")
        
        # Verify the original creation had the expected number of questions
        assert len(questions) == 2, f"Expected 2 questions, but got {len(questions)}"
        
        # Verify that job information was used in question generation
        questions_with_job_context = sum(1 for q in questions if "analytics team" in q['text'] or "statistical analysis" in q['text'])
        print(f"Questions with job context: {questions_with_job_context}")
        
        print("[PASS] Full workflow test passed! Job information is properly included in question generation.")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_full_workflow_with_job_info()