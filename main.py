import constants
import subprocess
import re
import stream
import receive
import logging


# figure out which camera/server this is by .the IP address.
# Causes issues if the camera is trying to record through a NAT router.
# uses a subprocess and regex to determine addresses to limit additional modules needed

def find_config():
    addr_pattern = re.compile("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")
    process_output = subprocess.run(
        'ip addr show', shell=True, stdout=subprocess.PIPE)
    addresses = re.findall(addr_pattern, str(process_output.stdout))
    if constants.central_server in addresses:
        config = constants.central_server
        return config
    for camera in constants.cameras:
        if constants.cameras[camera]['address'] in addresses:
            config = constants.cameras[camera]
    if not config:
        sys.exit(1)
    return config


if __name__ == "__main__":
    if find_config() != constants.central_server:
        stream.stream()
    else:
        receive.receive()
