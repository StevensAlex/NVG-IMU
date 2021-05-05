import numpy as np
import math 

class DataArrays():
    def _init_(self):
        self.dataTime = np.array([0])
        self.dataRegist = np.array([0])
        self.dataArray = np.array([0])
        self.eulerArray = np.array([0])
        self.rotationArray = np.array([0])
        self.dataQt = np.array([0])
        self.neckArray = np.array([0])
        self.neckTime = np.array([0])
        self.nEulArray = np.array([0])
        self.neckRegister = np.array([0])
    
    def setArrays(self,subject):
        self.dataTime = subject.LAtimeArray
        self.dataRegist = subject.LAregArray
        self.dataArray = subject.LAcalArray
        self.eulerArray = subject.LAeulerArray
        self.rotationArray = subject.LArotationArray
        self.dataQt = subject.LAquaternionArray
        self.neckArray = subject.NcalArray
        self.neckTime = subject.NtimeArray
        self.nEulArray = subject.NeulerArray
        self.neckRegister = subject.NregArray

    def getArray(self,argument):
        switcher = {
        "dataTime": self.dataTime,
        "dataRegist": self.dataRegist,
        "dataArray": self.dataArray,
        "eulerArray": self.eulerArray,
        "rotationArray": self.rotationArray,
        "dataQt": self.dataQt,
        "neckArray": self.neckArray,
        "neckTime": self.neckTime,
        "nEulArray": self.nEulArray,
        "neckRegister": self.neckRegister
        }
        return switcher.get(argument, 0)

    def timeConversion(self, argument, startSession, stopSession):  #Timeconversion from packets of selected arraylength starting at 0:
        packetArr = DataArrays.getArray(self,argument)
        if (argument == "dataArray" or argument == "eulerArray"):
            timeArray = DataArrays.getArray(self,"dataTime")
            register = DataArrays.getArray(self, "dataRegist")
        elif (argument == "neckArray" or argument == "nEulArray"):
            timeArray = DataArrays.getArray(self,"neckTime")
            register = DataArrays.getArray(self, "neckRegister")

        sampleFrekvens = DataArrays.getDataRate(register[69,2])                 #position in register for data rate acquisition
        if (startSession <= 0):
            timeStart = timeArray[0, 4]*3600 + timeArray[0, 5]*60 + timeArray[0, 6]
        else:
            for i in range(0, len(timeArray)):
                if( timeArray[i,0] <= (packetArr[startSession,0] + sampleFrekvens)):# and timeArray[i,0] >= (packetArr[startSession,0] - sampleFrekvens)):
                    timeStart = timeArray[i, 4]*3600 + timeArray[i, 5]*60 + timeArray[i, 6]
        if (stopSession >= (len(packetArr)-1)):
            timeStop = timeArray[(len(timeArray)-1), 4]*3600 + timeArray[(len(timeArray)-1), 5]*60 + timeArray[(len(timeArray)-1), 6]
        else:
            for i in range(0, len(timeArray)):
                if( timeArray[i,0] <= (packetArr[stopSession,0] + sampleFrekvens)):# and timeArray[i,0] >= (packetArr[stopSession,0] - sampleFrekvens)):
                    timeStop = timeArray[i, 4]*3600 + timeArray[i, 5]*60 + timeArray[i, 6]
        
        sessionTime = timeStop - timeStart

        cutPacks = packetArr[startSession:stopSession,0]
        T = np.empty((len(cutPacks)), dtype = float)
        for i in range(0, len(cutPacks)):
            T[i] = i*(sessionTime/len(cutPacks))
        return T

    def getDataRate(argument):
        switcher = {
            0x0000: "Disabled",
            0x0001: 1,
            0x0002: 2,
            0x0003: 4,
            0x0004: 8,
            0x0005: 16,
            0x0006: 32,
            0x0007: 64,
            0x0008: 128,
            0x0009: 256,
            0x000A: 512
        }
        return switcher.get(argument, 0)

    def getIndexFromTime(self, argument, time):
        packetArr = DataArrays.getArray(self,argument)
        sessionTime = DataArrays.timeConversion(self,"dataArray",0,(len(packetArr)))[(len(packetArr)-1)]        #Total trial time
        if(time <= 0):
            time = 0
        if(time >= sessionTime):
            time = sessionTime
        self.index = math.floor((len(packetArr)/sessionTime)*(time))
        return self.index

