from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from .base import Base
import uuid

class Application(Base):
    __tablename__ = "applications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False)
    assessment_id = Column(String, ForeignKey("assessments.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    answers = Column(Text)  # Stored as JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())