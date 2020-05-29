import StreamCamera
import constants
import multiprocessing


# To be executed on the central server. Initiates a camera intake stream for each configured camera under
# a unique process.

def startRecoring(target):
    cameramap[target].capture()

def receive():
    logging.basicConfig(filename=constants.logfile, level=logging.INFO)
    logging.info("Receiver program initialized")
    cameramap = {}
    for camera in constants.cameras:
        cameramap[camera] = StreamCamera.CaptureStream(listen=constants.central_server, config=constants.cameras[camera])
    for camera in cameramap:
        multiprocessing.Process(target=startRecoring,args=(camera,)).start()
