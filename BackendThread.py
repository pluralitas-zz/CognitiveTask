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
    samp = acq_rate*sam_period*samples #50*1*20 = 1000 samples
    degtravelled = []
    newdiff = 0
    speed = 0

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
        self.antdata = antrcv()
    
    #Run function
    def run(self):
        while True:       
            self.pedalRead=self.antdata.antacq()  #[[InstPower, AvgPower, InstCadence, pedalBalRight, eventCount][heartRate]]
            self._pedalValue.emit([self.pedalRead[0][0],self.pedalRead[0][1]*2,self.pedalRead[0][2],int(round(self.pedalRead[0][3]))]) 
            self._HeartRate.emit(self.pedalRead[1][0])
            self._ANTwrtout.emit([self.pedalRead[1][0],self.pedalRead[0][0],self.pedalRead[0][1]*2,self.pedalRead[0][2],int(round(self.pedalRead[0][3]))])#HeartRate,InstPower,AccumPower

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
        self.backend = EncDAQBackThread()
        self.pedalBackend=PedalThread()
        # Signal connect to Slot
        self.backend._encoderSpeed.connect(self.EncoderDisplay)             #Pass Speed to UI label2 
        self.backend._encoderSpeed.connect(self.controller.printSpeed)      #Pass Speed to controller slot
        self.pedalBackend.pedalInstantPower.connect(self.InstantPower)      #Pass InstantPower to UI label4
        self.pedalBackend.pedalAccumPower.connect(self.AccumPower)          #Pass AccumPower to UI label5
        self.pedalBackend.pedalInstantCandence.connect(self.InstantCandence)#Pass InstantCandence to UI label6
        self.pedalBackend.pedalBalance.connect(self.Balance)                #Pass Balance to UI label7 & 6
        self.pedalBackend.pedalPowerBaseLine.connect(self.PowerBaseLine)    #Pass PowerBaseLine to UI label9
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
                QtTest.QTest.qWait(1000)
                keyboard.release('z')                        
            #deceleration 
            elif self.speed<0:
                keyboard.press('a')
                QtTest.QTest.qWait(1000)
                keyboard.release('a') 

if __name__ == '__main__':
    pedThread = PedalThread()
    pedThread.start()
