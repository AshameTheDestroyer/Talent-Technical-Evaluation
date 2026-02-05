from abc import ABC, abstractmethod
from typing import List, Dict, Any
from schemas.assessment import AssessmentQuestion


class AIGeneratorInterface(ABC):
    """
    Interface for AI question generators.
    Defines the contract that all AI providers must implement.
    """

    @abstractmethod
    def generate_questions(
        self,
        title: str,
        questions_types: List[str],
        additional_note: str = None,
        job_info: Dict[str, Any] = None
    ) -> List[AssessmentQuestion]:
        """
        Generate questions based on the assessment title, job information, and specified question types.

        Args:
            title: The title of the assessment
            questions_types: List of question types to generate (choose_one, choose_many, text_based)
            additional_note: Additional information to guide question generation
            job_info: Information about the job the assessment is for

        Returns:
            List of generated AssessmentQuestion objects
        """
        pass

    @abstractmethod
    def score_answer(
        self,
        question: AssessmentQuestion,
        answer_text: str,
        selected_options: List[str] = None
    ) -> Dict[str, Any]:
        """
        Score an answer based on the question and the provided answer.

        Args:
            question: The question being answered
            answer_text: The text of the answer (for text-based questions)
            selected_options: Selected options (for multiple choice questions)

        Returns:
            Dictionary containing score information:
            {
                'score': float,  # Score between 0 and 1
                'rationale': str,  # Explanation of the score
                'correct': bool  # Whether the answer is correct
            }
        """
        pass

    @abstractmethod
    def estimate_duration(
        self,
        prompt: str
    ) -> str:
        """
        Estimate the duration for an assessment based on a prompt.

        Args:
            prompt: A detailed prompt describing the assessment

        Returns:
            String response from the AI containing the estimated duration
        """
        pass