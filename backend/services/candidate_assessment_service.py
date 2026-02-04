from sqlalchemy.orm import Session
from typing import List, Optional

from models.candidate_assessment import CandidateAssessment
from schemas.candidate_assessment import CandidateAssessmentCreate, CandidateAssessmentUpdate
from services.base_service import get_item_by_id, get_items, create_item, update_item

def get_candidate_assessment(db: Session, candidate_assessment_id: int) -> Optional[CandidateAssessment]:
    """Get candidate assessment by ID"""
    return get_item_by_id(db, CandidateAssessment, candidate_assessment_id)

def get_candidate_assessments(db: Session, skip: int = 0, limit: int = 100) -> List[CandidateAssessment]:
    """Get list of candidate assessments"""
    return get_items(db, CandidateAssessment, skip, limit)

def get_candidate_assessments_by_candidate(db: Session, candidate_id: int, skip: int = 0, limit: int = 100) -> List[CandidateAssessment]:
    """Get list of candidate assessments by candidate ID"""
    return db.query(CandidateAssessment).filter(CandidateAssessment.candidate_id == candidate_id).offset(skip).limit(limit).all()

def get_candidate_assessments_by_assessment(db: Session, assessment_id: int, skip: int = 0, limit: int = 100) -> List[CandidateAssessment]:
    """Get list of candidate assessments by assessment ID"""
    return db.query(CandidateAssessment).filter(CandidateAssessment.assessment_id == assessment_id).offset(skip).limit(limit).all()

def create_candidate_assessment(db: Session, candidate_assessment: CandidateAssessmentCreate) -> CandidateAssessment:
    """Create a new candidate assessment"""
    db_candidate_assessment = CandidateAssessment(**candidate_assessment.dict())
    return create_item(db, db_candidate_assessment)

def update_candidate_assessment(db: Session, candidate_assessment_id: int, candidate_assessment_update: CandidateAssessmentUpdate) -> Optional[CandidateAssessment]:
    """Update a candidate assessment"""
    db_candidate_assessment = get_candidate_assessment(db, candidate_assessment_id)
    if db_candidate_assessment:
        return update_item(db, db_candidate_assessment, **candidate_assessment_update.dict(exclude_unset=True))
    return None