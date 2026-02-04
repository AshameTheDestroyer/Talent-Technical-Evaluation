from typing import Optional
from pydantic import BaseModel
from .base import BaseSchema

class QuestionTagBase(BaseSchema):
    question_id: int
    tag_name: str

class QuestionTagCreate(QuestionTagBase):
    pass

class QuestionTagUpdate(BaseModel):
    tag_name: Optional[str] = None

class QuestionTagInDB(QuestionTagBase):
    id: int

    class Config:
        from_attributes = True