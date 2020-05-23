import subprocess
import ipaddress



class StreamCamera:
    def __init__(self, inputdevice=str,
                 resolution=str,
                 aspectratio=str,
                 destination=str,
                 port=int,
                 framerate=int,
                 inputcodec=str,
                 outputcodec=str):
        self.inputdevice=inputdevice
        self.resolution=resolution
        self.aspectratio=aspectratio
        self.destination=destination
        self.port=port
        self.framerate=framerate
        self.inputcodec=inputcodec
        self.outputcodec=outputcodec

    def record(self):
        self.execute = "ffmpeg -f " + self.inputcodec + \
            " -s " + self.resolution + \
            " -r " + str(self.framerate) + \
            " -i " + self.inputdevice + \
            " -c:v " + self.outputcodec + \
            " -f mpegts udp://" + self.destination + ":" + str(self.port)
        subprocess.call(self.execute, shell=True)