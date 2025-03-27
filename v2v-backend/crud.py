from database import SessionLocal
from models import Vehicle, Alert
from sqlalchemy.sql import func

# Maximum records to store
MAX_VEHICLE_RECORDS = 100
MAX_ALERT_RECORDS = 100

async def update_vehicle_data_in_db(vehicle_data):
    """Update vehicle data and maintain only the latest 100 records."""
    db = SessionLocal()
    vehicle_id = vehicle_data["vehicle_id"]
    
    # Check if vehicle already exists
    existing_vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()

    if existing_vehicle:
        existing_vehicle.speed = vehicle_data["speed"]
        existing_vehicle.lat = vehicle_data["location"]["lat"]
        existing_vehicle.lng = vehicle_data["location"]["lng"]
    else:
        new_vehicle = Vehicle(
            vehicle_id=vehicle_data["vehicle_id"],
            speed=vehicle_data["speed"],
            lat=vehicle_data["location"]["lat"],
            lng=vehicle_data["location"]["lng"]
        )
        db.add(new_vehicle)

    db.commit()

    # ✅ Call cleanup to keep only recent 100 records
    await cleanup_old_vehicle_data(db)
    db.close()

async def save_alert_to_db(alert_data):
    """Save an alert and maintain only the latest 100 alerts."""
    db = SessionLocal()
    new_alert = Alert(
        vehicle_id=alert_data["vehicle_id"],
        alert_type=alert_data["alert_type"],
        latitude=alert_data["latitude"],
        longitude=alert_data["longitude"],
    )
    db.add(new_alert)
    db.commit()

    # ✅ Call cleanup to keep only recent 100 alerts
    await cleanup_old_alert_data(db)
    db.close()

async def cleanup_old_vehicle_data(db):
    """Delete old vehicle records beyond the latest 100."""
    vehicle_count = db.query(Vehicle).count()
    if vehicle_count > MAX_VEHICLE_RECORDS:
        oldest_vehicles = (
            db.query(Vehicle)
            .order_by(Vehicle.timestamp.asc())
            .limit(vehicle_count - MAX_VEHICLE_RECORDS)
            .all()
        )
        for vehicle in oldest_vehicles:
            db.delete(vehicle)
        db.commit()

async def cleanup_old_alert_data(db):
    """Delete old alert records beyond the latest 100."""
    alert_count = db.query(Alert).count()
    if alert_count > MAX_ALERT_RECORDS:
        oldest_alerts = (
            db.query(Alert)
            .order_by(Alert.timestamp.asc())
            .limit(alert_count - MAX_ALERT_RECORDS)
            .all()
        )
        for alert in oldest_alerts:
            db.delete(alert)
        db.commit()
