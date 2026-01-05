from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TestBase(BaseModel):
    name: str
    status: Optional[str] = "pending"
    description: Optional[str] = None

class TestCreate(TestBase):
    pass

class TestUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

class TestOut(TestBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
