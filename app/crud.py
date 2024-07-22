from sqlalchemy.orm import Session
from app import models, schemas


def get_item(db: Session, item_id: int):
    return db.query(models.ToDoItem).filter(models.ToDoItem.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ToDoItem).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ToDoItemCreate):
    db_item = models.ToDoItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: schemas.ToDoItemCreate):
    db_item = get_item(db, item_id)
    if db_item:
        db_item.title = item.title
        db_item.description = item.description
        db_item.completed = item.completed
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item