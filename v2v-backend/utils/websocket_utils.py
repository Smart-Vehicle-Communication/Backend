from database import SessionLocal
from models import Vehicle
from sqlalchemy import func

async def get_vehicle_data_for_websocket():
    """Get vehicle data to send via WebSocket."""
    db = SessionLocal()
    vehicles = db.query(Vehicle).all()
    vehicle_data = []
    
    for vehicle in vehicles:
        vehicle_data.append({
            "vehicle_id": vehicle.vehicle_id,
            "speed": vehicle.speed,
            "location": {"lat": vehicle.latitude, "lng": vehicle.longitude}
        })
    
    db.close()
    return vehicle_data
