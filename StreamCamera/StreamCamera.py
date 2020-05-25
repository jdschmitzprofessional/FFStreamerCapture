import subprocess
import time


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
        # construct string to pass to StreamCamera, initializes stream to central server.
        while True:
            self.execute = "raspivid -a 12" + \
                       " -t 0" + \
                       " -w " + str(self.resolution[0]) + \
                       " -h " + str(self.resolution[1]) + \
                       " -ih" + \
                       " -fps " + self.framerate + \
                       " -o udp://" + self.destination + ":" + str(self.port)
            subprocess.call(self.execute, shell=True)
            time.sleep(5)