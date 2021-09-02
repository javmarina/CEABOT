import tkinter as tk

def launch(root):

    ## Main window (host)
    root.geometry("50x50+10+10")
    label1 = tk.Label(root, text="MAIN WINDOW")
    label1.pack()
    buttonClose = tk.Button(root, text="CLOSE ALL", command=root.destroy)
    buttonClose.pack()

    ## Girona cameras