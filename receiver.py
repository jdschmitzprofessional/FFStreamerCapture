import StreamCamera
import multiprocessing
if __name__ == "__main__":
    port = 6000
    porchcam = StreamCamera.CaptureStream(sourceaddress='192.168.50.125',
                                          sourceport=6000,
                                          retrievalmethod='ssh',
                                          remoteuser='pi',
                                          sshkey='/opt/key/id_rsa',
                                          savefolder="/tmp")
    porchcam.configure('/home/pi/config.sdp', '/tmp/eastgaragecam.sdp')
    porchcam.capture()