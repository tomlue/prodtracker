from trackers.tracker import Tracker
import time
import subprocess
import openai
import pathlib
import dotenv
import os
import structlog
import base64

dotenv.load_dotenv()    
imagedir = pathlib.Path(os.getenv('bucketpath')) / 'trackers' / 'window' / 'screenshots'
imagedir.mkdir(parents=True, exist_ok=True)
oaclient = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class ActiveWindowTracker(Tracker):

    def __init__(self, interval_seconds=10):
        super().__init__(interval_seconds)
        self.metric = 'active_window'
        self.windows_with_subwindows = {"chrome"}
        self.active_window = ''
        self.log = structlog.get_logger().bind(tracker=self.__class__.__name__)

    def _window_screenshot(self, window_id):
        outpath = imagedir / f"{int(time.time())}_{window_id}.jpeg"
        subprocess.run(f'import -window {hex(int(window_id))} -quality 85 -silent {outpath}', shell=True)
        return outpath
    
    # Function to encode the image
    def _encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    async def _llm_evaluation(self, active_window_image_path):
        active_window_image_path = next(imagedir.glob('*.png'))
        base64_image = self._encode_image(active_window_image_path)
        response = oaclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "What is in this image?",
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url":  f"data:image/jpeg;base64,{base64_image}"
                    },
                    },
                ],
                }
            ],
            )
        return response.choices[0].message.content


    def update_metrics(self):
        window_id = subprocess.check_output(["xdotool", "getactivewindow"]).decode("utf-8").strip()
        # window_title = subprocess.check_output(["xdotool", "getwindowname", window_id]).decode("utf-8").strip()
        # window_pid = subprocess.check_output(["xdotool", "getwindowpid", window_id]).decode("utf-8").strip()
        # window_ps = subprocess.check_output(["ps", "-p", window_pid, "-o", "comm="]).decode("utf-8").strip()
        # self.log.info("window_update", window_id=window_id, title=window_title, process=window_ps)
        self._window_screenshot(window_id)
        self.log.info("window_update", window_id=window_id)
        return (self.metric, "test")

    def setup(self):
        pass
    
    def teardown(self):
        pass

# example usage
aw = ActiveWindowTracker()
aw.update_metrics()
