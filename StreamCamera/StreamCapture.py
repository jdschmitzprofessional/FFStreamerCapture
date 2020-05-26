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
                      " -i udp://" + self.address + ":" + str(self.sourceport) + \
                      " -r 30" + \
                      " -c:v copy" + \
                      " -t 600 " + \
                      self.savefolder + "/" + dt.now().strftime('%Y-%m-%d-%H-%M-%S') + ".mkv"
            print(execute)
            subprocess.call(execute, shell=True)

    def getConfig(self):
        return self.__dict
