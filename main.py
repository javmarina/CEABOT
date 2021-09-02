import io
import tkinter as tk
import numpy as np
from PIL import Image
from cv2 import cv2

from utils import RobotModel, RobotHttpInterface


if __name__ == '__main__':
    robot_model = RobotModel.BLUE_ROV
    robot_http = RobotHttpInterface(robot_model)

    root = tk.Tk()
    # TODO: interfaz Tkinter

    while True:
        content = robot_http.get_image_udp(width=320, quality=50)
        im = np.array(Image.open(io.BytesIO(content)))
        cv2.imshow("a", im)
        # TODO: procesar imagen (tracking)
