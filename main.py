import matplotlib.pyplot as plt
import numpy as np
import math
import arrayImporter as imp

def getPoints(dataArray, RMS):
    packets = [0]
    points = dataArray[:,0][np.nonzero(dataArray[:,6] > 2.4*RMS)]           #Assign acc(Y)Value > 1.7xRMS to corrresponding packet
    for i in range (1,points.size):                                         #Assign packets that lies withing sf/2,
        if points[i]-points[i-1] < sampleFrekvens/2:
            packets.append(points[i])
    return packets

dataArray = imp.fileImport("LA")

sampleFrekvens = 131
aproxSekvensTime = 6
dataSelection = []
Square = 0

for i in range(1,len(dataArray)):
    Square += dataArray[i,6]**2
RMS = math.sqrt(Square/len(dataArray))

packets = getPoints(dataArray, RMS)
for i in range(1, len(packets)-1):                                      #Remove nearby packets and remain with farends of "packet-group"
    if packets[i] - packets[i-1] > aproxSekvensTime*sampleFrekvens*50:
        dataSelection.append(packets[i])
    elif packets[i+1] - packets[i] > aproxSekvensTime*sampleFrekvens*50:
        dataSelection.append(packets[i])
wait = 0
count = 0

while (count < len(dataSelection)):                                     #Remove groups that lies too close to other
    count += 1
    
    if (wait >= 1 ):
        if (dataSelection[wait] - dataSelection[wait-1] < sampleFrekvens*aproxSekvensTime*80):
                
            dataSelection.remove(dataSelection[wait])
            
            dataSelection.remove(dataSelection[wait-1])
            count -= 1
            wait -= 1
    wait += 1

indexes = []                                                            #Find the indexes of the selected points in the original matrix
for packet in dataSelection:
    indexes.append(np.where(dataArray[:,0] == packet))

cutArr = dataArray[int(indexes[4][0]):int(indexes[5][0]),4]             #Cut out an array during a walking trial
cutPacks = dataArray[int(indexes[4][0]):int(indexes[5][0]),0]

for i in range(0,len(dataSelection)):
        plt.axvline(dataSelection[i], color = 'r', ymin= 0.25, ymax=0.75)
plt.plot(dataArray[:,0], dataArray[:,4], label="X")
plt.plot(cutPacks, cutArr, label="cutArr (X)")
plt.xlabel('packet')
plt.ylabel('value')
plt.legend()
plt.show()



