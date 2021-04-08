import numpy as np
import tkinter as tk
from tkinter import filedialog

class Subject():
    def __init__(self):
        root = tk.Tk()
        root.withdraw()
        path = str(filedialog.askdirectory())
        if path != str():
            
            #import IMU's being used
            print("Loading data, this may take a while")

        #LA
        LAPath = path + "\\LA-200\\"
        files = os.listdir(LAPath)
        for file in files:
            if 'CalInertial' in file:
                LAcalPath = LAPath + file
            elif 'Registers' in file:
                LAregPath = LAPath + file
            elif 'DateTime' in file:
                LAtimePath = LAPath + file
        
        self.LAcalArray = np.genfromtxt(LAcalPath, delimiter=',', skip_header=1)
        self.LAtimeArray = np.genfromtxt(LAtimePath, delimiter=',', skip_header=1)
        self.LAregArray = np.genfromtxt(LAregPath, delimiter=',', skip_header=1)
        print("Loading complete!")
        