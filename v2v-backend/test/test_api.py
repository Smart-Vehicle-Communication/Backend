import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test adding vehicle data
def test_add_vehicle_data():
    response = client.post(
        "/vehicle/",
        json={"vehicle_id": "V123", "latitude": 12.9716, "longitude": 77.5946, "speed": 45.0}
    )
    assert response.status_code == 200
    assert response.json()["vehicle_id"] == "V123"

# Test getting latest vehicle data
def test_get_vehicle_data():
    response = client.get("/vehicle/V123/latest")
    assert response.status_code == 200
    assert len(response.json()) > 0

# Test sending accident alert
def test_send_accident_alert():
    response = client.post(
        "/alert/",
        json={"vehicle_id": "V123", "alert_type": "ACCIDENT", "latitude": 12.9716, "longitude": 77.5946}
    )
    assert response.status_code == 200
    assert response.json()["alert_type"] == "ACCIDENT"

# Test fetching alerts for a vehicle
def test_get_alerts():
    response = client.get("/alert/V123")
    assert response.status_code == 200
    assert len(response.json()) > 0
