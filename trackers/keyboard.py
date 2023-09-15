from .tracker import Tracker
from pynput import keyboard, mouse
import threading

class InputTracker(Tracker):

    def __init__(self, interval_seconds=0.5):
        super().__init__(interval_seconds)
        self.keys_pressed = 0
        self.clicks = 0
        self.keyboard_listener = None
        self.mouse_listener = None
        self.keyboard_thread = None
        self.mouse_thread = None

    def on_key_press(self, key):
        self.keys_pressed += 1

    def on_click(self, x, y, button, pressed):
        if pressed:  # Only count when mouse button is pressed down
            self.clicks += 1

    def update_metrics(self):
        newpressed = self.keys_pressed
        newclicks = self.clicks
        self.keys_pressed = 0
        self.clicks = 0
        return {"keys_pressed": newpressed, "mouse_clicks": newclicks}

    def keyboard_listener_func(self):
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            self.keyboard_listener = listener
            listener.join()

    def mouse_listener_func(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            self.mouse_listener = listener
            listener.join()

    def setup(self):
        self.keyboard_thread = threading.Thread(target=self.keyboard_listener_func)
        self.mouse_thread = threading.Thread(target=self.mouse_listener_func)
        
        self.keyboard_thread.start()
        self.mouse_thread.start()

    def teardown(self):
        if self.keyboard_listener is not None:
            self.keyboard_listener.stop()
        if self.keyboard_thread is not None:
            self.keyboard_thread.join()
        
        if self.mouse_listener is not None:
            self.mouse_listener.stop()
        if self.mouse_thread is not None:
            self.mouse_thread.join()
