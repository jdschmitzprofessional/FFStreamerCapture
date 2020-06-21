

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
        "save_folder": "/mnt/eastgarage",
        "frame_rate": 25,
        "resolution": "1600x900",
        "bit_rate": "5M",
        "loop_duration": 300
        # "restream_address": ""
        # "restream_port": ""
    },
    "porchcam": {
        "name": "porch",
        "port": 6001,
        "address": "192.168.50.124",
        "save_folder": "/mnt/porch",
        "frame_rate": 25,
        "resolution": "1600x900",
        "bit_rate": "5M",
        "loop_duration": 300
    }
}