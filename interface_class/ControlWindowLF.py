import tkinter as tk

import numpy as np

from ImagePipeline import ImagePipeline
from interface_class.CameraClient import CameraClient


class VisionLeaderFollowerMissionClient(CameraClient):
    def __init__(self, root, geometryString, name, pipeline: ImagePipeline):
        super().__init__(root, geometryString, name, pipeline.http_interface)

        self.root = root
        self.pipeline = pipeline

        self.missionLabel = tk.Label(self.cameraWindow, text="LEADER-FOLLOWER\nCONTROL STATE")
        self.missionLabel.grid(row=2, rowspan=1, column=1, columnspan=2)

        self.option = tk.IntVar()
        self.controlOff = tk.Radiobutton(self.cameraWindow, text="OFF", variable=self.option,
                                        value=1, command=self.pipeline[-1].stop_visual_servoing)
        self.controlOff.grid(row=3, rowspan=1, column=1, columnspan=1, sticky="nswe")
        self.controlOn = tk.Radiobutton(self.cameraWindow, text="ON", variable=self.option,
                                        value=2, command=self.pipeline[-1].resume_visual_servoing)
        self.controlOn.grid(row=3, rowspan=1, column=2, columnspan=1, sticky="nswe")


        # self.buttonShowMarkers = tk.Button(self.cameraWindow, text="Markers", command=self.applyDetectMarker)
        # self.buttonShowMarkers.grid(row=6, rowspan=1, column=1, columnspan=2, sticky="nswe")

    def getImage(self):
        img = self.pipeline.get_last_frame()
        if img is None:
            img = np.zeros((480, 640))
        return img
