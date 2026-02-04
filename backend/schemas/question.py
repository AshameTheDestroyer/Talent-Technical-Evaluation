from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from .base import BaseSchema

class QuestionBase(BaseSchema):
    assessment_id: int
    question_text: str
    question_type: str  # 'text', 'true_false', 'multiple_choice'
    is_knockout: bool = False
    weight: int = 1
    max_score: int = 10

class QuestionCreate(QuestionBase):
    question_text: str
    question_type: str

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    is_knockout: Optional[bool] = None
    weight: Optional[int] = None
    max_score: Optional[int] = None

class QuestionInDB(QuestionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True