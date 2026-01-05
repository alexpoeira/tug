from pydantic import BaseModel
from typing import List
from app.schemas.position_report import PositionReportCreate

class PositionReportBatch(BaseModel):
    data: List[PositionReportCreate]
