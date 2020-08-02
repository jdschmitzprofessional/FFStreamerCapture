import json
import logging
import time
from datetime import datetime as dt
import subprocess
import picamera
import constants


class StreamCamera:
    def __init__(self,
                 config: dict):
        self.camera_name = config['name']
        self.resolution: list[int] = config['resolution'].lower().split("x")
        self.bit_rate: str = config['bit_rate']
        self.mount_path: str = config['mount_path']
        self.frame_rate: int = config['frame_rate']
        self.start_time: str = dt.now().strftime(constants.date_format)
        self.loop_duration: int = config['loop_duration']
        self.logout: dict[str, str] = {}
        self.logger = logging.getLogger("FFStreamerCapture." + self.camera_name + ".post")
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("\"Instantiated Remote Camera\"")

    def record(self):
        with picamera.PiCamera() as camera:
            camera.annotate_background = picamera.Color("black")
            self.logout['hostname'] = self.camera_name
            self.logout['resolution'] = str(self.resolution)[1:-1]
            self.logout['start'] = str(time.time())
            self.logout['start_long'] = dt.now().strftime(constants.short_date_format)

            try:
                filename = f"/mnt/storage/{dt.now().strftime(constants.date_format)}.h264"
                self.logout['file'] = filename
                camera.start_recording(str(filename))
                while True:
                    while time.time() - float(self.logout['start']) <= self.loop_duration:
                        camera.annotate_text = dt.now().strftime(constants.short_date_format)
                        self.logout['stop'] = str(time.time())
                        self.logout['stop_long'] = dt.now().strftime(constants.short_date_format)
                        self.logger.info(json.dumps(self.logout))
                        self.logout['start'] = str(time.time())
                        self.logout['start_long'] = dt.now().strftime(constants.short_date_format)
                        old_filename = filename
                        filename = f"/mnt/storage/{dt.now().strftime(constants.date_format)}.h264"
                        self.logout['file'] = filename
                        camera.split_recording(filename)
                        try:
                            subprocess.call(f"mv {old_filename} {old_filename}.finished", shell=True)
                        except subprocess.CalledProcessError as e:
                            self.logout['Exception'] = str(e)
                            self.logger.warning(json.dumps(self.logout))
            except Exception as e:
                self.logout['Exception'] = str(e)
                self.logger.critical(json.dumps(self.logout))
                camera.stop_recording()
                return False


