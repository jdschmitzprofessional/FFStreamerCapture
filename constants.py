
functional_root = "/opt/cameras"
cameras = {
    "eastgaragecam": {
        "name": "eastgarage",
        "port": 20500,
        "user": "pi",
        "retrieval_method": "ssh",
        "keyfile": "/opt/key/id_rsa",
        "address": "192.168.50.125",
        "savefolder": "/mnt/eastgarage",
        "configpath": "/home/pi/config.sdp"
    },
    "porchcam": {
        "name": "porch",
        "port": 20501,
        "user": "pi",
        "retrieval_method": "ssh",
        "keyfile": "/opt/key/id_rsa",
        "address": "192.168.50.124",
        "savefolder": "/mnt/porch",
        "configpath": "/home/pi/config.sdp"
    }
}