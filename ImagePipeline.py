import io
import time

import cv2 as cv
import numpy as np
from PIL import Image
from cv2 import aruco

from utils import RobotModel, RobotHttpInterface
from pipeline.Pipeline import StraightPipeline
from pipeline.PipelineStage import Producer, PipelineStage, Consumer
from visual_servoing.visual_servoing import VisualServoing


class ImagePipeline(StraightPipeline):
    def __init__(self, address: str, http_interface: RobotHttpInterface, adq_rate):
        if address == "localhost":
            # Avoid DNS resolve for localhost
            address = "127.0.0.1"
        self.http_interface = http_interface

        final_camera_depth = 0.005  # Regulates velocity

        shape = (480, 640)
        cx = shape[1] / 2
        cy = shape[0] / 2
        tag_size = 40

        base = np.array([[[cx - tag_size / 2, cy - tag_size / 2],
                          [cx + tag_size / 2, cy - tag_size / 2],
                          [cx + tag_size / 2, cy + tag_size / 2],
                          [cx - tag_size / 2, cy + tag_size / 2]]])

        # Ver https://www.pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/
        desired_corners = base.flatten()
        dist_tol = 0.5

        super().__init__([
            FiringStage(adq_rate),
            AdqStage(self.http_interface),
            ImageConversionStage(),
            ArucoStage(),
            VisualServoingStage(self.http_interface, final_camera_depth, desired_corners, dist_tol)
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

        return img, corners[marker_pos], marker_pos

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


class VisualServoingStage(Consumer):
    def __init__(self, http_interface: RobotHttpInterface, final_camera_depth, desired_corners, dist_tol):
        super().__init__()
        self._http_interface = http_interface
        self._stopped = False

        self._vs = VisualServoing(ibvs=True)
        self._dist_tol = dist_tol
        Z = final_camera_depth
        ideal_cam_pose = np.array([0, 0, Z])
        self._vs.set_target(ideal_cam_pose, None, desired_corners)

    def _consume(self, in_data):
        img, corners, id = in_data
        if corners is not None and not self._stopped:
            """
            corners = array([[[291., 222.],
                [314., 222.],
                [317., 245.],
                [293., 247.]]], dtype=float32)
            """

            servo_vel, error = self._vs.get_next_vel(corners=corners)
            vx, vy, vz, wx, wy, wz = servo_vel
            if np.linalg.norm(error) < self._dist_tol:
                self.stop_visual_servoing()
            else:
                # Velocidades respecto cámara
                # X positivo: hacia alante
                # Y positivo: hacia derecha
                # Z positivo: hacia abajo
                self._http_interface.set_velocity(x=vz, y=vx, z=vy, az=-wy)  # TODO: comprobar
                print(servo_vel)

            img = aruco.drawDetectedMarkers(img.copy(), [corners], np.array([[id]]))
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
