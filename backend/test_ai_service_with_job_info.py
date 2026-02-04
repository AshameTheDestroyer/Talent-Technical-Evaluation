import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.assessment import Assessment
from models.job import Job
from models.user import User
from models.base import Base
from config import settings
from services.ai_service import generate_questions
from schemas.enums import QuestionType
from uuid import uuid4

def test_ai_service_directly_with_job_info():
    """Test the AI service directly with job information"""
    
    print("Testing AI service directly with job information...")
    
    # Prepare job information
    job_info = {
        "title": "Senior Python Developer",
        "seniority": "senior",
        "description": "Looking for experienced Python developers familiar with Django, Flask, and cloud technologies",
        "skill_categories": ["python", "django", "flask", "sql", "cloud"]
    }
    
    # Test the AI service directly with job info
    generated_questions = generate_questions(
        title="Backend Development Skills Assessment",
        questions_types=[QuestionType.choose_one.value, QuestionType.text_based.value],
        additional_note="Focus on Django and cloud deployment",
        job_info=job_info
    )
    
    print(f"Generated {len(generated_questions)} questions with job information:")
    for i, q in enumerate(generated_questions):
        print(f"  {i+1}. {q.text}")
        print(f"     Type: {q.type}, Weight: {q.weight}")
        print(f"     Skill categories: {q.skill_categories}")
        if q.options:
            print(f"     Options: {[opt.text for opt in q.options][:2]}...")  # Show first 2 options
            print(f"     Correct options: {q.correct_options}")
        print()
    
    # Verify that job-specific skills are included in the categories
    all_categories = [cat for q in generated_questions for cat in q.skill_categories]
    job_skills_found = any(skill in all_categories for skill in ['python', 'django', 'flask', 'sql', 'cloud'])
    seniority_skills_found = any(skill in all_categories for skill in ['leadership', 'architecture', 'decision-making'])
    
    print(f"Job-specific skills found in categories: {job_skills_found}")
    print(f"Seniority-specific skills found in categories: {seniority_skills_found}")
    
    # Check if job description context is included in questions
    questions_with_job_context = sum(1 for q in generated_questions if "Looking for experienced Python developers" in q.text)
    print(f"Questions with job context: {questions_with_job_context}")
    
    assert len(generated_questions) == 2, f"Expected 2 questions, but got {len(generated_questions)}"
    print("[PASS] AI service test with job information passed!")

if __name__ == "__main__":
    test_ai_service_directly_with_job_info()