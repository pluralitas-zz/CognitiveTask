import os, numpy as np
from psychopy import parallel

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
            self.prt = parallel.ParallelPort(address=0x3EFC)
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