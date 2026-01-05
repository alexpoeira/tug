from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Vessel(Base):
    __tablename__ = "vessels"

    id = Column(Integer, primary_key=True, index=True)
    mmsi = Column(String, unique=True, index=True, nullable=False)
    imo = Column(Integer, index=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    subtype = Column(String, nullable=True)
    callsign = Column(String, nullable=True)