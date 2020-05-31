central_server = '192.168.50.35'
logfile = "/var/log/camera.log"
cameras = {
    "eastgaragecam": {
        "name": "eastgarage",
        "port": 6000,
        "address": "192.168.50.125",
        "savefolder": "/mnt/eastgarage",
        "framerate": 25,
        "resolution": "1280x720",
        "bitrate": "1.5M"
    },
    "porchcam": {
        "name": "porch",
        "port": 6001,
        "address": "192.168.50.124",
        "savefolder": "/mnt/porch",
        "framerate": 25,
        "resolution": "1280x720",
        "bitrate": "1.5M"
    }
}