import numpy as np
import tkinter as tk
from tkinter import filedialog

def fileImport(name):

    root = tk.Tk()
    root.withdraw()

    fileName = filedialog.askopenfilename(title = ("Select", name, "file"),filetypes = (("csv files","*.csv"),("all files","*.*")))
    dataArray = np.genfromtxt(fileName, delimiter=',', skip_header=1)
    return dataArray
