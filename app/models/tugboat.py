from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Tugboat(Base):
    __tablename__ = "tugboats"

    mmsi = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
