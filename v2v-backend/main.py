# main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Vehicle, Alert, Base
from routers import ws
from mqtt_subscriber import start_mqtt
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or specify your frontend URL e.g., "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all vehicle data
@app.get("/vehicles/")
def get_vehicles(db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).all()
    return {"vehicles": vehicles}

# Get a vehicle by ID
@app.get("/vehicles/{vehicle_id}")
def get_vehicle_by_id(vehicle_id: str, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).all()
    return {"vehicle": vehicle}

@app.get("/")
def read_root():
    return {"message": "Vehicle Tracking System Running!"}

# Include WebSocket router
app.include_router(ws.router, prefix="")

# Start MQTT Subscriber on App Startup
@app.on_event("startup")
def startup_event():
    start_mqtt()
