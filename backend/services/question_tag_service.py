from sqlalchemy.orm import Session
from typing import List, Optional

from models.question_tag import QuestionTag
from schemas.question_tag import QuestionTagCreate, QuestionTagUpdate
from services.base_service import get_item_by_id, get_items, create_item, update_item

def get_question_tag(db: Session, question_tag_id: int) -> Optional[QuestionTag]:
    """Get question tag by ID"""
    return get_item_by_id(db, QuestionTag, question_tag_id)

def get_question_tags(db: Session, skip: int = 0, limit: int = 100) -> List[QuestionTag]:
    """Get list of question tags"""
    return get_items(db, QuestionTag, skip, limit)

def get_question_tags_by_question(db: Session, question_id: int, skip: int = 0, limit: int = 100) -> List[QuestionTag]:
    """Get list of question tags by question ID"""
    return db.query(QuestionTag).filter(QuestionTag.question_id == question_id).offset(skip).limit(limit).all()

def create_question_tag(db: Session, question_tag: QuestionTagCreate) -> QuestionTag:
    """Create a new question tag"""
    db_question_tag = QuestionTag(**question_tag.dict())
    return create_item(db, db_question_tag)

def update_question_tag(db: Session, question_tag_id: int, question_tag_update: QuestionTagUpdate) -> Optional[QuestionTag]:
    """Update a question tag"""
    db_question_tag = get_question_tag(db, question_tag_id)
    if db_question_tag:
        return update_item(db, db_question_tag, **question_tag_update.dict(exclude_unset=True))
    return None