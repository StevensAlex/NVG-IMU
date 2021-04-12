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
eulerArray = subject.LAeulerArray
rotationArray = subject.LArotationArray
dataQt = subject.LAquaternionArray
dtimeArray = dataTime[:,0]

quaterions = dataQt[:,:]
q0 =  quaterions[:, 1]
q1 =  quaterions[:, 2]
q2 =  quaterions[:, 3]
q3 =  quaterions[:, 4]

roll = []
pitch = []
yaw = []
for i in range(0, len(quaterions)):
    roll.append(math.atan2(2*(q0[i]*q1[i]+q2[i]*q3[i]),1-2*(q1[i]**2+q2[i]**2)))
    pitch.append(math.asin(2*(q0[i]*q2[i]-q3[i]*q1[i])))
    yaw.append(math.atan2(2*(q0[i]*q3[i]+q1[i]*q2[i]),1-2*(q2[i]**2+q3[i]**2)))

#Sample rate for data 
def switch_dataRate(argument):
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

def getPoints(dataArray, RMS):
    packets = [0]
    points = dataArray[:,0][np.nonzero(dataArray[:,6] > 2.4*RMS)]           #Assign acc(Z)Value > 1.7xRMS to corrresponding packet
    for i in range (1,points.size):                                         #Assign packets that lies withing sf/2,
        if points[i]-points[i-1] < sampleFrekvens/2:
            packets.append(points[i])
    return packets

sampleFrekvens = switch_dataRate(dataRegist[69,2])                          #DataRate for inertia and mag
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
startSession = 4
stopSession = 5
cutPacks = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),0]           #Cut out an array during a walking trial S4 4-5, S12 5-6

cutYArr = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),5]   #5 accY
cutXArr = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),4]   #4
cutZArr = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),6] 

    #Timeconversion of betingelse starting at 0:
for i in range(0, len(dtimeArray)):
    if dtimeArray[i] <= (dataSelection[startSession] + sampleFrekvens):
        timeStart = dataTime[i, 4]*3600 + dataTime[i, 5]*60 + dataTime[i, 6]
    if dtimeArray[i] <= (dataSelection[stopSession] + sampleFrekvens):
        timeStop = dataTime[i, 4]*3600 + dataTime[i, 5]*60 + dataTime[i, 6]

sessionTime = timeStop - timeStart
T = np.empty((len(cutPacks)), dtype = float)
for i in range(0, len(cutPacks)):
    T[i] = i*(sessionTime/len(cutPacks))

startSek = 180                                                         #Konstanter som väljs av användaren (start o stopp)
stopSek = 240

if (startSek > 0):
    intvalTimeStart = math.floor((len(cutPacks)/sessionTime)*(startSek-1))
else:
    intvalTimeStart = math.floor((len(cutPacks)/sessionTime)*(startSek))
if (stopSek < T[len(T)-1]-5):
    intvalTimeStop = math.floor((len(cutPacks)/sessionTime)*(stopSek+5))
else:
    intvalTimeStop = math.floor((len(cutPacks)/sessionTime)*(stopSek))

fqArray = []
stpFreq = []

print("Mean = " + str(stat.fmean(cutXArr)))                                     #Visual checker to see that following algorithm is plaussible

pointsInInterval = T[intvalTimeStart:intvalTimeStop][np.nonzero(cutXArr[intvalTimeStart:intvalTimeStop] > 0.4*stat.fmean(cutXArr))]     #(experimental 
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

print('During '+ str(fqArray[len(stpFreq)]-fqArray[0]) + ' s in the interval of '+ str(fqArray[0]) + '-' + str(fqArray[len(stpFreq)]) + ', '+ str(len(stpFreq)) + ' steps were made with an average step frequency of ' + str(stat.fmean(stpFreq)) + ' Hz')
print('Sample standard diviation: ' + str(stat.stdev(stpFreq)) + ' Hz')             #Sample standard deviation of data
  
    #Plotting:
plt.figure(2)
for i in range(0,len(fqArray)):
    plt.axvline((cutPacks[math.floor((len(cutPacks)/sessionTime)*fqArray[i])]), color = 'r', ymin= 0.15, ymax=0.85)   #Plot for whole or cutPacks
    #plt.axvline(fqArray[i], color = 'r', ymin= 0.15, ymax=0.85)                        #Plot for x-axis = T
plt.plot(dataArray[:,0], dataArray[:,4], label="X")                                    #Print whole dataArray
for i in range(0,len(dataSelection)):
       plt.axvline(dataSelection[i], color = 'r', ymin= 0.25, ymax=0.75)

#plt.plot(quaterions[:,0], roll, label="Roll|Phi|X(degree)")
#plt.plot(quaterions[:,0], pitch, label="Pitch|Theta|Y(degree)")
#plt.plot(quaterions[:,0], yaw, label="Yaw|Psi|Z(degree")
#plt.plot(T,roll, label="Roll|Phi|X(degree)")
#plt.plot(T, pitch, label="Pitch|Theta|Y(degree)")
#plt.plot(T, yaw, label="Yaw|Psi|Z(degree")
#plt.plot(T, cutXMag, label = "Mag X" )
#plt.plot(T, cutXArr, label="cutArr (X)")
#plt.plot(T, cutYArr, label="cutArr (Y)")                 #Bäst att detektera/se gait
#plt.plot(T, cutZArr, label="cutArr (Z)")
#plt.axvline(cutPacks[intvalTimeStart], color = 'g', ymin= 0.15, ymax=0.85)
#plt.axvline(cutPacks[intvalTimeStop], color = 'g', ymin= 0.15, ymax=0.85)


plt.xlabel('seconds')
plt.ylabel('value')
plt.legend()
plt.show()
