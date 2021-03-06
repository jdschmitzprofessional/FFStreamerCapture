import datetime as dt
import time

import StreamCamera
import constants


def stream(config):
    # instantiate the stream camera
    stream = StreamCamera.StreamCamera(config=config)
    with open('/home/pi/log.txt', 'a+') as outfile:
        while True:
            # continuously records with a 2 second gap when interrupted.
            outfile.write(str(dt.datetime.now()) + ' - started recording\n')
            stream.record()
            outfile.write(str(dt.datetime.now()) + ' - feed was interrupted!\n')
            time.sleep(2)
