import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import math
import arrayImporter as imp
import statistics as stat

subject = imp.Subject()
dataTime = subject.LAtimeArray
dataRegist = subject.LAregArray
dataArray = subject.LAcalArray

dtimeArray = dataTime[:,0]

def switch_dataRate(argument):
    switcher = {
        0: "Disabled",
        1: 1,
        2: 2,
        3: 4,
        4: 8,
        5: 16,
        6: 32,
        7: 64,
        8: 128,
        9: 256,
        10: 512
    }
    return switcher.get(argument, 0)

def getPoints(dataArray, RMS):
    packets = [0]
    points = dataArray[:,0][np.nonzero(dataArray[:,6] > 2.4*RMS)]           #Assign acc(Y)Value > 1.7xRMS to corrresponding packet
    for i in range (1,points.size):                                         #Assign packets that lies withing sf/2,
        if points[i]-points[i-1] < sampleFrekvens/2:
            packets.append(points[i])
    return packets

sampleFrekvens = switch_dataRate(8)     #dataRegist[69,2]                   #DataRate for inertia and mag
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


    #Decide which session to make calculations on:
startSession = 6
stopSession = 7
cutPacks = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),0]           #Cut out an array during a walking trial S4 4-5, S12 5-6

cutYArr = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),5] 
cutXArr = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),4]   #4
cutZArr = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),6] 


    #Timeconversion:
start = 0
stop = 0
tCount = 0
for i in range(0, len(dtimeArray)):
    if dtimeArray[i] <= (dataSelection[startSession] + sampleFrekvens) and dtimeArray[i] >= (dataSelection[startSession] - sampleFrekvens):
        start = 1
    if dtimeArray[i] <= (dataSelection[stopSession] + sampleFrekvens) and dtimeArray[i] >= (dataSelection[stopSession] - sampleFrekvens):
        stop = 1
    if (start > 0) and (stop == 0):
        tCount+=0.5
    
T = np.empty((len(cutPacks)), dtype = float)

for i in range(0, len(cutPacks)):
    #T.append((cutPacks[i]-zeroTime)/sampleFrekvens)         #ca 2perioder/s
    T[i] = i*(tCount/len(cutPacks))
    #T.append(i*(tCount/len(cutPacks)))             #ca 1 period/s


startSek = 180                                                          #Konstant som väljs av användaren (start o stopp)
stopSek = 240
intvalTimeStart = math.floor((len(cutPacks)/tCount)*startSek)
intvalTimeStop = math.floor((len(cutPacks)/tCount)*stopSek)

fqArray = []
stpFreq = []
pointsInInterval = T[intvalTimeStart:intvalTimeStop][np.nonzero(cutXArr[intvalTimeStart:intvalTimeStop] > -0.2)] #Justeras efter vilken arr o vilkor
fqArray.append(pointsInInterval[0])
for i in range(1, len(pointsInInterval)):
    if ( (pointsInInterval[i] - (pointsInInterval[0]+(stopSek-startSek)) < ((pointsInInterval[0]+(stopSek-startSek))-fqArray[len(fqArray)-1])) and (pointsInInterval[i]-fqArray[len(fqArray)-1]) > 0.61):
        fqArray.append(pointsInInterval[i])                                 
        stpFreq.append(1/(pointsInInterval[i]-pointsInInterval[i-1]))       #Converted to Hz (step/second)
                     
#print(stpFreq)
print('During '+ str(fqArray[len(stpFreq)]-fqArray[0]) + ' S in the interval of '+ str(startSek) + '-' + str(stopSek) + ', '+ str(len(stpFreq)) + ' steps where made')
print('Sample standard diviation: ' + str(stat.stdev(stpFreq)))             #Sample standard deviation of data

   
    #Plotting:
for i in range(0,len(fqArray)):
    plt.axvline(fqArray[i], color = 'r', ymin= 0.15, ymax=0.85)
#plt.plot(dataArray[:,0], dataArray[:,4], label="X")            #Print whole dataArray
#for i in range(0,len(dataSelection)):
#        plt.axvline(dataSelection[i], color = 'r', ymin= 0.25, ymax=0.75)

#plt.plot(T, cutXArr, label="cutArr (X)")
plt.plot(T, cutYArr, label="cutArr (Y)")                 #Bäst att detektera/se gait
#plt.plot(T, cutZArr, label="cutArr (Z)")
plt.axvline(T[intvalTimeStart], color = 'g', ymin= 0.15, ymax=0.85)
plt.axvline(T[intvalTimeStop], color = 'g', ymin= 0.15, ymax=0.85)


plt.xlabel('seconds')
plt.ylabel('value')
plt.legend()
plt.show()
