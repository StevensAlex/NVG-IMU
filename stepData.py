import matplotlib.pyplot as plt
import numpy as np
import math


class StepData:
    def __init__(self, stepsRaw, dt):
        self.stepsRaw = stepsRaw
        print('raw:', len(stepsRaw))
        print('raw:', len(stepsRaw[0]))
        self.dt = dt
        self.labAcc, eu = self.angleTransformation(self.stepsRaw)
        print('lab:', len(self.labAcc))
        print('lab:', len(self.labAcc[0]))
        preComp = self.driftComp(self.stepsRaw)
        print('now=====================================================')
        labPostComp, eulerActual = self.angleTransformation(preComp)
        print('done====================================================')
        labComp = self.driftComp(self.labAcc)
        print('labcomp:',len(labComp))
        print('labcomp:',len(labComp[0]))
        print('labcomp:',len(labComp[0][0]))
        #plt.figure()
        #step = labComp[0]
        ##xaccList=[]
        ##yaccList=[]
        ##zaccList=[]
        ##for point in step:
        ##    xaccList.append(point[0])
        ##    yaccList.append(point[1])
        ##    zaccList.append(point[2])
        #plt.plot(step[:,0], step[:,4], label='x')
        #print('asdasdasd')
        #plt.plot(labComp[0][:,0], labComp[0][:,5], label='y')
        #print('asd')
        #plt.plot(labComp[0][:,0], labComp[0][:,6], label='z')
        #plt.title('lab comp')

        self.pLists = self.integrator(self.labAcc)
        print('pLists:', len(self.pLists))
        print('pLists:', len(self.pLists[0]))
        print('pLists:', len(self.pLists[0][0]))

        #=======test======
        p_xList = []
        p_yList = []
        p_zList = []
        print('pre-plot')
        for arr in self.pLists[0]:
            p_xList.append(float(arr[0]))
            p_yList.append(float(arr[1]))
            p_zList.append(float(arr[2]))
        print('plot time')
        print(p_xList)
        plt.figure()
        plt.plot(self.stepsRaw[0][:,0], p_xList, label='x')
        print('1 plot')
        plt.plot(self.stepsRaw[0][:,0], p_yList, label='y')
        plt.plot(self.stepsRaw[0][:,0], p_zList, label='z')
        plt.title("foot movement")
        plt.legend()
        #=======test======
        #plt.figure()
        #plt.plot(self.stepsRaw[:][:,0], self.stepsRaw[:][:,5])
        #plt.title("test")
        #=======test======
        print('pre next integrator')
        self.pLists2 = self.fbIntegrator(self.labAcc)
        print('post next integrator')
        print('pList:', len(self.pLists2))
        print('pList:', len(self.pLists2[0]))
        print('pList:', len(self.pLists2[0][0]))

        p_xList2 = []
        p_yList2 = []
        p_zList2 = []
        print('pre-plot')
        for arr in self.pLists2[0]:
            p_xList2.append(float(arr[0]))
            p_yList2.append(float(arr[1]))
            p_zList2.append(float(arr[2]))
        print('plot time')
        plt.figure()
        plt.plot(self.stepsRaw[0][:,0], p_xList2, label='x')
        plt.plot(self.stepsRaw[0][:,0], p_yList2, label='y')
        plt.plot(self.stepsRaw[0][:,0], p_zList2, label='z')
        plt.title("foot movement fb integrator")
        plt.legend()
        plt.figure()
        plt.plot(self.stepsRaw[0][:,0], self.stepsRaw[0][:,1], label='x')
        plt.plot(self.stepsRaw[0][:,0], self.stepsRaw[0][:,2], label='y')
        plt.plot(self.stepsRaw[0][:,0], self.stepsRaw[0][:,3], label='z')
        plt.title('ang. vel')
        plt.legend()
        #=======test======
        stepAngles = eulerActual[0]
        #print(eulerActual)
        print('eulerlists:', len(eulerActual))
        print('stepAngles:', len(stepAngles))
        print('stepAngles content:', len(stepAngles[0]))
        print('stepAngles content inner:', len(stepAngles[0][0]))
        thetaList = []
        phiList = []
        psiList = []
        print('points')
        for i in range(len(stepAngles)):
            thetaList.append(stepAngles[i][0])
            phiList.append(stepAngles[i][1])
            psiList.append(stepAngles[i][2])
        #step = self.stepsRaw[0]
        #plt.figure()
        #plt.plot(step[:,0], thetaList, label = 'theta')
        #plt.plot(step[:,0], phiList, label = 'phi')
        #plt.plot(step[:,0], psiList, label = 'psi')
        #plt.legend()



    def angleTransformation(self, steps):
        stepAccLists = []
        eulerLists = []
        for j in range(len(steps)):
            step = steps[j]
            ax = (step[0, 4] *9.82)
            ay =  (step[0, 5] *9.82)
            az = (step[0, 6] *9.82)
            a_s = np.array([[ax],[ay],[az]])
            eulerVec = np.array([[0],[math.atan(-az/math.sqrt(ax**2 + ay**2))],[math.atan(-ay/ax)]])
            theta = eulerVec[0]
            phi = eulerVec[1]
            psi = eulerVec[2]

            R_se = np.array([[math.cos(phi)*math.cos(psi), -math.cos(phi)*math.sin(psi), math.sin(phi)],
                             [math.sin(theta)*math.sin(phi)*math.cos(psi) + math.cos(theta)*math.sin(psi), -math.sin(theta)*math.sin(phi)*math.sin(psi) + math.cos(theta)*math.cos(psi), -math.sin(theta)*math.cos(phi)],
                             [-math.cos(theta)*math.sin(phi)*math.cos(psi), math.cos(theta)*math.sin(phi)*math.sin(psi) + math.sin(theta)*math.cos(psi), math.cos(theta)*math.cos(phi)]])
            R_e = np.array([[math.cos(phi)*math.cos(psi)+math.sin(phi)*math.sin(theta)*math.sin(psi),-math.cos(phi)*math.sin(psi)+math.sin(phi)*math.sin(theta)*math.cos(psi), math.sin(phi)*math.cos(theta)],
                            [math.cos(theta)*math.sin(psi),math.cos(theta)*math.cos(psi),-math.sin(theta)],
                            [-math.sin(phi)*math.cos(psi)+math.cos(phi)*math.sin(theta)*math.sin(psi),math.sin(phi)*math.sin(psi)+math.cos(phi)*math.sin(theta)*math.cos(psi),math.cos(phi)*math.cos(theta)]])
            a_e = np.dot(R_se, a_s) - np.array([[0],[9.82],[0]])
            #compX = float(a_e[0])
            #compY = float(a_e[1])
            #compZ = float(a_e[2])
            #a_e = a_e - np.array([[compX],[0],[0]])
            
            eulerList = [eulerVec]
            a_eList = [a_e]
            angVelList = [np.array([[math.radians(step[0, 1])],[math.radians(step[0, 2])],[math.radians(step[0, 3])]])]
            for i in range(1, len(step[:,0])):
                a_s = np.array([[(step[i, 4] *9.82)],[(step[i, 5] *9.82)],[(step[i, 6] *9.82)]])
                angVel = np.array([[math.radians(step[i, 1])],[math.radians(step[i, 2])],[math.radians(step[i, 3])]])
                eulerVec += ((angVel + angVelList[-1])/2) * self.dt
                angVelList.append(angVel)
                eulerList.append(np.array([[eulerVec[0]],[eulerVec[1]],[eulerVec[2]]]))
                if j == 0:
                    print('euler:\n', eulerVec)
                theta = eulerVec[0]
                phi = eulerVec[1]
                psi = eulerVec[2]
                R_se = np.array([[math.cos(phi)*math.cos(psi), -math.cos(phi)*math.sin(psi), math.sin(phi)],
                                 [math.sin(theta)*math.sin(phi)*math.cos(psi) + math.cos(theta)*math.sin(psi), -math.sin(theta)*math.sin(phi)*math.sin(psi) + math.cos(theta)*math.cos(psi), -math.sin(theta)*math.cos(phi)],
                                 [-math.cos(theta)*math.sin(phi)*math.cos(psi), math.cos(theta)*math.sin(phi)*math.sin(psi) + math.sin(theta)*math.cos(psi), math.cos(theta)*math.cos(phi)]])
                R_e = np.array([[math.cos(phi)*math.cos(psi)+math.sin(phi)*math.sin(theta)*math.sin(psi),-math.cos(phi)*math.sin(psi)+math.sin(phi)*math.sin(theta)*math.cos(psi), math.sin(phi)*math.cos(theta)],
                            [math.cos(theta)*math.sin(psi),math.cos(theta)*math.cos(psi),-math.sin(theta)],
                            [-math.sin(phi)*math.cos(psi)+math.cos(phi)*math.sin(theta)*math.sin(psi),math.sin(phi)*math.sin(psi)+math.cos(phi)*math.sin(theta)*math.cos(psi),math.cos(phi)*math.cos(theta)]])
                a_e = np.dot(R_se, a_s) - np.array([[0],[9.82],[0]])
                a_eList.append(a_e)
            for i in range(len(a_eList)):
                step[i,4] = a_eList[i][0]
                step[i,5] = a_eList[i][1]
                step[i,6] = a_eList[i][2]
            if j == 0:
                print('list:', eulerList)
            eulerLists.append(eulerList)
            #print('=====\n=====\n=====')
            #print(eulerList)
            #print('=====\n=====\n=====')
        print('eulerLists[0]:',eulerLists[0])
        return steps, eulerLists
            #stepAccLists.append(a_eList)
        #return stepAccLists


    def driftComp(self, steps):
        for step in steps:
            for i in range(1,7):
                axis = step[:,i]
                if axis[0] < axis[-1]:
                    diffAxis = axis[-1] - axis[0]
                    compAxis = diffAxis/len(step[:,0])
                    for j in range(len(step[:,0])):
                        step[j,i] += -compAxis*j
                else:
                    diffAxis = axis[0] - axis[-1]
                    compAxis = diffAxis/len(step[:,0])
                    for j in range(len(step[:,0])):
                        step[j,i] += compAxis*j
        return steps

    def integrator(self, steps):
        pLists = []
        accLists = []
        print('plists declared')
        for step in steps:
            acc = step[:,4:7]
            accList = []
            for a in acc:
                accList.append(np.array([[a[0]], [a[1]], [a[2]]]))
            accLists.append(accList)
        for aList in accLists:
            v_e = np.array([[0], [0], [0]])
            p_e = np.array([[0], [0], [0]])
            vList = [v_e]
            pList = [p_e]
            #print('starting p loop')
            for i in range(1, len(aList)):
                v_e =  v_e + ((aList[i] + aList[i-1])/2) * self.dt
                vList.append(v_e)
                #print(i)
                p_e =  p_e + ((vList[i] + vList[i-1])/2) * self.dt
                pList.append(p_e)
            #print('p is made')
            pLists.append(pList)
        return pLists

    def fbIntegrator(self, steps):
        pLists = []
        accLists = []
        print('plists 2 declared')
        for step in steps:
            acc = step[:,4:7]
            accList = []
            for a in acc:
                accList.append(np.array([[a[0]], [a[1]], [a[2]]]))
            accLists.append(accList)
        for aList in accLists:
            v_ef = np.array([[0], [0], [0]])
            v_eb = np.array([[0], [0], [0]])
            vfList = [v_ef]
            vbList = [v_eb]
            weights = [0]
            m = 0.1
            N = len(aList)

            #aList = a_sList        #uncomment to view gait pre-transformation to room coordinates

            for i in range(1, N):
                v_ef = v_ef + ((aList[i] + aList[i-1])/2) * self.dt
                vfList.append(v_ef)

                j = N - i - 1
                v_eb = v_eb + ((aList[j]+ aList[j+1])/2) * self.dt
                vbList.append(v_eb)

                w = 1/(1 + math.exp(m*(i-(N/2))))
                weights.append(w)

            vbList.reverse()

            v_e = np.array([[0], [0], [0]])
            p_e = np.array([[0], [0], [0]])
            vList = [np.array([[0], [0], [0]])]
            pList = [np.array([[0], [0], [0]])]
            for i in range(1, len(vfList)):
                v_e = weights[i] * vfList[i] + (1-weights[i]) * vbList[i]
                vList.append(v_e)

                p_e = p_e + ((vList[i] + vList[i-1])/2) * self.dt
                pList.append(p_e)
            pLists.append(pList)
        return pLists

    def getPositionalArrays(self, pLists2):
        p_xList2 = np.zeros([len(pLists2),len(pLists2)*5],dtype=float)
        p_yList2 = np.zeros([len(pLists2),len(pLists2)*5],dtype=float)
        p_zList2 = np.zeros([len(pLists2),len(pLists2)*5],dtype=float)
        for i in range(len(pLists2)):
            j = 0
            for arr in self.pLists2[i]:
                p_xList2[i,j] = (float(arr[0]))
                p_yList2[i, j] = (float(arr[1]))
                p_zList2[i,j] = (float(arr[2]))
                j+= 1
        return p_xList2, p_yList2, p_zList2