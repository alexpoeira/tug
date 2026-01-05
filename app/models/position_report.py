from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from app.db.database import Base

class PositionReport(Base):
    __tablename__ = "position_reports"

    id = Column(Integer, primary_key=True, index=True)

    entity_type = Column(String, nullable=False)
    # "vessel" or "tugboat"

    entity_id = Column(Integer, nullable=False)
    # imo if vessel, mmsi if tugboat

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    speed = Column(Float, nullable=True)
    course = Column(Float, nullable=True)

    navigation_status = Column(String, nullable=True)

    timestamp = Column(DateTime(timezone=True), index=True)
