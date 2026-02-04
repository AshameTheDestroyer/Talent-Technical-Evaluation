from sqlalchemy.orm import Session
from typing import List, Optional

from models.question import Question
from schemas.question import QuestionCreate, QuestionUpdate
from services.base_service import get_item_by_id, get_items, create_item, update_item

def get_question(db: Session, question_id: int) -> Optional[Question]:
    """Get question by ID"""
    return get_item_by_id(db, Question, question_id)

def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[Question]:
    """Get list of questions"""
    return get_items(db, Question, skip, limit)

def get_questions_by_assessment(db: Session, assessment_id: int, skip: int = 0, limit: int = 100) -> List[Question]:
    """Get list of questions by assessment ID"""
    return db.query(Question).filter(Question.assessment_id == assessment_id).offset(skip).limit(limit).all()

def create_question(db: Session, question: QuestionCreate) -> Question:
    """Create a new question"""
    db_question = Question(**question.dict())
    return create_item(db, db_question)

def update_question(db: Session, question_id: int, question_update: QuestionUpdate) -> Optional[Question]:
    """Update a question"""
    db_question = get_question(db, question_id)
    if db_question:
        return update_item(db, db_question, **question_update.dict(exclude_unset=True))
    return None