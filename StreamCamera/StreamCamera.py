import subprocess
import logging


class StreamCamera:
    def __init__(self,
                 config=dict,
                 destination=str):
        self.resolution = config['resolution']
        self.bitrate = config['bitrate']
        self.destination = destination
        self.port = config['port']
        self.framerate = config['framerate']

    def record(self):
            self.execute = "raspivid -ae 14,0x00,0x00,20,20 -a 12" + \
                       " -t 0" + \
                       " -w " + str(self.resolution[0]) + \
                       " -h " + str(self.resolution[1]) + \
                       " -ih" + \
                       " -b " + self.bitrate + \
                       " -sh 100" + \
                       " --framerate " + str(self.framerate) + \
                       " -o udp://" + self.destination + ":" + str(self.port)
            subprocess.call(self.execute, shell=True)