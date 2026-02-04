from sqlalchemy import Column, String, Boolean, Text, CheckConstraint
from .base import Base
import uuid
import json
from typing import List, Optional

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, nullable=False)
    seniority = Column(String, nullable=False)  # intern, junior, mid, senior
    description = Column(Text)
    skill_categories = Column(String)  # Stored as JSON string
    active = Column(Boolean, default=True)

    # Add constraint to ensure seniority is valid
    __table_args__ = (CheckConstraint(seniority.in_(['intern', 'junior', 'mid', 'senior']), name='valid_seniority'),)

    def validate_skill_categories(self) -> bool:
        """Validate the skill_categories JSON structure"""
        try:
            if self.skill_categories:
                parsed_categories = json.loads(self.skill_categories)
                if not isinstance(parsed_categories, list):
                    return False
                # Validate that all items in the list are strings
                return all(isinstance(cat, str) for cat in parsed_categories)
            return True
        except (json.JSONDecodeError, TypeError):
            return False