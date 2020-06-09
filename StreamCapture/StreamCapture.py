import subprocess
from datetime import datetime as dt
import logging

class CaptureStream:
    def __init__(self, listen=str, config=dict):
        ### name of the camera
        self.name = config['name']
        ### address to listen from (remote camera)
        self.address = listen
        ### port to listen on
        self.sourceport = config['port']
        ### set the transfer bitrate
        self.bitrate = config['bitrate']
        ### set the framerate to force synchronicity
        self.framerate = config['framerate']
        ### empty string initialization, populates in capture method
        self.execute = str
        ### port to restream on. Calculates arbitrarily if not provided.
        self.logger = logging.getLogger("FFStreamerCapture." + self.name + ".capture")
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("\"Instantiated Stream Capture\"")
        try:
            self.restream_port = config['restream_port']
        except KeyError:
            self.restream_port = self.sourceport + 200
        ### address to restream to. Uses same as input address if not provided.
        try:
            self.restream_address = config['restream_address']
        except KeyError:
            self.restream_address = self.address

    def capture(self):
        while True:
            startTime = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
            execute = "ffmpeg" + \
                      " -i \"tcp://" + self.address + ":" + str(self.sourceport) + "?listen\"" + \
                      " -c:v copy" + \
                      " -t 300 " + \
                      " /tmp/" + self.name + "/" + startTime + ".h264" + \
                      " -c:v copy" + \
                      " -t 290 " + \
                      " -f h264 udp://" + self.restream_address + ":" + str(self.restream_port)
            print(execute)
            subprocess.call(execute, shell=True)
            reprocess = "mv -v /tmp/" + self.name + "/" + startTime + ".h264 /tmp/" + self.name + "/" + startTime + ".h264.finished"
            subprocess.call(reprocess, shell=True)



