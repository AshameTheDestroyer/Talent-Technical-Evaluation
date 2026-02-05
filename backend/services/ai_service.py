import re
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

def estimate_assessment_duration(title: str, job_info: dict, questions: List[AssessmentQuestion], additional_note: str = None, provider=None) -> int:
    """
    Estimate the duration needed for an assessment based on its details and questions.

    Args:
        title: The title of the assessment
        job_info: Information about the job the assessment is for
        questions: List of questions in the assessment
        additional_note: Additional information about the assessment
        provider: The AI provider to use (defaults to the default provider)

    Returns:
        Estimated duration in minutes
    """
    logger.info(f"Estimating duration for assessment: '{title}' with {len(questions)} questions")

    # Use the default provider if none is specified
    if provider is None:
        provider = DEFAULT_PROVIDER

    # Get the AI generator from the factory
    ai_generator = AIGeneratorFactory.create_generator(provider)

    # Prepare the prompt for the AI
    prompt = f"""
    Based on the following assessment details, estimate how many minutes a candidate would need to complete this assessment.
    Consider the complexity of the questions and the job requirements.
    
    Assessment Title: {title}
    
    Job Information:
    - Title: {job_info.get('title', 'N/A')}
    - Seniority: {job_info.get('seniority', 'N/A')}
    - Description: {job_info.get('description', 'N/A')}
    - Skill Categories: {', '.join(job_info.get('skill_categories', []))}
    
    Questions Count: {len(questions)}
    """

    # Add question details to the prompt
    for i, question in enumerate(questions[:5]):  # Limit to first 5 questions to avoid overly long prompts
        prompt += f"\nQuestion {i+1} ({question.type}): {question.text[:100]}..."
        if question.type == 'text_based':
            prompt += " (Text-based question requiring written response)"
        elif question.type in ['choose_one', 'choose_many']:
            prompt += f" (Multiple choice with {len(question.options)} options)"

    if additional_note:
        prompt += f"\nAdditional Notes: {additional_note}"

    prompt += "\n\nPlease provide only a number representing the estimated duration in minutes."

    # Get the AI's estimation
    duration_estimate = ai_generator.estimate_duration(prompt)

    # Extract the first number from the response using regex
    duration_match = re.search(r'\d+', duration_estimate)
    if duration_match:
        duration_minutes = int(duration_match.group())
        # Ensure the duration is within reasonable bounds (1-180 minutes)
        duration_minutes = max(1, min(180, duration_minutes))
        logger.info(f"Estimated duration for assessment '{title}': {duration_minutes} minutes")
        return duration_minutes
    else:
        # If no number is found in the response, return a default duration based on question count
        default_duration = min(60, max(5, len(questions) * 3))  # 3 minutes per question, capped at 60
        logger.warning(f"No duration found in AI response. Using default: {default_duration} minutes")
        return default_duration