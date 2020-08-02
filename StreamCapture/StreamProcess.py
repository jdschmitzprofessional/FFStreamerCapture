import logging
import os
import subprocess
import time
from datetime import datetime
import constants

from JsonConverter import JsonConverter

#TODO: Clean up thsi file, stop using self.__dict__ for logging
class StreamProcess:
    def __init__(self, config=dict, ram_disk=str):
        self.loop_duration: int = config['loop_duration']
        self.convert = JsonConverter
        self.cameraName: str = config['name']
        self.bit_rate: str = config['bit_rate']
        self.logger = logging.getLogger("FFStreamerCapture." + self.cameraName + ".post")
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("\"Instantiated Stream Processor\"")
        self.save_folder: str = config['save_folder']
        self.filepath: str = ram_disk + "/" + self.cameraName
        try:
            if not os.path.exists(self.filepath):
                os.mkdir(self.filepath)
            if not os.path.exists(self.save_folder):
                os.mkdir(self.save_folder)
        except OSError as e:
            self.error = e
            self.logger.warning(JsonConverter.dump_variables())
        # logging variables
        self.start_size: int = 0
        self.end_size: int = 0
        self.start_time: int = 0
        self.end_time: int = 0
        self.source_file: str = ""
        self.output_file: str = ""
        self.exit_status: str = ""
        self.error: str = ""
        self.compression_difference: int = ""
        self.current_date: str = datetime.now().strftime('%Y-%m-%d')

    def process(self):
        while True:
            self.error = ""
            if self.current_date != datetime.now().strftime('%Y-%m-%d'):
                self.current_date = datetime.now().strftime('%Y-%m-%d')
                self.sort_output_by_date()
            for footage in os.listdir(self.filepath):
                self.source_file = self.filepath + "/" + footage
                print(f"{self.source_file}")
                if "finished" in footage or (".h264" in footage and time.time() - os.path.getmtime(f"{self.source_file}") >= (self.loop_duration * 3)):
                    self.process_footage(footage)
            time.sleep(60)


    def sort_output_by_date(self):
        try:
            for file in os.listdir(self.save_folder):
                if os.path.isdir(self.save_folder + '/' + file):
                    continue
                file_date = str(file)[0:10]
                print(file_date)
                if file_date != self.current_date:
                    if not os.path.exists(self.save_folder + '/' + file_date):
                        os.mkdir(self.save_folder + '/' + file_date)
                    os.rename(self.save_folder + '/' + file, self.save_folder + "/" + file_date + "/" + file)
        except IOError or OSError as e:
            self.error = e
        except Exception as e:
            self.error = e

    def process_footage(self, footage):
        self.start_size = os.path.getsize(self.source_file) / 1024 / 1024
        self.start_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.output_file = self.save_folder + "/" + footage.replace(".h264.finished", ".mp4")
        execute = f"ffmpeg -vaapi_device /dev/dri/by-path/pci-0000\:0b\:00.0-render" + \
                  " -i " + self.source_file + \
                  " -vf 'format=nv12,hwupload' " + \
                  " -c:v hevc_vaapi " + self.output_file
        try:
            subprocess.check_output(execute, shell=True)
            self.exit_status = "SUCCESS"
            self.end_size = os.path.getsize(self.output_file) / 1024 / 1024
            self.end_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            self.compression_difference = int(self.start_size - self.end_size)
        except subprocess.CalledProcessError:
            self.exit_status = "FAIL"
        os.remove(self.filepath + "/" + footage)
