import numpy as np
import tkinter as tk
from tkinter import filedialog

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
        print("Loading complete!")
        

def fileImport(name):

    root = tk.Tk()
    root.withdraw()
    path = str(filedialog.askdirectory())
    filePath = (path + "\\LA-200\\NVG_2012_S4_A_LA_00203_CalInertialAndMag.csv")
    #fileName = filedialog.askopenfilename(title = ("Select", name, "file"),filetypes = (("csv files","*.csv"),("all files","*.*")))
    dataArray = np.genfromtxt(filePath, delimiter=',', skip_header=1)
    return dataArray

#fileImport("test")