import subprocess


# class for a remote camera to be streamed from, but do minimal processing. For the raspberry pi,
# requires the installation of h264_omx, which requires building StreamCamera from source. Otherwise
# a raspberry pi zero will cap out at 100% cpu and provide only 6 FPS at 640x480. h264_omx allows
# substantially higher quality with about 15% cpu load, allowing cameras to be deployed in less
# ideal circumstances such as outdoors in the phoenix summer with passive cooling.


class StreamCamera:
    def __init__(self, inputdevice=str,
                 resolution=str,
                 destination=str,
                 port=int,
                 framerate=int,
                 inputcodec=str,
                 outputcodec=str):
        self.inputdevice = inputdevice
        self.resolution = resolution
        self.destination = destination
        self.port = port
        self.framerate = framerate
        self.inputcodec = inputcodec
        self.outputcodec = outputcodec

    def record(self):
        # construct string to pass to StreamCamera, initializes stream to central server.
        self.execute = "ffmpeg -f " + self.inputcodec + \
                       " -s " + self.resolution + \
                       " -r " + str(self.framerate) + \
                       " -i " + self.inputdevice + \
                       " -flags:v +global_header " + \
                       " -c:v " + self.outputcodec + \
                       " -f rtp rtp://" + self.destination + ":" + str(self.port) + \
                       " > /tmp/config.sdp"
        subprocess.call(self.execute, shell=True)