import pandas as pd
import sqlite3
import threading
from datetime import datetime
from config import socketio

DB_NAME = "metrics.db"
DB_LOCK = threading.Lock()

def with_db_lock(func):
    def wrapper(*args, **kwargs):
        with DB_LOCK:
            return func(*args, **kwargs)
    return wrapper


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

@with_db_lock
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

@with_db_lock
def fetch_all_metrics(timestamp=datetime.now().strftime('%Y-%m-%d 00:00:00')):
    conn = sqlite3.connect(DB_NAME)
    end_timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d 23:59:59')
    query = f"SELECT timestamp, metric, value, unit FROM metrics WHERE timestamp > '{timestamp}' AND timestamp < '{end_timestamp}'"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
