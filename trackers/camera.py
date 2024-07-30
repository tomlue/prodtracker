from .tracker import Tracker
import cv2

class UserPresentTracker(Tracker):

    def __init__(self, interval_seconds=1, camera_device='/dev/video2'):
        super().__init__(interval_seconds)
        self.cap = cv2.VideoCapture(camera_device)
        self.metric = 'duration_at_computer'
        self.duration_at_computer = 0

        # Load the pre-trained DNN model
        prototxt_path = 'resources/deploy.prototxt'
        caffemodel_path = 'resources/res10_300x300_ssd_iter_140000.caffemodel'
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

    def update_metrics(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            return (self.metric, 0)

        # Prepare the frame for DNN input
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

        # Pass the blob through the network and obtain the detections
        self.net.setInput(blob)
        detections = self.net.forward()

        faces = 0
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Confidence threshold
                faces += 1

        print(f'There are {faces} faces')
        duration = self.interval_seconds if faces != 0 else 0
        return (self.metric, duration)