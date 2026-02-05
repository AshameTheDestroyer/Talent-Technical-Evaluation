from typing import List, Dict, Any
from schemas.assessment import AssessmentQuestion
from schemas.application import ApplicationAnswerWithQuestion
from integrations.ai_integration.ai_factory import AIGeneratorFactory, DEFAULT_PROVIDER
from logging_config import get_logger

# Create logger for this module
logger = get_logger(__name__)

def generate_questions(title: str, questions_types: List[str], additional_note: str = None, job_info: dict = None, provider=None) -> List[AssessmentQuestion]:
    """
    Generate questions based on the assessment title, job information, and specified question types.

    Args:
        title: The title of the assessment
        questions_types: List of question types to generate (choose_one, choose_many, text_based)
        additional_note: Additional information to guide question generation
        job_info: Information about the job the assessment is for
        provider: The AI provider to use (defaults to the default provider)

    Returns:
        List of generated AssessmentQuestion objects
    """
    logger.info(f"Generating questions for assessment: '{title}' with types: {questions_types}")

    # Use the default provider if none is specified
    if provider is None:
        provider = DEFAULT_PROVIDER

    # Get the AI generator from the factory
    ai_generator = AIGeneratorFactory.create_generator(provider)

    # Generate questions using the selected AI provider
    generated_questions = ai_generator.generate_questions(
        title=title,
        questions_types=questions_types,
        additional_note=additional_note,
        job_info=job_info
    )

    logger.info(f"Generated {len(generated_questions)} questions for assessment: '{title}' using {provider.value} provider")
    return generated_questions

def score_answer(question: AssessmentQuestion, answer_text: str, selected_options: List[str] = None, provider=None) -> Dict[str, Any]:
    """
    Score an answer based on the question and the provided answer.

    Args:
        question: The question being answered
        answer_text: The text of the answer (for text-based questions)
        selected_options: Selected options (for multiple choice questions)
        provider: The AI provider to use (defaults to the default provider)

    Returns:
        Dictionary containing score information:
        {
            'score': float,  # Score between 0 and 1
            'rationale': str,  # Explanation of the score
            'correct': bool  # Whether the answer is correct
        }
    """
    logger.info(f"Scoring answer for question: '{question.text[:50]}...' using {provider.value if provider else DEFAULT_PROVIDER.value} provider")

    # Use the default provider if none is specified
    if provider is None:
        provider = DEFAULT_PROVIDER

    # Get the AI generator from the factory
    ai_generator = AIGeneratorFactory.create_generator(provider)

    # Score the answer using the selected AI provider
    score_result = ai_generator.score_answer(
        question=question,
        answer_text=answer_text,
        selected_options=selected_options
    )

    logger.info(f"Scored answer with score: {score_result['score']}, correct: {score_result['correct']}")
    return score_result