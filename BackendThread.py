import time
import timer
import numpy
import sys
import threading
import serial
import numpy as np
from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime 
from PyQt5.QtWidgets import QApplication,  QDialog,  QLineEdit,QLabel, QVBoxLayout,QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from DAQAcq import daq
from EncoderNew import encoder
from xinput3_KeyboardControll_NES_Shooter_addGameTask import sample_first_joystick
from pynput.keyboard import Key, Controller
from Powermeter_Test2 import *

class CalTimeThread(QThread):
    #Initialize time
    time=pyqtSignal(str,int,int)

    # Run function
    def run(self):
        self.cyclingTime_min=0
        self.cyclingTime_sec=0
        #start time
        self.startTime=time.time()
        while True:
            #Cycling date
            data = QDateTime.currentDateTime()
            self.currTime = data.toString("yyyy-MM-dd hh:mm:ss")
            #Cycling Time(second)
            self.cyclingTime=int(round(time.time()-self.startTime))
            #Convert cycling time to mins+sec
            if self.cyclingTime>60:
                self.cyclingTime_min=self.cyclingTime/60
                self.cyclingTime_sec=self.cyclingTime%60
            else:
                self.cyclingTime_min=0
                self.cyclingTime_sec=self.cyclingTime
            #Emit data for display function
            self.time.emit(self.currTime,self.cyclingTime_min,self.cyclingTime_sec)
            time.sleep(1)

class EncorderBackendThread(QThread):
    #Initialize Encoder
    global Encoder
    Encoder=encoder()
    # Create Signal Slot 
    encorderSpeed = pyqtSignal(int)

    # Run function
    def run(self):
        while True:
            #data = QDateTime.currentDateTime()
            #currTime = data.toString("yyyy-MM-dd hh:mm:ss")
            #Read Encoder Speedzz
            x=Encoder.spd
            #Send Encorder speed to slot
            self.encorderSpeed.emit(x)
            time.sleep(1)               #time sleep must be>1s

class DAQBackThread(QThread):
    global DAQ
    DAQ = daq()

    samp_rate = 1000 #for DAQ (Hz)
    samples = 100 #per acquisition
    HRrange = [60,140] #Range of HR
    HRxVal = 2.5 #Threshold for edge detection for PPG
    HRcaltime = 4 #seconds for refreshing HR values, more = more accurate

    HRcalarray = HRcaltime*samp_rate
    HRarrdaq = np.array(list())

    #determines while loop sampling rate
    t = time.time()
    period = 1/samp_rate*samples

    #create signal slots
    _EMGarray = pyqtSignal(np.ndarray) #EMG signal slot
    _PPGHeartRate = pyqtSignal(int) #PPG signal slot

    def run(self):
        while True:
            self.t+=self.period

            self.daqarr = DAQ.acqdaq(self.samp_rate,self.samples)
            self._EMGarray.emit(self.daqarr[:,1:]) #emit all the EMG signal array

            if len(self.HRarrdaq) != self.HRcalarray:
                self.HRarrdaq = np.append(self.HRarrdaq, self.daqarr[:,0])
            else:
                self.HRarrdiff = np.diff(self.HRarrdaq)
                self.HRperiod = (np.where(self.HRarrdiff>self.HRxVal)[0]+1)/self.samp_rate
                self.HRperioddiff = np.diff(self.HRperiod)
                self.HRper_in = self.HRperioddiff[np.all([self.HRperioddiff > (60/self.HRrange[1]), self.HRperioddiff < (60/self.HRrange[0])], axis=0)]

                self.HR = 0 if len(self.HRper_in) == 0 else int(60/np.mean(self.HRper_in))
                self._PPGHeartRate.emit(self.HR)
                self.HRarrdaq = np.array(list())

            time.sleep(max(0,self.t-time.time()))

class PedalThread(QThread):
    # Create Signal Slot 
    pedalInstantPower=pyqtSignal(object)
    pedalAccumPower=pyqtSignal(object)
    pedalInstantCandence=pyqtSignal(object)
    pedalBalance=pyqtSignal(object)
    pedalPowerBaseLine=pyqtSignal(object)
    #Initlilize Pedal
    global baseline_init
    baseline_init=main()
    
    #Run function
    def run(self):      
        while True:       
            #Read Pedal 
            pedalRead=DAQfunc(baseline_init[0],baseline_init[1])
            #print(type(pedalRead[0]))
            #Send pedal to slot
            self.pedalInstantPower.emit(pedalRead[0][0])
            self.pedalAccumPower.emit(pedalRead[0][1])
            self.pedalInstantCandence.emit(pedalRead[0][2])
            self.pedalBalance.emit(pedalRead[0][3])
            self.pedalPowerBaseLine.emit(pedalRead[1])

class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.title="Cognitive Project"
        self.iconName="icon.png"
        self.top=200
        self.left=400
        self.width=400
        self.height=600
        self.initWindow()
        self.previousBalance=50

    #UI Display Time    
    def TimeDisplay(self, data1,data2,data3):
        self.label0.setText("Date: " +str(data1) )
        self.label1.setText("Cycling time: " +str(data2)+ " mins  " + str(data3)+ "sec")
        #start cycling after 10 second calibration by pedal
        if (data3==20 and data2==0):
            self.label2.setText("You can Start cycling!" )
            

    # UI Display Encoder
    def EncoderDisplay(self, data):
        self.label3.setText("Speed: " +str(data) +" rpm")       

    # UI Display InstantPower
    def InstantPower(self, data):
        self.label4.setText("Instantaneous Power:    "+ str(data)+" W")

    # UI Display AccumPower
    def AccumPower(self, data):
        self.label5.setText("Accumlated Power:       "+ str(data)+" W")

    # UI Display InstantCandence
    def InstantCandence(self, data):
        self.label6.setText("Instantaneous Candence: "+ str(data)+" rpm")

    # UI Display Balance
    def Balance(self, data):
        if data>0:
            self.previousBalance=data
            self.label7.setText("Right Balance:          "+ str(data)+" %")
            self.label8.setText("Left Balance:          "+ str(100-data)+" %")
        else:
            self.label7.setText("Right Balance:          "+ str(self.previousBalance)+" %")
            self.label8.setText("Left Balance:          "+ str(100-self.previousBalance)+" %")

    # UI Display PowerBaseLine
    def PowerBaseLine(self, data):
        self.label9.setText("Power BaseLine:         "+ str(data)+" W")

    #Initialize Window
    def initWindow(self):
        #Set Window title,size,icon
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setGeometry(self.left,self.top,self.width,self.height)
        # Create label
        self.vbox = QVBoxLayout()
        self.label0 = QLabel("Date")
        self.label1 = QLabel("Cycling Time")
        ###for Label 2####
        self.label2 = QLabel("Taking Calibration")
        ###################
        self.label3 = QLabel(" ")
        self.label4 = QLabel(" ")
        self.label5 = QLabel(" ")
        self.label6 = QLabel(" ")
        self.label7 = QLabel(" ")
        self.label8 = QLabel(" ")
        self.label9 = QLabel(" ")
        #Add label into vbox.widget
        self.vbox.addWidget(self.label0)
        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self.label2)
        self.vbox.addWidget(self.label3)
        self.vbox.addWidget(self.label4)
        self.vbox.addWidget(self.label5)
        self.vbox.addWidget(self.label6)
        self.vbox.addWidget(self.label7)
        self.vbox.addWidget(self.label8)
        self.vbox.addWidget(self.label9)
        #Add vbox into layout
        self.setLayout(self.vbox)
        #Initialize Controller
        self.controller=self.Controller()        
        th_Controller=threading.Thread(target=self.controller.thread_Controller, args=(),daemon=True)
        th_Controller.start()
        #start signal slot connection
        self.initiSignalSlot() 

    #Initialize Signal Slot
    def initiSignalSlot(self):
        # Create backend Thread
        self.timebackend=CalTimeThread()
        self.backend = EncorderBackendThread()
        self.pedalBackend=PedalThread()
        # Signal connect to Slot
        self.timebackend.time.connect(self.TimeDisplay)                     #Pass time to UI label0-1 
        self.backend.encorderSpeed.connect(self.EncoderDisplay)             #Pass Speed to UI label2 
        self.backend.encorderSpeed.connect(self.controller.printSpeed)      #Pass Speed to controller slot
        self.pedalBackend.pedalInstantPower.connect(self.InstantPower)      #Pass InstantPower to UI label4
        self.pedalBackend.pedalAccumPower.connect(self.AccumPower)          #Pass AccumPower to UI label5
        self.pedalBackend.pedalInstantCandence.connect(self.InstantCandence)#Pass InstantCandence to UI label6
        self.pedalBackend.pedalBalance.connect(self.Balance)                #Pass Balance to UI label7 & 6
        self.pedalBackend.pedalPowerBaseLine.connect(self.PowerBaseLine)    #Pass PowerBaseLine to UI label9
        # Start thread (call run() in EncorderBackendThread())
        self.timebackend.start()
        self.backend.start()
        self.pedalBackend.start()


    #Create Controller Class
    class Controller():
        #intitiaz controller
        def __init__(self):
            self.speed=0
            
        #Controller Threading
        def thread_Controller(self):
            sample_first_joystick()
            
        #Controller Slot to recieve Encoder Speed
        def printSpeed(self,data):
            self.speed=data
            #print(data)
            keyboard = Controller()
            #while 1:
            #read speed
            #acceleration
            if self.speed>2:
                keyboard.press('z')            
                time.sleep(1)
                keyboard.release('z')                        
            #deceleration 
            elif self.speed<0:
                keyboard.press('a')
                time.sleep(1)
                keyboard.release('a') 

if __name__ == '__main__':
    #Initialize Window
    app =QApplication(sys.argv)
    MainWin = Window()
    MainWin.show()
    sys.exit(app.exec_())
