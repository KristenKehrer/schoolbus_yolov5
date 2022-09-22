from os.path import exists
import cv2


def get_rtsp_url():

    # we get the IP address of the camera from our router software
    camera_address = "192.168.4.81"

    # This path and port is documented in our security camera's user manual
    rtsp_path = "/H264/ch1/main/av_stream"
    rtsp_port = 554

    # The name of a file which we will exclude from version control, and save our username and password in it.
    creds_file = '.camera_credentials'

    if not exists(creds_file):
        raise f'Missing configuration file: {creds_file}'

    # This variable will hold the username and password used to connect to
    # the security camera.  Will look like: "username:password"
    camera_auth = open(creds_file, 'r').read().strip()  # open() is how you can read/write files

    # return the open cv object with the authenticated RTSP address.
    full_url = f'rtsp://{camera_auth}@{camera_address}:{rtsp_port}{rtsp_path}'
    return full_url
