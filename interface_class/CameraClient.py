import numpy as np
import cv2
from threading import Thread
import tkinter as tk
import PIL.Image, PIL.ImageTk
import time
from utils import RobotHttpInterface


class CameraClient(Thread):
    def __init__(self, root, geometryString, name, robot: RobotHttpInterface):
        Thread.__init__(self)
        self.root = root
        self.name = name
        self.robot = robot
        self.cameraWindow = tk.Toplevel(root)
        self.label = tk.Label(self.cameraWindow, text=self.robot._camera_url)
        self.label.grid(row=0, column=0, columnspan=3)

        self.cameraWindow.title(name)
        self.cameraWindow.geometry(geometryString)

        self.imageScalePercentage = 50
        self.exit = False
        self.gap = 0.02
        self.image = None
        self.width = 315
        self.height = 235
        self.canvas = tk.Canvas(self.cameraWindow, width=self.width, height=self.height)
        self.canvas.grid(row=1, rowspan=6, column=0, columnspan=1, sticky="nswe")

    def getImage(self):
        img = self.url_to_image()
        w = int(img.shape[1] * (self.imageScalePercentage / 100))
        h = int(img.shape[0] * (self.imageScalePercentage / 100))
        img = cv2.resize(img, dsize=(w, h), interpolation=cv2.INTER_AREA)
        return img

    def url_to_image(self, readFlag=cv2.IMREAD_COLOR):
        resp = self.robot.get_image()
        image = np.asarray(bytearray(resp), dtype="uint8")
        image = cv2.imdecode(image, readFlag)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def run(self):
        while (not self.exit):
            self.image = self.getImage()
            imageForCanvas = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.image))
            self.canvas.create_image(self.width/2, self.height/2, image=imageForCanvas, anchor=tk.CENTER)
            time.sleep(self.gap)