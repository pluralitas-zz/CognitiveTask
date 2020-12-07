import time, threading, numpy as np
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtTest
from DAQAcq import daq
from EncoderNew import encoder
from antreceiver import antrcv
from xinput3_KeyboardControll_NES_Shooter_addGameTask import sample_first_joystick
from pynput.keyboard import Key, Controller
#from Powermeter_Test2 import main, DAQfunc
from writeout import wrtbin
            
class EncDAQBackThread(QtCore.QThread):
    DAQ = daq()
    # create signal slots
    _encoderSpeed = QtCore.pyqtSignal(int)
    _etime = QtCore.pyqtSignal(int)

    # Variables for DAQ
    samp_rate = 1000 #for DAQ (Hz)
    samples = 20 #per acquisition
    inittime = 0
    daqarr = [[0]*samples]*4

    # determines EncDAQ while loop sampling rate
    period = 1/samp_rate*samples #1/1000*20 = 0.02

    # Variables for encoder
    acq_rate = samp_rate/samples #sample rate of Encoder slaved to each acquisition of DAQ 100/2 = 50 
    sam_period = 1 #period to collect signals sec 
    samp = acq_rate*sam_period #50*1*20 = 1000 samples
    degtravelled = []
    newdiff = 0
    speed = 0
    counter = 0

    # Variables for Writeout 
    timecount = 0
    antwout = [0,0,0,0,0]

    def __init__(self,data):
        super(EncDAQBackThread,self).__init__()
        self.inittime = time.time()
        self.counter = 0

        self.writefile=wrtbin(data) # Initialize writeout data file
        self.comb = []

        self.Encoder=encoder() # Initialize Encoder
        self.degold = self.Encoder.deg

    def run(self):
        while True:
            self.t = (time.time() + self.period)*1000
        ############################# Encoder
            self.degnow = self.Encoder.deg #Read Encoder Degree
            ## check whether encoder is going forward or in reverse
            if ((self.degold - self.degnow) > 180):
                self.newdiff = self.degnow - self.degold + 360
            elif ((self.degold - self.degnow) < -180):
                self.newdiff = self.degnow - self.degold - 360
            else:
                self.newdiff = self.degnow - self.degold
            self.degold = self.degnow
            self.degtravelled.append(self.newdiff)
            
            ## if appended to size defined by sam_period then calculate speed and emit
            if len(self.degtravelled) == self.samp:
                self.speed = int(sum(self.degtravelled)/self.sam_period*60/360) #calculate rpm
                self._encoderSpeed.emit(self.speed)
                self.degtravelled=[]

            ############################# Acquire DAQ data
            self.daqarr = self.DAQ.acqdaq(self.samp_rate,self.samples)

            ############################# combine System Time, Elapsed Time, Degree, Speed, EMG output, HR and Pedal output to emit to writeout.py
            self.comb.append([(time.time()-self.inittime)*1000] * self.samples)
            self.comb.append([self.timecount]                   * self.samples)
            self.comb.append([self.degnow*10]                   * self.samples)
            self.comb.append([self.speed]                       * self.samples)
            for i in range(4):
                self.comb.append(self.daqarr[i])
            for i in range(5):
                self.comb.append([self.antwout[i]]              * self.samples)

            self.writeout(np.array(self.comb).T.astype('uint16'))
            if self.counter == self.acq_rate/2:
                self._etime.emit((time.time()-self.inittime)*1000)
                self.counter = 0
            else: pass
            ############################# Reset
            self.comb = []
            self.counter += 1
            QtTest.QTest.qWait(max(0,self.t-time.time()*1000))

    def writeout(self,data): #systime, elapsed time, deg, speed, EMG x 4, heartrate, InstPower, AccumPower, InstCadence, pedalBalRight
        self.writefile.appendfile(data) #write data to file

    def ANTrcv(self,data):
        self.antwout = data

    def Timercv(self,data):
        self.timecount = data
         
class PedalThread(QtCore.QThread):
    # Create Signal Slot 
    _pedalValue = QtCore.pyqtSignal(list)
    _HeartRate = QtCore.pyqtSignal(int)
    _ANTwrtout = QtCore.pyqtSignal(list)

    def __init__(self):
        super(PedalThread,self).__init__()
        self.antdata = antrcv()
    
    #Run function
    def run(self):
        while True:
            self.pedalRead=self.antdata.antacq()  #[[InstPower, AvgPower, InstCadence, pedalBalRight, eventCount][heartRate]]           
            self._pedalValue.emit([self.pedalRead[0][0],self.pedalRead[0][1]*2,self.pedalRead[0][2],self.pedalRead[0][3]]) 
            self._HeartRate.emit(self.pedalRead[1][0])
            self._ANTwrtout.emit([self.pedalRead[1][0],self.pedalRead[0][0],self.pedalRead[0][1]*2,self.pedalRead[0][2],self.pedalRead[0][3]])#HeartRate,InstPower,AccumPower

if __name__ == '__main__':
    pedThread = PedalThread()
    pedThread.start()
