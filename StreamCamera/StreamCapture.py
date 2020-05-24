import subprocess
import time
from datetime import datetime as dt


class CaptureStream:
    def __init__(self, root=str,config=dict):
            self.name = config['name']
            self.functional_root = root
            self.remoteuser = config['user']
            self.sourceaddress = config['address']
            self.sourceport = config['port']
            self.retrievalmethod = config['retrieval_method']
            self.sshkey = config['keyfile']
            self.savefolder = config['savefolder']
            self.configpath = config['configpath']
            self.sdp = str
            self.execute = str
            self.retreiveconfig = str

    def configure(self):
        self.sdp = self.functional_root + "/" + self.name + ".sdp"
        print(self.sdp)
        retreiveconfig = "scp -i " + self.sshkey + " " + \
                                self.remoteuser + "@" + self.sourceaddress + ":" + \
                                self.configpath + " " + \
                                self.sdp
        try:
            subprocess.call(retreiveconfig, shell=True)
        except Exception as e:
            print(e)

    def capture(self):

        while True:
            execute = "ffmpeg -protocol_whitelist rtp,udp,file" + \
                        " -i " + self.sdp + \
                        " -t 600 " + \
                        " -vf \"drawtext=text='timestamp: %{pts\:gmtime\:" + str(int(time.time()) - 25200) + "\:%Y\-%m\-%d %H\-%M\-%S}:x=60:y=34:fontsize=20:fontcolor=0xffffff7f'\"" + \
                        " " + self.savefolder + "/" + dt.now().strftime('%Y-%m-%d-%H-%M-%S')  + ".mkv"
            print(execute)
            subprocess.call(execute,shell=True)

    def getConfig(self):
        return self.__dict__

