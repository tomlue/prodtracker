from .tracker import Tracker
from pynput import keyboard
import threading

class KeyboardTracker(Tracker):
    
    def __init__(self, interval_seconds=0.5):
        super().__init__(interval_seconds)
        self.keys_pressed = 0
        self.metric = 'keys_pressed'
        self.listener = None

    def on_press(self, key):
        self.keys_pressed += 1
        
    def update_metrics(self):
        newpressed = self.keys_pressed
        self.keys_pressed = 0
        return (self.metric, newpressed)
            
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
