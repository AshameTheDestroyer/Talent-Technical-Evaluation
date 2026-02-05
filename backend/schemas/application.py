from typing import Optional, List
from pydantic import BaseModel, Field
from .base import BaseSchema
from .enums import QuestionType

class ApplicationAnswer(BaseModel):
    question_id: str = Field(..., min_length=1)
    text: Optional[str] = Field(None, max_length=5000)
    options: Optional[List[str]] = []

class ApplicationUser(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str

class ApplicationQuestion(BaseModel):
    id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1, max_length=1000)
    weight: int = Field(..., ge=1, le=5)  # range 1-5
    skill_categories: List[str] = Field(..., min_items=1)
    type: QuestionType
    options: Optional[List[dict]] = []  # Using dict for simplicity
    correct_options: Optional[List[str]] = []

class ApplicationAnswerWithQuestion(ApplicationAnswer):
    question_text: str = Field(..., min_length=1, max_length=1000)
    weight: int = Field(..., ge=1, le=5)  # range 1-5
    skill_categories: List[str] = Field(..., min_items=1)
    type: QuestionType
    question_options: Optional[List[dict]] = []  # Options for the question
    correct_options: Optional[List[str]] = []
    rationale: str = Field(..., min_length=1, max_length=1000)

class ApplicationBase(BaseSchema):
    job_id: str = Field(..., min_length=1)
    assessment_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    answers: List[ApplicationAnswer] = Field(..., min_items=1)

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    answers: Optional[List[ApplicationAnswer]] = Field(None, min_items=1)

class ApplicationAssessment(BaseModel):
    id: str
    title: str
    passing_score: Optional[int] = None
    created_at: Optional[str] = None

class ApplicationResponse(ApplicationBase):
    id: str
    score: Optional[float] = None
    passing_score: Optional[float] = None
    assessment_details: Optional[ApplicationAssessment] = None

    class Config:
        from_attributes = True

class ApplicationDetailedResponse(ApplicationResponse):
    user: ApplicationUser
    answers: List[ApplicationAnswerWithQuestion]

class ApplicationListResponse(BaseModel):
    count: int
    total: int
    data: List[ApplicationResponse]

class ApplicationDetailedListResponse(BaseModel):
    count: int
    total: int
    data: List[ApplicationResponse]

class MyApplicationsJob(BaseModel):
    id: str
    title: str
    seniority: str
    description: str

class MyApplicationsAssessment(BaseModel):
    id: str
    title: str
    passing_score: float

class MyApplicationResponse(BaseModel):
    id: str
    job: MyApplicationsJob
    assessment: MyApplicationsAssessment
    score: float
    created_at: Optional[str] = None

class MyApplicationsListResponse(BaseModel):
    count: int
    total: int
    data: List[MyApplicationResponse]
