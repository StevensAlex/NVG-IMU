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
import csv

class GUI:

    def __init__(self, window):
        window.title("xIMU analysis")
        window.minsize(400,600)
        #window.geometry()
        
        self.min_t_val = 0
        self.min_t_val = 0
        self.indexStart=0
        self.indexStop=0
        self.total_steps = 0
        self.step_frequency =0
        self.stdv_steps =0
        self.step_height = 0
        self.stdv_height = 0
        self.max_height = 0
        self.min_height = 0
        self.step_length = 0
        self.stdv_length = 0
        self.stepsText = tk.StringVar(window)
        self.frequencyText = tk.StringVar(window)
        self.heightText1 = tk.StringVar(window)
        self.heightText2 = tk.StringVar(window)
        self.lengthText = tk.StringVar(window)
        self.updateValues(self.total_steps,self.step_frequency,self.stdv_steps,self.step_height,self.stdv_height,self.max_height,self.min_height,self.step_length,self.stdv_length)
        self.stepsLabel = tk.Label(window, textvariable=self.stepsText, font=("Arial", 11)).place(x=35,y=150)
        self.frequencyLabel = tk.Label(window,textvariable=self.frequencyText,font=("Arial", 11)).place(x=35,y=170)
        self.heightLabel1 = tk.Label(window,textvariable=self.heightText1,font=("Arial", 11)).place(x=35,y=230)
        self.heightLabel2 = tk.Label(window,textvariable=self.heightText2,font=("Arial", 11)).place(x=35,y=250)
        self.lengthLabel = tk.Label(window,textvariable=self.lengthText,font=("Arial", 11)).place(x=35,y=310)
        
        tk.Button(
            window,
            text="Välj fil",
            bg='gray',
            fg='black',
            command= self.enterData
            ).place(x=50, y=25)

        tk.Button(
            window,
            text="Välj betingelse",
            bg='gray',
            fg='black',
            command=self.enterBet
            ).place(x=165, y=25)

        tk.Label(text="Tidsinterval:",font=("Arial", 10)).place(x=30, y=65)
        self.t1String = tk.StringVar(window)
        self.t2String = tk.StringVar(window)
        self.t1 = tk.Entry(window, textvariable=self.t1String, width=6, bg='#FDF0CC', font=("Arial", 11)).place(x=35, y=85)          #change to beige-gray instead of yellow
        self.t2 = tk.Entry(window, textvariable=self.t2String, width=6, bg='#FDF0CC', font=("Arial", 11)).place(x=90, y=85)
        
        tk.Button(
            window,
            text="Kör!",
            bg='green',
            fg='white',
            command=self.runCalc          
            ).place(x=180, y=80)
        
        tk.Label(text="Stegfrekvens:",font=("Arial", 15)).place(x=30, y=120)        
        tk.Label(text="Steghöjd:",font=("Arial", 15)).place(x=30, y=200)
        tk.Label(text="Steglängd:",font=("Arial", 15)).place(x=30, y=280)
        #tk.Label(text="Sidostegsvariation:",font=("Arial", 15)).place(x = 30, y = 340)
        tk.Label(text="Se grafer:",font=("Arial", 15)).place(x=30, y=400)

        tk.Button(
            window,
            text="2D",
            bg='gray',
            fg='black',
            command=self.plot2d
            ).place(x=60, y=430)
        tk.Button(
            window,
            text="3D",
            bg='gray',
            fg='black',
            command=self.plot3d
            ).place(x=160, y=430)
        
        tk.Label(text="Lägg till kommentar:",font=("Arial", 11)).place(x = 30, y = 500)
        self.comment = tk.StringVar(window)
        self.entry = tk.Entry(window,textvariable=self.comment, width=31, borderwidth=5, font=("Arial", 12)).place(x=35, y=525)

        tk.Button(
            window,
            text="Spara",
            command=self.saveToFile
            ).place(x=340, y=525)
    

    def updateValues(self, total_steps, step_frequency, stdv_steps, step_height, stdv_height, max_height, min_height, step_length, stdv_length):
        self.stepsText.set('Antal steg ' + f"{str(self.total_steps):<5}")
        self.frequencyText.set('Medel '+ f"{str(self.step_frequency)+ ' m':<18}" +'  Stdv ' + f"{str(self.stdv_steps)+ ' m':<18}")
        self.heightText1.set('Medelhöjd ' + f"{str(self.step_height) + ' m':<18}"+ '  Stdv ' + f"{str(stdv_height)+ ' m':<18}")
        self.heightText2.set('Maxhöjd   '+ f"{str(self.max_height)+ ' m':<18}" + '  Minhöjd ' + f"{str(self.min_height)+ ' m':<18}")
        self.lengthText.set('Medellängd ' + f"{str(self.step_length)+ ' m':<18}" + '  Stdv ' + f"{str(self.stdv_length)+ ' m':<18}")

    def enterData(self):
        try:
            self.subject = imp.Subject()
            self.dataArrays = arrH.DataArrays()
            self.dataArrays.setArrays(self.subject)
            tk.Label(window, text="Laddat",font=("Arial", 8)).place(x=55,y=50)
            messagebox.showinfo("Notification","Datat har laddat färdigt!")
        except:
            messagebox.showerror("Notification","Datat kunde inte laddas! \nFörsök igen!")

    def enterBet(self):
        try:
            arrLA = self.dataArrays.getArray("dataArray")
            arrN = self.dataArrays.getArray("neckArray")
            self.fig, self.ax = plt.subplots()
            if (len(arrLA) >= len(arrN)):
                time = self.dataArrays.timeConversion("dataArray",0,(len(arrLA)))
                newArr = np.zeros((len(arrLA)), dtype = float)
                for i in range(len(arrN)):
                    newArr[i] = arrN[i,5]
                self.ax.plot(time, arrLA[:,5],label="LA-y")
            else:
                time = self.dataArrays.timeConversion("neckArray",0,(len(arrN)))
                newArr = np.zeros((len(arrN)), dtype = float)
                for i in range(len(arrLA)):
                    newArr[i] = arrLA[i,5]
                self.ax.plot(time, arrN[:,5],label="N-y")
            self.ax.plot(time, newArr,label="acc-y")

            self.minP = 0
            self.maxP = 0
            lineprops = {'color': 'red','linewidth': 4, 'alpha': 0.8}
            self.lasso = LassoSelector(self.ax, onselect = self.onSelect, lineprops= lineprops, button=1)
            self.fig.canvas.mpl_connect("key_press_event", self.accept)
            self.ax.set_title("Press enter to accept selected points.")
            plt.legend()
            plt.show()
        except:
            messagebox.showwarning("Notification", "Ingen fil är annu inläst!")


    def onSelect(self,xy):
        dtype = [('x', float), ('y', float)]
        points = np.array(xy, dtype=dtype)
        sPoints = np.sort(points, order= 'x')
        spPoints = np.reshape(sPoints,[len(sPoints),1])
        self.minP = float(spPoints[0]['x']) 
        self.maxP = float(spPoints[(len(sPoints)-1)]['x'])

    def accept(self, event):
        if event.key == "enter":
            if (self.minP >= 0 and self.maxP>0):
                start = self.dataArrays.getIndexFromTime("dataArray",self.minP)
                stopp = self.dataArrays.getIndexFromTime("dataArray",self.maxP)
                self.lasso.disconnect_events()
                self.ax.set_title("")
                plt.close('all')
                if( (stopp > start ) and (stopp > 0 )):
                    self.calculations = calc.Calculations(self.dataArrays)
                    self.calculations.setArrayHandler(self.dataArrays)
                    self.betArr = self.calculations.betDetection(start, stopp)
                    if(len(self.betArr)>=2):
                        cutTime = self.dataArrays.timeConversion("dataArray",int(self.betArr[0][0]),int(self.betArr[1][0]))
                        self.indexStart = int(self.betArr[0][0])
                        self.indexStop = int(self.betArr[1][0])
                        if len(self.betArr) > 2:
                            messagebox.showinfo("Notification", "Mer än en betingelse detekterades! \nBeräknar på första. Om osäker på vilken det är,\nvänligen välj ny betingelse.")
                        self.t1String.set(cutTime[0])
                        self.t2String.set(cutTime[(len(cutTime)-1)])
                        self.min_t_val = float(self.t1String.get())
                        self.max_t_val = float(self.t2String.get())
                    else:
                        messagebox.showwarning("Notification", "Ingen data detekterades, \nvänligen försök igen!")
                        self.t1String.set(' ')
                        self.t2String.set(' ')
                else:
                    messagebox.showwarning("Notification", "Ingen korrekt markering av data gjordes!")
                    self.t1String.set(' ')
                    self.t2String.set(' ')
   
    def runCalc(self):
        try:
            self.timeStart = float(self.t1String.get())
            self.timeStop = float(self.t2String.get())
            if(self.timeStop - self.timeStart < 30 ):
                mssagebox.showinfo("Notification", "Intervallet är för kort! \nMåste vara större än 30 sekunder!")
            elif(self.timeStop>self.timeStart and self.timeStart>=self.min_t_val and self.timeStop<=self.max_t_val):
                self.calculations.setDataArray(self.timeStart,self.timeStop, self.indexStart,self.indexStop)
                self.calculations.setDt(self.calculations.dataArrays.dataTime, self.dataArrays.dataArray)
                a = self.calculations.getGaits()
                #Temporärt utseende
                stepsArr = self.calculations.stepFrequency()
                self.total_steps = len(stepsArr)
                self.step_frequency = stat.mean(stepsArr)
                self.stdv_steps = stat.stdev(stepsArr)
            elif(self.timeStart<self.min_t_val and self.max_t_val>0 ):
                messagebox.showinfo("Notification", "Starttiden kan inte vara mindre \nän "+ str(self.min_t_val)+ "!")
            elif(self.timeStop>self.max_t_val and self.max_t_val>0 ):
                messagebox.showinfo("Notification", "Sluttiden kan inte vara större \nän "+ str(self.max_t_val)+ "!")
            elif(self.timeStart>self.timeStop):
                messagebox.showinfo("Notification", "Starttiden kan inte vara större än sluttiden!")
            else:
                messagebox.showinfo("Notification", "Ingen data är tillgänglig! \nVänligen kontrollera att filer är \nimporterade och betingelse är vald.")
        except:
            messagebox.showinfo("Notification", "Fönstrena tar bara emot siffror! \nKontrollera att inget tecken kom med och försök igen.")
        self.updateValues(self.total_steps, self.step_frequency, self.stdv_steps, self.step_height, self.stdv_height,self.max_height,self.min_height,self.step_length,self.stdv_length)

    def plot2d(self):   #Not yet done
        print("2D")

    def plot3d(self):   #Not yet done
        print("3D")
        ax = plt.axes(projection='3d')
        ax.scatter3D(p_xList, p_yList, p_zList);
        plt.title('Gait movement')
        plt.show()

    def saveToFile(self):
        try:
        #fN = imp.Subject.getFileName(self)
        #print(fN)
        #csv.register_dialect('myDialect', delimiter='/', quoting=csv.QUOTE_NONE)
            myData = [self.timeStart, self.timeStop, str(self.total_steps), str(self.step_frequency), str(self.stdv_steps),str(self.step_height), str(self.stdv_height), 
                    str(self.max_height),str(self.min_height),str(self.step_length),str(self.stdv_length), self.comment.get()]
            print(myData)
        #myFile = open('resultat.csv', 'w')
        #with myFile:
        #    writer = csv.writer(myFile, dialect='myDialect')
        #    myFields = ['Startsek', 'Stopsek', 'Antal steg', 'Stegfrekvens', 'Stdv stegfrekvens', 'Medelhöjd', 'Stdv steghöjd',
        #     '         Maxhöjd', 'Minhöjd', 'Steglängd', 'Stdv steglängd', 'Kommentar']
        #    writer = csv.DictWriter(myFile, fieldnames=myFields)    
        #    writer.writeheader()
        #    writer.writerow(myData)
        except:
            messagebox.showwarning("Notification", "Saknas tillräckligt med information! \nHar beräkning genomförts?")
window = tk.Tk()
GUI(window)
window.mainloop()