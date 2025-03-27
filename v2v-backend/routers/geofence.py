from fastapi import APIRouter

router = APIRouter(prefix="/geofence", tags=["Geofence"])

# Check geofence status
@router.get("/status")
def geofence_status():
    return {"status": "Geofencing Active"}

# Add geofencing logic here (coming soon!)
