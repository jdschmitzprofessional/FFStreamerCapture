import subprocess
from datetime import datetime as dt

class CaptureStream:
    def __init__(self, listen=str, config=dict):
        ### name of the camera
        self.name = config['name']
        ### address to listen from (remote camera)
        self.address = listen
        ### port to listen on
        self.sourceport = config['port']
        ### folder to save files to
        self.savefolder = config['savefolder']
        ### set the transfer bitrate
        self.bitrate = config['bitrate']
        ### set the framerate to force synchronicity
        self.framerate = config['framerate']
        ### empty string initialization, populates in capture method
        self.execute = str
        ### port to restream on. Calculates arbitrarily if not provided.
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
            ### Construct ffmpeg command
            ### hwaccel vaapi... uses vaapi hardware decoding, maps to the pci id for an RX570.
            ### -i udp...   where the stream for this instance is coming from
            ### -c:v h264_vaapi... specifies to use vaapi for re-encoding as well at a bitrate of 1.5Mb/s.
            ### -framerate ... specifies frame to force synchronicity with the remote camera.
            ### self.savefolder... specifies a dynamically named output file.
            ### -c:v copy... options from here are for the re-stream. Specifies to do nothing and just rebroadcast.
            ### -flags global... specifies to include headers on all packets in case something starts in the middle.
            ### -f h264 udp... format to rebroadcast and where to rebroadcast it to.

            execute = "ffmpeg" + \
                      " -hwaccel vaapi -hwaccel_output_format vaapi -hwaccel_device /dev/dri/by-path/pci-0000\:13\:00.0-render" + \
                      " -i udp://" + self.address + ":" + str(self.sourceport) + \
                      " -c:v h264_vaapi -b:v " + self.bitrate + \
                      " -probesize 60M " + \
                      " -t 3600 " + \
                      self.savefolder + "/" + dt.now().strftime('%Y-%m-%d-%H-%M-%S') + ".mp4"
            print(execute)
            subprocess.call(execute, shell=True)