
"""
This module provides access to the data provided by the AR.Drone.
"""

import select
import socket
import threading
import multiprocessing
import cv2
import logging

import libardrone
import utilities

############# Setup ################
utilities.setup()
logger = logging.getLogger("ARdrone-controller")


class ARDroneNetworkProcess(multiprocessing.Process):
    """ARDrone Network Process.

    This process collects data from the video and navdata port, converts the
    data and sends it to the IPCThread.
    """

    def __init__(self, nav_pipe, com_pipe):
        multiprocessing.Process.__init__(self)
        self.nav_pipe = nav_pipe
        self.com_pipe = com_pipe

    def run(self):
        nav_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        nav_socket.setblocking(0)
        nav_socket.bind(('', libardrone.ARDRONE_NAVDATA_PORT))
        nav_socket.sendto("\x01\x00\x00\x00", (libardrone.ARDRONE_ADDR, libardrone.ARDRONE_NAVDATA_PORT))

        stopping = False
        while not stopping:
            inputready, outputready, exceptready = select.select([nav_socket, self.com_pipe], [], [])
            for i in inputready:
                if i == nav_socket:
                    while 1:
                        try:
                            data = nav_socket.recv(65535)
                        except IOError:
                            # we consumed every packet from the socket and
                            # continue with the last one
                            break
                    navdata = libardrone.decode_navdata(data)
                    self.nav_pipe.send(navdata)
                elif i == self.com_pipe:
                    _ = self.com_pipe.recv()
                    stopping = True
                    break

        nav_socket.close()


class ARDroneVideoProcess(multiprocessing.Process):
    """ARDrone Video Process.

    This process collects data from the video port and sends it to the IPCThread.
    """

    def __init__(self, video_pipe, com_pipe):
        multiprocessing.Process.__init__(self)
        self.video_pipe = video_pipe
        self.com_pipe = com_pipe

    def run(self):
        cam = cv2.VideoCapture('tcp://{}:{}'.format(libardrone.ARDRONE_ADDR, libardrone.ARDRONE_VIDEO_PORT))
        stopping = False

        while not stopping:
            # check for kill switch
            if self.com_pipe.poll():
                _ = self.com_pipe.recv()
                stopping = True

            # get video frame
            running, frame = cam.read()
            if running:
                self.video_pipe.send(frame)

        cam.release()
        cv2.destroyAllWindows()


class IPCThread(threading.Thread):
    """Inter Process Communication Thread.

    This thread collects the data from the ARDroneNetworkProcess and forwards
    it to the ARDrone.
    """

    def __init__(self, drone):
        threading.Thread.__init__(self)
        self.drone = drone
        self.stopping = False

    def run(self):
        while not self.stopping:
            inputready, outputready, exceptready = select.select([self.drone.video_pipe, self.drone.nav_pipe], [], [], 1)
            for i in inputready:
                if i == self.drone.video_pipe:
                    while self.drone.video_pipe.poll():
                        image = self.drone.video_pipe.recv()
                    self.drone.image = image
                elif i == self.drone.nav_pipe:
                    while self.drone.nav_pipe.poll():
                        navdata = self.drone.nav_pipe.recv()
                    self.drone.navdata = navdata

    def stop(self):
        """Stop the IPCThread activity."""
        self.stopping = True
