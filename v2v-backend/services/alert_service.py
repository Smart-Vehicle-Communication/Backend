from crud import create_alert
from schemas import AlertCreate
from sqlalchemy.orm import Session

# Generate an accident alert for a vehicle
def trigger_accident_alert(db: Session, vehicle_id: str, lat: float, lon: float):
    alert_data = AlertCreate(
        vehicle_id=vehicle_id,
        alert_type="Accident",
        latitude=lat,
        longitude=lon
    )
    return create_alert(db, alert_data)

# Generate an SOS alert for a vehicle
def trigger_sos_alert(db: Session, vehicle_id: str, lat: float, lon: float):
    alert_data = AlertCreate(
        vehicle_id=vehicle_id,
        alert_type="SOS",
        latitude=lat,
        longitude=lon
    )
    return create_alert(db, alert_data)

# Check if accident or SOS alert needs to be triggered
def handle_alert_conditions(db: Session, vehicle_id: str, lat: float, lon: float, is_accident: bool = False, is_sos: bool = False):
    if is_accident:
        return trigger_accident_alert(db, vehicle_id, lat, lon)
    elif is_sos:
        return trigger_sos_alert(db, vehicle_id, lat, lon)
    return {"status": "No alert triggered"}
