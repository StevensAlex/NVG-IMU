import matplotlib.pyplot as plt
import numpy as np
import math


class StepData:
    def __init__(self, stepsRaw, dt):
        self.stepsRaw = stepsRaw
        print('raw:', len(stepsRaw))
        print('raw:', len(stepsRaw[0]))
        self.dt = dt
        self.sensComp = self.driftComp(self.stepsRaw)
        self.labAcc, eu = self.angleTransformation(self.sensComp)
        
        print('pre next integrator')
        self.pLists2 = self.fbIntegrator(self.labAcc)
        self.pLists2 = self.pComp(self.pLists2)
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
        print(len(self.stepsRaw[0][:,0]))
        print(len(p_xList2))
        plt.figure()
        plt.plot(self.stepsRaw[0][:,0], p_xList2, label='x')
        plt.plot(self.stepsRaw[0][:,0], p_yList2, label='y')
        plt.plot(self.stepsRaw[0][:,0], p_zList2, label='z')
        plt.title("foot movement fb integrator")
        plt.legend()
        print('plotted')
        #=======test======
        

    def pComp(self, pLists):
        for pList in pLists:
            print('hey')
            if float(pList[0][1]) < float(pList[-1][1]):
                diff = float(pList[-1][1]) - float(pList[0][1])
                print('d',diff)
                compVal = diff/len(pList)
                print(compVal)
                for i in range(len(pList)):
                    pList[i][1] = float(pList[i][1]) - (compVal*i)
            if float(pList[0][1]) > float(pList[-1][1]):
                diff = float(pList[0][1]) - float(pList[-1][1])
                print('di', diff)
                compVal = diff/len(pList)
                print(compVal)
                for i in range(len(pList)):
                    pList[i][1] = float(pList[i][1]) + (compVal*i)
                    
        print('returning')
        return pLists


    def angleTransformation(self, steps):
        stepAccLists = []
        eulerLists = []
        a_eLists = []
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
            
            eulerList = [eulerVec]
            a_eList = [a_e]
            angVelList = [np.array([[math.radians(step[0, 1])],[math.radians(step[0, 2])],[math.radians(step[0, 3])]])]
            for i in range(1, len(step[:,0])):
                a_s = np.array([[float((step[i, 4]) *9.82)],[(float(step[i, 5]) *9.82)],[(float(step[i, 6]) *9.82)]])
                angVel = np.array([[math.radians(float(step[i, 1]))],[math.radians(float(step[i, 2]))],[math.radians(float(step[i, 3]))]])
                eulerVec += ((angVel + angVelList[-1])/2) * self.dt
                angVelList.append(angVel)
                eulerList.append(np.array([[eulerVec[0]],[eulerVec[1]],[eulerVec[2]]]))
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
            eulerLists.append(eulerList)
            a_eLists.append(a_eList)
        print('end angTran')
        return a_eLists, eulerLists


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

    def fbIntegrator(self, a_eLists):
        pLists = []
        accLists = []
        print('plists 2 declared')
        #for a_eList in a_eLists:
        #    acc = a_eList
        #    accList = []
        #    for a in acc:
        #        accList.append(np.array([[a[0]], [a[1]], [a[2]]]))
        #    accLists.append(accList)
        count = 0
        for aList in a_eLists:
            print(count)
            count += 1
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