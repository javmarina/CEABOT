import tkinter as tk

from ImagePipeline import ImagePipeline
from interface_class.CameraClient import CameraClient
from interface_class.ControlWindowGirona import ControlWindow
from interface_class.ControlWindowLF import VisionLeaderFollowerMissionClient
from utils import RobotModel, RobotHttpInterface


def main():
    root = tk.Tk()

    def close():
        root.destroy()
        exit(0)

    ## Main window (host)
    root.geometry("50x50+10+10")
    label1 = tk.Label(root, text="MAIN WINDOW")
    label1.pack()
    buttonClose = tk.Button(root, text="CLOSE ALL", command=close)
    buttonClose.pack()

    girona1_http = RobotHttpInterface(RobotModel.GIRONA_500_1)
    girona2_http = RobotHttpInterface(RobotModel.GIRONA_500_2)
    bluerov_http = RobotHttpInterface(RobotModel.BLUE_ROV)

    ## Girona cameras
    c1 = CameraClient(root, "320x262+10+100", "G500_1 Camera (Yellow)", girona1_http)
    c2 = CameraClient(root, "320x262+350+100", "G500_2 Camera (Red)", girona2_http)

    ## Girona controllers
    r1 = ControlWindow(root, "320x260+10+420", "G500_1 Control (Yellow)", girona1_http)
    r2 = ControlWindow(root, "320x260+350+420", "G500_2 Control (Red)", girona2_http)

    ## BlueRov camera
    pipeline = ImagePipeline("localhost", bluerov_http, 10)
    cB = VisionLeaderFollowerMissionClient(root, "375x262+690+100", "BlueROV Camera", pipeline)

    ## BlueRov Control
    blueRov = ControlWindow(root, "320x260+690+420", "BlueROV Control", bluerov_http)

    c1.start()
    c2.start()
    cB.start()
    pipeline.start()
    root.mainloop()


if __name__ == '__main__':
    main()
