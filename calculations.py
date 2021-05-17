import numpy as np
import math
import arrayHandler as arrH
import statistics as stat
import gaitFinder

class Calculations():
    def __init__(self, dataArrays):
        self.startTime = 0
        self.stopTime = 0
        self.dataArr = np.array([0])
        self.timeArr = np.array([0])
        self.dataArrays = arrH.DataArrays()

    def setDt(self, dataTime, dataArray):
        timeStart = dataTime[0, 4]*3600 + dataTime[0, 5]*60 + dataTime[0, 6]
        last = len(dataTime[:,0]) - 1
        timeStop = dataTime[last, 4]*3600 + dataTime[last, 5]*60 + dataTime[last, 6]
        timeTotal = timeStop - timeStart
        self.dt = timeTotal / len(dataArray[:,0])

    def setArrayHandler(self, dataArrays):
        self.dataArrays = dataArrays

    def setDataArray(self, startSek, stopSek, indexStart, indexStop):
        T = self.dataArrays.timeConversion("dataArray",indexStart,indexStop)
        cutArr = self.dataArrays.getArray("dataArray")[indexStart:indexStop, :]
        if (startSek >= 1):
            intvalTimeStart = math.floor((len(cutArr)/(T[len(T)-1]-T[0]))*(startSek-1))
        else:
            intvalTimeStart = math.floor((len(cutArr)/(T[len(T)-1]-T[0]))*(startSek))
        if (stopSek < T[len(T)-1]-5):
            intvalTimeStop = math.floor((len(cutArr)/(T[len(T)-1]-T[0]))*(stopSek+5))
        else:
            intvalTimeStop = math.floor((len(cutArr)/(T[len(T)-1]-T[0]))*(stopSek))
        self.startTime = startSek
        self.stopTime = stopSek
        self.dataArr = cutArr[intvalTimeStart:intvalTimeStop,:]
        self.timeArr = T[intvalTimeStart:intvalTimeStop]

    def getGaits(self):
        self.gf = gaitFinder.GaitFinder(self.dataArr, self.dt)
        

    def betDetection(self, startIndex, stopIndex):
        dataArray = self.dataArrays.getArray("dataArray")
        def getPoints(dataArray, RMS):
            packets = []
            points = dataArray[startIndex:stopIndex,0][np.nonzero(dataArray[startIndex:stopIndex,5] > 2.4*RMS)]           #Assign acc(Z)Value > 1.7xRMS to corrresponding packet
            for i in range (1,points.size):                                         #Assign packets that lies withing sf/2,
                if points[i]-points[i-1] < sampleFrekvens/2:
                    packets.append(points[i])
            return packets
        
        sampleFrekvens = self.dataArrays.getDataRate(self.dataArrays.getArray("dataRegist")[69,2])             #DataRate for inertia and mag
        aproxSekvensTime = 3
        dataSelection = []
        Square = 0

        for i in range(0,len(dataArray)):
            Square += dataArray[i,5]**2
        RMS = math.sqrt(Square/len(dataArray))

        packets = getPoints(dataArray, RMS)
        for i in range(1, len(packets)-1):                                      #Remove nearby packets and remain with farends of "packet-group"
            if( i == 1 and (packets[i] - packets[i-1] < aproxSekvensTime*sampleFrekvens*50)):
                dataSelection.append(packets[0])
            elif( packets[i] - packets[i-1] > aproxSekvensTime*sampleFrekvens*20):
                dataSelection.append(packets[i])
            elif( packets[i+1] - packets[i] > aproxSekvensTime*sampleFrekvens*20):
                dataSelection.append(packets[i])
            elif( i == (len(packets)-2) and (packets[i+1] - packets[i] < aproxSekvensTime*sampleFrekvens*50)):
                dataSelection.append(packets[i+1])

        betData = []
        if(len(dataSelection)%2 == 0 and len(dataSelection) >= 2):
            if (len(dataSelection) == 2):
                betData.append(dataSelection[0])
                betData.append(dataSelection[1])
            else:
                for i in range(1,(len(dataSelection))):
                    if (i%2 != 0 and (dataSelection[i]-dataSelection[i-1]) > aproxSekvensTime*sampleFrekvens*120):
                        betData.append(dataSelection[i-1])
                        betData.append(dataSelection[i])
        indexes = []
        if( len(betData) >=2):
            for packet in betData:
                indexes.append(np.where(dataArray[:,0] == packet))
        return indexes

    def stepFrequency(self):
        fqArray = []
        stpFreq = []
        cutXArr = self.dataArr[:,4]
        T = self.timeArr[:]
        startSek = self.startTime
        stopSek = self.stopTime
        
        pointsInInterval = T[np.nonzero(cutXArr > 0.4*stat.mean(cutXArr))]              #(experimental "top" value)
        fqArray.append(pointsInInterval[0])
        for i in range(1, len(pointsInInterval)):
            if ( (pointsInInterval[i] - (pointsInInterval[0]+(stopSek-startSek)) < ((pointsInInterval[0]+(stopSek-startSek))-fqArray[len(fqArray)-1])) and (pointsInInterval[i]-fqArray[len(fqArray)-1]) > 0.61):   #(experimental time value)
                fqArray.append(pointsInInterval[i])
                if (len(fqArray) >= 2):
                    stpFreq.append(1/(pointsInInterval[i]-fqArray[len(fqArray)-2]))       #Converted to Hz (step/second)
                if (len(stpFreq) == 2):
                    if (stpFreq[0] > 1.4*stpFreq[1]):                                     #Remove intitial step that is too short (experimental frequency value)
                        fqArray.remove(fqArray[0])
                        stpFreq.remove(stpFreq[0]) 
        return stpFreq
    
    def newMeasurements(self):
        steps = len(self.gf.splits) - 1
        stepFq = stat.mean(self.gf.fqs)
        fqStdev = stat.stdev(self.gf.fqs)


        return steps, stepFq, fqStdev
