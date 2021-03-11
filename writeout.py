import os, numpy as np
from psychopy import parallel

class paraout:
    def __init__(self):
        #LPT1 = 0x378, LPT2=0x278, LPT3=0x3BC
        # try:
        #     self.prt = parallel.ParallelPort(address=0x0278)
        #     self.prtsuccess = True
        # except:
            self.prtsuccess = False

    def parawrite(self,data):
        if self.prtsuccess == True:
            self.prt.setData(data)
            self.prt.setData(0)

if __name__ == "__main__":
    import numpy as np
    import time