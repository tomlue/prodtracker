from .tracker import Tracker
import cv2
import pygetwindow as gw

class ActiveWindowTracker(Tracker):
    def __init__(self, interval_seconds=1):
        super().__init__(interval_seconds)
        self.metric = 'active_window'
        self.active_window = ''

    def update_metrics(self):
        self.active_window = gw.getActiveWindow()
        window_title = self.active_window.title if self.active_window else 'No active window'
        return (self.metric, window_title)