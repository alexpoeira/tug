from sqlalchemy import Column, Integer, DateTime, ForeignKey, Table
from app.db.database import Base

tug_job_tugboats = Table(
    "tug_job_tugboats",
    Base.metadata,
    Column("tug_job_id", Integer, ForeignKey("tug_jobs.id")),
    Column("tugboat_mmsi", Integer, ForeignKey("tugboats.mmsi")),
)

class TugJob(Base):
    __tablename__ = "tug_jobs"

    id = Column(Integer, primary_key=True, index=True)

    vessel_imo = Column(Integer, ForeignKey("vessels.imo"))

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
