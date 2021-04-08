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
dataQt = subject.LAqtArray
dtimeArray = dataTime[:,0]



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
startSession = 4
stopSession = 5
cutPacks = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),0]           #Cut out an array during a walking trial S4 4-5, S12 5-6

cutYArr = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),1]   #5 accY
cutXArr = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),4]   #4
cutZArr = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),6] 

cutXMag = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),8]
cutEuler = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0])]

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

startSek = 180                                                          #Konstanter som väljs av användaren (start o stopp)
stopSek = 240
intvalTimeStart = math.floor((len(cutPacks)/sessionTime)*startSek)
intvalTimeStop = math.floor((len(cutPacks)/sessionTime)*(stopSek+5))

fqArray = []
stpFreq = []
newArray = []
pointsInInterval = T[intvalTimeStart:intvalTimeStop][np.nonzero(cutXArr[intvalTimeStart:intvalTimeStop] > -0.3)] #Justeras efter vilken arr o vilkor
fqArray.append(pointsInInterval[0])
for i in range(1, len(pointsInInterval)):
    if ( (pointsInInterval[i] - (pointsInInterval[0]+(stopSek-startSek)) < ((pointsInInterval[0]+(stopSek-startSek))-fqArray[len(fqArray)-1])) and (pointsInInterval[i]-fqArray[len(fqArray)-1]) > 0.71):
        fqArray.append(pointsInInterval[i])
        if (len(fqArray) >= 2):
            stpFreq.append(1/(pointsInInterval[i]-fqArray[len(fqArray)-2]))       #Converted to Hz (step/second)
                     
#print(stpFreq)
print('During '+ str(fqArray[len(stpFreq)]-fqArray[0]) + ' s in the interval of '+ str(startSek) + '-' + str(stopSek) + ', '+ str(len(stpFreq)) + ' steps were made with an average step frequency of ' + str(stat.fmean(stpFreq)) + ' Hz')
print('Sample standard diviation: ' + str(stat.stdev(stpFreq)) + ' Hz')             #Sample standard deviation of data


timeStart = dataTime[0, 4]*3600 + dataTime[0, 5]*60 + dataTime[0, 6]
last = len(dataTime[:,0]) - 1
timeStop = dataTime[last, 4]*3600 + dataTime[last, 5]*60 + dataTime[last, 6]
timeTotal = timeStop - timeStart
print(timeTotal)
dt = timeTotal / len(dataArray[:,0])
print("time per packet: ", dt, 's implying data rate of ', 1/dt , 'Hz')
globalTimeArr = np.linspace(0, timeTotal, num=len(dataArray[:,0]))

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

#a_x = []
#a_z = []
#thetaArray = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),2]    #skapa en arry med data[0,2] inom betingelsen
#degToRad = math.pi/180
#theta = thetaArray[intvalTimeStart]*dt*degToRad
#for i in range(intvalTimeStart, intvalTimeStop):                                        #gör beräkningarna enbart på "60 s" intervallet
#    dTheta = thetaArray[i]*degToRad
#    dThetaPrev = thetaArray[i-1]*degToRad
#    theta = (dTheta*dt*i) - (dThetaPrev*dt*(i-1))
#    mat = np.array([[-(math.sin(theta)), math.cos(theta)],[math.cos(theta), math.sin(theta)]])
#    vec = np.array([[cutXArr[i]*9.80665],[cutZArr[i]*9.80665]])
#    product = np.dot(mat, vec)
#    accVec = (-product) - np.array([[9.80665],[0]])
#    a_x.append(accVec[0,0])
#    a_z.append(accVec[1,0])
#
#xList = [(a_x[0]*dt**2)/2]
#zList = [(a_z[0]*dt**2)/2]
#x=0
#z=0
#for i in range(len(a_x) - 1):
#    x = ((a_x[i+1]*(dt**2))/2) - ((a_x[i]*(dt**2))/2)
#    z = ((a_z[i+1]*(dt**2))/2) - ((a_z[i]*(dt**2))/2)
#    xList.append(x)
#    zList.append(z)

#zGait = []
#c = 0
#for i in range(len(a_z) ):
#    z += zList[i]
#    zGait.append(z)
#    if (T[intvalTimeStart+i] == fqArray[c]):                                            #T är i s, så matcha T med de gait-tider som finns i fqArray
#        if (c < len(fqArray)-1):
#            c += 1
#        z = 0
#        plt.axvline(T[intvalTimeStart+i], color = 'r', ymin= 0.25, ymax=0.75)

#plt.figure(1)
#plt.plot(T[intvalTimeStart:intvalTimeStop], zGait)
#plt.title("horizontal foot movement")
#plt.show()

   
    #Plotting:
plt.figure(2)
for i in range(0,len(fqArray)):
    plt.axvline((cutEuler[math.floor((len(cutPacks)/sessionTime)*fqArray[i]),0]), color = 'r', ymin= 0.15, ymax=0.85)   #Plot for whole or cutPacks
    #plt.axvline(fqArray[i], color = 'r', ymin= 0.15, ymax=0.85)                        #Plot for x-axis = T
#plt.plot(dataArray[:,0], dataArray[:,4], label="X")                                    #Print whole dataArray
#for i in range(0,len(dataSelection)):
#       plt.axvline(dataSelection[i], color = 'r', ymin= 0.25, ymax=0.75)

plt.plot(quaterions[:,0], roll, label="Roll|Phi|X(degree)")
plt.plot(quaterions[:,0], pitch, label="Pitch|Theta|Y(degree)")
plt.plot(quaterions[:,0], yaw, label="Yaw|Psi|Z(degree")
#plt.plot(T,roll, label="Roll|Phi|X(degree)")
#plt.plot(T, pitch, label="Pitch|Theta|Y(degree)")
#plt.plot(T, yaw, label="Yaw|Psi|Z(degree")
#plt.plot(T, cutXMag, label = "Mag X" )
#plt.plot(cutPacks, cutXArr, label="cutArr (X)")
#plt.plot(T, cutYArr, label="cutArr (Y)")                 #Bäst att detektera/se gait
#plt.plot(T, cutZArr, label="cutArr (Z)")
#plt.axvline(cutPacks[intvalTimeStart], color = 'g', ymin= 0.15, ymax=0.85)
#plt.axvline(cutPacks[intvalTimeStop], color = 'g', ymin= 0.15, ymax=0.85)


plt.xlabel('seconds')
plt.ylabel('value')
plt.legend()
plt.show()
