import cv2 as cv
import numpy as np
from cv2 import aruco
from visual_servoing.ibvs_eih import IbvsEih


class VisionTracker:
    """
    Controller to follow the ArUco markers
    """
    def __init__(self, RobotHttpInterface):
        self.RobotHttpInterface = RobotHttpInterface
        self.start = False
        self.corners = []

        self.parameters = aruco.DetectorParameters_create()
        import aruco_utils
        self.dictionary = aruco_utils.get_custom_dict()

        # Auxiliary variables
        self.exit = False
        self.pause = False
        """ PARAMETROS PROVISIONALES"""
        # Set desired camera depth and desired feature coordinates as well as distance from goal before stopping
        self.final_camera_depth = 0.1
        self.desired_corners = np.array([10, 10, -10, 10, 10, -10, -10, -10])
        self.dist_tol = 0.5

    def act_track(self):
        self.start = True
        self.active_ctrl()

    def des_track(self):
        self.pause = True
        self.RobotHttpInterface.stop()

    def aaaa(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.dictionary, parameters=self.parameters)
        if len(corners) > 0 and 0 in ids:
            frame_markers = aruco.drawDetectedMarkers(img.copy(), corners, ids)
            img = frame_markers

            ids = list(ids.flatten())

            def compute_area(x, y):
                # https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
                return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

            # Track marker with ID 0
            corner = corners[ids.index(0)]
            x = corner[:, :, 0].flatten()
            y = corner[:, :, 1].flatten()
            area = compute_area(x, y)

            slope = np.mean([y[1] - y[0], y[3] - y[2]])

            # Velocidades respecto cámara
            # X positivo: hacia alante
            # Y positivo: hacia derecha
            # Z positivo: hacia abajo

    def run(self):
        ibvseih = IbvsEih(self.RobotHttpInterface)
        while not self.exit:
            if self.start:
                ibvseih.pause = False
                ibvseih.move_to_position(self.final_camera_depth, self.desired_corners, self.dist_tol)
                self.detectMarker = False

            if self.pause:
                ibvseih.pause = self.pause
                self.pause = False

