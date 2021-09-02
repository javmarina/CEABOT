#!/usr/bin/env python
"""
Performs eye in hand (eih) image based visual servoing (ibvs). 
Written by Alex Zhu (alexzhu(at)seas.upenn.edu)
"""
import time

from utils import RobotHttpInterface
from visual_servoing.aruco_client import ArucoClient
from visual_servoing.visual_servoing import VisualServoing
from utility import *


class IbvsEih:
    """
    Performs eye in hand (eih) image based visual servoing (ibvs). 
    """

    def __init__(self, robot_http_interface: RobotHttpInterface):
        self._robot_http_interface = robot_http_interface

        # ArUco specific code. You don't need this if you're using another tracking system.
        # Initializes the marker that the arm should track
        target_marker = 0
        self._aruco_client = ArucoClient(target_marker)

        self._visual_servo = VisualServoing(ibvs=True)

        self.pause = False  # To stop the controller in the middle of the process.

    def new_image_arrived(self):
        """
        Boolean to test if a new image has arrived.
        """
        if self._aruco_client.corners is not None:
            self._aruco_client.corners = None
            return True
        return False

    def _get_detected_corners(self):
        """
        Returns the most recently detected corners in the image.
        """
        return self._aruco_client.corners

    def _command_velocity(self, vel):
        """
        Move the camera at the specified v and omega in vel (6x1 vector).
        """
        vx, vy, vz, wx, wy, wz = vel
        self._robot_http_interface.set_velocity(vx, vy, vz, wz)

    def set_target(self, final_camera_depth, desired_corners):
        """
        Sets the final camera depth (Z) and desired position for the tracked features
        at the goal position.
        """
        Z = final_camera_depth
        ideal_cam_pose = np.array([0, 0, Z])
        self._visual_servo.set_target(ideal_cam_pose, None, desired_corners)

    def move_to_position(self, final_camera_depth, desired_corners, dist_tol):
        """
        Runs one instance of the visual servoing control law. Call when a new
        image has arrived.
        """
        self.set_target(final_camera_depth, desired_corners)
        error = np.inf
        while np.linalg.norm(error) > dist_tol and not self.pause:
            if not self.new_image_arrived():
                continue

            # Continue if no corners detected
            marker_corners = self._get_detected_corners()
            if marker_corners is None:
                continue

            # Don't move if the target hasn't been set
            if not self._visual_servo._target_set:
                continue

            # Get control law velocity and transform to body frame, then send to robot
            servo_vel, error = self._visual_servo.get_next_vel(corners=marker_corners)
            self._command_velocity(servo_vel)
            time.sleep(1/60)
