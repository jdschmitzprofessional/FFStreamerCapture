import json
import logging
import time
from datetime import datetime as dt
import picamera


class StreamCamera:
    def __init__(self,
                 config: dict):
        self.camera_name = config['name']
        self.resolution: list[int] = config['resolution'].lower().split("x")
        self.bit_rate: str = config['bit_rate']
        self.mount_path: str = config['mount_path']
        self.frame_rate: int = config['frame_rate']
        self.start_time: str = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.loop_duration = config['loop_duration']
        self.logout: dict[str, str] = {}
        self.logger = logging.getLogger("FFStreamerCapture." + self.camera_name + ".post")
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("\"Instantiated Stream Processor\"")

    def record(self):
        with picamera.PiCamera() as camera:
            while True:
                camera.annotate_background = picamera.Color("black")
                start = dt.now()
                self.logout['hostname'] = self.camera_name
                self.logout['start'] = str(time.time())
                self.logout['start_long'] = dt.now().strftime("%H:%M:%S %D")
                self.logout['resolution'] = str(self.resolution)[1:-1]
                camera.start_preview()
                filename = f"/mnt/storage/{dt.now().strftime('%Y-%m-%d-%H-%M-%S')}.h264"
                self.logout['file'] = filename
                try:
                    camera.start_recording(str(filename))
                    while (dt.now() - start).seconds < self.loop_duration:
                        camera.annotate_text = dt.now().strftime("%H:%M:%S %D")
                        camera.wait_recording(0.2)
                    self.logout['stop'] = str(time.time())
                    self.logout['stop_long'] = dt.now().strftime("%H:%M:%S %D")
                    self.logger.info(json.dumps(self.logout))
                except Exception as e:
                    self.logout['Exception'] = str(e)
                    self.logger.critical(json.dumps(self.logout))
