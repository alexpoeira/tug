from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LocationSchema(BaseModel):
    lat: float
    long: float

class NavigationSchema(BaseModel):
    draught: Optional[float]
    status: Optional[str]
    location: LocationSchema
    speed: Optional[float]
    time: datetime
    course: Optional[float]

class VesselSchema(BaseModel):
    type: str
    callsign: Optional[str]
    subtype: Optional[str]
    imo: int
    name: str

class DeviceSchema(BaseModel):
    mmsi: int

class PositionReportCreate(BaseModel):
    vessel: Optional[VesselSchema]
    navigation: NavigationSchema
    device: DeviceSchema

class PositionReportRead(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    latitude: float
    longitude: float
    speed: float | None
    course: float | None
    navigation_status: str | None
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
