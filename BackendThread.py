import time, threading, numpy as np
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PyQt5 import QtCore, QtGui
from DAQAcq import daq
from EncoderNew import encoder
from xinput3_KeyboardControll_NES_Shooter_addGameTask import sample_first_joystick
from pynput.keyboard import Key, Controller
#from Powermeter_Test2 import main, DAQfunc
from antreceiver import antrcv
            
class EncDAQBackThread(QtCore.QThread):
    DAQ = daq()
    # create signal slots
    _woutBackEndArray = QtCore.pyqtSignal(np.ndarray) #EMG signal slot
    _encoderSpeed = QtCore.pyqtSignal(int)

    # Variables for DAQ
    samp_rate = 1000 #for DAQ (Hz)
    samples = 10 #per acquisition
    samparr = np.ones((samples,1))

    # determines while loop sampling rate
    t = time.time()
    period = 1/samp_rate*samples #1/100 = 0.01s

    # Initialize Encoder
    Encoder=encoder()

    # Variables for encoder
    sam_rate = samp_rate/samples #sample rate of Encoder slaved to each acquisition of DAQ #100hz
    sam_period = 1 #period to collect signals sec 
    samp = sam_rate*sam_period #100*1 = 100 samples
    degold = Encoder.deg
    degtravelled = []
    newdiff = 0
    speed = 0
    degnowarr = []
    def run(self):
        while True:
            self.t += self.period
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

            ############################# combine Time, Degree, Speed, HR and EMG output to emit to writeout.py
            # pad signal to equal sample size of EMG for DAQ
            self.speedarr = self.samparr * self.speed
            self.degnowarr = self.samparr * self.degnow
            
            #self.degnowarrout = np.array(self.degnowarr)
            self.comb = np.column_stack([self.degnowarr*100,self.speedarr,self.daqarr*1000]) #stack deg, speed and EMG x 4, PPGRaw
            self._woutBackEndArray.emit(self.comb.astype(int)) #emit all the EMG signal array

            ############################# Reset
            self.degarrout = np.array(list())
        
            time.sleep(max(0,self.t-time.time()))
            
class PedalThread(QtCore.QThread):
    # Create Signal Slot 
    _pedalValue = QtCore.pyqtSignal(list)
    _HeartRate = QtCore.pyqtSignal(int)

    #Initialise Pedal
    antdata = antrcv()
    # determines while loop sampling rate
    t = time.time()
    period = 0.5   
    
    #Run function
    def run(self):
        while True:       
            self.t+=self.period
            self.pedalRead=self.antdata.antacq()  #[[InstPower, AvgPower, InstCadence, pedalBalRight, evenCount][heartRate]]
            self._pedalValue.emit([self.pedalRead[0][0],self.pedalRead[0][1],self.pedalRead[0][2],int(round(self.pedalRead[0][3]))]) 
            self._HeartRate.emit(self.pedalRead[1][0])
            time.sleep(max(0,self.t-time.time()))

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
                time.sleep(1)
                keyboard.release('z')                        
            #deceleration 
            elif self.speed<0:
                keyboard.press('a')
                time.sleep(1)
                keyboard.release('a') 

if __name__ == '__main__':
    pedThread = PedalThread()
    pedThread.start()
