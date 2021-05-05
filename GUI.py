import numpy as np
import tkinter as tk
from tkinter import messagebox
import arrayImporter as imp
import arrayHandler as arrH
import calculations as calc
import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from mpl_toolkits.mplot3d import axes3d
import statistics as stat                   #temporärt i GUI

class GUI:

    def __init__(self, window):
        window.title("xIMU analysis")
        window.minsize(400,600)
        #window.geometry()
        
        self.total_steps = 0
        self.step_frequency =0
        self.stdv_steps =0
        self.step_height = 0
        self.stdv_height = 0
        self.max_height = 0
        self.min_height = 0
        self.step_length = 0
        self.stdv_length = 0
        self.frequencyText = tk.StringVar(window)
        self.heightText1 = tk.StringVar(window)
        self.heightText2 = tk.StringVar(window)
        self.lengthText = tk.StringVar(window)
        self.updateValues(self, self.total_steps,self.step_frequency,self.stdv_steps,self.step_height,self.max_height,self.min_height,self.step_length,self.stdv_length)
        self.frequencyLabel = tk.Label(window,textvariable=self.frequencyText,font=("Arial", 10)).place(x=35,y=160)
        self.heightLabel1 = tk.Label(window,textvariable=self.heightText1,font=("Arial", 10)).place(x=35,y=230)
        self.heightLabel2 = tk.Label(window,textvariable=self.heightText2,font=("Arial", 10)).place(x=35,y=250)
        self.lengthLabel = tk.Label(window,textvariable=self.lengthText,font=("Arial", 10)).place(x=35,y=320)
        
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
        self.t1String = tk.StringVar(window)
        self.t2String = tk.StringVar(window)
        self.t1 = tk.Entry(window,textvariable =self.t1String, width=6, bg="yellow", font=("Arial", 10)).place(x=35, y=85)          #change to beige-gray instead of yellow
        self.t2 = tk.Entry(window, textvariable =self.t2String, width=6, bg="yellow", font=("Arial", 10)).place(x=90, y=85)
        
        tk.Button(
            window,
            text="Kör!",
            bg='green',
            fg='white',
            command=self.runCalc          
            ).place(x = 180, y = 80)
        
        tk.Label(text="Stegfrekvens:",font=("Arial", 15)).place(x = 30, y = 130)        
        tk.Label(text="Steghöjd:",font=("Arial", 15)).place(x = 30, y = 200)
        tk.Label(text="Steglängd:",font=("Arial", 15)).place(x = 30, y = 290)
        #tk.Label(text="Sidostegsvariation:\n",font=("Arial", 15)).place(x = 30, y = 340)
        tk.Label(text="Se grafer:",font=("Arial", 15)).place(x = 30, y = 400)

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
        
        tk.Label(text="Lägg till kommentar:",font=("Arial", 10)).place(x = 30, y = 500)
        entry = tk.Entry(window,width=31, borderwidth=5, font=("Arial", 10)).place(x=35, y=525)
    

    def updateValues(self, total_steps, step_frequency, stdv_steps, step_height, stdv_height, max_height, min_height, step_length, stdv_length):
        self.frequencyText.set('Antal steg ' + f"{str(self.total_steps):<5}" + ' Medel '+ f"{str(self.step_frequency)+ ' m':<10}" +'  Stdv ' + f"{str(self.stdv_steps)+ ' m':<10}")
        self.heightText1.set('Medelhöjd ' + f"{str(self.step_height) + ' m':<15}"+ '  Stdv ' + f"{str(stdv_height)+ ' m':<15}")
        self.heightText2.set('Maxhöjd   '+ f"{str(self.max_height)+ ' m':<15}" + '  Minhöjd ' + f"{str(self.min_height)+ ' m':<15}")
        self.lengthText.set('Medellängd ' + f"{str(self.step_length)+ ' m':<15}" + '  Stdv ' + f"{str(self.stdv_length)+ ' m':<15}")

    def enterData(self):
        subject = imp.Subject()
        if subject != UnboundLocalError:
            arrH.DataArrays.setArrays(self,subject)
            tk.Label(window, text="Laddat",font=("Arial", 8)).place(x=55,y=50)
            messagebox.showinfo("Notification","Datat har laddat färdigt!")
        else:
            messagebox.showerror("Notification","Datat kunde inte laddas!")

    def enterBet(self):
        arrLA = arrH.DataArrays.getArray(self,"dataArray")
        arrN = arrH.DataArrays.getArray(self, "neckArray")
        self.fig, self.ax = plt.subplots()
        if (len(arrLA) >= len(arrN)):
            time = arrH.DataArrays.timeConversion(self,"dataArray",0,(len(arrLA)))
            newArr = np.zeros((len(arrLA)), dtype = float)
            for i in range(len(arrN)):
                newArr[i] = arrN[i,5]
            self.ax.plot(time, arrLA[:,5],label="LA-y")
        else:
            time = arrH.DataArrays.timeConversion(self,"neckArray",0,(len(arrN)))
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
            dataLen = arrH.DataArrays.getArray(self,"dataArray")                      #kontroll
            start = arrH.DataArrays.getIndexFromTime(self,"dataArray",self.minP)
            stopp = arrH.DataArrays.getIndexFromTime(self,"dataArray",self.maxP)
            print("från " + str(start) + " till " + str(stopp) + " utifrån " + str(len(dataLen)))
            #indexes = np.arange(start,stopp)
            self.lasso.disconnect_events()
            self.ax.set_title("")
            plt.close('all')
            #plt.plot(indexes, dataLen[start:stopp,5])                           #Temporär kontroll
            #plt.show()
            if( (stopp > start ) and (stopp > 0 )):
                self.betArr = calc.Calculations.betDetection(self, start, stopp)
                print(self.betArr)
                print("längden " + str(len(self.betArr)))
                cutTime = arrH.DataArrays.timeConversion(self,"dataArray",int(self.betArr[0][0]),int(self.betArr[1][0]))          
                indexes = np.arange(int(self.betArr[0][0]),int(self.betArr[1][0]))
                #plt.plot(indexes,dataLen[int(self.betArr[0][0]):int(self.betArr[1][0]),5])
                #plt.show()
                self.indexStart = int(self.betArr[0][0])
                self.indexStop = int(self.betArr[1][0])
                if len(self.betArr) > 2:
                    messagebox.showinfo("Notification", "Mer än en betingelse detekterades! \n Beräknar på första. Om osäker på vilken det är,\nvänligen välj ny betingelse.")
                self.t1String.set(cutTime[0])
                self.t2String.set(cutTime[(len(cutTime)-1)])
            else:
                messagebox.showwarning("Notification", "Ingen korrekt markering av data gjordes!")
            #tk.Label(window, text="Vald",font=("Arial", 8)).place(x=170,y=50)
   
    def runCalc(self):
        t1 = float(self.t1String.get())
        t2 = float(self.t2String.get())
        if(t2>t1 and t1 >= 0):
            stepsArr = calc.Calculations.stepFrequency(self,t1,t2, self.indexStart,self.indexStop)
            print(stepsArr)
            self.total_steps = len(stepsArr)
            self.step_frequency = stat.mean(stepsArr)
            self.stdv_steps = stat.stdev(stepsArr)
        self.updateValues(self, self.total_steps,self.step_frequency,self.stdv_steps,self.step_height,self.max_height,self.min_height,self.step_length,self.stdv_length)

    def plot2d(self):
        print("2D")

    def plot3d(self):   #Not yet done
        print("3D")
        ax = plt.axes(projection='3d')
        ax.scatter3D(p_xList, p_yList, p_zList);
        plt.title('Gait movement')
        plt.show()


window = tk.Tk()
GUI(window)
window.mainloop()