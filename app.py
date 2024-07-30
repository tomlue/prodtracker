import threading
from flask import Flask, render_template, jsonify
from datastore import initialize_db, fetch_all_metrics
from flask_socketio import emit
import plotly.express as px
import json

from trackers import UserPresentTracker, InputTracker
from config import socketio

def create_app():
    # Initialize SQLite DB
    initialize_db()
    print("Initialized DB")
    
    # Initialize trackers
    user_present_tracker = UserPresentTracker()
    keyboard_tracker = InputTracker()

    # Start tracking in separate threads
    user_present_thread = threading.Thread(target=user_present_tracker.start)
    keyboard_thread = threading.Thread(target=keyboard_tracker.start)

    user_present_thread.start()
    keyboard_thread.start()
    
    return Flask(__name__, static_folder='static', template_folder='templates')

app = create_app()
socketio.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('request_data_sync')
def handle_request_data_sync():
    metrics = fetch_all_metrics().to_dict(orient='records')
    emit('update_data', metrics)


# Instead of the usual app.run()
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0",port=6323)
