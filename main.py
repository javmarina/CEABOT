import io
import tkinter as tk
import numpy as np
from PIL import Image
from cv2 import cv2

from utils import RobotModel, RobotHttpInterface
from interface_class.launch import launch


if __name__ == '__main__':
    robot_model = RobotModel.BLUE_ROV
    bluerov_http = RobotHttpInterface(robot_model)
    robot_model = RobotModel.GIRONA_500_1
    girona1_http = RobotHttpInterface(robot_model)
    robot_model = RobotModel.GIRONA_500_2
    girona2_http = RobotHttpInterface(robot_model)

    root = tk.Tk()
    # TODO: interfaz Tkinter
    launch(root, girona1_http, girona2_http, bluerov_http)

    # while True:
    #     content = robot_http.get_image_udp(width=320, quality=50)
    #     im = np.array(Image.open(io.BytesIO(content)))
    #     cv2.imshow("a", im)
    #     # TODO: procesar imagen (tracking)