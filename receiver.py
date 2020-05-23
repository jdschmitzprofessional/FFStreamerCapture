import ipaddress
import ffmpeg




if __name__ == "__main__":
    destinationAddress = '192.168.50.111'
    print(destinationAddress)
    port = 6000
    cam = ffmpeg.StreamCamera(inputdevice="/dev/video0",resolution="640x480",aspectratio="4:3",destination=destinationAddress,framerate=30, inputcodec="video4linux2", outputcodec="h264_omx", port=6000)
    cam.record()
