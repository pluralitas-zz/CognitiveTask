import time, threading, numpy as np
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PyQt5 import QtCore, QtGui
from DAQAcq import daq
from EncoderNew import encoder
from xinput3_KeyboardControll_NES_Shooter_addGameTask import sample_first_joystick
from pynput.keyboard import Key, Controller
from Powermeter_Test2 import main, DAQfunc
            
class EncDAQBackThread(QtCore.QThread):
    DAQ = daq()
    #create signal slots
    _woutBackEndArray = QtCore.pyqtSignal(np.ndarray) #EMG signal slot
    _PPGHeartRate = QtCore.pyqtSignal(int) #PPG signal slot

    samp_rate = 1000 #for DAQ (Hz)
    samples = 100 #per acquisition
    samparr = np.ones((samples,1))
    HRrange = [60,140] #Range of HR
    HRxVal = 2.5 #Threshold for edge detection for PPG
    HRcaltime = 4 #seconds for refreshing HR values, more = more accurate
    HR = 0
    HRcalarray = HRcaltime*samp_rate
    HRarrdaq = np.array(list())

    #determines while loop sampling rate
    t = time.time()
    period = 1/samp_rate*samples

    #Initialize Encoder
    Encoder=encoder()
    # Create Signal Slot 
    encorderSpeed = QtCore.pyqtSignal(int)

    # Variables
    sam_rate = samp_rate/samples #sample rate of Encoder slaved to each acquisition of DAQ
    sam_period = 1 #period to collect signals sec
    samp = sam_rate*sam_period
    encperiod = sam_period/sam_rate
    degold = Encoder.deg
    degtravelled = []
    newdiff = 0
    speed = 0

    def run(self):
        while True:
            self.t+=self.period
        ############################# PPG
            self.daqarr = self.DAQ.acqdaq(self.samp_rate,self.samples)
            
            #PPG calculations (depends on HRaltime, else just append into HRarrdaq)
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
                self.encorderSpeed.emit(self.speed)
                self.degtravelled=[]

        ############################# combine Time, Degree, Speed, HR and EMG output to emit to writeout.py
            self.HRarr = self.samparr * self.HR
            self.speedarr = self.samparr * self.speed
            self.degnowarr = self.samparr * self.degnow
            
            self.comb = np.column_stack([self.degnowarr,self.speedarr,self.HRarr,self.daqarr[:,1:]]) #stack deg, speed, heartrate and EMG x 4
            self._woutBackEndArray.emit(self.comb) #emit all the EMG signal array
        
        #############################    
            time.sleep(max(0,self.t-time.time()))

class PedalThread(QtCore.QThread):
    # Create Signal Slot 
    _pedalValue = QtCore.pyqtSignal(list)
    
    #Initlilize Pedal
    baseline_init=main()
    
    #Run function
    def run(self):
        while True:       
            self.pedalRead=DAQfunc(self.baseline_init[0],self.baseline_init[1]) #Read Pedal
            '''
            self.pedalRead[0][0] = Instant Power
            self.pedalRead[0][1] = Accum. Power
            self.pedalRead[0][2] = Instance Cadence
            self.pedalRead[0][3] = Pedal Balance Right
            self.pedalRead[1] = Power Baseline    
            ''' #InstPower, AccumPower, InstCadence, pedalBalRight
            self._pedalValue.emit([self.pedalRead[0][0],self.pedalRead[0][1],self.pedalRead[0][2],self.pedalRead[0][3]]) 

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
        self.backend.encorderSpeed.connect(self.EncoderDisplay)             #Pass Speed to UI label2 
        self.backend.encorderSpeed.connect(self.controller.printSpeed)      #Pass Speed to controller slot
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
    import sys
    #Initialize Window
    app =QApplication(sys.argv)
    MainWin = Window()
    MainWin.show()
    sys.exit(app.exec_())
