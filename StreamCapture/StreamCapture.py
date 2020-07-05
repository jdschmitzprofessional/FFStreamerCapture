import logging
import os
import subprocess
from datetime import datetime as dt

import JsonConverter


class CaptureStream:
    def __init__(self, listen=str, config=dict):
        self.converter = JsonConverter.JsonConverter
        self.loop_duration = config['loop_duration']
        ### name of the camera
        self.camera_name = config['name']
        ### address to listen from (remote camera)
        self.listen_address = listen
        self.remote_address = config['address']
        ### port to listen on
        self.listen_port = config['port']
        ### set the framerate to force synchronicity
        self.frame_rate = config['frame_rate']
        ### empty string initialization, populates in capture method
        self.execute = str
        self.logger = logging.getLogger("FFStreamerCapture." + self.camera_name + ".capture")
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("\"action\": \"Instantiated Stream Capture\"")
        ### port to restream on. Calculates arbitrarily if not provided.
        try:
            self.restream_port = config['restream_port']
        except KeyError:
            self.restream_port = self.listen_port + 200
        ### address to restream to. Uses same as input address if not provided.
        try:
            self.restream_address = config['restream_address']
        except KeyError:
            self.restream_address = self.listen_address
        # logging initialization
        self.buffer = '/tmp/' + self.camera_name
        self.start_time = str
        self.end_time = str
        self.file_size = str
        self.error = None

    def capture(self):
        self.clean_ram_disk()
        while True:
            self.error = None
            try:
                self.start_time = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
                execute = "ffmpeg" + \
                          " -i \"tcp://" + self.listen_address + ":" + str(self.listen_port) + "?listen\"" + \
                          " -c:v copy" + \
                          " -t " + str(self.loop_duration) + \
                          " " + self.buffer + "/" + self.start_time + ".h264" + \
                          " -c:v copy" + \
                          " -t " + str(self.loop_duration) + \
                          " -f h264 udp://" + self.restream_address + ":" + str(self.restream_port)
                print(execute)
                subprocess.call(execute, shell=True)
                self.end_time = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
                self.logger.info(self.converter.dump_variables(self.__dict__))
                reprocess = "mv -v /tmp/" + self.camera_name + "/" + self.start_time + ".h264 /tmp/" + self.camera_name + "/" + self.start_time + ".h264.finished"
                subprocess.call(reprocess, shell=True)
            except Exception as e:
                self.error = e
                self.logger.critical(self.converter.dump_variables(self.__dict__))

    def clean_ram_disk(self):
        for file in os.listdir(self.buffer):
            if "finished" not in file:
                os.remove(self.buffer + '/' + file)
                self.logger.info("\"Removed " + file + "\"")
