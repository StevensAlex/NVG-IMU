import numpy as np
import tkinter as tk
from tkinter import messagebox
import arrayImporter as imp
import arrayHandler as arrH

import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import axes3d
import math                                 #temporärt i GUI

class GUI:

    def __init__(self, window):
        window.title("xIMU analysis")
        window.minsize(350,600)
        #window.geometry()
        
        my_string_var = tk.StringVar()
        my_string_var.set("hej")
        self.kattLabel = tk.Label(window,text =my_string_var)
        self.kattLabel.place(x=50, y=0)
        self.total_steps = 0
        self.step_frequency =0
        self.stdv_steps =0
        self.step_height = 0
        self.stdv_height = 0
        self.max_height = 0
        self.min_height = 0
        self.step_length = 0
        self.stdv_length = 0
        self.frequencyText = tk.StringVar()
        self.heightText1 = tk.StringVar()
        self.frequencyText.set("Antal steg " + str(self.total_steps)+ " m   Medel "+ str(self.step_frequency) +" m  Stdv " + str(self.stdv_steps) + " m")
        self.heightText1.set("Medelhöjd " +str(self.step_height)+" m Stdv " + str(self.stdv_height)+ " m")
        #self.updateValues(self, self.total_steps,self.step_frequency,self.stdv_steps,self.step_height,self.max_height,self.min_height,self.step_length,self.stdv_length)
        self.frequencyLabel = tk.Label(window,text=self.frequencyText,font=("Arial", 10)).place(x=35,y=160)
        self.heightLabel1 = tk.Label(window,text=self.heightText1,font=("Arial", 10)).place(x=35,y=230)

        tk.Button(
            window,
            text="Välj fil",
            bg='gray',
            fg='black',
            command= self.enterData
            ).place(x = 50, y = 25)

        tk.Button(
            window,
            text="Välj betingelse",
            bg='gray',
            fg='black',
            command=self.enterBet
            ).place(x = 165, y = 25)

        tk.Label(text="Tidsinterval:\n",font=("Arial", 10)).place(x = 30, y = 65)
        self.t1 = tk.Entry(window,font=("Arial", 10)).place(x=35, y=85)
        self.t2 = tk.Entry(window,font=("Arial", 10)).place(x=100, y=85)

        tk.Button(
            window,
            text="Kör!",
            bg='green',
            fg='white',
            command=lambda: self.updateKatt(self.katt, 5)
            #command=lambda: self.runCalc(self.t1)          #Riktiga
            ).place(x = 180, y = 80)

        #steg = 0
        #msteg = 0
        #stdsteg = 0
        tk.Label(text="Stegfrekvens:\n",font=("Arial", 15)).place(x = 30, y = 130)        
        tk.Label(text="Steghöjd:\n",font=("Arial", 15)).place(x = 30, y = 200)
        tk.Label(text="Steglängd:\n",font=("Arial", 15)).place(x = 30, y = 290)
        #tk.Label(text="Sidostegsvariation:\n",font=("Arial", 15)).place(x = 30, y = 340)
        tk.Label(text="Se grafer:\n",font=("Arial", 15)).place(x = 30, y = 400)

        tk.Button(
            window,
            text="2D",
            bg='gray',
            fg='black',
            command=self.plot2d
            ).place(x = 60, y = 430)
        tk.Button(
            window,
            text="3D",
            bg='gray',
            fg='black',
            command=self.plot3d
            ).place(x = 160, y = 430)
        
        tk.Label(text="Lägg till kommentar:\n",font=("Arial", 10)).place(x = 30, y = 500)
        entry = tk.Entry(window,font=("Arial", 10)).place(x=35, y=525)
    

    #def updateValues(self, total_steps, step_frequency, stdv_steps, step_height, stdv_height, max_height, min_height, step_length, stdv_length):
    #    self.frequencyText.set("Antal steg " + str(self.total_steps)+ " m   Medel "+ str(self.step_frequency) +" m  Stdv " + str(self.stdv_steps) + " m")
    #    self.heightText1.set("Medelhöjd " +str(self.step_height)+" m Stdv " + str(self.stdv_height)+ " m")
        
    #Orginaltexter
        tk.Label(text="Antal steg " + str(self.total_steps)+ " m   Medel "+ str(self.step_frequency) +" m  Stdv " + str(self.stdv_steps) + " m",font=("Arial", 10)).place(x=35,y=160)
        tk.Label(text='Medelhöjd ' +str(self.step_height)+' m Stdv ' + str(self.stdv_height)+ ' m',font=("Arial", 10)).place(x=35,y=230)
        tk.Label(text='Maxhöjd '+ str(self.max_height)+ ' m  Minhöjd '+str(self.min_height)+ ' m',font=("Arial", 10)).place(x=35,y=250)
        tk.Label(text="Medellängd " +str(self.step_length)+ " m  Stdv " + str(self.stdv_length) + " m",font=("Arial", 10)).place(x=35,y=320)

    def enterData(self):
        subject = imp.Subject()
        if subject != UnboundLocalError:
            hej = arrH.DataArrays()
            arrH.dataArrays.setArrays(self,subject)
            tk.Label(window, text="Laddat",font=("Arial", 8)).place(x=55,y=50)
            messagebox.showinfo("Notification","Datat har laddat färdigt!")
        else:
            messagebox.showerror("Notification","Datat kunde inte laddas!")

    def enterBet(self):
        
        arrLA = arrH.getArray(self,"dataArray")
        arrN = arrH.getArray(self, "neckArray")
        self.fig, self.ax = plt.subplots()
        if (len(arrLA) >= len(arrN)):
            time = arrH.timeConversion(self,"dataArray",0,(len(arrLA)))
            newArr = np.zeros((len(arrLA)), dtype = float)
            for i in range(len(arrN)):
                newArr[i] = arrN[i,5]
            self.ax.plot(time, arrLA[:,5],label="LA-y")
        else:
            time = arrH.timeConversion(self,"neckArray",0,(len(arrN)))
            newArr = np.zeros((len(arrN)), dtype = float)
            for i in range(len(arrLA)):
                newArr[i] = arrLA[i,5]
            self.ax.plot(time, arrN[:,5],label="N-y")
        
        self.ax.plot(time, newArr,label="acc-y")

        lineprops = {'color': 'red','linewidth': 4, 'alpha': 0.8}
        self.lasso = LassoSelector(self.ax, onselect = self.onSelect, lineprops= lineprops, button=1)
        
        self.fig.canvas.mpl_connect("key_press_event", self.accept)
        self.ax.set_title("Press enter to accept selected points.")
        plt.legend()
        plt.show()

    def onSelect(self,xy):
        dtype = [('x', float), ('y', float)]
        points = np.array(xy, dtype=dtype)
        sPoints = np.sort(points, order= 'x')
        spPoints = np.reshape(sPoints,[len(sPoints),1])
        self.minP = float(spPoints[0]['x']) 
        self.maxP = float(spPoints[(len(sPoints)-1)]['x'])
        #print(spPoints)                                         #kontroll

    def accept(self, event):
        if event.key == "enter":
            dataLen = arrH.getArray(self,"dataArray")                      #kontroll
            start = arrH.getIndexFromTime(self,"dataArray",self.minP)
            stopp = arrH.getIndexFromTime(self,"dataArray",self.maxP)
            print("från " + str(start) + " till " + str(stopp) + " utifrån " + str(len(dataLen)))
            #cutTime = arrH.timeConversion(self,"dataArray",start,stopp)
            self.lasso.disconnect_events()
            self.ax.set_title("")
            plt.close('all')
            #plt.plot(cutTime, dataLen[start:stopp,5])                           #Temporär kontroll
            #plt.show()
            if( (stopp > start ) and (stopp > 0 )):
                self.betArr = Calculations.betDetection(self, start, stopp)
                print(self.betArr)
            else:
                messagebox.showwarning("Notification", "Ingen korrekt markering av data gjordes!")
            #tk.Label(window, text="Vald",font=("Arial", 8)).place(x=170,y=50)

        
        
    def runCalc(self, t1):
        print(str(self.t1))
        self.updateValues(self, self.total_steps,self.step_frequency,self.stdv_steps,self.step_height,self.max_height,self.min_height,self.step_length,self.stdv_length)

    def plot2d(self):
        print("2D")

    def plot3d(self):
        print("3D")


class Calculations:
    def _init_(self):
        print("hej")

    def betDetection(self, startIndex, stopIndex):
        dataArray = arrH.getArray(self, "dataArray")
        print("betDet")
        def getPoints(dataArray, RMS):
            packets = []
            points = dataArray[startIndex:stopIndex,0][np.nonzero(dataArray[startIndex:stopIndex,6] > 2.4*RMS)]           #Assign acc(Z)Value > 1.7xRMS to corrresponding packet
            for i in range (1,points.size):                                         #Assign packets that lies withing sf/2,
                if points[i]-points[i-1] < sampleFrekvens/2:
                    packets.append(points[i])
            return packets
        
        sampleFrekvens = arrH.getDataRate(dataArrays.getArray(self, "dataRegist")[69,2])             #DataRate for inertia and mag
        aproxSekvensTime = 6
        dataSelection = []
        Square = 0

        for i in range(startIndex,stopIndex):
            Square += dataArray[i,6]**2
        RMS = math.sqrt(Square/(stopIndex-startIndex))
        print(RMS)

        packets = getPoints(dataArray, RMS)
        print(packets)
        for i in range(1, len(packets)-1):                                      #Remove nearby packets and remain with farends of "packet-group"
            if packets[i] - packets[i-1] > aproxSekvensTime*sampleFrekvens*50:
                dataSelection.append(packets[i])
            elif packets[i+1] - packets[i] > aproxSekvensTime*sampleFrekvens*50:
                dataSelection.append(packets[i])

        print(dataSelection)
        indexes = []
        for packet in dataSelection:
            indexes.append(np.where(dataArray[:,0] == packet))
        return indexes

    def stepFrequency(self, intvalTimeStart, intvalTimeStop):
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


window = tk.Tk()
GUI(window)
window.mainloop()