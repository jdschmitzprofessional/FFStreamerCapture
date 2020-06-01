import subprocess
import logging


class StreamCamera:
    def __init__(self,
                 config=dict,
                 destination=str):
        self.resolution = config['resolution'].lower().split("x")
        self.bitrate = config['bitrate']
        self.destination = destination
        self.port = config['port']
        self.framerate = config['framerate']

    def record(self):
            self.execute = "raspivid -ae 14 -a 1036" + \
                       " -t 0" + \
                       " -w " + str(self.resolution[0]) + \
                       " -h " + str(self.resolution[1]) + \
                       " -ih" + \
                       " -b " + self.bitrate + \
                       " -sh 100" + \
                       " --framerate " + str(self.framerate) + \
                       " -o udp://" + self.destination + ":" + str(self.port)
            subprocess.call(self.execute, shell=True)