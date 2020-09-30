import os, numpy as np, pandas as pd
from psychopy import parallel

class wrtout:
    savepath = "C:\\Data" #data savepath
    head = 'Time*1000,ElapsedTime,Deg*100,Speed,QCLeft*1000,HSLeft*1000,QCRight*1000,HSRight*1000,PPGRaw*1000,HeartRate,InstPower,AvgPower,InstCad,BalanceR' #header
    init = np.zeros([1,14])
    comms = "1000Hz sampling rate, 10samples from DAQ for EMG(s)\r\nEncoder angle w.r.t. LEFT crank angle is synchronised to DAQ once every 10 samples(100Hz)\r\nHeart Rate Data, Pedal Data at 1 Hz\r\n" #comments

    def __init__(self,filename):
        self.timenow = str(np.datetime64('now')).replace(":","") #create timestamp for file
        self.fname = filename + "_" + self.timenow + ".csv" #join username with timestamp for file name
        self.fpath = os.path.join(self.savepath, self.fname)
        np.savetxt(self.fpath, self.init, fmt="%d", delimiter=',', header=self.head, comments=self.comms) #fmt = formatting(3 decimal places float), delimiter is comma cause csv

    def appendfile(self, data):
        with open(self.fpath, 'ab') as filpath: #'ab' for append, binary mode
            np.savetxt(filpath, data, fmt="%d", delimiter=',')

class wrtdframe:
    savepath = "C:\\Data" #data savepath
    head = 'Time*1000,ElapsedTime,Deg*100,Speed,QCLeft*1000,HSLeft*1000,QCRight*1000,HSRight*1000,PPGRaw*1000,HeartRate,InstPower,AvgPower,InstCad,BalanceR' #header
    init = np.zeros([1,14])
    comms = "1000Hz sampling rate, 10samples from DAQ for EMG(s)\r\nEncoder angle w.r.t. LEFT crank angle is synchronised to DAQ once every 10 samples(100Hz)\r\nHeart Rate Data, Pedal Data at 1 Hz\r\n\r\n" #comments

    def __init__(self,filename):
        self.timenow = str(np.datetime64('now')).replace(":","") #create timestamp for file
        self.fname = filename + "__" + self.timenow + ".csv" #join username with timestamp for file name
        self.fpath = os.path.join(self.savepath, self.fname)
        self.fpath = os.path.join(self.savepath, self.fname)
        np.savetxt(self.fpath, self.init, fmt="%d", delimiter=',', header=self.head, comments=self.comms) #fmt = formatting(3 decimal places float), delimiter is comma cause csv

    def appendfile(self,dat):
        self.dt = pd.DataFrame(data=dat,dtype=np.int64)
        self.dt.to_csv(self.fpath,mode='a', index=False, header=False)

class wrtbin:
    savepath = "C:\\Data" #data savepath
    head = 'Time*1000,ElapsedTime,Deg*100,Speed,QCLeft*1000,HSLeft*1000,QCRight*1000,HSRight*1000,PPGRaw*1000,HeartRate,InstPower,AvgPower,InstCad,BalanceR' #header
    init = np.zeros([1,14])

    def __init__(self,filename):
        self.timenow = str(np.datetime64('now')).replace(":","") #create timestamp for file
        self.fname = filename + "__" + self.timenow + ".dat" #join username with timestamp for file name
        self.fpath = os.path.join(self.savepath, self.fname)
        self.init.tofile(self.fpath)

    def appendfile(self,data):
        with open(self.fpath, 'ab') as filpath:
            data.tofile(filpath)

class wrttask:
    savepath = "C:\\Data"
    head = 'Time, ID'
    init = np.zeros([0,2])

    def __init__(self,filename):
        self.timenow = str(np.datetime64('now')).replace(":","") #create timestamp for file
        self.fname = filename + "_task_" + self.timenow + ".csv" #join username with timestamp for file name
        self.fpath = os.path.join(self.savepath, self.fname)
        np.savetxt(self.fpath, self.init, fmt="%s", delimiter=',', header=self.head, comments=self.comms) #fmt = formatting(3 decimal places float), delimiter is comma cause csv
    
    def appendfile(self, data):
        with open(self.fpath, 'ab') as filpath: #'ab' for append, binary mode
            np.savetxt(filpath, data, delimiter=',',fmt="%s")

class paraout:
    prtsuccess = True
    def __init__(self):
        #LPT1 = 0x378, LPT2=0x278, LPT3=0x3BC
        try:
            self.prt = parallel.ParallelPort(address=0x0278)
        except:
            self.prtsuccess = False

    def parawrite(self,data):
        if self.prtsuccess == True:
            self.prt.setData(data)
            self.prt.setData(0)

if __name__ == "__main__":
    import numpy as np
    import time

    test = wrtbin("testt")
    wans = np.random.rand(5,13)*1000
    timenow = str(np.datetime64('now')).replace(":","")
    out = np.column_stack([np.ones((5,1))*time.time()*1000, wans])
    out = out
    print(out)
    for i in range(100):
        test.appendfile(out.astype('int64'))