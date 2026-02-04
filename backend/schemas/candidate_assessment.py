from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from .base import BaseSchema

class CandidateAssessmentBase(BaseSchema):
    candidate_id: int
    assessment_id: int
    status: str = 'not_started'  # 'not_started', 'in_progress', 'completed'
    total_score: Optional[int] = None

class CandidateAssessmentCreate(CandidateAssessmentBase):
    candidate_id: int
    assessment_id: int

class CandidateAssessmentUpdate(BaseModel):
    status: Optional[str] = None
    total_score: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class CandidateAssessmentInDB(CandidateAssessmentBase):
    id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True