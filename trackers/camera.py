from .tracker import Tracker
import cv2

class UserPresentTracker(Tracker):

    def __init__(self, interval_seconds=1, camera_device='/dev/video1'):
        super().__init__(interval_seconds)
        self.camera_device = camera_device
        self.cap = None
        self.metric = 'duration_at_computer'
        self.duration_at_computer = 0

        # Try to initialize the camera
        self.initialize_camera()

        # Load the pre-trained DNN model
        prototxt_path = 'resources/deploy.prototxt'
        caffemodel_path = 'resources/res10_300x300_ssd_iter_140000.caffemodel'
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

    def initialize_camera(self):
        # List of camera devices to try if the given one fails
        camera_devices = [self.camera_device] + ['/dev/video{}'.format(i) for i in range(5)]  # Adjust range as needed

        for device in camera_devices:
            self.cap = cv2.VideoCapture(device)
            if self.cap.isOpened():
                ret, _ = self.cap.read()
                if ret:
                    print(f"Camera initialized with device: {device}")
                    return
                else:
                    self.cap.release()
            print(f"Failed to initialize camera with device: {device}")

        raise Exception("Could not find a working camera device.")

    def __del__(self):
        # Release the capture when the object is destroyed
        if self.cap:
            self.cap.release()

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
