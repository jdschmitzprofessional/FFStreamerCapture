

# manually designate the central server's IP address. Used on both cameras and central server.
central_server = '192.168.50.35'
# path to log
log_path = "/var/log/camera"
log_level = "debug"
# camera names must be unique for logging purposes.
# port must be unique
# address must be unique IPv4
# optional categories are restream address/port. If not provided, central server reuses
# its own address and adds 200 to port.
cameras = {
    "eastgaragecam": {
        "name": "eastgarage",
        "port": 6000,
        "address": "192.168.50.125",
        "savefolder": "/mnt/eastgarage",
        "framerate": 30,
        "resolution": "1280x720",
        "bitrate": "1.5M"
        # "restream_address": ""
        # "restream_port": ""
    },
    "porchcam": {
        "name": "porch",
        "port": 6001,
        "address": "192.168.50.124",
        "savefolder": "/mnt/porch",
        "framerate": 30,
        "resolution": "1280x720",
        "bitrate": "1.5M"
    }
}