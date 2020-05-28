import StreamCamera
import constants
import multiprocessing



### To be executed on the central server. Initiates a camera intake stream for each configured camera under
### a unique process.

def startRecoring(target):
    cameramap[target].capture()

if __name__ == "__main__":
    cameramap = {}
    for camera in constants.cameras:
        cameramap[camera] = StreamCamera.CaptureStream(listen=constants.local_address, config=constants.cameras[camera])
    for camera in cameramap:
        multiprocessing.Process(target=startRecoring,args=(camera,)).start()
