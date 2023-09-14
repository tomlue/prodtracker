import pandas as pd
import sqlite3
from datetime import datetime
from config import socketio

DB_NAME = "metrics.db"

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            timestamp TEXT,
            metric TEXT,
            value REAL,
            unit TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_metric(metric, value, unit="seconds"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO metrics (timestamp, metric, value, unit) VALUES (?, ?, ?, ?)", (timestamp, metric, value, unit))
    
    conn.commit()
    conn.close()
    
    if socketio is None:
        return None
    
    # After data insertion
    new_data = {
        'timestamp': timestamp,
        'metric': metric,
        'value': value,
        'unit': unit
    }
    socketio.emit('new_data_inserted', new_data)

def fetch_all_metrics():
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT timestamp, metric, value, unit FROM metrics"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
