import StreamCamera
import constants
import multiprocessing


def startRecoring(target):
    cameramap[target].capture()

if __name__ == "__main__":
    cameramap = {}
    for camera in constants.cameras:
        print(camera)
        cameramap[camera] = StreamCamera.CaptureStream(listen=constants.local_address, root=constants.program_root, config=constants.cameras[camera])
    for camera in cameramap:
        print(cameramap[camera])
        multiprocessing.Process(target=startRecoring,args=(camera,)).start()
    # porchcam = StreamCamera.CaptureStream(sourceaddress='192.168.50.125',
    #                                       sourceport=6000,
    #                                       retrievalmethod='ssh',
    #                                       remoteuser='pi',
    #                                       sshkey='/opt/key/id_rsa',
    #                                       savefolder="/tmp")
    # porchcam.configure('/home/pi/config.sdp', '/tmp/eastgaragecam.sdp')
    # porchcam.capture()