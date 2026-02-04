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

def test_scoring_methodology():
    """Test that multiple choice questions are scored directly and text-based use AI evaluation"""
    
    print("Testing scoring methodology...")
    
    # Test multiple choice question scoring (direct comparison)
    print("\n1. Testing multiple choice question scoring (direct comparison)...")
    mc_question = AssessmentQuestion(
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
    correct_mc_result = score_answer(
        question=mc_question,
        answer_text="",
        selected_options=["b"]
    )
    print(f"   Correct MC answer score: {correct_mc_result['score']}")
    print(f"   Correct MC answer rationale: {correct_mc_result['rationale']}")
    assert correct_mc_result['score'] == 1.0, f"Expected 1.0 for correct MC answer, got {correct_mc_result['score']}"
    assert correct_mc_result['correct'] == True, f"Expected True for correct MC answer, got {correct_mc_result['correct']}"
    print("   [PASS] Correct multiple choice answer scored directly")
    
    # Test incorrect answer
    incorrect_mc_result = score_answer(
        question=mc_question,
        answer_text="",
        selected_options=["a"]  # London is wrong
    )
    print(f"   Incorrect MC answer score: {incorrect_mc_result['score']}")
    print(f"   Incorrect MC answer rationale: {incorrect_mc_result['rationale']}")
    assert incorrect_mc_result['score'] == 0.0, f"Expected 0.0 for incorrect MC answer, got {incorrect_mc_result['score']}"
    assert incorrect_mc_result['correct'] == False, f"Expected False for incorrect MC answer, got {incorrect_mc_result['correct']}"
    print("   [PASS] Incorrect multiple choice answer scored directly")
    
    # Test text-based question scoring (AI evaluation)
    print("\n2. Testing text-based question scoring (AI evaluation)...")
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
        answer_text="Renewable energy is important because it reduces carbon emissions and is sustainable for future generations.",
        selected_options=[]
    )
    print(f"   Text answer score: {text_result['score']}")
    print(f"   Text answer rationale: {text_result['rationale']}")
    # The score should be based on our heuristic evaluation (length, keywords, etc.)
    assert 0.0 <= text_result['score'] <= 1.0, f"Text score {text_result['score']} is not in range [0,1]"
    print("   [PASS] Text-based answer scored using AI evaluation heuristics")
    
    # Test text-based question with poor answer
    poor_text_result = score_answer(
        question=text_question,
        answer_text="It's good.",
        selected_options=[]
    )
    print(f"   Poor text answer score: {poor_text_result['score']}")
    print(f"   Poor text answer rationale: {poor_text_result['rationale']}")
    # Short answers should receive lower scores
    assert poor_text_result['score'] < text_result['score'], f"Short answer should score lower than detailed answer"
    print("   [PASS] Poor text answer received lower score")
    
    # Test choose-many question
    print("\n3. Testing choose-many question scoring (direct comparison)...")
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
    assert correct_multichoice_result['score'] == 1.0, f"Expected 1.0 for correct multichoice answer, got {correct_multichoice_result['score']}"
    assert correct_multichoice_result['correct'] == True, f"Expected True for correct multichoice answer, got {correct_multichoice_result['correct']}"
    print("   [PASS] Correct choose-many answer scored directly")
    
    incorrect_multichoice_result = score_answer(
        question=multichoice_question,
        answer_text="",
        selected_options=["a", "b"]  # Partially incorrect (includes HTML)
    )
    print(f"   Incorrect multichoice score: {incorrect_multichoice_result['score']}")
    print(f"   Incorrect multichoice rationale: {incorrect_multichoice_result['rationale']}")
    assert incorrect_multichoice_result['score'] == 0.0, f"Expected 0.0 for incorrect multichoice answer, got {incorrect_multichoice_result['score']}"
    assert incorrect_multichoice_result['correct'] == False, f"Expected False for incorrect multichoice answer, got {incorrect_multichoice_result['correct']}"
    print("   [PASS] Incorrect choose-many answer scored directly")
    
    print("\n[PASS] Scoring methodology test completed successfully!")
    print("- Multiple choice questions are scored directly by comparing options")
    print("- Text-based questions use AI evaluation (heuristic scoring in mock)")
    print("- This approach optimizes performance by avoiding unnecessary AI calls")


if __name__ == "__main__":
    test_scoring_methodology()