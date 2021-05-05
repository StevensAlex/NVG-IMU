import numpy as np
import math
import arrayHandler as arrH
import statistics as stat

class Calculations():
    def _init_(self):
        print("hej")

    def betDetection(self, startIndex, stopIndex):
        dataArray = arrH.DataArrays.getArray(self, "dataArray")
        def getPoints(dataArray, RMS):
            packets = []
            points = dataArray[startIndex:stopIndex,0][np.nonzero(dataArray[startIndex:stopIndex,6] > 2.4*RMS)]           #Assign acc(Z)Value > 1.7xRMS to corrresponding packet
            for i in range (1,points.size):                                         #Assign packets that lies withing sf/2,
                if points[i]-points[i-1] < sampleFrekvens/2:
                    packets.append(points[i])
            return packets
        
        sampleFrekvens = arrH.DataArrays.getDataRate(arrH.DataArrays.getArray(self, "dataRegist")[69,2])             #DataRate for inertia and mag
        aproxSekvensTime = 3
        dataSelection = []
        Square = 0

        for i in range(0,len(dataArray)):
            Square += dataArray[i,6]**2
        RMS = math.sqrt(Square/len(dataArray))

        packets = getPoints(dataArray, RMS)
        for i in range(1, len(packets)-1):                                      #Remove nearby packets and remain with farends of "packet-group"
            if( i == 1 and (packets[i] - packets[i-1] < aproxSekvensTime*sampleFrekvens*50)):
                dataSelection.append(packets[0])
            elif( packets[i] - packets[i-1] > aproxSekvensTime*sampleFrekvens*50):
                dataSelection.append(packets[i])
            elif( packets[i+1] - packets[i] > aproxSekvensTime*sampleFrekvens*50):
                dataSelection.append(packets[i])
            elif( i == (len(packets)-2) and (packets[i+1] - packets[i] < aproxSekvensTime*sampleFrekvens*50)):
                dataSelection.append(packets[i+1])

        print(dataSelection)
        indexes = []
        for packet in dataSelection:
            indexes.append(np.where(dataArray[:,0] == packet))
        return indexes

    def stepFrequency(self, startSek, stopSek, indexStart, indexStop):
        fqArray = []
        stpFreq = []
        T = arrH.DataArrays.timeConversion(self,"dataArray",indexStart,indexStop)
        cutXArr = arrH.DataArrays.getArray(self, "dataArray")[indexStart:indexStop, 4]
        #cutXArr = dataArray[indexStart:indexStop, 4]
        if (startSek > 0):
            intvalTimeStart = math.floor((len(cutXArr)/(T[len(T)-1]-T[0]))*(startSek-1))
        else:
            intvalTimeStart = math.floor((len(cutXArr)/(T[len(T)-1]-T[0]))*(startSek))
        if (stopSek < T[len(T)-1]-5):
            intvalTimeStop = math.floor((len(cutXArr)/(T[len(T)-1]-T[0]))*(stopSek+5))
        else:
            intvalTimeStop = math.floor((len(cutXArr)/(T[len(T)-1]-T[0]))*(stopSek))
        
       
        print("Mean = " + str(stat.mean(cutXArr)))                                     #Visual checker to see that following algorithm is plaussible
        
        pointsInInterval = T[intvalTimeStart:intvalTimeStop][np.nonzero(cutXArr[intvalTimeStart:intvalTimeStop] > 0.4*stat.mean(cutXArr))]     #(experimental "top" value)
        fqArray.append(pointsInInterval[0])
        for i in range(1, len(pointsInInterval)):
            if ( (pointsInInterval[i] - (pointsInInterval[0]+(stopSek-startSek)) < ((pointsInInterval[0]+(stopSek-startSek))-fqArray[len(fqArray)-1])) and (pointsInInterval[i]-fqArray[len(fqArray)-1]) > 0.61):   #(experimental time value)
                fqArray.append(pointsInInterval[i])
                if (len(fqArray) >= 2):
                    stpFreq.append(1/(pointsInInterval[i]-fqArray[len(fqArray)-2]))       #Converted to Hz (step/second)
                if (len(stpFreq) == 2):
                    if (stpFreq[0] > 1.4*stpFreq[1]):                                       #Remove intitial step that is too short (experimental frequency value)
                        fqArray.remove(fqArray[0])
                        stpFreq.remove(stpFreq[0]) 

        return stpFreq

