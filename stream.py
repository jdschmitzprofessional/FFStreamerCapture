import StreamCamera
import time
import datetime as dt
import subprocess
import constants
import re

import sys

if __name__ == "__main__":
    # figure out which camera this is by .the IP address.
    # Causes issues if the camera is trying to record through a NAT router.
    # uses a subprocess and regex to determine addresses to limit additional moreceiverdules needed
    addr_pattern = re.compile("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")
    process_output = subprocess.call(
        'ip addr show', shell=True)
    addresses = re.search(addr_pattern, str(process_output))
    for camera in constants.cameras:
        if camera['address'] in addresses.groups():
            config = constants.cameras[camera]
    if not config:
        print("No matching configuration could be determined.")
        sys.exit(1)
    # instantiate the stream camera
    stream = StreamCamera.StreamCamera(resolution=config['resolution'],
                                       destination=constants.central_server,
                                       framerate=config['framerate'],
                                       port=config['port'])
    with open('/home/pi/log.txt','a+') as outfile:
        while True:
            # continuously records with a 2 second gap when interrupted.
            outfile.write(str(dt.datetime.now()) + ' - started recording\n')
            stream.record()
            outfile.write( str(dt.datetime.now()) + ' - feed was interrupted!\n')
            time.sleep(2)
