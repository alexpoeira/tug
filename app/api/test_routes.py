from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.test import TestCreate, TestOut, TestUpdate
from app.crud.test import (
    create_test,
    get_test,
    get_tests,
    update_test,
    delete_test,
)
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=TestOut)
def create_test_route(test_data: TestCreate, db: Session = Depends(get_db)):
    return create_test(db, test_data)

@router.get("/", response_model=list[TestOut])
def list_tests(db: Session = Depends(get_db)):
    return get_tests(db)

@router.get("/{test_id}", response_model=TestOut)
def read_single_test(test_id: int, db: Session = Depends(get_db)):
    test = get_test(db, test_id)
    if not test:
        raise HTTPException(404, "Test not found")
    return test

@router.put("/{test_id}", response_model=TestOut)
def update_test_route(test_id: int, updates: TestUpdate, db: Session = Depends(get_db)):
    updated = update_test(db, test_id, updates)
    if not updated:
        raise HTTPException(404, "Test not found")
    return updated

@router.delete("/{test_id}")
def delete_test_route(test_id: int, db: Session = Depends(get_db)):
    deleted = delete_test(db, test_id)
    if not deleted:
        raise HTTPException(404, "Test not found")
    return {"message": "Deleted"}
