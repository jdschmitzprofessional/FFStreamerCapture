import StreamCapture
import constants
import multiprocessing


# To be executed on the central server. Initiates a camera intake stream for each configured camera under
# a unique process.

def startRecoring(target):
    target.capture()

def processFootage(target):
    target.process()


def receive(cameras=dict):
    cameramap = {}
    encodermap = {}
    for camera in cameras:
        cameramap[camera] = StreamCapture.CaptureStream(listen=constants.central_server,
                                                       config=constants.cameras[camera])
        encodermap[camera] = StreamCapture.StreamProcess(config=cameras[camera],
                                                         ram_disk='/tmp')

    for camera in cameramap:
        multiprocessing.Process(target=startRecoring, args=(cameramap[camera],)).start()
    for encoder in encodermap:
        multiprocessing.Process(target=processFootage, args=(encodermap[encoder],)).start()

