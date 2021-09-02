import tkinter as tk
from utils import RobotHttpInterface


class ControlWindow:
    def __init__(self, root, geometryString, name, robot: RobotHttpInterface):
        self.root = root
        self.name = name
        self.robot = robot

        self.robotWindow = tk.Toplevel(root)
        self.robotWindow.geometry(geometryString)
        self.robotWindow.title(self.name)

        self.label = tk.Label(self.robotWindow, text=robot._movement_url)
        self.label.grid(row=0, sticky="n", columnspan=3)

        self.w = 7
        self.h = 3

        self.pos = ["", "", ""]

        #### Grid de botones de control ####
        self.robotFw = tk.Button(self.robotWindow, text="\u2B9D", command=self.robot.forward)
        self.robotFw.config(height=self.h, width=self.w)
        self.robotFw.grid(row=1, column=1, columnspan=1, sticky="WE")

        self.robotL = tk.Button(self.robotWindow, text="\u2B9C", command=self.robot.move_left)
        self.robotL.configure(height=self.h, width=self.w)
        self.robotL.grid(row=2, column=0, columnspan=1, sticky="WE")

        self.robotR = tk.Button(self.robotWindow, text="\u2B9E", command=self.robot.move_right)
        self.robotR.configure(height=self.h, width=self.w)
        self.robotR.grid(row=2, column=2, columnspan=1, sticky="WE")

        self.robotBw = tk.Button(self.robotWindow, text="\u2B9F", command=self.robot.backward)
        self.robotBw.configure(height=self.h, width=self.w)
        self.robotBw.grid(row=3, column=1, columnspan=1, sticky="WE")

        self.robotStop = tk.Button(self.robotWindow, text="\u23F8", command=self.robot.stop)
        self.robotStop.configure(height=self.h, width=self.w)
        self.robotStop.grid(row=2, column=1, columnspan=1, sticky="WE")

        self.robotTl = tk.Button(self.robotWindow, text="\u2B6E", command=self.robot.turn_left)
        self.robotTl.configure(height=self.h, width=self.w)
        self.robotTl.grid(row=3, column=0, columnspan=1, sticky="WE")

        self.robotTr = tk.Button(self.robotWindow, text="\u2B6F", command=self.robot.turn_right)
        self.robotTr.configure(height=self.h, width=self.w)
        self.robotTr.grid(row=3, column=2, columnspan=1, sticky="WE")

        self.robotUp = tk.Button(self.robotWindow, text="\u2303", command=self.robot.move_up)
        self.robotUp.configure(height=self.h, width=self.w)
        self.robotUp.grid(row=1, column=2, columnspan=1, sticky="WE")

        self.robotDown = tk.Button(self.robotWindow, text="\u2304", command=self.robot.move_down)
        self.robotDown.configure(height=self.h, width=self.w)
        self.robotDown.grid(row=1, column=0, columnspan=1, sticky="WE")
        #### --------------------------- ####

        self.separator = tk.Label(self.robotWindow, text=" ")
        self.separator.grid(row=0, column=4, rowspan=10)

        ####  Slider para control de velocidad ####
        self.sliderVel = tk.Scale(self.robotWindow, from_=0, to=200, sliderlength=10, width=10,
                                  orient=tk.VERTICAL, command=self.setVelocityPctg)
        self.sliderVel.set(0)
        self.sliderVel.grid(row=1, column=5, columnspan=1, rowspan=2, sticky="WENS")

        self.label2 = tk.Label(self.robotWindow, text="% Z Vel")
        self.label2.grid(row=0, column=5, sticky="WE", columnspan=1)
        #### --------------------------------- ####

        #### Tomar posición actual (x, y, z) ####
        txt = "Get Position\n\n" + self.name.split(" ")[0]
        self.buttonGetPos = tk.Button(self.robotWindow, text=txt, command=self.getPosition)
        self.buttonGetPos.configure(height=self.h, width=self.w * 2)
        self.buttonGetPos.grid(row=3, column=5, columnspan=2, rowspan=1, sticky="WENS")

        self.labelPosX = tk.Label(self.robotWindow, text=self.pos[0])
        self.labelPosX.config(font=('TkDefaultFont', 8))
        self.labelPosX.grid(row=4, column=5, columnspan=2, sticky="W")
        self.labelPosY = tk.Label(self.robotWindow, text=self.pos[1])
        self.labelPosY.config(font=('TkDefaultFont', 8))
        self.labelPosY.grid(row=5, column=5, columnspan=2, sticky="W")
        self.labelPosZ = tk.Label(self.robotWindow, text=self.pos[2])
        self.labelPosZ.config(font=('TkDefaultFont', 8))
        self.labelPosZ.grid(row=6, column=5, columnspan=2, sticky="W")
        #### ------------------------------- ####

        ### Controlar Gripper ###
        self.buttonOpenG = tk.Button(self.robotWindow, text="Open\nGripper", command=self.robot.open_gripper)
        self.buttonOpenG.grid(row=5, column=0, rowspan=2, sticky="NSWE")
        self.buttonCloseG = tk.Button(self.robotWindow, text="Close\nGripper", command=self.robot.close_gripper)
        self.buttonCloseG.grid(row=5, column=1, rowspan=2, sticky="NSWE")
        self.buttonStopG = tk.Button(self.robotWindow, text="Stop\nGripper", command=self.robot.stop_gripper)
        self.buttonStopG.grid(row=5, column=2, rowspan=2, sticky="NSWE")
        ### ----------------- ###

    def setVelocityPctg(self, val):
        self.robot.set_velocity(0, 0, 0.1, val)

    def setVelocity(self, x_vel, y_vel, z_vel, za_vel, vel_pctg):
        self.robot.set_velocity(x_vel, y_vel, z_vel, za_vel, vel_pctg)

    def getPosition(self):
        self.pos = self.robot.get_position()
        return self.pos[0], self.pos[1], self.pos[2]
