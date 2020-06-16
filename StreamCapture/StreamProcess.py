import os
import subprocess
import time
import logging
from JsonConverter import JsonConverter
from datetime import datetime


class StreamProcess:
    def __init__(self, config=dict, ram_disk=str):
        self.convert = JsonConverter
        self.cameraName = config['name']
        self.logger = logging.getLogger("FFStreamerCapture." + self.cameraName + ".post")
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("\"Instantiated Stream Processor\"")
        # folder to save files to
        self.save_folder = config['save_folder']
        # construct filepath to ramdisk for temporary storage
        self.filepath = ram_disk + "/" + self.cameraName
        try:
            if not os.path.exists(self.filepath):
                os.mkdir(self.filepath)
            if not os.path.exists(self.save_folder):
                os.mkdir(self.save_folder)
        except OSError as e:
            self.error = e
            self.logger.warning(JsonConverter.dump_variables())
        # logging variables
        self.start_size = None
        self.end_size = int
        self.start_time = int
        self.end_time = None
        self.source_file = None
        self.output_file = None
        self.exit_status = None
        self.error = None
        self.compression_difference = int
        self.current_date = datetime.now().strftime('%Y-%m-%d')

    def process(self):
        try:
            while True:
                self.error = None
                if self.current_date != datetime.now().strftime('%Y-%m-%d'):
                    self.current_date = datetime.now().strftime('%Y-%m-%d')
                    self.sort_output_by_date()
                for footage in os.listdir(self.filepath):
                    self.source_file = self.filepath + "/" + footage
                    if "finished" in footage:
                        self.start_size = os.path.getsize(self.source_file)/1024/1024
                        self.start_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                        self.output_file = self.save_folder + "/" + footage.replace(".h264.finished", ".mp4")
                        execute = "ffmpeg" + \
                                  " -hwaccel vaapi -hwaccel_output_format vaapi" + \
                                  " -hwaccel_device /dev/dri/by-path/pci-0000\:13\:00.0-render" + \
                                  " -i " + self.source_file + \
                                  " -b:v 1500K" + \
                                  " -c:v h264_vaapi " + self.output_file
                        try:
                            subprocess.check_output(execute, shell=True)
                            self.exit_status = "SUCCESS"
                            self.end_size = os.path.getsize(self.output_file)/1024/1024
                            self.end_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                            self.compression_difference = int(self.start_size - self.end_size)
                            self.logger.info(self.convert.dump_variables(self.__dict__))
                        except subprocess.CalledProcessError:
                            self.exit_status = "FAIL"
                            self.logger.warning(self.convert.dump_variables(self.__dict__))
                            os.remove(self.source_file)
                            self.logger.warning("\"Removed " + self.source_file + "\"")
                            continue
                        os.remove(self.filepath + "/" + footage)

                    else:
                        continue
                time.sleep(60)
        except Exception as e:
            self.error = e
            self.logger.critical(self.convert.dump_variables(self.__dict__))

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
            self.logger.warning(self.convert.dump_variables(self.__dict__))
        except Exception as e:
            self.error = e
            self.logger.critical(self.convert.dump_variables(self.__dict__))
