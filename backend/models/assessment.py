from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, CheckConstraint
from .base import Base
import uuid
import json
from pydantic import ValidationError
from typing import Dict, Any

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False)
    title = Column(String, nullable=False)
    duration = Column(Integer)  # in seconds
    passing_score = Column(Integer)  # range 20-80
    questions = Column(Text)  # Stored as JSON string
    active = Column(Boolean, default=True)

    # Add constraint to ensure passing_score is in range 20-80
    __table_args__ = (
        CheckConstraint(passing_score >= 20, name='passing_score_min'),
        CheckConstraint(passing_score <= 80, name='passing_score_max'),
    )

    def validate_questions(self) -> bool:
        """Validate the questions JSON structure"""
        try:
            if self.questions:
                parsed_questions = json.loads(self.questions)
                if not isinstance(parsed_questions, list):
                    return False

                # Validate each question
                for question in parsed_questions:
                    if not self._validate_single_question(question):
                        return False
                return True
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    def _validate_single_question(self, question: Dict[str, Any]) -> bool:
        """Validate a single question structure"""
        required_fields = {'id', 'text', 'weight', 'skill_categories', 'type'}
        if not all(field in question for field in required_fields):
            return False

        # Validate weight is in range 1-5
        if not isinstance(question['weight'], int) or question['weight'] < 1 or question['weight'] > 5:
            return False

        # Validate skill_categories is a list
        if not isinstance(question['skill_categories'], list):
            return False

        # Validate type is one of the allowed types
        allowed_types = {'choose_one', 'choose_many', 'text_based'}
        if question['type'] not in allowed_types:
            return False

        return True