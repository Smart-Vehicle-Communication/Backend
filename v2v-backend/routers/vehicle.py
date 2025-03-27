from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json
from crud import update_vehicle_data_in_db, save_alert_to_db
from utils.websocket_utils import get_vehicle_data_for_websocket

router = APIRouter()

# Store active WebSocket connections
active_connections: List[WebSocket] = []

# Lock to handle connection updates safely
connection_lock = asyncio.Lock()

# Periodic GPS update interval (every 2 seconds)
UPDATE_INTERVAL = 2

async def broadcast_data(data: dict):
    """Send data to all connected clients."""
    disconnected_clients = []
    for connection in active_connections:
        try:
            await connection.send_json(data)
        except Exception:
            disconnected_clients.append(connection)

    # Remove disconnected clients
    async with connection_lock:
        for client in disconnected_clients:
            active_connections.remove(client)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connection on /ws."""
    await websocket.accept()
    async with connection_lock:
        active_connections.append(websocket)

    print("🚀 WebSocket connection established. Listening for messages...")

    # Start background task for periodic vehicle data
    vehicle_task = asyncio.create_task(send_vehicle_data_to_clients())

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            # Handle incoming messages from frontend
            if payload.get("type") == "alert":
                await handle_alert(payload)
            elif payload.get("type") == "vehicle_update":
                await handle_vehicle_update(payload)

    except WebSocketDisconnect:
        async with connection_lock:
            active_connections.remove(websocket)
        print("🔌 WebSocket disconnected.")
    
    finally:
        vehicle_task.cancel()

async def handle_alert(payload):
    """Save alert to DB and broadcast it."""
    alert_data = payload["details"]
    print(f"📢 Alert received: {alert_data}")
    
    # Save alert to DB
    await save_alert_to_db(alert_data)
    
    # Broadcast alert to all clients
    await broadcast_data({"type": "alert", "details": alert_data})

async def handle_vehicle_update(payload):
    """Update vehicle data in DB and broadcast update."""
    vehicle_data = payload["data"]
    print(f"🚗 Vehicle update received: {vehicle_data}")

    # Update vehicle data in DB
    await update_vehicle_data_in_db(vehicle_data)
    
    # Broadcast updated vehicle data to all clients
    await broadcast_data({"type": "vehicle_update", "data": vehicle_data})

async def send_vehicle_data_to_clients():
    """Send periodic vehicle data updates to clients."""
    print("✅ send_vehicle_data_to_clients() started...")
    while True:
        vehicle_data = await get_vehicle_data_for_websocket()
        if vehicle_data:
            print(f"🚗 Sending vehicle data: {vehicle_data}")
            await broadcast_data({"type": "vehicle_update", "data": vehicle_data})
        else:
            print("⚠️ No vehicle data available...")
        await asyncio.sleep(UPDATE_INTERVAL)
