from sqlalchemy.orm import Session
from app.models.test import Test
from app.schemas.test import TestCreate

def create_test(db: Session, data: TestCreate):
    test = Test(**data.dict())
    db.add(test)
    db.commit()
    db.refresh(test)
    return test

def get_tests(db: Session):
    return db.query(Test).all()

def get_test(db: Session, test_id: int):
    return db.query(Test).filter(Test.id == test_id).first()
