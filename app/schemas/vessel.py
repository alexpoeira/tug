from pydantic import BaseModel
from typing import Optional

class VesselRead(BaseModel):
    id: int
    imo: int
    mmsi: int
    name: str
    type: str
    callsign: Optional[str] = None
    subtype: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
