import sys, os, csv, time, numpy as np
from PyQt5.QtCore import QThread,  pyqtSignal,  QDateTime, Qt 

if __name__ == "__main__":

    filed = os.path.join(os.getcwd()+"out.txt")
    header = ["Time","Elapsed Time","Deg","Speed","EMG 1","EMG 2","EMG 3","EMG 4","Heart Rate","Inst. Power","Accum. Power","Balance R"]
    with open("out.txt", "w") as output:
        output.write(str(header)+ '\n')
    output.close()