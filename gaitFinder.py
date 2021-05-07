import numpy as np
import statistics as stat
import matplotlib.pyplot as plt

class GaitFinder:
    def __init__(self, dataArray, dt):

        #Prepare data
        self.gyroZ = dataArray[:,3]
        self.filZ = self.filter(self.gyroZ)
        plt.figure()

        #Calculate new data
        self.peaks = self.findPeaks(self.filZ)
        self.strikes = self.findStrikes(self.peaks, self.filZ)
        self.offs = self.findOffs(self.strikes, self.filZ)
        self.splits = self.findSplits(self.filZ, self.strikes, self.offs)
        self.cutArr, self.splits = self.dataCutter(self.splits, self.filZ, dt)
        self.fqs = self.getFqs(self.splits, dt)

        #===========Plot-stuff==============
        xArr = np.arange(len(self.gyroZ))
        plt.plot(xArr, self.gyroZ, label='raw')
        plt.plot(xArr, self.filZ, label='filtered')
        plt.legend()
        for peak in self.peaks:
            plt.axvline(peak, color = 'r', ymin= 0.15, ymax=0.85)
        for strike in self.strikes:
            plt.axvline(strike, color = 'g', ymin= 0.15, ymax=0.85)
        for off in self.offs:
            plt.axvline(off, color = 'm', ymin= 0.15, ymax=0.85)
        plt.show()
        #===========Plot-stuff==============


    def filter(self, data):           # A median filter on a 1d array
        windowSize = 5
        radius = int(windowSize/2)
        newData = np.zeros(len(data))
        for i in range(radius, len(data)-1-radius):
            newData[i] = stat.median(data[i-radius:i+radius])
        return newData

    def findPeaks(self, data):
        peaks = []
        i = 0
        while i < len(data):
            if data[i] < -200:
                #step until > -200, find miniumum in between, set i to index where data[i]>-200 again
                for j in range(i+1, len(data)):
                    if data[j] > -200:
                        peaks.append(i + np.argmin(data[i:j]))
                        i = j
                        break
            i += 1
        return peaks

    def findStrikes(self, peaks, data):
        threshold = 90
        heelStrikes = []
        i = 0
        while i < len(peaks) - 1:
            for j in range(peaks[i], peaks[i] + int((peaks[i+1] - peaks[i])/2)):
                if data[j] > threshold:
                    for k in range(j, peaks[i] + int((peaks[i+1] - peaks[i])/2)):
                        if data[k] < threshold:
                            if data[k + np.argmax(data[k:k+int((peaks[i+1] - peaks[i])/4)])] > threshold:
                                heelStrikes.append(k + np.argmax(data[k:k+int((peaks[i+1] - peaks[i])/4)]))
                            else:
                                heelStrikes.append(j + np.argmax(data[j:k]))
                            break
                    break
            i += 1
        return heelStrikes

    def findOffs(self, strikes, data):
        threshold = 120
        offs = []
        i = 0
        while i < len(strikes):
            for j in range(strikes[i] + 50, strikes[i]+150):
                if data[j] > threshold:
                    for k in range(j, strikes[i]+150):
                        if data[k] < threshold:
                            offs.append(j + np.argmax(data[j:k]))
                            break
                    break
            i += 1
        return offs

    def findSplits(self, data, strikes, offs):
        splits = []
        for i in range(len(strikes)):
            raw = data[strikes[i]:offs[i]]
            axis = np.arange(strikes[i], offs[i])
            model = np.poly1d(np.polyfit(axis, raw, 2))
            split = strikes[i] + np.argmin(model(axis))
            plt.plot(axis, model(axis), color='b')
            plt.axvline(split, color = 'b', ymin= 0.15, ymax=0.85)
            splits.append(split)
        return splits

    def dataCutter(self, splits, data, dt):
        minTime = 60
        t = 0
        finalSplitIndex = 0
        for i in range(len(splits) - 1):
            t += (splits[i+1] - splits[i]) * dt
            if t > minTime:
                finalSplitIndex = i
                break
        cutArr = data[splits[0]:splits[finalSplitIndex]]
        splits = splits[0:finalSplitIndex]
        return cutArr, splits
        
    def getFqs(self, splits, dt):
        fqs = []
        for i in range(1, len(splits)-1):
            t = (splits[i] - splits[i-1]) * dt
            fqs.append(1/t)
        print(stat.mean(fqs), 'hz')
            
