import tkinter as tk
import cv2
import cv2.aruco as aruco
from CameraClient import CameraClient
from itertools import chain

class VisionLeaderFollowerMissionClient(CameraClient):
    def __init__(self, root, geometryString, name, url, brov):
        super().__init__(root, geometryString, name, url)

        self.root = root
        self.url = url
        self.brov = brov

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
        self.brov.setVelocity(0, 0, 0, 0, 0)

    def getImage(self):
        image_corrected = super().getImage()
        # cv2.imshow("image_corrected", image_corrected)

        if self.detectMarkers:
            gray = cv2.cvtColor(image_corrected, cv2.COLOR_BGR2GRAY)
            aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
            parameters = aruco.DetectorParameters_create()
            print("parameters:", parameters)
            my_dict = get_custom_dict()
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, my_dict, parameters=parameters)
            print("corners", corners)
            print("ids", ids)
            print("rejectedImgPoints", rejectedImgPoints)
            frame_markers = aruco.drawDetectedMarkers(image_corrected.copy(), corners, ids)
            image_corrected = frame_markers

            # Control stage
            if ids is not None:
                ids_f = list(chain.from_iterable(ids))
            else:
                ids_f = []
                self.brov.stop()

            if 0 in ids_f: # Aruco target found
                idx = ids_f.index(0)
                corners_f = list(chain.from_iterable(corners))
                corners_des = corners_f[idx]
                self.brov_control(corners_des)
            else:
                self.brov.stop()
                print("WARNING: Follower (BlueROV) lost Leader (G5002). Stop moving follower.")

        return image_corrected

    def brov_control(self, points):
        # points = points[0]
        w = points[1][0] - points[0][0]
        h = points[3][1] - points[0][1]
        area = w * h                   # input for PID in X axis
        cx = points[0][0] + (w // 2)  # input for PID in Y axis
        cy = points[0][1] + (h // 2)  # input for PID in Z axis

        # TODO: get velocities from the control loop
        # vx, vy, vz = self.pid((area, cx, cy))
        # self.brov.setVelocity(vy, -vx, -vz, 0, 100)
        # self.brov.getPosition()


numMarkers = 2
markerSize = 4
CUSTOM_DICT = aruco.custom_dictionary(numMarkers, markerSize, 0)


def get_custom_dict():
    return CUSTOM_DICT