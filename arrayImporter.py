import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
import re

class Subject():
    def __init__(self):
        root = tk.Tk()
        self.file_path = ''
        root.withdraw()
        try:
            path = str(filedialog.askdirectory())
            files = os.listdir(path)
            #import IMU's being used
            print("Loading data, this may take a while")
            self.file_path = path
            #LA
            patternLA = 'LA-200'
            comparePat = re.compile(patternLA)
            if (patternLA in files or comparePat.search(path)):
                if patternLA in files:
                    LAPath = path + "/" + patternLA + "/"
                else:
                    LAPath = path + "/"
                print("Loading LA-200")
                filesLA = os.listdir(LAPath)
                for file in filesLA:
                    if 'CalInertial' in file:
                        LAcalPath = LAPath + file
                    elif 'Registers' in file:
                        LAregPath = LAPath + file
                    elif 'DateTime' in file:
                        LAtimePath = LAPath + file
        
                self.LAcalArray = np.genfromtxt(LAcalPath, delimiter=',', skip_header=1)
                self.LAtimeArray = np.genfromtxt(LAtimePath, delimiter=',', skip_header=1)
                self.LAregArray = np.genfromtxt(LAregPath, delimiter=',', skip_header=1)
                print("Loading LA-200 complete!")

            #N
            patternN = 'N-600'
            comparePat = re.compile(patternN)
            if (patternN in files or comparePat.search(path)):
                if patternN in files:
                    NPath = path + "/" + patternN + "/"
                else:
                    NPath = path + "/"
                print("Loading N-600")
                filesN = os.listdir(NPath)
                for file in filesN:
                    if 'CalInertial' in file:
                        NcalPath = NPath + file
                    elif 'Registers' in file:
                        NregPath = NPath + file
                    elif 'DateTime' in file:
                        NtimePath = NPath + file
        
                self.NcalArray = np.genfromtxt(NcalPath, delimiter=',', skip_header=1)
                self.NtimeArray = np.genfromtxt(NtimePath, delimiter=',', skip_header=1)
                self.NregArray = np.genfromtxt(NregPath, delimiter=',', skip_header=1)
                print("Loading N-600 complete!")
            print("Loading complete!")
        except FileNotFoundError:
            print("Loading failed!")
