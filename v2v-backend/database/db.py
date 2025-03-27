# database/db.py

import sqlite3
from config.config import DB_FILE

def create_db():
    """Initialize database and create vehicle_data table if not exists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicle_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT,
            latitude REAL,
            longitude REAL,
            speed REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_vehicle_data(vehicle_id, latitude, longitude, speed):
    """Insert vehicle data into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO vehicle_data (vehicle_id, latitude, longitude, speed)
        VALUES (?, ?, ?, ?)
    ''', (vehicle_id, latitude, longitude, speed))
    
    conn.commit()
    conn.close()
