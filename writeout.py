import os, numpy as np
from psychopy import parallel

class wrtout:
    savepath = "C:\\Data" #data savepath
    head = 'Time*1000,ElapsedTime,Deg*10,Speed,QCLeft*1000,HSLeft*1000,QCRight*1000,HSRight*1000,HeartRate,InstPower,AvgPower,InstCad,BalanceR' #header
    init = np.zeros([1,13])
    comms = "1000Hz sampling rate, 10samples from DAQ for EMG(s)\r\nEncoder angle w.r.t. LEFT crank angle is synchronised to DAQ once every 10 samples(100Hz)\r\nHeart Rate Data, Pedal Data at 1 Hz\r\n" #comments

    def __init__(self,filename):
        self.timenow = str(np.datetime64('now')).replace(":","") #create timestamp for file
        self.fname = filename + "_" + self.timenow + ".csv" #join username with timestamp for file name
        self.fpath = os.path.join(self.savepath, self.fname)
        np.savetxt(self.fpath, self.init, fmt="%d", delimiter=',', header=self.head, comments=self.comms) #fmt = formatting(3 decimal places float), delimiter is comma cause csv

    def appendfile(self, data):
        with open(self.fpath, 'ab') as filpath: #'ab' for append, binary mode
            np.savetxt(filpath, data, fmt="%d", delimiter=',')

class wrtbin:
    savepath = "C:\\Data" #data savepath
    head = 'Time*1000,ElapsedTime,Deg*10,Speed,QCLeft*1000,HSLeft*1000,QCRight*1000,HSRight*1000,HeartRate,InstPower,AvgPower,InstCad,BalanceR' #header
    init = np.zeros([1,13])

    def __init__(self,filename):
        self.timenow = str(np.datetime64('now')).replace(":","") #create timestamp for file
        self.fname = filename + "__" + self.timenow + "_13col_uint16.dat" #join username with timestamp for file name
        self.fpath = os.path.join(self.savepath, self.fname)
        self.init.tofile(self.fpath)

    def appendfile(self,data):
        with open(self.fpath, 'ab') as filpath:
            data.tofile(filpath)

class wrttask:
    savepath = "C:\\Data"
    head = 'Time, ID'
    comms = "Check ID"
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
    t = 23.45
    out3 =[]
    test = wrtbin("testt")
    # wans = np.random.rand(4,12)*1000
    samparr = np.ones((1,5))
    wans = np.ones((4,5))
    toos = np.ones((5,6))
    timenow = str(np.datetime64('now')).replace(":","")
    # out = np.column_stack([np.ones((5,1))*(time.time()-t)*1000, wans])


    out = np.append(samparr*t*100,samparr*t*1000,axis=0)
    out2 = np.concatenate((samparr*t*100,samparr*t*1000),axis=0)

    out = np.append(out, np.ones((2,5))*3,axis=0)
    out2 = np.concatenate((out2,np.ones((2,5))*3),axis=0)    

    # out = np.append(out, np.ones((1,5))*t*10,axis=0)
    # out2 = np.concatenate((out2,np.ones((1,5))*t*10),axis=0)

    # out = np.append(out, wans,axis=0)
    # out2 = np.concatenate((out2,wans),axis=0)

    out = np.append(out,toos.T*2,axis=0).T
    out2 = np.concatenate((out2,toos.T*2),axis=0).T

    print(out.astype(int))
    print("space")
    # print(out2.astype(int))

    samparr = np.ones(5)

    a = samparr*t*100
    out3.append(a.tolist())
    a = samparr*t*1000
    out3.append(a.tolist())
    a = np.ones((2,5))*3
    for i in range(2):
        out3.append(a[i].tolist())
    # out3.append(np.ones((1,5))*t*10.tolist())
    # out3.append(wans.tolist())
    a = toos*2
    for i in range(6):
        out3.append(a.T[i].tolist())
    print(np.array(out3).T.astype(int))

    # for i in range(100):
    #     test.appendfile(out.astype('int32'))