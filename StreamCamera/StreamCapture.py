import subprocess
import time
from datetime import datetime as dt


class CaptureStream:
    def __init__(self, sourceaddress=str, sourceport=int, retrievalmethod=str,sshkey=str, savefolder=str, remoteuser=str):
        self.remoteuser=remoteuser
        self.sourceaddress=sourceaddress
        self.sourceport = sourceport
        self.execute = str
        self.retrievalmethod = retrievalmethod
        self.retreiveconfig = str
        self.sdp = str
        self.sshkey = sshkey
        self.savefolder=savefolder
    def configure(self, filepath, filedest):
        self.sdp = filedest
        retreiveconfig = "scp -i " + self.sshkey + " " + \
                                self.remoteuser + "@" + self.sourceaddress + ":" + \
                                filepath + " " + \
                                filedest
        try:
            subprocess.call(retreiveconfig, shell=True)
        except Exception as e:
            print(e)

    def capture(self):
        if type(self.sdp) != str:
            print("Please configure first.")
            return False
        while True:
            execute = "ffmpeg -protocol_whitelist rtp,udp,file" + \
                        " -i " + self.sdp + \
                        " -t 600 " + \
                        " -vf \"drawtext=text='timestamp: %{pts\:gmtime\:" + str(int(time.time()) - 25200) + "\:%Y\-%m\-%d %H\-%M\-%S}:x=60:y=34:fontsize=20:fontcolor=0xffffff7f'\"" + \
                        " " + self.savefolder + "/" + dt.now().strftime('%Y-%m-%d-%H-%M-%S')  + ".mkv"
            print(execute)
            subprocess.call(execute,shell=True)


