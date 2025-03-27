# mqtt_subscriber.py

import paho.mqtt.client as mqtt
import json
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Vehicle
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

def on_connect(client, userdata, flags, rc):
    """ Callback when the MQTT client connects to the broker. """
    if rc == 0:
        print(f"Connected to MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    """ Callback when an MQTT message is received. """
    try:
        data = json.loads(msg.payload.decode())

        vehicle_id = data["vehicle_id"]
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])
        speed = float(data["speed"])

        # Store data in DB using SQLAlchemy
        db = SessionLocal()
        vehicle_entry = Vehicle(
            vehicle_id=vehicle_id, latitude=latitude, longitude=longitude, speed=speed
        )
        db.add(vehicle_entry)
        db.commit()
        db.close()

        print(f"Stored in DB: {data}")

    except Exception as e:
        print(f"Error processing message: {e}")

def start_mqtt():
    """ Start MQTT client and listen for messages. """
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
