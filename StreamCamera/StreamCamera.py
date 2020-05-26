import subprocess
import logging


class StreamCamera:
    def __init__(self,
                 resolution=str,
                 destination=str,
                 port=int,
                 framerate=int):
        self.resolution = resolution.split('x')
        self.destination = destination
        self.port = port
        self.framerate = framerate

    def record(self):
            self.execute = "raspivid --ae 10,0x00,0x8080FF -a 12" + \
                       " -t 0" + \
                       " -w " + str(self.resolution[0]) + \
                       " -h " + str(self.resolution[1]) + \
                       " -ih" + \
                       " -fps " + str(self.framerate) + \
                       " -o udp://" + self.destination + ":" + str(self.port)
            subprocess.call(self.execute, shell=True)