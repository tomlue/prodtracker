from .tracker import Tracker
import cv2

class UserPresentTracker(Tracker):
    
    def __init__(self, interval_seconds=1):
        super().__init__(interval_seconds)
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.metric = 'duration_at_computer'
        self.duration_at_computer = 0

    def update_metrics(self):
        _, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        duration = self.interval_seconds if len(faces) != 0 else 0
        return (self.metric, duration)