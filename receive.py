import StreamCapture
import constants
import multiprocessing


# To be executed on the central server. Initiates a camera intake stream for each configured camera under
# a unique process.

def startRecoring(target):
    target.capture()


def receive(cameras=dict):
    print("boop")
    cameramap = {}
    for camera in cameras:
        cameramap[camera] = StreamCapture.CaptureStream(listen=constants.central_server,
                                                       config=constants.cameras[camera])
    for camera in cameramap:
        multiprocessing.Process(target=startRecoring, args=(cameramap[camera],)).start()

