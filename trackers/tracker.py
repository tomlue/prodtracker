import cv2
import time
from pynput import keyboard
from datetime import datetime
import threading
from datastore import insert_metric

class Tracker:
    
    def __init__(self, interval_seconds=0.5):
        self.interval_seconds = interval_seconds
    
    def update_metrics(self):
        "return a tuple of (metric, value)"
        pass
    
    def write_to_db(self):
        metric, value = self.update_metrics()
        insert_metric(metric, value)
    
    def setup(self):
        "setup the tracker"
        pass
    
    def teardown(self):
        "teardown the tracker"
        pass
                
    def start(self):
        self.setup()
        try:
            while True:
                time.sleep(self.interval_seconds)
                self.write_to_db()
        except KeyboardInterrupt:
            self.teardown()
            