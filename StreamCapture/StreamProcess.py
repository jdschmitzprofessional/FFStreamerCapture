import os
import subprocess
import time
import logging
import JsonConverter
from datetime import datetime

class StreamProcess:
    def __init__(self, config, ramDisk):
        self.jsonlog = JsonConverter
        ### camera name
        self.cameraName = config['name']
        self.logger = logging.getLogger("FFStreamerCapture." + self.cameraName + ".post")
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("\"Instantiated Stream Processor\"")
        ### folder to save files to
        self.saveFolder = config['save_folder']
        ### construct filepath to ramdisk
        self.filepath = ramDisk + "/" + self.cameraName
        try:
            if not os.path.exists(self.filepath):
                os.mkdir(self.filepath)
            if not os.path.exists(self.saveFolder):
                os.mkdir(self.saveFolder)
        except OSError as e:
            self.error = e
            self.logger.warning(self.jsonlog.dumpVariables(self.__dict__))
        # logging variables
        self.start_size = None
        self.end_size = None
        self.start_time = None
        self.end_time = None
        self.source_file = None
        self.output_file = None
        self.exit_status = None
        self.error = None


    def process(self):
        try:
            while True:
                for footage in os.listdir(self.filepath):
                    if "finished" in footage:
                        self.source_file = self.filepath + "/" + footage
                        self.start_size = str(os.path.getsize(self.source_file)/1024/1024)
                        self.start_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                        self.output_file = self.saveFolder + "/" + footage.replace(".h264.finished", ".mp4")
                        execute = "ffmpeg" + \
                                  " -hwaccel vaapi -hwaccel_output_format vaapi" + \
                                  " -hwaccel_device /dev/dri/by-path/pci-0000\:13\:00.0-render" + \
                                  " -i " + self.filepath + "/" + footage + \
                                  " -b:v 1500K" + \
                                  " -c:v h264_vaapi " + self.output_file
                        try:
                            subprocess.check_output(execute, shell=True)
                            self.exit_status = "SUCCESS"
                            self.end_size = str(os.path.getsize(self.output_file)/1024/1024)
                            self.end_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                            self.logger.info(self.jsonlog.dumpVariables(self.__dict__))
                        except subprocess.CalledProcessError:
                            self.exit_status = "FAIL"
                            self.logger.warning(self.jsonlog.dumpVariables(self.__dict__))
                            continue
                        os.remove(self.filepath + "/" + footage)

                    else:
                        continue
                time.sleep(60)
        except Exception as e:
            self.error = e
            self.logger.critical(self.jsonlog.dumpVariables(self.__dict__))