import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Progressbar
import arrayImporter as imp
import arrayHandler as arrH
import calculations as calc
import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from mpl_toolkits.mplot3d import axes3d
import statistics as stat                   #temporärt i GUI
import csv
import threading

class GUI:

    def __init__(self, window):
        window.title("xIMU analysis")
        window.minsize(410,600)
        #window.geometry()
        
        self.stepsText = tk.StringVar(window)
        self.frequencyText = tk.StringVar(window)
        self.heightText1 = tk.StringVar(window)
        self.heightText2 = tk.StringVar(window)
        self.lengthText = tk.StringVar(window)
        self.loading_text = tk.StringVar()
        self.stepsLabel = tk.Label(window, textvariable=self.stepsText, font=("Arial", 11)).place(x=35,y=150)
        self.frequencyLabel = tk.Label(window,textvariable=self.frequencyText,font=("Arial", 11)).place(x=35,y=170)
        self.heightLabel1 = tk.Label(window,textvariable=self.heightText1,font=("Arial", 11)).place(x=35,y=230)
        self.heightLabel2 = tk.Label(window,textvariable=self.heightText2,font=("Arial", 11)).place(x=35,y=250)
        self.lengthLabel = tk.Label(window,textvariable=self.lengthText,font=("Arial", 11)).place(x=35,y=310)

        self.progress = Progressbar(window,orient='horizontal',length=100, mode='indeterminate')
        self.fileimp_btn = tk.Button(window, text="Välj fil", bg='gray', fg='black', command= self.enterData)
        self.fileimp_btn.place(x=50, y=17)
        self.loading_label = tk.Label(window, textvariable=self.loading_text,fg='green',font=("Arial", 8))

        self.betsel_btn = tk.Button(window, text="Välj betingelse", bg='gray', fg='black', command=self.enterBet)
        self.betsel_btn.place(x=165, y=17)

        tk.Label(text="Tidsinterval:",font=("Arial", 10)).place(x=30, y=67)
        self.t1String = tk.StringVar(window)
        self.t2String = tk.StringVar(window)
        self.t1 = tk.Entry(window, textvariable=self.t1String, width=6, bg='#FDF0CC', font=("Arial", 11)).place(x=35, y=88)          #change to beige-gray instead of yellow
        self.t2 = tk.Entry(window, textvariable=self.t2String, width=6, bg='#FDF0CC', font=("Arial", 11)).place(x=90, y=88)
        
        self.makecalc_btn = tk.Button(window, text="Kör!", bg='green', fg='white', command=self.runCalc)
        self.makecalc_btn.place(x=180, y=85)
        
        tk.Label(text="Stegfrekvens:",font=("Arial", 15)).place(x=30, y=120)        
        tk.Label(text="Steghöjd:",font=("Arial", 15)).place(x=30, y=200)
        tk.Label(text="Steglängd:",font=("Arial", 15)).place(x=30, y=280)
        #tk.Label(text="Sidostegsvariation:",font=("Arial", 15)).place(x = 30, y = 340)
        tk.Label(text="Se grafer:",font=("Arial", 15)).place(x=30, y=400)

        tk.Button(window, text="2D", bg='gray', fg='black', command=self.plot2d).place(x=60, y=440)
        tk.Button(window, text="3D", bg='gray', fg='black', command=self.plot3d).place(x=160, y=440)

        self.prevplot_btn = tk.Button(window, text="-", fg='black', command=self.plotPrevious)
        self.prevplot_btn.place(x=230,y=440)
        self.gaitNumber = tk.IntVar(window)
        tk.Entry(window, textvariable=self.gaitNumber, width=4, font=("Arial", 11)).place(x=245, y=442)
        self.nxtplot_btn = tk.Button(window, text="+", fg='black', command=self.plotNext)
        self.nxtplot_btn.place(x=275,y=440)
        
        tk.Label(text="Lägg till kommentar:",font=("Arial", 11)).place(x = 30, y = 500)
        self.comment = tk.StringVar(window)
        self.entry = tk.Entry(window,textvariable=self.comment, width=31, borderwidth=5, font=("Arial", 12)).place(x=35, y=525)

        self.save_filename = ''
        self.saveas_btn = tk.Button(window, text="Spara som", command=self.saveAsFile).place(x=337, y=525)
        self.save_btn = tk.Button(window, text="Spara", command=self.saveToFile).place(x=337, y=555)
        
        self.resetWindow()

    def resetWindow(self):
        self.indexStart=0
        self.indexStop=0
        self.min_t_val = 0
        self.max_t_val = 0
        self.total_steps = 0
        self.step_frequency =0
        self.stdv_steps =0
        self.step_height = 0
        self.stdv_height = 0
        self.max_height = 0
        self.min_height = 0
        self.step_length = 0
        self.stdv_length = 0
        self.timeStop = 0
        self.t1String.set('')
        self.t2String.set('')
        self.comment.set('')
        self.updateValues(self.total_steps,self.step_frequency,self.stdv_steps,self.step_height,self.stdv_height,self.max_height,self.min_height,self.step_length,self.stdv_length)

    def updateValues(self, total_steps, step_frequency, stdv_steps, step_height, stdv_height, max_height, min_height, step_length, stdv_length):
        stp_fq = round(self.step_frequency,4)
        stdv_stp = round(self.stdv_steps,5)
        stp_he = round(self.step_height,4)
        stdv_he = round(self.stdv_height,5)
        max_he = round(self.max_height,4)
        min_he = round(self.min_height,4)
        stp_le = round(self.step_length, 4)
        stdv_le = round(self.stdv_length,5)
        self.stepsText.set('Antal steg ' + f"{str(total_steps):<5}")
        self.frequencyText.set('Medel '+ f"{str(stp_fq)+ ' Hz':<18}" +'  Stdv ' + f"{str(stdv_stp)+ ' Hz':<18}")
        self.heightText1.set('Medelhöjd ' + f"{str(stp_he) + ' m':<18}"+ '  Stdv ' + f"{str(stdv_he)+ ' m':<18}")
        self.heightText2.set('Maxhöjd   '+ f"{str(max_he)+ ' m':<18}" + '   Minhöjd ' + f"{str(min_he)+ ' m':<18}")
        self.lengthText.set('Medellängd ' + f"{str(stp_le)+ ' m':<18}" + '  Stdv ' + f"{str(stdv_le)+ ' m':<18}") 

    def enterData(self):
        def importing():
            try:
                self.loading_label.place_forget()
                self.subject = imp.Subject()
                self.dataArrays = arrH.DataArrays()
                self.dataArrays.setArrays(self.subject)
                data_name = self.dataArrays.getArray("fileName").split('/')        #funkar
                self.loading_text.set(str(data_name[len(data_name)-1]) +' laddat!')
                self.loading_label.place(x=42,y=47)
                self.resetWindow()
                messagebox.showinfo("Notification","Datat har laddat färdigt!")
            except:
                messagebox.showerror("Notification","Datat kunde inte laddas! \nFörsök igen!")
            finally:
                self.progress.stop()
                self.progress.place_forget()
                self.fileimp_btn['state']='normal'
                self.betsel_btn['state'] = 'normal'
                self.makecalc_btn['state']= 'normal'

        self.fileimp_btn['state'] ='disabled'
        self.betsel_btn['state'] = 'disabled'
        self.makecalc_btn['state']= 'disabled'
        self.progress.place(x=30, y=45)
        self.progress.start()
        threading.Thread(target=importing).start()

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
             #Select indexes of start and stop
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
                        self.t1String.set('')
                        self.t2String.set('')
                else:
                    messagebox.showwarning("Notification", "Ingen korrekt markering av data gjordes!")
                    self.t1String.set('')
                    self.t2String.set('')
   
    def runCalc(self):
        try:
            self.timeStart = float(self.t1String.get())
            self.timeStop = float(self.t2String.get())
            if(self.timeStart>self.timeStop):
                messagebox.showinfo("Notification", "Starttiden kan inte vara större än sluttiden!")
            elif(self.timeStop - self.timeStart < 30 ):
                messagebox.showinfo("Notification", "Intervallet är för kort! \nMåste vara större än 30 sekunder!")
            elif(self.timeStop>self.timeStart and self.timeStart>=self.min_t_val and self.timeStop<=self.max_t_val):
                self.calculations.setDataArray(self.timeStart,self.timeStop, self.indexStart,self.indexStop)
                self.calculations.setDt(self.calculations.dataArrays.dataTime, self.dataArrays.dataArray)
                a = self.calculations.getGaits()
                self.calculations.calcOutput()
                #--Temporärt utseende-------------------------------------------#
                stepsArr = self.calculations.stepFrequency()
                self.total_steps = len(stepsArr)
                self.step_frequency = stat.mean(stepsArr)
                self.stdv_steps = stat.stdev(stepsArr)
                #---------------------------------------------------------------#
            elif(self.timeStart<self.min_t_val and self.max_t_val>0 ):
                messagebox.showinfo("Notification", "Starttiden kan inte vara mindre \nän "+ str(self.min_t_val)+ "!")
            elif(self.timeStop>self.max_t_val and self.max_t_val>0 ):
                messagebox.showinfo("Notification", "Sluttiden kan inte vara större \nän "+ str(self.max_t_val)+ "!")
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

    def plotPrevious(self):
        self.gaitNumber.set(self.gaitNumber.get()-1)        

    def plotNext(self):
        self.gaitNumber.set(self.gaitNumber.get()+1)

    def saveAsFile(self):
        try:
            self.save_filename = filedialog.asksaveasfilename(title="Save data",filetypes=(("csv files", "*csv"),("all files", "")))
            if(self.save_filename != ''):
                if self.save_filename.endswith(".csv"):
                    pass
                else:
                    self.save_filename = f'{self.save_filename}.csv'
                self.saveToFile()
        except:
            messagebox.showwarning("Notification", "Något hände!")
            

    def saveToFile(self):
        try:
            if self.save_filename == '':
                self.saveAsFile()
            else:
                data_name = self.dataArrays.getArray("fileName").split('/')       #funkar
                data_name = data_name[len(data_name)-1]
                csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)
                with open(self.save_filename, 'a',  newline='') as myFile:
                    myFields = ['Filnamn', 'Startsek', 'Stopsek', 'Antal steg', 'Stegfrekvens', 'Stdv stegfrekvens', 'Medelhöjd', 'Stdv steghöjd',
                                'Maxhöjd', 'Minhöjd', 'Steglängd', 'Stdv steglängd', 'Kommentar']
                
                    writer = csv.DictWriter(myFile, fieldnames=myFields,dialect='myDialect')
                    header_check = np.genfromtxt(self.save_filename, delimiter=',')
                    if( len(header_check) == 0 ):                          #Assumes that if the file isn't new that it already have correct header
                        writer.writeheader()
                
                    writer.writerow({'Filnamn': data_name,'Startsek': self.timeStart, 'Stopsek': self.timeStop, 'Antal steg': self.total_steps, 
                        'Stegfrekvens':self.step_frequency, 'Stdv stegfrekvens':self.stdv_steps, 'Medelhöjd':self.step_height, 'Stdv steghöjd':self.stdv_height, 
                        'Maxhöjd':self.max_height, 'Minhöjd':self.min_height, 'Steglängd':self.step_length, 'Stdv steglängd':self.stdv_length, 
                        'Kommentar':self.comment.get()})
        except:
            self.save_filename = ''
            messagebox.showwarning("Notification", "Saknas tillräckligt med information! \nHar beräkning genomförts?")

window = tk.Tk()
GUI(window)
window.mainloop()