import subprocess
from datetime import datetime as dt

class CaptureStream:
    def __init__(self, root=str, listen=str, config=dict):
        self.name = config['name']
        self.address = listen
        self.functional_root = root
        self.sourceport = config['port']
        self.savefolder = config['savefolder']
        self.execute = str

    def capture(self):
        while True:
            execute = "ffmpeg" + \
                      " -hwaccel vaapi -hwaccel_output_format vaapi -hwaccel_device /dev/dri/by-path/pci-0000\:13\:00.0-render" + \
                      " -i udp://" + self.address + ":" + str(self.sourceport) + \
                      " -c:v h264_vaapi -b:v 100K " + \
                      " -t 600 -r 30 " + \
                      self.savefolder + "/" + dt.now().strftime('%Y-%m-%d-%H-%M-%S') + ".mp4"
            print(execute)
            subprocess.call(execute, shell=True)

    def getConfig(self):
        return self.__dict
