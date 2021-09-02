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
    c1 = CameraClient(root, "300x300+200+10", "Camera_1", girona1_http)
    c2 = CameraClient(root, "300x300+200+10", "Camera_2", girona2_http)

    ## Girona controllers
    r1 = ControlWindow(root, "200x400+300+10", "Yellow_robot", girona1_http)
    r2 = ControlWindow(root, "200x400+300+10", "Red_robot", girona2_http)

    ## BlueRov camera
    pipeline = ImagePipeline("localhost", bluerov_http, 10)
    cB = VisionLeaderFollowerMissionClient(root, "300x300+200+10", "Camera_BlueRov", pipeline)

    ## BlueRov Control
    blueRov = ControlWindow(root, "200x400+300+10", "BlueRov", bluerov_http)

    c1.start()
    c2.start()
    cB.start()
    pipeline.start()
    root.mainloop()


if __name__ == '__main__':
    main()
