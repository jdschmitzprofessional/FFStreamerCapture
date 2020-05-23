import os
from datetime import datetime as dt
import time
class ffmpeg:
    def __init__(self, raspi=int, device=str, timestampNames=bool, aspect=str, xRes=int, framerate=int, loopDuration=int, codec=str, outputDirectory=str):
        self.raspi=raspi
        self.device=device
        self.codec=codec
        self.framerate=framerate
        self.xRes = xRes
        self.timestampNames=timestampNames
        self.duration = loopDuration
        self.framerate = framerate
        self.aspect = aspect
        self.outputDirectory = outputDirectory
        self.calculateRatio = AspectRatio(aspect,self.xRes).getResolutions()
        self.resolution = str(str(self.calculateRatio[0]) + "x" + str(self.calculateRatio[1]))
        print(self.resolution)
    def record(self):
        if self.timestampNames:
            self.outputFile=dt.now().strftime('%Y-%m-%d-%H-%M-%S') + str(".mp4")
        self.startTime=int(time.time())-25200
        if self.raspi == 0:
            execute = "ffmpeg -f video4linux2 "+ \
                " -input_format h264 " + \
                " -video_size " + self.resolution + \
                " -framerate " + self.framerate + \
                " -i " + self.device + \
                " vf \"drawtext=text='timestamp: %{pts\:gmtime\:" + str(self.startTime) + "\:%Y %m %d %H %M %S}'\" -vcodec " + self.codec + \
                " -an " + self.outputDirectory + "/" + self.outputFile
        else:

            execute = "ffmpeg -f video4linux2 -i " + self.device + \
                " -s " + self.resolution + \
                " -t " + str(self.duration) + \
                " -r " + str(self.framerate) + \
                " -vf \"drawtext=text='timestamp: %{pts\:gmtime\:" + str(self.startTime) + "\:%Y %m %d %H %M %S}'\" -vcodec " + self.codec + \
                ' -f mp4 ' + self.outputDirectory + '/' + self.outputFile
        print(execute)
        os.system(str(execute))

class AspectRatio:
    def __init__(self,aspectRatio,xRes=int):
        self.xRes=xRes
        self.aspectRatio=aspectRatio.split(":")
        self.xRatio=int(self.aspectRatio[0])
        self.yRatio=int(self.aspectRatio[1])
        self.conversionRatio = self.yRatio/self.xRatio
        self.yRes = int(self.xRes*self.conversionRatio)
    def getConversionFactor(self):
        return self.conversionRatio
    def getResolutions(self):
        ret = [ self.xRes, self.yRes ]
        return ret


