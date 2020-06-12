import subprocess
import logging
import time


class StreamCamera:
    def __init__(self,
                 config=dict,
                 destination=str):
        self.resolution = config['resolution'].lower().split("x")
        self.bitrate = config['bit_rate']
        self.destination = destination
        self.port = config['port']
        self.framerate = config['framerate']

    def record(self):
            self.execute = "raspivid -ae 14 -a 1036" + \
                       " -t 0" + \
                       " -w " + str(self.resolution[0]) + \
                       " -h " + str(self.resolution[1]) + \
                       " -ih" + \
                       " --framerate " + str(self.framerate) + \
                       " -o tcp://" + self.destination + ":" + str(self.port)
            try:
                subprocess.check_call(self.execute, shell=True)
            except subprocess.CalledProcessError:
                time.sleep(3)