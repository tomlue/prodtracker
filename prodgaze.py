import cv2
import time
from pynput import keyboard
from datetime import datetime
import threading

class Tracker:
    
    def __init__(self, filename, lock, interval_seconds=0.5):
        self.filename = filename
        self.lock = lock
        self.interval_seconds = interval_seconds
    
    def update_metrics(self):
        "return a tuple of (metric, value)"
        pass
    
    def write_to_file(self):
        metric, value = self.update_metrics()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self.lock:
            with open(self.filename, 'a') as f:
                f.write(f"{current_time}, {metric}, {value}\n")
    
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
                self.write_to_file()
        except KeyboardInterrupt:
            self.teardown()
            
class UserPresentTracker(Tracker):
    
    def __init__(self, filename, lock, interval_seconds=0.5):
        super().__init__(filename, lock)
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.metric = 'duration_at_computer'
        self.duration_at_computer = 0

    def update_metrics(self):
        _, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) != 0:
            self.duration_at_computer += self.interval_seconds
        return (self.metric, self.duration_at_computer)

class KeyboardTracker(Tracker):
    
    def __init__(self, filename, lock, interval_seconds=0.5):
        super().__init__(filename, lock, interval_seconds)
        self.keys_pressed = 0
        self.metric = 'keys_pressed'
        self.listener = None

    def on_press(self, key):
        self.keys_pressed += 1
        
    def update_metrics(self):
        return (self.metric, self.keys_pressed)
            
    def keyboard_listener(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            self.listener = listener
            listener.join()
            
    def setup(self):
        self.keyboard_thread = threading.Thread(target=self.keyboard_listener)
        self.keyboard_thread.start()
    
    def teardown(self):
        if self.listener is not None:
            self.listener.stop()
        if self.keyboard_thread is not None:
            self.keyboard_thread.join()

# Initialize file lock and trackers
lock = threading.Lock()
user_present_tracker = UserPresentTracker('metrics.txt', lock)
keyboard_tracker = KeyboardTracker('metrics.txt', lock)

# Start tracking in separate threads
user_present_thread = threading.Thread(target=user_present_tracker.start)
keyboard_thread = threading.Thread(target=keyboard_tracker.start)

user_present_thread.start()
keyboard_thread.start()

try:
    user_present_thread.join()
    keyboard_thread.join()
except KeyboardInterrupt:
    user_present_tracker.teardown()
    keyboard_tracker.teardown()