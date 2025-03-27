import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Vehicle, Alert
from crud import create_vehicle, get_latest_vehicle_data, create_alert, get_alerts
from schemas import VehicleCreate, AlertCreate

# Test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Setup and teardown
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# Test vehicle creation
def test_create_vehicle(test_db):
    vehicle_data = VehicleCreate(vehicle_id="V123", latitude=12.9716, longitude=77.5946, speed=45.0)
    vehicle = create_vehicle(test_db, vehicle_data)
    assert vehicle.vehicle_id == "V123"
    assert vehicle.speed == 45.0

# Test getting latest vehicle data
def test_get_latest_vehicle_data(test_db):
    data = get_latest_vehicle_data(test_db, "V123")
    assert len(data) > 0
    assert data[0].vehicle_id == "V123"

# Test alert creation
def test_create_alert(test_db):
    alert_data = AlertCreate(vehicle_id="V123", alert_type="ACCIDENT", latitude=12.9716, longitude=77.5946)
    alert = create_alert(test_db, alert_data)
    assert alert.alert_type == "ACCIDENT"

# Test fetching alerts
def test_get_alerts(test_db):
    alerts = get_alerts(test_db, "V123")
    assert len(alerts) > 0
    assert alerts[0].vehicle_id == "V123"
