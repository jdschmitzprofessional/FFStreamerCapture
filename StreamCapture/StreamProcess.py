import os
import subprocess
import time


class StreamProcess:
    def __init__(self, config, ramDisk):
        ### folder to save files to
        self.saveFolder = config['savefolder']
        ### camera name
        self.cameraName = config['name']
        ### construct filepath to ramdisk
        self.filepath = ramDisk + "/" + self.cameraName
        try:
            os.mkdir(self.filepath)
            os.mkdir(self.saveFolder)
        except OSError:
            print("Unable to create target directory.")


    def process(self):
        while True:
            for footage in os.listdir(self.filepath):
                if "finished" in footage:
                    execute = "ffmpeg" + \
                              " -hwaccel vaapi -hwaccel_output_format vaapi" + \
                              " -hwaccel_device /dev/dri/by-path/pci-0000\:13\:00.0-render" + \
                              " -i " + self.filepath + "/" + footage + \
                              " -b:v 1500K" + \
                              " -c:v hevc_vaapi " + self.saveFolder + "/" + footage.replace(".h264.finished", ".mp4")
                    try:
                       subprocess.check_output(execute, shell=True)
                    except subprocess.CalledProcessError:
                        continue
                    os.remove(self.filepath + "/" + footage)
                else:
                    continue
            time.sleep(60)