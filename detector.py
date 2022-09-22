from timeit import default_timer as timer
from datetime import datetime
import os
import cv2
import time
import aws


class Detector:
    """A class to manage notifications for when the bus comes"""

    num_seconds_between_texts = 60
    probability_threshold = .8
    last_text = timer()

    def __init__(self):
        print('Detector: Ready for object detection...')
        if not os.path.exists('images'):
            os.mkdir('images')

    def objects_detected(self, **kwargs):
        """Function to be called whenever our model detects an object."""

        # Extract the things we want from the `**kwargs`
        objects = kwargs['objects']
        img = kwargs['img']

        # We will only attempt to notify for these labels, and where the confidence exceeds our
        # `self.probability_threshold`
        notify_for = ['schoolbus']
        confident_objects = list(
            filter(lambda o: o['confidence'] > self.probability_threshold and o['label'] in notify_for, objects))

        # If we end up with nothing, return without doing anything.
        if len(confident_objects) == 0:
            return

        # Just do some console logging of detected objects
        object_names = ', '.join(map(lambda o: o['label'], confident_objects))
        print(f'Detected objects: {object_names}')

        # If it has been long enough since the last text, send another notification
        now = timer()
        if (now - self.last_text) > self.num_seconds_between_texts:
            self.last_text = now
            self.send_notification(confident_objects[0], img)

    def send_notification(self, obj, img):
        """Notify users that a bus has passed!"""
        print('Sending notification!')

        # Get a string of the current timestamp
        now = datetime.now()
        timestamp = now.strftime('%m-%d-%Y_%H-%M-%S-%f')

        # Write the opencv `img` to a file
        filename = f'images/{timestamp}_{obj["label"]}.jpg'
        cv2.imwrite(filename, img)

        # Save the image file to aws s3 file storage
        img_url = aws.save_file(filename)
        confidence_pct = "{0:.0%}".format(obj["confidence"])

        # Post an sms message to users with a message and image link
        aws.send_sms(f'The {obj["label"]} drove by at {now.strftime("%H:%M:%S")} ({confidence_pct}'
                     f' confidence) {img_url}')


