import asyncio
import websockets
import json
import pytest

# URL for WebSocket connection
URL = "ws://localhost:8000/ws"

# Test WebSocket connection and broadcast
@pytest.mark.asyncio
async def test_websocket_connection():
    async with websockets.connect(URL) as websocket:
        # Send test data
        message = {"vehicle_id": "V123", "latitude": 12.9716, "longitude": 77.5946, "speed": 45.0}
        await websocket.send(json.dumps(message))

        # Receive and validate response
        response = await websocket.recv()
        data = json.loads(response)
        assert data["vehicle_id"] == "V123"
        assert data["speed"] == 45.0
