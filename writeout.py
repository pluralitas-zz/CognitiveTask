import os, numpy as np

class wrtout:
    savepath = "C:\\Data" #data savepath
    head = 'Time,Elapsed Time,Deg,Speed,Heart Rate,QC Left,HS Left,QC Right,HS Right,Inst. Power,Accum. Power,Inst. Cad,Balance R' #header
    init = np.zeros([1,13])
    comms = "1000Hz, 100samples from DAQ; HR and EMG(s)\r\nEncoder angle w.r.t. LEFT crank is synchronised to DAQ once every 100 samples\r\nPedal Data at 1 Hz\r\n" #comments

    def __init__(self,filename):
        self.timenow = str(np.datetime64('now')).replace(":","") #create timestamp for file
        self.fname = filename + "_" + self.timenow + ".csv" #join username with timestamp for file name
        self.fpath = os.path.join(self.savepath, self.fname)
        np.savetxt(self.fpath, self.init, fmt="%1.3f", delimiter=',', header=self.head, comments=self.comms) #fmt = formatting(3 decimal places float), delimiter is comma cause csv

    def appendfile(self, data):
        with open(self.fpath, 'ab') as filpath: #'ab' for append, binary mode
            np.savetxt(filpath, data, fmt="%1.3f", delimiter=',')

class wrttask:
    savepath = "C:\\Data"
    head = 'Time, ID'
    init = np.zeros([0,2])
    comms = 'Check ID'

    def __init__(self,filename):
        self.timenow = str(np.datetime64('now')).replace(":","") #create timestamp for file
        self.fname = filename + "_task_" + self.timenow + ".csv" #join username with timestamp for file name
        self.fpath = os.path.join(self.savepath, self.fname)
        np.savetxt(self.fpath, self.init, fmt="%s", delimiter=',', header=self.head, comments=self.comms) #fmt = formatting(3 decimal places float), delimiter is comma cause csv
    
    def appendfile(self, data):
        with open(self.fpath, 'ab') as filpath: #'ab' for append, binary mode
            np.savetxt(filpath, data, delimiter=',',fmt="%s")

if __name__ == "__main__":

    test = wrttask("test")
    wans = "Hello World"
    timenow = str(np.datetime64('now')).replace(":","")
    out = np.column_stack([timenow, str(wans)])
    for i in range(100):
        test.appendfile(out)

class paraout:
    def __init__(self):
        #LPT1 = 0x378, LPT2=0x278, LPT3=0x3BC
        port = parallel.ParallelPort(address=0x0278)
        port.setData(0)

    def parawrite(self,data):
        port.setData(data)
        port.setData(0)