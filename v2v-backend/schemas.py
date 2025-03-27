from pydantic import BaseModel
from datetime import datetime

# Vehicle Schema
class VehicleBase(BaseModel):
    vehicle_id: str
    latitude: float
    longitude: float
    speed: float

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# Alert Schema
class AlertBase(BaseModel):
    vehicle_id: str
    alert_type: str
    latitude: float
    longitude: float

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
