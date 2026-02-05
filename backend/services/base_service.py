from sqlalchemy.orm import Session

def get_item_by_id(db: Session, model, item_id: int):
    """Generic function to get an item by ID"""
    return db.query(model).filter(model.id == item_id).first()

def get_items(db: Session, model, skip: int = 0, limit: int = 100):
    """Generic function to get a list of items"""
    return db.query(model).offset(skip).limit(limit).all()

def create_item(db: Session, db_item):
    """Generic function to create an item"""
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, db_item, **kwargs):
    """Generic function to update an item"""
    for key, value in kwargs.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, db_item):
    """Generic function to delete an item"""
    db.delete(db_item)
    db.commit()
    return db_item