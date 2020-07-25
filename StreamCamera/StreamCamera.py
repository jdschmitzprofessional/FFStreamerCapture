import subprocess
import time
from datetime import datetime as dt


class StreamCamera:
    def __init__(self,
                 config: dict):
        self.resolution: list[int] = config['resolution'].lower().split("x")
        self.bit_rate: str = config['bit_rate']
        self.destination: str = config['mount_path']
        self.frame_rate: int = config['frame_rate']
        self.start_time: str = dt.now().strftime('%Y-%m-%d-%H-%M-%S')

    def record(self):
        self.start_time = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.execute = f"raspivid -ae 14 -a 1036 \
                        -t 0 \
                        -w {self.resolution[0]} \
                        -h {self.resolution[1]} \
                        -ih \
                        --framerate {self.frame_rate} \
                        -o /mnt/storage/{self.start_time}.h264"
        try:
            subprocess.check_call(self.execute, shell=True)
        except subprocess.CalledProcessError:
            time.sleep(3)
        try:
            self.execute = f"mv {self.start_time}.h264 {self.start_time}.h264.finished"
            subprocess.check_call(self.execute, shell=True)
        except subprocess.CalledProcessError:
            pass
        ## will add logging