import io
import time

import cv2 as cv
import numpy as np
from PIL import Image
from cv2 import aruco
from simple_pid import PID

from utils import RobotHttpInterface
from pipeline.Pipeline import StraightPipeline
from pipeline.PipelineStage import Producer, PipelineStage, Consumer


class ImagePipeline(StraightPipeline):
    def __init__(self, address: str, http_interface: RobotHttpInterface, adq_rate):
        if address == "localhost":
            # Avoid DNS resolve for localhost
            address = "127.0.0.1"
        self.http_interface = http_interface

        super().__init__([
            FiringStage(adq_rate),
            AdqStage(self.http_interface),
            ImageConversionStage(),
            ArucoStage(),
            PositionControlStage(self.http_interface)
        ])

    def get_last_frame(self):
        return self.get_consumer_output()


class FiringStage(Producer):
    def __init__(self, adq_rate):
        super().__init__()
        self._sleep_seconds = 1.0 / adq_rate

    def _produce(self):
        time.sleep(self._sleep_seconds)
        return ()


class AdqStage(PipelineStage):
    def __init__(self, http_interface: RobotHttpInterface):
        super().__init__()
        self._http_interface = http_interface

    def _process(self, _):
        return self._http_interface.get_image()


class ImageConversionStage(PipelineStage):
    def _process(self, in_data):
        response_content = in_data
        return np.array(Image.open(io.BytesIO(response_content)))


class ArucoStage(PipelineStage):
    def __init__(self, target_marker: int = -1):
        super().__init__()
        self._last_marker = target_marker

        self.corners = None
        self.image = None

        self.parameters = aruco.DetectorParameters_create()
        import aruco_utils
        self.dictionary = aruco_utils.get_custom_dict()

    def _process(self, in_data):
        img = in_data

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.dictionary, parameters=self.parameters)
        if ids is None:
            ids = []
        else:
            ids = ids.flatten().tolist()

        # Get best marker for gripper pose
        (my_marker, marker_pos) = self._get_marker(ids=ids)

        if my_marker is None:
            return img, None, None

        return img, corners[marker_pos], my_marker

    def _get_marker(self, ids):
        """
        Parses an ArUco ids vector and gets the index for the last used marker, or
        simply the first one found if the last one was not seen. Returns -1 if nothing found.
        """
        if len(ids) == 0:
            return None, None
        marker_idx = self._find_marker(ids, self._last_marker)
        if marker_idx != -1:
            return self._last_marker, marker_idx
        else:
            self._last_marker = ids[0]
            return ids[0], 0

    @staticmethod
    def _find_marker(ids, marker_num):
        """
        Finds index of marker #marker_num in the ArUco ids vector. If not found, returns -1.
        """
        for i, id in enumerate(ids):
            if id == marker_num:
                return i
        return -1


class PositionControlStage(Consumer):
    def __init__(self, http_interface: RobotHttpInterface):
        super().__init__()
        self._http_interface = http_interface
        self._stopped = True

        shape = (480, 640)
        self.pid_x = PID(Kp=0.001, Ki=0.0, Kd=0.0, setpoint=1000)
        self.pid_y = PID(Kp=0.005, Ki=0.0, Kd=0.0, setpoint=shape[1] / 2)
        self.pid_z = PID(Kp=0.01, Ki=0.0, Kd=0.0, setpoint=shape[0] / 2)
        self.pid_az = PID(Kp=0.025, Ki=0.0, Kd=0.0, setpoint=0)

    @staticmethod
    def compute_area(x, y):
        # https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def _consume(self, in_data):
        img, corners, id = in_data
        if corners is not None and not self._stopped:
            """
            corners = array([[[291., 222.],
                [314., 222.],
                [317., 245.],
                [293., 247.]]], dtype=float32)
            """

            x = corners[:, :, 0].flatten()
            y = corners[:, :, 1].flatten()

            area = self.compute_area(x, y)
            cx = np.mean(x)
            cy = np.mean(y)
            slope = np.mean([(y[1] - y[0])/(x[1]-x[0]), (y[3] - y[2])/(x[3] - x[2])])

            # Velocidades respecto cámara
            # X positivo: hacia alante
            # Y positivo: hacia derecha
            # Z positivo: hacia abajo

            vx = self.pid_x(area)
            vy = -self.pid_y(cx)
            vz = -self.pid_z(cy)
            az = self.pid_az(slope)

            self._http_interface.set_velocity(vx, vy, vz, az, 100.0)

            img = aruco.drawDetectedMarkers(img.copy(), [corners], np.array([[id]]))
        else:
            self._http_interface.stop()
        return img

    def stop_visual_servoing(self):
        self._stopped = True
        self._http_interface.stop()

    def resume_visual_servoing(self):
        self._stopped = False

    def is_stopped(self):
        return self._stopped

    def _on_stopped(self):
        self._http_interface.stop()
