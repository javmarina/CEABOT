import tkinter as tk
import cv2
import cv2.aruco as aruco
from interface_class.CameraClient import CameraClient
from itertools import chain
from tracker import VisionTracker

class VisionLeaderFollowerMissionClient(CameraClient):
    def __init__(self, root, geometryString, name, tracker:VisionTracker):
        super().__init__(root, geometryString, name, tracker.RobotHttpInterface)

        self.root = root
        self.tracker = tracker

        self.buttonShowMarkers = tk.Button(self.cameraWindow, text="Markers", command=self.applyDetectMarket)
        self.buttonShowMarkers.grid(row=6, rowspan=1, column=1, columnspan=2, sticky="nswe")

        self.detectMarkers = False

        # Reference parameters
        self.ref_area = 1600  # 40 * 40 pixels
        self.ref_x = 157
        self.ref_y = 117

        # TODO: Implement control
        # # PID parameters
        # P = [2, 2, 2]
        # I = [0, 0, 0]
        # D = [0, 0, 0]
        # self.timesleep = 0.1
        # self.output_lims = (-0.2, 0.2)
        # self.pid = PIDController(P, I, D, self.timesleep, self.output_lims)
        # self.pid.setpoint((self.ref_area, self.ref_x, self.ref_y))

    def applyDetectMarket(self):
        self.detectMarkers = not self.detectMarkers
        self.tracker.RobotHttpInterface.set_velocity(0,0,0,0)
        if(self.detectMarkers):
            self.tracker.act_track()
        else:
            self.tracker.des_track()

    def getImage(self):
        image_corrected = super().getImage()

        # TODO: Implementar la funcion de markers de javi

        return image_corrected


numMarkers = 2
markerSize = 4
CUSTOM_DICT = aruco.custom_dictionary(numMarkers, markerSize, 0)


def get_custom_dict():
    return CUSTOM_DICT