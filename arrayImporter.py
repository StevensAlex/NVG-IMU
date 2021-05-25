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
            #LA - left ankle
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
            #N - neck
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
#            #RA - right ankle
#            patternRA = 'RA-100'
#            comparePat = re.compile(patternRA)
#            if (patternRA in files or comparePat.search(path)):
#                if patternRA in files:
#                    RAPath = path + "/" + patternRA + "/"
#                else:
#                    RAPath = path + "/"
#                print("Loading RA-100")
#                filesRA = os.listdir(RAPath)
#                for file in filesRA:
#                    if 'CalInertial' in file:
#                        RAcalPath = RAPath + file
#                    elif 'Registers' in file:
#                        RAregPath = RAPath + file
#                    elif 'DateTime' in file:
#                        RAtimePath = RAPath + file       
#                self.RAcalArray = np.genfromtxt(RAcalPath, delimiter=',', skip_header=1)
#                self.RAtimeArray = np.genfromtxt(RAtimePath, delimiter=',', skip_header=1)
#                self.RAregArray = np.genfromtxt(RAregPath, delimiter=',', skip_header=1)
#                print("Loading RA-100 complete!")
#            #LT - left thigh
#            patternLT = 'LT-400'
#            comparePat = re.compile(patternLT)
#            if (patternLT in files or comparePat.search(path)):
#                if patternLT in files:
#                    LTPath = path + "/" + patternLT + "/"
#                else:
#                    LTPath = path + "/"
#                print("Loading LT-400")
#                filesLT = os.listdir(LTPath)
#                for file in filesLT:
#                    if 'CalInertial' in file:
#                        LTcalPath = LTPath + file
#                    elif 'Registers' in file:
#                        LTregPath = LTPath + file
#                    elif 'DateTime' in file:
#                        LTtimePath = LTPath + file       
#                self.LTcalArray = np.genfromtxt(LTcalPath, delimiter=',', skip_header=1)
#                self.LTtimeArray = np.genfromtxt(LTtimePath, delimiter=',', skip_header=1)
#                self.LTregArray = np.genfromtxt(LTregPath, delimiter=',', skip_header=1)
#                print("Loading LT-400 complete!")
#            #RT - right thigh
#            patternRT = 'RT-300'
#            comparePat = re.compile(patternRT)
#            if (patternRT in files or comparePat.search(path)):
#                if patternRT in files:
#                    RTPath = path + "/" + patternRT + "/"
#                else:
#                    RTPath = path + "/"
#                print("Loading RT-300")
#                filesRT = os.listdir(RTPath)
#                for file in filesRT:
#                    if 'CalInertial' in file:
#                        RTcalPath = RTPath + file
#                    elif 'Registers' in file:
#                        RTregPath = RTPath + file
#                    elif 'DateTime' in file:
#                        RTtimePath = RTPath + file       
#                self.RTcalArray = np.genfromtxt(RTcalPath, delimiter=',', skip_header=1)
#                self.RTtimeArray = np.genfromtxt(RTtimePath, delimiter=',', skip_header=1)
#                self.RTregArray = np.genfromtxt(RTregPath, delimiter=',', skip_header=1)
#                print("Loading RT-300 complete!")
#            #B - back/sacrum
#            patternB = 'B-500'
#            comparePat = re.compile(patternB)
#            if (patternB in files or comparePat.search(path)):
#                if patternB in files:
#                    BPath = path + "/" + patternB + "/"
#                else:
#                    BPath = path + "/"
#                print("Loading B-500")
#                filesB = os.listdir(BPath)
#                for file in filesB:
#                    if 'CalInertial' in file:
#                        BcalPath = BPath + file
#                    elif 'Registers' in file:
#                        BregPath = BPath + file
#                    elif 'DateTime' in file:
#                        BtimePath = BPath + file       
#                self.BcalArray = np.genfromtxt(BcalPath, delimiter=',', skip_header=1)
#                self.BtimeArray = np.genfromtxt(BtimePath, delimiter=',', skip_header=1)
#                self.BregArray = np.genfromtxt(BregPath, delimiter=',', skip_header=1)
#                print("Loading B-500 complete!")
#            #LH - left hand
#            patternLH = 'LH-800'
#            comparePat = re.compile(patternLH)
#            if (patternLH in files or comparePat.search(path)):
#                if patternLH in files:
#                    LHPath = path + "/" + patternLH + "/"
#                else:
#                    LHPath = path + "/"
#                print("Loading LH-800")
#                filesLH = os.listdir(LHPath)
#                for file in filesLH:
#                    if 'CalInertial' in file:
#                        LHcalPath = LHPath + file
#                    elif 'Registers' in file:
#                        LHregPath = LHPath + file
#                    elif 'DateTime' in file:
#                        LHtimePath = LHPath + file       
#                self.LHcalArray = np.genfromtxt(LHcalPath, delimiter=',', skip_header=1)
#                self.LHtimeArray = np.genfromtxt(LHtimePath, delimiter=',', skip_header=1)
#                self.LHregArray = np.genfromtxt(LHregPath, delimiter=',', skip_header=1)
#                print("Loading LH-800 complete!")
#            print("Loading complete!")
#            #RH - right hand
#            patternRH = 'RH-700'
#            comparePat = re.compile(patternRH)
#            if (patternRH in files or comparePat.search(path)):
#                if patternRH in files:
#                    RHPath = path + "/" + patternRH + "/"
#                else:
#                    RHPath = path + "/"
#                print("Loading RH-700")
#                filesRH = os.listdir(RHPath)
#                for file in filesRH:
#                    if 'CalInertial' in file:
#                        RHcalPath = RHPath + file
#                    elif 'Registers' in file:
#                        RHregPath = RHPath + file
#                    elif 'DateTime' in file:
#                        RHtimePath = RHPath + file       
#                self.RHcalArray = np.genfromtxt(RHcalPath, delimiter=',', skip_header=1)
#                self.RHtimeArray = np.genfromtxt(RHtimePath, delimiter=',', skip_header=1)
#                self.RHregArray = np.genfromtxt(RHregPath, delimiter=',', skip_header=1)
#                print("Loading RH-700 complete!")
        except FileNotFoundError:
            print("Loading failed!")
