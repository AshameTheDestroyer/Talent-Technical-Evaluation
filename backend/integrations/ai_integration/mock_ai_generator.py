import random
import uuid
from typing import List, Dict, Any
from schemas.assessment import AssessmentQuestion, AssessmentQuestionOption
from schemas.enums import QuestionType
from integrations.ai_integration.ai_generator_interface import AIGeneratorInterface


class MockAIGenerator(AIGeneratorInterface):
    """
    Mock AI Generator implementation for testing purposes.
    Generates questions based on predefined templates and job information.
    """
    
    def generate_questions(
        self, 
        title: str, 
        questions_types: List[str], 
        additional_note: str = None, 
        job_info: Dict[str, Any] = None
    ) -> List[AssessmentQuestion]:
        """
        Generate questions using mock AI logic based on job information.
        """
        num_questions = len(questions_types)
        generated_questions = []
        
        for i, q_type in enumerate(questions_types):
            # Create a question ID
            question_id = str(uuid.uuid4())
            
            # Generate question text based on the assessment title, job info and question type
            question_text = self._generate_question_text(title, q_type, i+1, additional_note, job_info)
            
            # Determine weight (random between 1-5)
            weight = random.randint(1, 5)
            
            # Generate skill categories based on the assessment title and job info
            skill_categories = self._generate_skill_categories(title, job_info)
            
            # Generate options and correct options based on the question type
            options = []
            correct_options = []
            
            if q_type in [QuestionType.choose_one.value, QuestionType.choose_many.value]:
                options = self._generate_multiple_choice_options(q_type, question_text)
                correct_options = self._select_correct_options(options, q_type)
            
            # Create the AssessmentQuestion object
            question = AssessmentQuestion(
                id=question_id,
                text=question_text,
                weight=weight,
                skill_categories=skill_categories,
                type=QuestionType(q_type),
                options=options,
                correct_options=correct_options
            )
            
            generated_questions.append(question)
        
        return generated_questions

    def _generate_question_text(self, title: str, q_type: str, question_number: int, additional_note: str = None, job_info: Dict[str, Any] = None) -> str:
        """Generate a question text based on the assessment title, job info and question type."""
        # Normalize the title to lowercase for processing
        normalized_title = title.lower()
        
        # Use job information if available to enhance question relevance
        job_title = job_info.get('title', '') if job_info else ''
        job_description = job_info.get('description', '') if job_info else ''
        job_seniority = job_info.get('seniority', '') if job_info else ''
        job_skills = job_info.get('skill_categories', []) if job_info else []
        
        # Create a base question depending on the assessment title and job information
        if "python" in normalized_title or "programming" in normalized_title or "python" in job_title.lower() or "programming" in job_title.lower():
            base_questions = [
                f"What is the correct way to declare a variable in {title}?",
                f"How would you implement a function to solve a problem in {title}?",
                f"Which of the following is a characteristic of {title}?",
                f"What is the time complexity of this operation in {title}?",
                f"In {title}, what is the purpose of this code snippet?",
                f"What is the output of this {title} code?",
                f"Which {title} concept is best suited for this scenario?",
                f"What is the main advantage of using {title} in this context?"
            ]
        elif "software" in normalized_title or "engineer" in normalized_title or "software" in job_title.lower() or "engineer" in job_title.lower():
            base_questions = [
                f"What is the most efficient approach to design a system for {title}?",
                f"Which software development principle applies to {title}?",
                f"How would you optimize the performance of a {title} application?",
                f"What is the best practice for error handling in {title}?",
                f"Which testing methodology is most appropriate for {title}?",
                f"What architectural pattern would you recommend for {title}?",
                f"How would you ensure scalability in {title}?",
                f"What security consideration is important for {title}?"
            ]
        elif "data" in normalized_title or "analysis" in normalized_title or "data" in job_title.lower() or "analysis" in job_title.lower():
            base_questions = [
                f"How would you clean and preprocess data for {title}?",
                f"Which statistical method is appropriate for {title}?",
                f"What visualization technique best represents {title}?",
                f"How would you handle missing values in {title}?",
                f"What is the correlation between variables in {title}?",
                f"Which machine learning model is suitable for {title}?",
                f"How would you validate the results of {title}?",
                f"What ethical consideration applies to {title}?"
            ]
        elif job_skills:  # If job has specific skill categories, use them to generate relevant questions
            # Join the skills to form a context
            skills_context = ", ".join(job_skills)
            base_questions = [
                f"How would you apply {skills_context} skills in this {title} role?",
                f"What challenges might you face using {skills_context} in this position?",
                f"Which {skills_context} techniques are most relevant for this {title}?",
                f"How would you leverage your {skills_context} experience in this role?",
                f"What {skills_context} methodologies would you use for this {title}?",
                f"How do {skills_context} skills contribute to success in this position?",
                f"What {skills_context} tools would be most effective for this {title}?",
                f"How would you apply {skills_context} best practices in this role?"
            ]
        else:
            # Generic questions if title doesn't match known patterns
            base_questions = [
                f"What is the fundamental concept behind {title}?",
                f"How would you approach solving a problem in {title}?",
                f"What are the key characteristics of {title}?",
                f"What is the main purpose of {title}?",
                f"Which principle governs {title}?",
                f"How does {title} differ from similar concepts?",
                f"What are the advantages of using {title}?",
                f"What limitations should be considered in {title}?"
            ]
        
        # Select a question based on the question number to ensure variety
        question_index = (question_number * 7) % len(base_questions)  # Use prime number to create variation
        question_text = base_questions[question_index]
        
        # Add context from additional note if provided
        if additional_note:
            question_text += f" ({additional_note})"
        
        # Add context from job description if available
        if job_description:
            question_text += f" Consider the following job description: {job_description[:100]}..."  # Truncate to avoid overly long questions
        
        return question_text

    def _generate_skill_categories(self, title: str, job_info: Dict[str, Any] = None) -> List[str]:
        """Generate skill categories based on the assessment title and job information."""
        normalized_title = title.lower()
        categories = ["general"]
        
        # Use job information if available to enhance category relevance
        job_title = job_info.get('title', '') if job_info else ''
        job_seniority = job_info.get('seniority', '') if job_info else ''
        job_skills = job_info.get('skill_categories', []) if job_info else []
        
        # Combine title and job title for broader matching
        combined_title = f"{title} {job_title}".lower()
        
        if "python" in combined_title:
            categories.extend(["python", "programming", "backend"])
        elif "javascript" in combined_title or "js" in combined_title:
            categories.extend(["javascript", "programming", "frontend"])
        elif "react" in combined_title:
            categories.extend(["react", "javascript", "frontend"])
        elif "data" in combined_title or "analysis" in combined_title:
            categories.extend(["data-analysis", "statistics", "visualization"])
        elif "machine learning" in combined_title or "ml" in combined_title:
            categories.extend(["machine-learning", "algorithms", "data-science"])
        elif "devops" in combined_title:
            categories.extend(["devops", "ci/cd", "infrastructure"])
        elif "security" in combined_title:
            categories.extend(["security", "cybersecurity", "vulnerability"])
        elif "software" in combined_title or "engineer" in combined_title:
            categories.extend(["software-engineering", "design-patterns", "algorithms"])
        
        # Add job-specific skills if available
        if job_skills:
            categories.extend(job_skills)
        
        # Add seniority-specific categories
        if job_seniority:
            if job_seniority == "intern":
                categories.extend(["learning", "basic-concepts", "mentoring"])
            elif job_seniority == "junior":
                categories.extend(["development", "coding", "implementation"])
            elif job_seniority == "mid":
                categories.extend(["problem-solving", "architecture", "teamwork"])
            elif job_seniority == "senior":
                categories.extend(["leadership", "architecture", "decision-making"])
        
        # Add a few more generic categories
        categories.extend(["problem-solving", "critical-thinking"])
        
        # Limit to 5 categories max to prevent overly long lists
        return list(set(categories))[:5]

    def _generate_multiple_choice_options(self, q_type: str, question_text: str) -> List[AssessmentQuestionOption]:
        """Generate multiple choice options for a question."""
        options = []
        
        # Generate 3-5 options depending on the question
        num_options = random.randint(3, 5)
        
        for i in range(num_options):
            option_letter = chr(ord('a') + i)  # 'a', 'b', 'c', etc.
            
            # Create option text based on the question
            if "python" in question_text.lower():
                option_texts = [
                    f"Option {option_letter}: This approach uses Python's built-in functions",
                    f"Option {option_letter}: This solution involves a custom class implementation",
                    f"Option {option_letter}: This method leverages external libraries",
                    f"Option {option_letter}: This technique uses recursion",
                    f"Option {option_letter}: This algorithm has O(n) time complexity",
                    f"Option {option_letter}: This pattern follows Python best practices"
                ]
            elif "software" in question_text.lower() or "design" in question_text.lower():
                option_texts = [
                    f"Option {option_letter}: This follows the singleton pattern",
                    f"Option {option_letter}: This implements the observer pattern",
                    f"Option {option_letter}: This uses the factory method",
                    f"Option {option_letter}: This applies the decorator pattern",
                    f"Option {option_letter}: This utilizes microservices architecture",
                    f"Option {option_letter}: This employs event-driven design"
                ]
            else:
                option_texts = [
                    f"Option {option_letter}: This is the correct approach",
                    f"Option {option_letter}: This is an alternative method",
                    f"Option {option_letter}: This is a common misconception",
                    f"Option {option_letter}: This relates to advanced concepts",
                    f"Option {option_letter}: This is a basic implementation",
                    f"Option {option_letter}: This is an outdated approach"
                ]
            
            # Select an option text based on the option index
            option_index = (i * 11) % len(option_texts)  # Use prime number for variation
            option_text = option_texts[option_index]
            
            option = AssessmentQuestionOption(
                text=option_text,
                value=option_letter
            )
            
            options.append(option)
        
        return options

    def _select_correct_options(self, options: List[AssessmentQuestionOption], q_type: str) -> List[str]:
        """Select the correct options for a question."""
        if not options:
            return []

        # For 'choose_one', select exactly one correct option
        if q_type == QuestionType.choose_one.value:
            # Randomly select one option as correct (index 0 to len(options)-1)
            correct_index = random.randint(0, len(options) - 1)
            return [options[correct_index].value]

        # For 'choose_many', select 1-2 correct options
        elif q_type == QuestionType.choose_many.value:
            # Randomly decide how many correct options (1 or 2)
            num_correct = random.randint(1, min(2, len(options)))

            # Randomly select indices for correct options
            correct_indices = random.sample(range(len(options)), num_correct)

            # Return the values of the selected correct options
            return [options[i].value for i in correct_indices]

        # For other types, return empty list
        return []

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
        # For multiple choice questions - score directly without AI
        if question.type in [QuestionType.choose_one, QuestionType.choose_many]:
            if selected_options is None:
                selected_options = []

            # Check if the selected options match the correct options
            correct = set(selected_options) == set(question.correct_options)

            if correct:
                score = 1.0
                rationale = f"The selected options {selected_options} match the correct options {question.correct_options}."
            else:
                score = 0.0
                rationale = f"The selected options {selected_options} do not match the correct options {question.correct_options}."

            return {
                'score': score,
                'rationale': rationale,
                'correct': correct
            }

        # For text-based questions - this is where AI evaluation would happen
        elif question.type == QuestionType.text_based:
            # For mock implementation, we'll give a score based on whether text is provided
            if answer_text and answer_text.strip():
                # In a real implementation, this would use AI to evaluate the quality of the answer
                # For now, we'll simulate a more nuanced scoring
                # Consider factors like length, keywords related to the question, etc.
                score = self._evaluate_text_answer(answer_text, question.text)
                rationale = f"The text answer was evaluated with score {score}."
            else:
                score = 0.0
                rationale = "No answer was provided."

            return {
                'score': score,
                'rationale': rationale,
                'correct': score > 0.5  # Consider correct if score > 0.5
            }

        # Default case
        return {
            'score': 0.0,
            'rationale': "Unable to score this type of question.",
            'correct': False
        }

    def _evaluate_text_answer(self, answer_text: str, question_text: str) -> float:
        """
        Evaluate a text-based answer (simulated AI evaluation).
        In a real implementation, this would call an AI service to evaluate the answer quality.

        Args:
            answer_text: The text of the answer provided by the user
            question_text: The text of the question being answered

        Returns:
            Score between 0 and 1
        """
        # Simple heuristics for mock evaluation
        score = 0.0

        # Check if answer is substantial (not just a few words)
        if len(answer_text.split()) >= 5:  # At least 5 words
            score += 0.3

        # Check if answer contains relevant keywords from the question
        question_keywords = set(question_text.lower().split())
        answer_words = set(answer_text.lower().split())
        common_words = question_keywords.intersection(answer_words)

        if len(common_words) > 0:
            score += 0.2  # Bonus for mentioning relevant terms

        # Additional bonus for longer, more detailed answers
        if len(answer_text) > 100:
            score += 0.2

        # Cap the score at 1.0
        return min(score, 1.0)