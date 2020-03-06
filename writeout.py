import sys, os, csv    
import time
import timer
import numpy as np
import serial
import VideoPlayer, cdown #videos
import flank, verb, verbB, spaceA #tasks
import threading
from xinput3_KeyboardControll_NES_Shooter_addGameTask import sample_first_joystick
from PyQt5 import Qt, QtCore, QtGui, QtWidgets, QtMultimediaWidgets, QtMultimedia,QtTest
from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime, Qt 
from PyQt5.QtWidgets import QApplication,  QDialog,  QLineEdit,QLabel, QVBoxLayout,QMessageBox
from EncoderNew import encoder
from pynput.keyboard import Key, Controller
from Powermeter_Test2 import *
from BackendThread import EncDAQBackThread, PedalThread


class writeout:

    _writearray = pyqtSignal(np.array())

    def __init__:
        pass






if __name__ == "__main__":
    filed = os.path.join(os.getcwd()+"out.txt")
header = ["Time","Elapsed Time", "Speed", "EMG 1", "EMG 2", "EMG 3", "EMG 4","Heart Rate", "Inst. Power", "Accum. Power", "Balance L", "Balance R"]
with open("out.txt", "w") as output:
    output.write(str(header)+ '\n')
output.close()

#EMG data
EMGarr = np.ones((10,4))

#Actual Time
TimeAct = time.time()

#HUD Values
TimeElsp = 50
encspd = 30
HR = 93
PwInst = 10
PwAcc = 2.3754576
CadInst = 30
BalL = 50
BalR = 50

# Tasks
TaskCon = "User Answer"


###############################################################s

#Gen array for HUD values
HUDValArr = np.empty((len(EMGarr),1))*np.nan
#HUDValArr = np.ones((len(EMGarr),1))
HUDValArr[0] = 1

#Create list for Task Condition
TaskConList=[None]*len(EMGarr)
TaskConList[0] = TaskCon

#Insert HUD values into array
TimeActArr = HUDValArr*TimeAct
TimeElspArr = HUDValArr*TimeElsp
encspdArr = HUDValArr*encspd
HRArr = HUDValArr*HR
PwInstArr = HUDValArr*PwInst
PwAccArr = HUDValArr*PwAcc
CadInstArr = HUDValArr*CadInst
BalLArr = HUDValArr*BalL
BalRArr = HUDValArr*BalR


OutArr=np.concatenate((TimeActArr, TimeElspArr, encspdArr, EMGarr, HRArr, PwInstArr, PwAccArr, BalLArr, BalRArr),axis=1)
OutArr = np.array_str(OutArr, precision=3)

print(OutArr)
# f = open("out.txt","a")
# np.savetxt(f,OutArr,delimiter=",")
# f.close()
