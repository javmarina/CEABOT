import tkinter as tk
from interface_class.CameraClient import CameraClient
from interface_class.ControlWindowGirona import ControlWindow

def launch(root, r1, r2, br):

    ## Main window (host)
    root.geometry("50x50+10+10")
    label1 = tk.Label(root, text="MAIN WINDOW")
    label1.pack()
    buttonClose = tk.Button(root, text="CLOSE ALL", command=root.destroy)
    buttonClose.pack()

    ## Girona cameras
    c1 = CameraClient(root, "300x300+200+10", "Camera_1", r1)
    c2 = CameraClient(root, "300x300+200+10", "Camera_2", r2)

    ## Girona controllers
    r1 = ControlWindow(root,"200x400+300+10", "Yellow_robot", r1)
    r2 = ControlWindow(root, "200x400+300+10", "Red_robot", r2)

    ## BlueRov camera
    cB = CameraClient(root, "300x300+200+10", "Camera_BlueRov", br)

    ## BlueRov Control
    blueRov = ControlWindow(root,"200x400+300+10", "BlueRov", br)

    c1.start()
    c2.start()
    cB.start()
    root.mainloop()