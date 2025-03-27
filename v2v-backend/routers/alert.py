from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import create_alert, get_alerts
from schemas import AlertCreate, AlertResponse
from database import SessionLocal

router = APIRouter(prefix="/alerts", tags=["Alerts"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add alert (accident/SOS)
@router.post("/", response_model=AlertResponse)
def add_alert(alert_data: AlertCreate, db: Session = Depends(get_db)):
    return create_alert(db, alert_data)

# Get all alerts for a vehicle
@router.get("/{vehicle_id}", response_model=list[AlertResponse])
def get_alert_data(vehicle_id: str, db: Session = Depends(get_db)):
    alerts = get_alerts(db, vehicle_id)
    if not alerts:
        raise HTTPException(status_code=404, detail="No alerts found for this vehicle")
    return alerts
