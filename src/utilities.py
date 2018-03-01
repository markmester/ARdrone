#!/usr/bin/env python

import yaml
import os
import cv2
import subprocess
import numpy

import logging.config


def setup(path=None):
    """Helper for all project setup functions
    """
    if not path:
        path = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/config/config.yml"
    if not os.path.exists(path):
        print "Unable to find config! Exiting..."
        exit(1)

    setup_logging(path)

    return get_config(path)


def get_config(path):
    """Load project configuration
    """
    with open(path, "r") as f:
        return yaml.safe_load(f.read())


def setup_logging(path, level=logging.INFO):
    """Setup logging configuration
    """
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())['logging']
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)


def get_udp_stream():
    FFMPEG_BIN = "ffmpeg"
    command = [FFMPEG_BIN,
               '-i', 'udp://0.0.0.0:5000',
               '-err_detect', 'ignore_err',
               '-pix_fmt', 'bgr24',  # opencv requires bgr24 pixel format.
               '-vcodec', 'rawvideo',
               '-an', '-sn',  # we want to disable audio processing (there is no audio)
               '-f', 'image2pipe', '-']
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=10 ** 8)

    while True:
        # Capture frame-by-frame
        raw_image = pipe.stdout.read(480 * 360 * 3)
        # transform the byte read into a numpy array
        image = numpy.fromstring(raw_image, dtype='uint8')
        if len(image) != 0:
            image = image.reshape((360, 480, 3))  # Notice how height is specified first and then width
        else:
            image = None

        if image is not None:
            cv2.imshow('Video', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        pipe.stdout.flush()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    pass
