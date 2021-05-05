import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
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
neckArray = subject.NcalArray
nEulArray = subject.NeulerArray

#plt.figure(1)
#plt.plot(eulerArray[:,0], eulerArray[:,1], label='x/phi')
#plt.plot(eulerArray[:,0], eulerArray[:,2], label='y/theta')
#plt.plot(eulerArray[:,0], eulerArray[:,3], label='z/psi')
#plt.legend()
#plt.show()

timeStart = dataTime[0, 4]*3600 + dataTime[0, 5]*60 + dataTime[0, 6]
last = len(dataTime[:,0]) - 1
timeStop = dataTime[last, 4]*3600 + dataTime[last, 5]*60 + dataTime[last, 6]
timeTotal = timeStop - timeStart
print(timeTotal)
dt = timeTotal / len(dataArray[:,0])
print("time per packet: ", dt, 'implying data rate of ', 1/dt , 'Hz')
globalTimeArr = np.linspace(0, timeTotal, num=len(dataArray[:,0]))


def q_conjugate(q):
    w, x, y, z = q
    return(w, -x, -y, -z)
def qv_mult(q1, v1):
    q2=(0.0,)+v1
    return q_mult(q_mult(q1,q2),q_conjugate(q1))[1:]
def q_mult(q1,q2):
    w1,x1,y1,z1 = q1
    w2,x2,y2,z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z
quaterions = dataQt
q0 = quaterions[:,1]
q1 = quaterions[:,2]
q2 = quaterions[:,3]
q3 = quaterions[:,4]
roll = []
pitch = []
yaw = []
for i in range(0, len(quaterions)):
    roll.append(math.atan2(2*(q0[i]*q1[i]+q2[i]*q3[i]),1-2*(q1[i]**2+q2[i]**2)))
    pitch.append(math.asin(2*(q0[i]*q2[i]-q3[i]*q1[i])))
    yaw.append(math.atan2(2*(q0[i]*q3[i]+q1[i]*q2[i]),1-2*(q2[i]**2+q3[i]**2)))


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

tempArr = []                                                            #identifying knocks on IMU (neck)
knPoints = [0]
MS = stat.mean(neckArray[:,6])
print(MS)
for i in range(len(neckArray)):
    if( neckArray[i,6] > 4*math.sqrt(MS**2)):
        tempArr.append(neckArray[i,0])
        if (tempArr[len(tempArr)-1] > (knPoints[len(knPoints)-1]+5*sampleFrekvens)):
            knPoints.append(tempArr[len(tempArr)-1])

    #Decide which session to make calculations on:
startSession = 4
stopSession = 5
cutPacks = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),0]           #Cut out an array during a walking trial S4 4-5, S12 5-6

cutYArr = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),5]   #5 accY
cutXArr = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),4]   #4
cutZArr = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),6] 

cutXdeg = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),1]
cutYdeg = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),2]
cutZdeg = dataArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),3]

cutEul = eulerArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),:]

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

        #Calculations
fqArray = []
stpFreq = []
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

print('During '+ str(fqArray[len(stpFreq)]-fqArray[0]) + ' s in the interval of '+ str(fqArray[0]) + '-' + str(fqArray[len(stpFreq)]) + ', '+ str(len(stpFreq)) + ' steps were made with an average step frequency of ' + str(stat.mean(stpFreq)) + ' Hz')
print('Sample standard diviation: ' + str(stat.stdev(stpFreq)) + ' Hz')             #Sample standard deviation of data

frekvensA = []
steg = []

for i in range(intvalTimeStart,intvalTimeStop-1):
    if (cutZdeg[i+1]-cutZdeg[i] > -0.12 and cutZdeg[i+1]-cutZdeg[i] < 0.12 ):
        frekvensA.append(T[i])
        if (len(frekvensA) >= 2):
            steg.append(1/(T[i]-frekvensA[len(frekvensA)-2]))

print(steg)
print(len(steg))
print(frekvensA)
print('calculating acceleration vector')
cutEu = eulerArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),:]
cutRot = rotationArray[int(indexes[startSession][0]):int(indexes[stopSession][0]),:]
aList = [np.array([[0], [0], [0]])]
c = 5
#for c in range(1,len(fqArray)):
gaitTime = []
for i in range(math.floor((len(cutPacks)/sessionTime)*fqArray[c-1]),math.floor((len(cutPacks)/sessionTime)*fqArray[c])):
    gaitTime.append(T[i])
    theta = cutEu[i,1] * (math.pi/180)
    R_se = np.array([[cutRot[i, 1], cutRot[i, 2], cutRot[i, 3]], [cutRot[i, 4],cutRot[i, 5], cutRot[i, 6]], 
                     [cutRot[i, 7], cutRot[i, 8], cutRot[i, 9]]])              #rotation matrix from IMU coordinates 's' to room coordinates 'e'
    a_s = np.array([[cutXArr[i]*9.80665],[cutYArr[i]*9.80665], [cutZArr[i]*9.80665]])   #acceleration in IMU coordinates

    a_e = -(np.dot(R_se, a_s)) - np.array([[9.80665], [0], [0]])                                       #acceleration in room coordinates - gravity
    aList.append(a_e)
print('done!')
print('calculating velocity and position vectors')
vList = [np.array([[0], [0], [0]])]
pList = [np.array([[0], [0], [0]])]
v_e = [np.array([[0], [0], [0]])]
p_e = [np.array([[0], [0], [0]])]
for i in range(1, len(aList)-1):
    v_e =  ((aList[i] + aList[i-1])/2) * dt
    vList.append(v_e)
    #print(v_e)

    p_e =  ((vList[i] + vList[i-1])/2) * dt
    pList.append(p_e)
print('done!')
p_xList = []
p_yList = []
p_zList = []

for arr in pList:
    p_xList.append(arr[0])
    p_yList.append(arr[1])
    p_zList.append(arr[2])

plt.figure(2)
plt.plot(gaitTime, p_xList)
plt.title("vertical foot movement")
#plt.show()
#print(p_xList)
#print(p_yList)
#print(p_zList)
  
    #Plotting:
x = 1
y = 2
z = 3
plt.figure(3)
for i in range(0,len(fqArray)):
    #plt.axvline((cutPacks[math.floor((len(cutPacks)/sessionTime)*fqArray[i])]), color = 'r', ymin= 0.15, ymax=0.85)   #Plot for whole or cutPacks
    plt.axvline(fqArray[i], color = 'r', ymin= 0.15, ymax=0.85)                        #Plot for x-axis = T
for i in range(0,len(frekvensA)):
    plt.axvline(frekvensA[i], color='k', ymin= 0.15, ymax=0.85)
#plt.plot(eulerArray[:,0], eulerArray[:,x], label="X")                                    #Print whole dataArray
#plt.plot(eulerArray[:,0], eulerArray[:,y], label="Y")
#plt.plot(eulerArray[:,0], eulerArray[:,z], label="Z")
#for i in range(0,len(dataSelection)):
#       plt.axvline(dataSelection[i], color = 'm', ymin= 0.25, ymax=0.75)
#for i in range(0,len(knPoints)):
#       plt.axvline(knPoints[i], color = 'k', ymin= 0.25, ymax=0.75)

plt.title("Accelorometre")
#plt.plot(quaterions[:,0], roll, label="Roll|Phi|X(degree)")
#plt.plot(quaterions[:,0], pitch, label="Pitch|Theta|Y(degree)")
#plt.plot(quaterions[:,0], yaw, label="Yaw|Psi|Z(degree")
#plt.plot(T,roll, label="Roll|Phi|X(degree)")
#plt.plot(T, pitch, label="Pitch|Theta|Y(degree)")
#plt.plot(T, yaw, label="Yaw|Psi|Z(degree")
#plt.plot(T, cutXMag, label = "Mag X" )
#plt.plot(T, cutXArr, label="cutArr (X)")
#plt.plot(T, cutYArr, label="cutArr (Y)")                 
plt.plot(T, cutZArr, label="cutArr (Z)")
plt.legend()
#plt.axvline(cutPacks[intvalTimeStart], color = 'g', ymin= 0.15, ymax=0.85)
#plt.axvline(cutPacks[intvalTimeStop], color = 'g', ymin= 0.15, ymax=0.85)
plt.figure(5)
#for i in range(0,len(knPoints)):
#       plt.axvline(knPoints[i], color = 'k', ymin= 0.25, ymax=0.75)
for i in range(0,len(fqArray)):
    #plt.axvline((cutPacks[math.floor((len(cutPacks)/sessionTime)*fqArray[i])]), color = 'r', ymin= 0.15, ymax=0.85)   #Plot for whole or cutPacks
    plt.axvline(fqArray[i], color = 'r', ymin= 0.15, ymax=0.85)
for i in range(0,len(frekvensA)):
    plt.axvline(frekvensA[i], color='k', ymin= 0.15, ymax=0.85)
#plt.plot(T, cutXdeg, label="x")
#plt.plot(T, cutYdeg, label="y")
plt.plot(T, cutZdeg, label="z")
#print(dataSelection)
#print(knPoints)
#plt.plot(nEulArray[:,0], nEulArray[:,x], label="X")                          
#plt.plot(nEulArray[:,0], nEulArray[:,y], label="Y")
#plt.plot(nEulArray[:,0], nEulArray[:,z], label="Z")
plt.title("Angularvelocity")
plt.legend()
plt.figure(4)
ax = plt.axes(projection='3d')
ax.scatter3D(p_xList, p_yList, p_zList);
plt.title('Gait movement')
#plt.xlabel('seconds')
#plt.ylabel('value')
plt.figure(8)
plt.plot(dataArray[:,0], dataArray[:,4])
plt.show()
