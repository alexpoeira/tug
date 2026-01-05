# app/crud/test.py

from sqlalchemy.orm import Session
from app.models.test import Test
from app.schemas.test import TestCreate, TestUpdate

def create_test(db: Session, test_data: TestCreate):
    db_test = Test(**test_data.model_dump())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

def get_test(db: Session, test_id: int):
    return db.query(Test).filter(Test.id == test_id).first()

def get_tests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Test).offset(skip).limit(limit).all()

def update_test(db: Session, test_id: int, updates: TestUpdate):
    db_test = get_test(db, test_id)
    if not db_test:
        return None

    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_test, key, value)

    db.commit()
    db.refresh(db_test)
    return db_test

def delete_test(db: Session, test_id: int):
    db_test = get_test(db, test_id)
    if not db_test:
        return False

    db.delete(db_test)
    db.commit()
    return True
