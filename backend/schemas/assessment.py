from typing import Optional, List
from pydantic import BaseModel, Field
from .base import BaseSchema
from .enums import QuestionType

class AssessmentQuestionOption(BaseModel):
    text: str
    value: str

class AssessmentQuestion(BaseModel):
    id: str
    text: str
    weight: int = Field(..., ge=1, le=5)  # range 1-5
    skill_categories: List[str]
    type: QuestionType
    options: Optional[List[AssessmentQuestionOption]] = []
    correct_options: Optional[List[str]] = []

class AssessmentBase(BaseSchema):
    title: str = Field(..., min_length=1, max_length=200)
    duration: Optional[int] = Field(None, ge=1)  # Duration in seconds, if provided should be positive
    passing_score: int = Field(..., ge=20, le=80)  # range 20-80
    questions: Optional[List[AssessmentQuestion]] = []
    active: bool = True

class AssessmentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    passing_score: int = Field(..., ge=20, le=80)  # range 20-80
    questions_types: List[QuestionType]  # array of enum(choose_one, choose_many, text_based)
    additional_note: Optional[str] = Field(None, max_length=500)

class AssessmentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    passing_score: Optional[int] = Field(None, ge=20, le=80)  # range 20-80
    questions: Optional[List[AssessmentQuestion]] = None
    active: Optional[bool] = None

class AssessmentRegenerate(BaseModel):
    questions_types: Optional[List[QuestionType]] = None  # array of enum(choose_one, choose_many, text_based)
    additional_note: Optional[str] = Field(None, max_length=500)

class AssessmentResponse(AssessmentBase):
    id: str
    questions_count: int = 0

    class Config:
        from_attributes = True

class AssessmentListResponse(BaseModel):
    count: int
    total: int
    data: List[AssessmentResponse]

class AssessmentDetailedResponse(AssessmentResponse):
    questions: List[AssessmentQuestion]