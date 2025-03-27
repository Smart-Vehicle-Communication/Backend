from sqlalchemy import Column, String, Float, Integer, DateTime
from database import Base
from datetime import datetime

# Vehicle data model
class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Alert data model
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String, index=True)
    alert_type = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
