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
        print(self.fpath)
        np.savetxt(self.fpath, self.init, fmt="%1.3f", delimiter=',', header=self.head, comments=self.comms) #fmt = formatting(3 decimal places float), delimiter is comma cause csv

    def appendfile(self, data):
        with open(self.fpath, 'a') as filpath:
            np.savetxt(filpath, data, fmt="%1.3f", delimiter=',')

if __name__ == "__main__":

    test = wrtout("test")
    wans = np.ones([100,13])
    
    for i in range(100):
        test.appendfile(wans)