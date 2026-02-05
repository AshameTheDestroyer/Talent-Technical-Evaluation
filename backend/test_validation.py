from schemas.assessment import AssessmentCreate, AssessmentQuestion, AssessmentQuestionOption
from schemas.enums import QuestionType
from pydantic import ValidationError
import json

def test_assessment_validation():
    """Test assessment schema validation"""
    print("Testing Assessment Schema Validation...")
    
    # Test valid assessment
    try:
        valid_question = AssessmentQuestion(
            id="test-id",
            text="Sample question?",
            weight=3,
            skill_categories=["python", "programming"],
            type=QuestionType.choose_one,
            options=[
                AssessmentQuestionOption(text="Option A", value="a"),
                AssessmentQuestionOption(text="Option B", value="b")
            ],
            correct_options=["a"]
        )
        
        valid_assessment = AssessmentCreate(
            title="Valid Assessment",
            passing_score=70,
            questions=[valid_question]
        )
        print("[PASS] Valid assessment creation succeeded")
    except ValidationError as e:
        print(f"[FAIL] Valid assessment creation failed: {e}")

    # Test invalid weight (too low)
    try:
        invalid_question_low_weight = AssessmentQuestion(
            id="test-id",
            text="Sample question?",
            weight=0,  # Invalid: below minimum of 1
            skill_categories=["python", "programming"],
            type=QuestionType.choose_one
        )
        print("[FAIL] Invalid weight (too low) should have failed validation")
    except ValidationError:
        print("[PASS] Invalid weight (too low) correctly failed validation")

    # Test invalid weight (too high)
    try:
        invalid_question_high_weight = AssessmentQuestion(
            id="test-id",
            text="Sample question?",
            weight=6,  # Invalid: above maximum of 5
            skill_categories=["python", "programming"],
            type=QuestionType.choose_one
        )
        print("[FAIL] Invalid weight (too high) should have failed validation")
    except ValidationError:
        print("[PASS] Invalid weight (too high) correctly failed validation")

    # Test invalid passing score (too low)
    try:
        valid_question = AssessmentQuestion(
            id="test-id",
            text="Sample question?",
            weight=3,
            skill_categories=["python", "programming"],
            type=QuestionType.choose_one
        )

        invalid_assessment_low_score = AssessmentCreate(
            title="Invalid Assessment",
            passing_score=10,  # Invalid: below minimum of 20
            questions=[valid_question]
        )
        print("[FAIL] Invalid passing score (too low) should have failed validation")
    except ValidationError:
        print("[PASS] Invalid passing score (too low) correctly failed validation")

    # Test invalid passing score (too high)
    try:
        valid_question = AssessmentQuestion(
            id="test-id",
            text="Sample question?",
            weight=3,
            skill_categories=["python", "programming"],
            type=QuestionType.choose_one
        )

        invalid_assessment_high_score = AssessmentCreate(
            title="Invalid Assessment",
            passing_score=90,  # Invalid: above maximum of 80
            questions=[valid_question]
        )
        print("[FAIL] Invalid passing score (too high) should have failed validation")
    except ValidationError:
        print("[PASS] Invalid passing score (too high) correctly failed validation")

    # Test title length validation
    try:
        too_long_title = "x" * 201  # Exceeds max length of 200
        invalid_assessment_title = AssessmentCreate(
            title=too_long_title,
            passing_score=70,
            questions=[valid_question]
        )
        print("[FAIL] Invalid title length should have failed validation")
    except ValidationError:
        print("[PASS] Invalid title length correctly failed validation")

def test_user_validation():
    """Test user schema validation"""
    print("\nTesting User Schema Validation...")
    
    from schemas.user import UserCreate
    from schemas.enums import UserRole
    # Test valid user
    try:
        valid_user = UserCreate(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            role=UserRole.hr,
            password="securepassword123"
        )
        print("[PASS] Valid user creation succeeded")
    except ValidationError as e:
        print(f"[FAIL] Valid user creation failed: {e}")

    # Test invalid first name (too long)
    try:
        invalid_user_long_name = UserCreate(
            first_name="x" * 51,  # Exceeds max length of 50
            last_name="Doe",
            email="john.doe@example.com",
            role=UserRole.hr,
            password="securepassword123"
        )
        print("[FAIL] Invalid first name length should have failed validation")
    except ValidationError:
        print("[PASS] Invalid first name length correctly failed validation")

    # Test invalid last name (too short, empty)
    try:
        invalid_user_empty_name = UserCreate(
            first_name="John",
            last_name="",  # Invalid: empty
            email="john.doe@example.com",
            role=UserRole.hr,
            password="securepassword123"
        )
        print("[FAIL] Invalid last name (empty) should have failed validation")
    except ValidationError:
        print("[PASS] Invalid last name (empty) correctly failed validation")

def test_job_validation():
    """Test job schema validation"""
    print("\nTesting Job Schema Validation...")
    
    from schemas.job import JobCreate
    from schemas.enums import JobSeniority
    
    # Test valid job
    try:
        valid_job = JobCreate(
            title="Software Engineer",
            seniority=JobSeniority.mid,
            description="Develop software solutions"
        )
        print("[PASS] Valid job creation succeeded")
    except ValidationError as e:
        print(f"[FAIL] Valid job creation failed: {e}")
    
    # Test invalid title (too long)
    try:
        invalid_job_long_title = JobCreate(
            title="x" * 201,  # Exceeds max length of 200
            seniority=JobSeniority.junior,
            description="Develop software solutions"
        )
        print("[FAIL] Invalid job title length should have failed validation")
    except ValidationError:
        print("[PASS] Invalid job title length correctly failed validation")

    # Test invalid description (too long)
    try:
        invalid_job_long_desc = JobCreate(
            title="Software Engineer",
            seniority=JobSeniority.junior,
            description="x" * 1001  # Exceeds max length of 1000
        )
        print("[FAIL] Invalid job description length should have failed validation")
    except ValidationError:
        print("[PASS] Invalid job description length correctly failed validation")

def test_application_validation():
    """Test application schema validation"""
    print("\nTesting Application Schema Validation...")
    
    from schemas.application import ApplicationAnswer, ApplicationCreate
    
    # Test valid application
    try:
        valid_answer = ApplicationAnswer(
            question_id="question-1",
            text="Sample answer text",
            options=["option1", "option2"]
        )
        
        valid_application = ApplicationCreate(
            job_id="job-1",
            assessment_id="assessment-1",
            user_id="user-1",
            answers=[valid_answer]
        )
        print("[PASS] Valid application creation succeeded")
    except ValidationError as e:
        print(f"[FAIL] Valid application creation failed: {e}")
    
    # Test invalid question_id (empty)
    try:
        invalid_answer = ApplicationAnswer(
            question_id="",  # Invalid: empty
            text="Sample answer text"
        )
        print("[FAIL] Invalid question_id should have failed validation")
    except ValidationError:
        print("[PASS] Invalid question_id correctly failed validation")

    # Test invalid answer text (too long)
    try:
        invalid_answer_long_text = ApplicationAnswer(
            question_id="question-1",
            text="x" * 5001  # Exceeds max length of 5000
        )
        print("[FAIL] Invalid answer text length should have failed validation")
    except ValidationError:
        print("[PASS] Invalid answer text length correctly failed validation")

if __name__ == "__main__":
    test_assessment_validation()
    test_user_validation()
    test_job_validation()
    test_application_validation()
    print("\nAll validation tests completed!")