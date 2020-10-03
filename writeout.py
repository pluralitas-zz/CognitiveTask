import os, numpy as np
from psychopy import parallel

class wrtout:
    savepath = "C:\\Data" #data savepath
    head = 'Time*1000,ElapsedTime,Deg*10,Speed,QCLeft*1000,HSLeft*1000,QCRight*1000,HSRight*1000,HeartRate,InstPower,AvgPower,InstCad,BalanceR' #header
    init = np.zeros([1,13])
    comms = "1000Hz sampling rate, 10samples from DAQ for EMG(s)\r\nEncoder angle w.r.t. LEFT crank angle is synchronised to DAQ once every 10 samples(100Hz)\r\nHeart Rate Data, Pedal Data at 1 Hz\r\n" #comments

    def __init__(self,filename):
        self.timenow = str(np.datetime64('now')).replace(":","").replace("-","") #create timestamp for file
        self.fname = filename + "_" + self.timenow + ".csv" #join username with timestamp for file name
        self.fpath = os.path.join(self.savepath, self.fname)
        np.savetxt(self.fpath, self.init, fmt="%d", delimiter=',', header=self.head, comments=self.comms) #fmt = formatting(3 decimal places float), delimiter is comma cause csv

    def appendfile(self, data):
        with open(self.fpath, 'ab') as filpath: #'ab' for append, binary mode
            np.savetxt(filpath, data, fmt="%d", delimiter=',')

class wrtbin:
    savepath = "C:\\Data" #data savepath
    init = np.zeros([1,13]).astype("uint16")

    def __init__(self,filename):
        self.timenow = str(np.datetime64('now')).replace(":","").replace("-","") #create timestamp for file
        self.fname = filename + "_13col_uint16_" + self.timenow + ".dat" #join username with timestamp for file name
        self.fpath = os.path.join(self.savepath, self.fname)
        self.init.tofile(self.fpath)

    def appendfile(self,data):
        with open(self.fpath, 'ab') as filpath:
            data.tofile(filpath)

class wrttask:
    savepath = "C:\\Data"
    head = 'Time, ID\r\n'

    def __init__(self,filename):
        self.timenow = str(np.datetime64('now')).replace(":","").replace("-","") #create timestamp for file
        self.fname = filename + "_task_" + self.timenow + ".txt" #join username with timestamp for file name
        self.fpath = os.path.join(self.savepath, self.fname)
        with open(self.fpath, 'wb') as filpath:
            filpath.write(self.head.encode('ascii'))

    def appendfile(self, data):
        with open(self.fpath, 'ab') as filpath: #'ab' for append, binary mode
            filpath.write(data.encode('ascii'))

class paraout:
    def __init__(self):
        #LPT1 = 0x378, LPT2=0x278, LPT3=0x3BC
        try:
            self.prt = parallel.ParallelPort(address=0x0278)
            self.prtsuccess = True
        except:
            self.prtsuccess = False

    def parawrite(self,data):
        if self.prtsuccess == True:
            self.prt.setData(data)
            self.prt.setData(0)

if __name__ == "__main__":
    import numpy as np
    import time
    t = 23.45
    out =[]
    test = wrtbin("testt")
    # wans = np.random.rand(4,12)*1000
    samparr = np.ones((1,5))
    wans = np.ones((4,5))
    toos = np.ones((5,6))
    timenow = str(np.datetime64('now')).replace(":","")

    samp = 10
    ant = [90,20,10,5,2]
    daq = [[0]*samp]*4
    # daq = np.zeros([4,samp],dtype='uint16').tolist()
    out.append( [t*100] * samp)
    out.append( [t*100] * samp)
    out.append( [t*100] * samp)
    out.append( [t*100] * samp)
    for i in range(4):
        out.append(daq[i])
    for i in range(5):
        out.append([ant[i]]*samp)

    # for i in range(100):
    test.appendfile(np.array(out).T.astype('uint16'))