import json
import os
from typing import List, Dict, Any
from mistralai import Mistral
from schemas.assessment import AssessmentQuestion, AssessmentQuestionOption
from schemas.enums import QuestionType
from integrations.ai_integration.ai_generator_interface import AIGeneratorInterface
from config import settings


class MistralGenerator(AIGeneratorInterface):
    """
    Mistral Generator implementation for generating assessment questions using Mistral AI API.
    """

    def __init__(self):
        """
        Initialize the MistralGenerator with API key from settings.
        """
        api_key = os.getenv("MISTRAL_API_KEY") or getattr(settings, 'mistral_api_key', None)

        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is not set")

        self.client = Mistral(api_key=api_key)

    def generate_questions(
        self,
        title: str,
        questions_types: List[str],
        additional_note: str = None,
        job_info: Dict[str, Any] = None
    ) -> List[AssessmentQuestion]:
        """
        Generate questions using Mistral AI API based on the assessment title, job information, and specified question types.
        """
        # Prepare the prompt for Mistral AI
        prompt = self._create_prompt(title, questions_types, additional_note, job_info)

        messages = [
            {"role": "system", "content": "You generate technical assessment questions."},
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.complete(
            model="mistral-small-latest",
            messages=messages,
            temperature=0.2,
        )

        content = response.choices[0].message.content
        passed = 0
        while passed < 5:
            try:
                try:
                    # Parse the JSON response from Mistral
                    questions_data = json.loads(content)
                    passed = 10
                except json.JSONDecodeError:
                    content = content[7:-3].strip()
                    questions_data = json.loads(content)
                    passed = 10
            except json.JSONDecodeError:
                raise ValueError("Mistral returned invalid JSON")

        # Convert the response to AssessmentQuestion objects
        return self._convert_to_assessment_questions(questions_data)

    def score_answer(
        self,
        question: AssessmentQuestion,
        answer_text: str,
        selected_options: List[str] = None
    ) -> Dict[str, Any]:
        """
        Score an answer using Mistral AI API based on the question and the provided answer.
        """
        # Create a prompt for scoring the answer
        if question.type == QuestionType.text_based:
            prompt = f"""
            Evaluate the following answer to a text-based question:

            Question: {question.text}
            Answer: {answer_text}

            Please provide a score between 0 and 1, where 1 means completely correct and 0 means completely incorrect.
            Also provide a brief rationale for the score.

            Respond in the following JSON format:
            {{
                "score": float,
                "rationale": str,
                "correct": bool
            }}
            """
        else:
            # For multiple choice questions
            selected_str = ", ".join(selected_options) if selected_options else "No options selected"
            correct_str = ", ".join(question.correct_options) if question.correct_options else "Unknown"

            prompt = f"""
            Evaluate the following answer to a multiple-choice question:

            Question: {question.text}
            Selected Options: {selected_str}
            Correct Options: {correct_str}

            Please provide a score between 0 and 1, where 1 means completely correct and 0 means completely incorrect.
            Also provide a brief rationale for the score.

            Respond in the following JSON format:
            {{
                "score": float,
                "rationale": str,
                "correct": bool
            }}
            """

        messages = [
            {"role": "system", "content": "You are an expert at evaluating assessment answers."},
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.complete(
            model="mistral-small-latest",
            messages=messages,
            temperature=0.2,
        )

        content = response.choices[0].message.content
        passed = 0
        while passed < 5:
            try:
                try:
                    result = json.loads(content)
                    passed = 10  # Exit the loop successfully
                except json.JSONDecodeError:
                    # Try to strip markdown code block markers
                    content = content[7:-3].strip()
                    result = json.loads(content)
                    passed = 10  # Exit the loop successfully
            except json.JSONDecodeError:
                raise ValueError("Mistral returned invalid JSON for answer scoring")

        return {
            'score': result.get('score', 0.0),
            'rationale': result.get('rationale', ''),
            'correct': result.get('correct', False)
        }

    def _create_prompt(
        self,
        title: str,
        questions_types: List[str],
        additional_note: str = None,
        job_info: Dict[str, Any] = None
    ) -> str:
        """
        Create a prompt for Mistral AI based on the assessment requirements.
        """
        # Map question types to the expected format for Mistral
        type_mapping = {
            QuestionType.choose_one.value: "MCQ",
            QuestionType.choose_many.value: "MCQ",  # Multiple choice with multiple correct answers
            QuestionType.text_based.value: "TEXT"
        }

        # Count the number of each type of question needed
        mcq_count = questions_types.count(QuestionType.choose_one.value) + \
                    questions_types.count(QuestionType.choose_many.value)
        text_count = questions_types.count(QuestionType.text_based.value)

        # Build the job information section of the prompt
        job_details = ""
        if job_info:
            job_title = job_info.get('title', '')
            job_skills = job_info.get('skill_categories', [])
            job_seniority = job_info.get('seniority', '')

            job_details = f"""
Job Information:
- Title: {job_title}
- Skills: {', '.join(job_skills)}
- Seniority: {job_seniority}
"""
        else:
            job_details = f"""
Job Information:
- Title: {title}
"""

        # Add additional note if provided
        if additional_note:
            job_details += f"- Additional Note: {additional_note}\n"

        prompt = f"""
You are an assessment generator.

Generate EXACTLY {len(questions_types)} questions for the following job.

{job_details}

MANDATORY RULES:
1. Output MUST be a JSON ARRAY with EXACTLY {len(questions_types)} objects.
2. The list MUST contain:
   - {mcq_count} MCQ questions (multiple choice)
   - {text_count} TEXT questions (text-based)
3. Do NOT include explanations or markdown.
4. Follow the schema EXACTLY.

Schema for each question:

{{
  "type": "MCQ | TEXT",
  "prompt": "string",
  "choices": ["string"],  // For MCQ questions only
  "correct_answer": "string | null",  // For MCQ questions, string for correct choice; for TEXT questions, null
  "difficulty": "easy | medium | hard",
  "skill": "string"
}}

Rules per type:
- MCQ → 4 choices + correct_answer as the text of the correct choice
- TEXT → correct_answer = null

Return ONLY the JSON array.
"""

        return prompt

    def _convert_to_assessment_questions(self, questions_data: List[Dict]) -> List[AssessmentQuestion]:
        """
        Convert the JSON response from Mistral to AssessmentQuestion objects.
        """
        assessment_questions = []

        for i, q_data in enumerate(questions_data):
            # Generate a unique ID for the question
            question_id = f"mistral_{i}"

            # Determine the question type based on the response
            if q_data.get("type") == "MCQ":
                # For multiple choice questions
                question_type = QuestionType.choose_one  # Default to choose_one

                # Create options
                options = []
                for choice in q_data.get("choices", []):
                    option = AssessmentQuestionOption(text=choice, value=choice)
                    options.append(option)

                # Find the correct option
                correct_options = []
                correct_answer = q_data.get("correct_answer")
                if correct_answer:
                    # Find the option that matches the correct answer
                    for opt in options:
                        if opt.text == correct_answer:
                            correct_options.append(opt.value)
                            break
            else:
                # For text-based questions
                question_type = QuestionType.text_based
                options = []
                correct_options = []

            # Create the AssessmentQuestion object
            question = AssessmentQuestion(
                id=question_id,
                text=q_data.get("prompt", ""),
                weight=3,  # Default weight
                skill_categories=[q_data.get("skill", "General")],  # Default to General if no skill specified
                type=question_type,
                options=options,
                correct_options=correct_options
            )

            assessment_questions.append(question)

        return assessment_questions

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
        messages = [
            {"role": "system", "content": "You estimate assessment durations. Respond with only a number representing minutes."},
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.complete(
            model="mistral-small-latest",
            messages=messages,
            temperature=0.2,
        )

        content = response.choices[0].message.content
        return content
