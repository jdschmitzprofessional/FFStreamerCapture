
# cameras = {
#       "sample_1": {
#           "port": 6000,
#           "retrieval_method": "http | ssh | manual"
#       }
# }
#
# retreival methods under construction: http | ssh


cameras = {
    "eastgaragecam": {
        "port": 20500,
        "retrieval_method": "ssh",
        "keyfile": "/opt/keys/id_rsa",
        "address": "192.168.50.125",
        "savefolder": "/tmp/eastgaragecam"
    }
}