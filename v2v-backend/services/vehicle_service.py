from utils.gps_utils import calculate_distance
from crud import get_latest_vehicle_data
from sqlalchemy.orm import Session

# Check if a vehicle is within 2 km range of another vehicle
def is_vehicle_in_range(db: Session, vehicle_id: str, target_lat: float, target_lon: float, max_distance_km: float = 2.0):
    vehicle_data = get_latest_vehicle_data(db, vehicle_id)
    if not vehicle_data:
        return False

    for record in vehicle_data:
        distance = calculate_distance(target_lat, target_lon, record.latitude, record.longitude)
        if distance <= max_distance_km:
            return True
    return False

# Monitor vehicle speed and return speed status
def check_speed_compliance(speed: float, speed_limit: float = 80.0):
    if speed <= speed_limit:
        return {"status": "Within limit", "speed": speed}
    else:
        return {"status": "Over speed!", "speed": speed}
