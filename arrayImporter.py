import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

class Subject():
    def __init__(self):
        root = tk.Tk()
        root.withdraw()
        path = str(filedialog.askdirectory())

        #import IMU's being used
        print("Loading data, this may take a while")
        LAcalPath = (path + "\\LA-200\\NVG_2012_S4_A_LA_00203_CalInertialAndMag.csv")
        LAtimePath = (path + "\\LA-200\\NVG_2012_S4_A_LA_00203_DateTime.csv")
        LAregPath = (path + "\\LA-200\\NVG_2012_S4_A_LA_00203_Registers.csv")

        self.LAcalArray = np.genfromtxt(LAcalPath, delimiter=',', skip_header=1)
        self.LAtimeArray = np.genfromtxt(LAtimePath, delimiter=',', skip_header=1)
        self.LAregArray = np.genfromtxt(LAregPath, delimiter=',', skip_header=1)
        self.LAeulerArray = np.genfromtxt(LAeulerPath, delimiter=',', skip_header=1)
        self.LArotationArray = np.genfromtxt(LArotationPath, delimiter=',', skip_header=1)
        print("Loading complete!")
        