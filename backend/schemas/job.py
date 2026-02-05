from typing import Optional, List
from pydantic import BaseModel, Field
from .base import BaseSchema
from .enums import JobSeniority

class JobBase(BaseSchema):
    title: str = Field(..., min_length=1, max_length=200)
    seniority: JobSeniority
    description: Optional[str] = Field(None, max_length=1000)
    skill_categories: Optional[List[str]] = []
    active: bool = True

class JobCreate(JobBase):
    title: str = Field(..., min_length=1, max_length=200)
    seniority: JobSeniority
    description: Optional[str] = Field(None, max_length=1000)

class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    seniority: Optional[JobSeniority] = None
    description: Optional[str] = Field(None, max_length=1000)
    skill_categories: Optional[List[str]] = None
    active: Optional[bool] = None

class JobResponse(JobBase):
    id: str
    applicants_count: int = 0

    class Config:
        from_attributes = True

class JobListResponse(BaseModel):
    count: int
    total: int
    data: List[JobResponse]