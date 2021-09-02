import tkinter as tk

import numpy as np

from ImagePipeline import ImagePipeline
from interface_class.CameraClient import CameraClient


class VisionLeaderFollowerMissionClient(CameraClient):
    def __init__(self, root, geometryString, name, pipeline: ImagePipeline):
        super().__init__(root, geometryString, name, pipeline.http_interface)

        self.root = root
        self.pipeline = pipeline

        self.buttonShowMarkers = tk.Button(self.cameraWindow, text="Markers", command=self.applyDetectMarker)
        self.buttonShowMarkers.grid(row=6, rowspan=1, column=1, columnspan=2, sticky="nswe")

        self.detectMarkers = False

    def applyDetectMarker(self):
        self.detectMarkers = not self.detectMarkers
        if self.detectMarkers:
            self.pipeline[-1].resume_visual_servoing()
        else:
            self.pipeline[-1].stop_visual_servoing()

    def getImage(self):
        img = self.pipeline.get_last_frame()
        if img is None:
            img = np.zeros((480, 640))
        return img
