# Created by: PyQt5 UI code generator 5.6, Form implementation generated from reading ui file 'task.ui'
# Run on Anaconda3-4.3.0-Windows-x86_64, Python Version 3.6.10
import sys, os, time, threading, numpy as np, random
import VideoPlayer, cdown, task_flank, task_workmem, task_nback, task_divAttn, trngComplete #custom .py
from xinput3_KeyboardControll_NES_Shooter_addGameTask import sample_first_joystick
from PyQt5 import Qt, QtCore, QtGui, QtWidgets, QtTest
from pynput.keyboard import Key, Controller
from BackendThread import EncDAQBackThread, PedalThread #Encoder=COM5, DAQ=Dev1
from writeout import wrtout, wrttask
# from psychopy import parallel #for usage with Parallel Port DB25 LPT communication with EEG machine

_translate = QtCore.QCoreApplication.translate
class Ui_root(QtWidgets.QMainWindow):
    _answer = QtCore.pyqtSignal(str) #QtSlot for answering questions in task subpy
    _speed = QtCore.pyqtSignal(int,int) #QtSlot for speed

# Define your USER ID/NAME HERE
    UserIDNAME = "Test"

# Define TRAINING TIME HERE 
    traintime = QtCore.QTime(0,0,0) #(hours, minutes, seconds)
    traintimemax = QtCore.QTime(0,25,0) #1,15,0)
    trainsec = QtCore.QTime(0,0,0).secsTo(traintimemax)

# Define ALL YOUR TASKS FUNCTION HERE
    def tasks(self,numb):
        if numb is 0:
            self.flnk.run_task(self.counter)
        elif numb is 1:
            self.wrkVerb.run_task(self.counter)
        elif numb is 2:
            self.wrkSpace.run_task(self.counter)
        elif numb is 3:
            self.nbckVerb.run_task(self.counter)
        elif numb is 4:
            self.nbckSpace.run_task(self.counter)
        else:
            pass

# Define your task events here
    def task_run(self):
        ################################################### 
        ###############     RUN TASKS     #################
        self.tasksnum = random.sample(range(0, 4), 4) # randomise tasks
        self.firsttaskone = True
        self.firsttasktwo = True
        self.firsttaskthree = True
        self.firsttaskfour = True

        while self.timecount < self.trainsec:
            QtTest.QTest.qWait(1000)
            
            if 420 >= self.timecount > 120: #1200 300 in seconds
                if self.firsttaskone is True:
                    self.counter = 0
                    self.CntDisplay()
                    self.firsttaskone = False
                    self.cd.run_cd(5) #5 seconds count down
                self.wouttask("Do Task " + str(self.tasksnum[0]))
                self.tasks(self.tasksnum[0])

            elif 840 >= self.timecount > 540: #2400 1500
                if self.firsttasktwo is True:
                    self.counter = 0
                    self.CntDisplay()
                    self.firsttasktwo = False
                    self.cd.run_cd(5) #5 seconds count down
                self.wouttask("Do Task " + str(self.tasksnum[1]))
                self.tasks(self.tasksnum[1])

            elif 1260 >= self.timecount > 960: #3600 2700
                if self.firsttaskthree is True:
                    self.counter = 0
                    self.CntDisplay()
                    self.firsttaskthree = False
                    self.cd.run_cd(5) #5 seconds count down
                self.wouttask("Do Task " + str(self.tasksnum[2]))
                self.tasks(self.tasksnum[2])

            elif 1680 >= self.timecount > 1380: #3600 2700
                if self.firsttaskfour is True:
                    self.counter = 0
                    self.CntDisplay()
                    self.firsttaskfour = False
                    self.cd.run_cd(5) #5 seconds count down
                self.wouttask("Do Task " + str(self.tasksnum[3]))
                self.tasks(self.tasksnum[3])

            else:
                QtTest.QTest.qWait(1000)

        self.complet.run_com(1)
        ###################################################

    class Controller(): #Create Controller Class
        
        def __init__(self): #intialise controller
            self.speed=0 #speed value

        #Controller Threading
        def thread_Controller(self):
            sample_first_joystick()

    def __init__(self):
        #values    
        super(Ui_root,self).__init__()
        self.paraportstat = False
        self.counter = 0 #counter value to change task difficulty
        self.disparr = [] #array to store values for displaying on buttons
        self.previousBalance=50 #default Force Balance Value
        self.pausespd = 10 #Pause/Play Threshold Speed
        self.ansdict={}
        self.timecount = 0
        self.pictures = "Pictures" #location of pictures in folder "Pictures"
        #self.picd = os.path.join(os.getcwd(),self.pictures)
        self.picd = os.path.join(os.path.dirname(__file__),self.pictures)

        self.setupUi(self)
        self.StartBtn.clicked.connect(lambda:self.StartBtnPress())
        self.GameBtn.clicked.connect(lambda:self.NoHWButton())
        #self.GameBtn.clicked.connect(lambda:self.Gamebutton()) #Change 2nd Start button to Game Mode

        self.initTaskSigSlot() #Connect signal slots used for Tasks

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.TimeDisplay) #connect QtTimer for Elapsed Time
        #self.vidFrame.startVid() #Start Video

        
        # try: #try to connect to parallel port
        #     self.paraport = parallel.ParallelPort(address=0x0E100) #LPT port PCI Express address for EEG PC in ERB 1104
        #     self.paraportstat = True
        # except:
        #     pass

# Task Stuff
    def initTaskSigSlot(self): #Initialise Task Stuff
        
        #connect countdown
        self.cd = cdown.countdown_main()
        self.cd._qnsdisp.connect(self.disp_qns)

        #connect training complete screen
        self.complet = trngComplete.trngCom_main()
        self.complet._qnsdisp.connect(self.disp_qns)

        #connect divided attention task
        self.divattn = task_divAttn.divattn_main()
        self.divattn._qnsdisp.connect(self.disp_qns)
        self.divattn._ansdisp.connect(self.disp_ans)
        self.divattn._counter.connect(self.counter_add)
        self.divattn._qnsshowhide.connect(self.showhideAnswers)
        # try:
        #     self.divattn._paraport(self.paraport_send)
        # except:pass
        self._answer.connect(self.divattn.append_ans)
        self._speed.connect(self.divattn.current_speed)

        #connect flank task
        self.flnk = task_flank.flank_main()
        self.flnk._qnsdisp.connect(self.disp_qns)
        self.flnk._ansdisp.connect(self.disp_ans)
        self.flnk._counter.connect(self.counter_add)
        self.flnk._level.connect(self.LevelDisplay)
        self.flnk._qnsshowhide.connect(self.showhideAnswers)
        # try:
        #     self.flnk._paraport(self.paraport_send)
        # except:pass
        self._answer.connect(self.flnk.append_ans)
        self._speed.connect(self.flnk.current_speed)

        #connect working memory Verbal task
        self.wrkVerb = task_workmem.workmemVerb_main()
        self.wrkVerb._qnsdisp.connect(self.disp_qns)
        self.wrkVerb._ansdisp.connect(self.disp_ans)
        self.wrkVerb._counter.connect(self.counter_add)
        self.wrkVerb._level.connect(self.LevelDisplay)
        self.wrkVerb._qnsshowhide.connect(self.showhideAnswers)
        # try:
        #     self.wrkVerb._paraport(self.paraport_send)
        # except:pass
        self._answer.connect(self.wrkVerb.append_ans)
        self._speed.connect(self.wrkVerb.current_speed)

        #connect n-back verbal task
        self.nbckVerb = task_nback.nbackVerb_main()
        self.nbckVerb._qnsdisp.connect(self.disp_qns)
        self.nbckVerb._ansdisp.connect(self.disp_ans)
        self.nbckVerb._counter.connect(self.counter_add)
        self.nbckVerb._level.connect(self.LevelDisplay)
        self.nbckVerb._qnsshowhide.connect(self.showhideAnswers)
        # try:
        #     self.nbckVerb._paraport(self.paraport_send)
        # except:pass
        self._answer.connect(self.nbckVerb.append_ans)
        self._speed.connect(self.nbckVerb.current_speed)

        #connect nback task
        self.nbckSpace = task_nback.nbackSpace_main()
        self.nbckSpace._qnsdisp.connect(self.disp_qns)
        self.nbckSpace._ansdisp.connect(self.disp_ans)
        self.nbckSpace._counter.connect(self.counter_add)
        self.nbckSpace._level.connect(self.LevelDisplay)
        self.nbckSpace._qnsshowhide.connect(self.showhideAnswers)
        # try:
        #     self.nbckSpace._paraport(self.paraport_send)
        # except:pass
        self._answer.connect(self.nbckSpace.append_ans)
        self._speed.connect(self.nbckSpace.current_speed)

        #connect working memory Spatial task
        self.wrkSpace = task_workmem.workmemSpace_main()
        self.wrkSpace._qnsdisp.connect(self.disp_qns)
        self.wrkSpace._ansdisp.connect(self.disp_ans)
        self.wrkSpace._counter.connect(self.counter_add)
        self.wrkSpace._level.connect(self.LevelDisplay)
        self.wrkSpace._qnsshowhide.connect(self.showhideAnswers)
        # try:
        #     self.wrkSpace._paraport(self.paraport_send)
        # except:pass
        self._answer.connect(self.wrkSpace.append_ans)
        self._speed.connect(self.wrkSpace.current_speed)

        #create shortcut for buttons
        self.QuesBtn_A.setShortcut("c")
        self.QuesBtn_B.setShortcut("v")
        self.QuesBtn_X.setShortcut("d")
        self.QuesBtn_Y.setShortcut("f")
        self.QuesBtn_Up.setShortcut(QtCore.Qt.Key_Up)
        self.QuesBtn_Down.setShortcut(QtCore.Qt.Key_Down)
        self.QuesBtn_Left.setShortcut(QtCore.Qt.Key_Left)
        self.QuesBtn_Right.setShortcut(QtCore.Qt.Key_Right)
        self.QuesBtn_ShldL.setShortcut("e")
        self.QuesBtn_ShldR.setShortcut("r")

        #connect the buttons to answering definition
        self.QuesBtn_A.clicked.connect(lambda:self.answer())
        self.QuesBtn_B.clicked.connect(lambda:self.answer())
        self.QuesBtn_X.clicked.connect(lambda:self.answer())
        self.QuesBtn_Y.clicked.connect(lambda:self.answer())
        self.QuesBtn_Up.clicked.connect(lambda:self.answer())
        self.QuesBtn_Down.clicked.connect(lambda:self.answer())
        self.QuesBtn_Left.clicked.connect(lambda:self.answer())
        self.QuesBtn_Right.clicked.connect(lambda:self.answer())
        self.QuesBtn_ShldL.clicked.connect(lambda:self.answer())
        self.QuesBtn_ShldR.clicked.connect(lambda:self.answer())

    def showhideAnswers(self,value): #Show/Hide UI buttons for displaying answers
        if value == 0:
            self.QuesBtn_Left.hide()
            self.QuesBtn_Down.hide()
            self.QuesBtn_Up.hide()
            self.QuesBtn_Right.hide()

            self.QuesBtn_X.hide()
            self.QuesBtn_Y.hide()
            self.QuesBtn_B.hide()
            self.QuesBtn_A.hide()

            self.QuesBtn_ShldL.hide()
            self.QuesBtn_ShldR.hide()
        elif value == 1:
            self.QuesBtn_Left.show()
            self.QuesBtn_Down.show()
            self.QuesBtn_Up.show()
            self.QuesBtn_Right.show()

            self.QuesBtn_X.show()
            self.QuesBtn_Y.show()
            self.QuesBtn_B.show()
            self.QuesBtn_A.show()

            self.QuesBtn_ShldL.show()
            self.QuesBtn_ShldR.show()
        else:
            pass

    def counter_add(self,boo): #Add/minus to counter
        if boo == 1:
            self.counter += 1
            self.wouttask("Answered Correct")
        else:
            #if self.counter > 0:
            self.counter -=1
            self.wouttask("Answered Wrong")
        self.CntDisplay()

        if self.counter in (3, 5, 7): #change videos if counter reached X value(s)
            #self.vidFrame.restartVid()
            pass
    
    # def paraport_send(self,data): #EEG send value over LPT PCI Express Parallel port
    #     if self.paraportstat == True:
    #         self.paraport.setData(0)
    #         self.paraport.setData(data)            
    #     else:
    #         pass

    def disp_qns(self,data,wid,hei): #Display list of Questions in TaskFrame
        pixmap = QtGui.QPixmap(os.path.join(os.path.join(os.path.dirname(__file__),"Pictures"), data))
        #pixmap = pixmap.scaled(self.TaskFrame.width(),self.TaskFrame.height(),QtCore.Qt.KeepAspectRatio)
        pixmap = pixmap.scaled(wid,hei,QtCore.Qt.KeepAspectRatio)

        if data == "Blank.png" or data =="Center.png":
            pass
        else:
            self.wouttask("Question Shown")

        self.TaskFrame.setPixmap(pixmap)

    def disp_ans(self,data): #Display Answers in relevant buttons
        
        if len(data) == 2: #if value is 2, allow all left 4(arrows) and right 4(ABXY) buttons to do the same thing
            [data.insert(1,data[0]) for i in range(3)]
            [data.insert(5,data[4]) for i in range(3)]
            [data.append('Blank.png') for i in range(10 - len(data))] #append to 10 data with 'Blank.png'

            self.ansdict = {'A':data[0],'B':data[1],'X':data[2],'Y':data[3],'U':data[4],'D':data[5],'L':data[6],'R':data[7],'L1':data[8],'R1':data[9]} #dictionary to compare button to picture displayed
            for i in range(3):
                data[i+1] = 'Blank.png'
                data[i+5] = 'Blank.png'

        elif len(data) != 2 and len(data) < 10: #append to fit the list of buttons if list of values are not enough
            [data.append('Blank.png') for i in range(10 - len(data))] #append to 10 data with 'Blank.png'
            self.ansdict = {'A':data[0],'B':data[1],'X':data[2],'Y':data[3],'U':data[4],'D':data[5],'L':data[6],'R':data[7],'L1':data[8],'R1':data[9]} #dictionary to compare button to picture displayed

        elif len(data) > 10:
            data = random.sample(data,10)
            self.ansdict = {'A':data[0],'B':data[1],'X':data[2],'Y':data[3],'U':data[4],'D':data[5],'L':data[6],'R':data[7],'L1':data[8],'R1':data[9]} #dictionary to compare button to picture displayed

        else:
            self.ansdict = {'A':data[0],'B':data[1],'X':data[2],'Y':data[3],'U':data[4],'D':data[5],'L':data[6],'R':data[7],'L1':data[8],'R1':data[9]} #dictionary to compare button to picture displayed

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[0])))
        self.QuesBtn_A.setIcon(icon)
        self.QuesBtn_A.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[1])))
        self.QuesBtn_B.setIcon(icon)
        self.QuesBtn_B.setIconSize(QtCore.QSize(200,200))
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[2])))
        self.QuesBtn_X.setIcon(icon)
        self.QuesBtn_X.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[3])))
        self.QuesBtn_Y.setIcon(icon)
        self.QuesBtn_Y.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[4])))
        self.QuesBtn_Up.setIcon(icon)
        self.QuesBtn_Up.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[5])))
        self.QuesBtn_Down.setIcon(icon)
        self.QuesBtn_Down.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[6])))
        self.QuesBtn_Left.setIcon(icon)
        self.QuesBtn_Left.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[7])))
        self.QuesBtn_Right.setIcon(icon)
        self.QuesBtn_Right.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[8])))
        self.QuesBtn_ShldL.setIcon(icon)
        self.QuesBtn_ShldL.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[9])))
        self.QuesBtn_ShldR.setIcon(icon)
        self.QuesBtn_ShldR.setIconSize(QtCore.QSize(200,200))

    def answer(self): #emit answer to task subpy
        sender = self.sender()
        ans = self.ansdict[sender.text()] #check dict in disp_ans for correct value
        self.wouttask("User Answered")
        self._answer.emit(ans)

    def LevelDisplay(self, data):
        self.TaskValLevel.setText("<font color='White'>"+ str(data) +"</font>")

    def CntDisplay(self):
        self.TaskValCnt.setText("<font color='White'>"+ str(self.counter) +"</font>")

# Write out to file Stuff
    def writeout(self,data): #time, elapsed time, deg, speed, heartrate, EMG x 4, InstPower, AccumPower, InstCadence, pedalBalRight
        self.comb = np.column_stack([np.ones((self.daqbackend.samples,1))*time.time(),np.ones((self.daqbackend.samples,1))*self.timecount,data,self.pedalwoutarr])
        self.writefile.appendfile(self.comb) #write data to file
    
    def wouttask(self,data):
        self.timenow = str(np.datetime64('now')).replace(":","")
        self.taskcomb = np.column_stack([self.timenow, str(data)]) #time, data value
        self.writetask.appendfile(self.taskcomb) #write task data to file

# Video Playing Stuff
    def pauseVid(self): #Pause video + Show warning "speed too low"
        self.vidFrame.pauseVid()
        self.WarnFrame.show()

    def playVid(self): #Play video + Hide warning "speed too low"
        self.vidFrame.startVid()
        self.WarnFrame.hide()

    def videoStartPause(self,data): #Play/Pause video if Speed more or less than
        if data < self.pausespd: #Pause video if speed <pausespd
            self.pauseVid()
        else: #start video if speed >=pausespd
            self.playVid()

# Start Task Button Stuff & Game Start Button
    def StartBtnPress(self): #Start Video/Task Mode
        self.StartBtn.hide()
        self.GameBtn.hide()
        self.vidFrame.startVid() #Start video 

        #start Backend signal slot connection
        self.initBackendThread()
 
        # Start thread(s)
        self.pedalBackend.start()
        self.daqbackend.start()
        self.timer.start(1000)

        self.task_run()

    def NoHWButton(self): #Start No Hardware Task mode
        self.StartBtn.hide()
        self.GameBtn.hide()
        self.vidFrame.startVid() #Start video

        #Hide HUD Frame
        self.HUDValAccPwr.hide()
        #self.HUDValHR.hide()
        self.HUDValInstCad.hide()
        self.HUDValInstPwr.hide()
        self.HUDValPBalL.hide()
        self.HUDValPBalR.hide()
        self.HUDValSpd.hide()
        
        self.HUDLabAccPwr.hide()
        #self.HUDLabHR.hide()
        self.HUDLabInstCad.hide()
        self.HUDLabInstPwr.hide()
        self.HUDLabPedBal.hide()
        self.HUDLabPedBalSpr.hide()
        self.HUDLabSpd.hide()

        #start Backend signal slot connection
        self.initBackendThread()
        
        # Start thread(s)
        self.timer.start(1000)

        self.task_run()

    def Gamebutton(self): #Start Game mode
        self.StartBtn.hide()
        self.GameBtn.hide()

        #Hide tasks stuff
        self.TaskFrame.hide()
        self.TaskLabCnt.hide()
        self.TaskValCnt.hide()
        self.TaskLabLevel.hide()
        self.TaskValLevel.hide()
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint) #make window transparent

        #start Backend signal slot connection
        self.initBackendThread()
        self.daqbackend.encorderSpeed.connect(self.Controller_Game) #Pass Speed to controller slot for pressing buttons with Encoder

        # Start thread(s)
        self.pedalBackend.start()
        self.daqbackend.start()
        self.timer.start(1000)

# HUD Stuff
    def TimeDisplay(self):
        self.timecount += 1
        self.timeleft = self.traintime.addSecs(self.timecount)
        self.timedisp = self.timeleft.toString()  
        self.HUDValTime.setText("<font color='White'>"+ self.timedisp[3:] +"</font>")

    def HRDisplay(self,data):
        self.heartrate = str(data)
        self.HUDValHR.setText("<font color='White'>"+ self.heartrate +"</font>")

    def EncoderDisplay(self, data): # UI Slot to recieve Encoder
        self.speed=str(data)
        self._speed.emit(data,self.pausespd)
        self.HUDValSpd.setText("<font color='White'>"+ self.speed+"</font>")
        #self.HUDValSpd.setText(_translate("root", ("<font color='White'>"+str(data)+"</font>")))

    def PedalDisplay(self,data): #InstPower, AccumPower, InstCadence, pedalBalRight
        self.pedalwoutarr[0] = data #append into array for writeout
        self.HUDValInstPwr.setText(_translate("root","<font color='White'>" + str(data[0]) + "</font>"))
        self.HUDValAccPwr.setText(_translate("root","<font color='White'>" + str(data[1]) + "</font>"))
        self.HUDValInstCad.setText(_translate("root","<font color='White'>"+ str(data[2]) + "</font>"))

        if data[3] > 0:
            self.HUDValPBalR.setText(_translate("root","<font color='White'>"+ str(int(round(data[3])))+"</font>"))
            self.HUDValPBalL.setText(_translate("root","<font color='White'>"+ str(int(round(100-data[3])))+"</font>"))

# Game Stuff
    def Controller_Game(self,data): #Controller Slot to recieve Encoder Speed and translate to button inputs
        self.speed=data
        keyboard = Controller()
        
        if self.speed>30: #acceleration, pressed
            keyboard.press('z')            
            QtTest.QTest.qWait(1000)                  
        elif 30>=self.speed>10: #acceleration, tapping
            keyboard.press('z')
            QtTest.QTest.qWait(1000)
            keyboard.release('z')
        elif 10>=self.speed>=0: #deceleration, not pressed
            keyboard.release('z')
            QtTest.QTest.qWait(1000)
        elif self.speed<0:
            keyboard.press('a')
            QtTest.QTest.qWait(1000)
            keyboard.release('a') 
    
# Initialize Signal Slots for Backend Threads
    def initBackendThread(self): 
        # Create backend Threads
        self.pedalBackend=PedalThread()
        self.daqbackend= EncDAQBackThread()
        self.pedalwoutarr = np.zeros((self.daqbackend.samples,4)) #blank array for use with writeout

        #Initialize Controller
        self.controller=self.Controller()        
        self.th_Controller=threading.Thread(target=self.controller.thread_Controller, args=(),daemon=True)
        self.th_Controller.start()

        #Initialise and create Writeout file with username
        self.writefile=wrtout(self.UserIDNAME)
        self.writetask=wrttask(self.UserIDNAME)

        # Signal connect to Slots for Data
        self.daqbackend.encorderSpeed.connect(self.EncoderDisplay)  #Pass Speed to UI label2 
        self.daqbackend.encorderSpeed.connect(self.videoStartPause) #Encoder Speed control Start/Pause video
        self.daqbackend._PPGHeartRate.connect(self.HRDisplay)       #Pass Heart Rate to UI label 3
        self.daqbackend._woutBackEndArray.connect(self.writeout)    #Writeout
        self.pedalBackend._pedalValue.connect(self.PedalDisplay)    #Pass all pedal values

# Setup UI Stuff
    def setupUi(self, root):
        root.setObjectName("MainWindow")
        root.resize(1600, 900)
        root.setMinimumSize(QtCore.QSize(1600, 900))
        root.setMaximumSize(QtCore.QSize(1600, 900))
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)  #make window transparent/stay always on top, for Games only
        root.setAttribute(QtCore.Qt.WA_TranslucentBackground,on=True)

        root.closeEvent = self.closeEvent

        # Define Video Task as centralwidget
        self.vidFrame = VideoPlayer.MainWid(self)
        self.setCentralWidget(self.vidFrame)
        #self.vidFrame.hide() #hide video frame
        #self.centralwidget.setObjectName("centralwidget")

        # Define Start Button
        self.StartBtn = QtWidgets.QPushButton(self)
        self.StartBtn.setGeometry(QtCore.QRect(1250, 800, 100, 40))
        self.StartBtn.setFlat(False)
        self.StartBtn.setObjectName("StartBtn")

        # Define Game Button
        self.GameBtn = QtWidgets.QPushButton(self)
        self.GameBtn.setGeometry(QtCore.QRect(1250, 850, 100, 40))
        self.GameBtn.setFlat(False)
        self.GameBtn.setObjectName("GameBtn")

        #Define Warning Frame
        self.WarnFrame = QtWidgets.QLabel(self)
        self.WarnFrame.setGeometry(QtCore.QRect(300,100,800,100))
        self.WarnFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.WarnFrame.setMaximumSize(QtCore.QSize(1000, 800))    
        self.WarnFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.WarnFrame.setText("")
        self.WarnFrame.setAlignment(QtCore.Qt.AlignCenter)
        self.WarnFrame.setObjectName("TaskFrame")
        pixmap = QtGui.QPixmap(os.path.join(self.picd, "Pause.png"))
        self.WarnFrame.setPixmap(pixmap)
        self.WarnFrame.hide()

        #Define Task Frame
        self.TaskFrame = QtWidgets.QLabel(self)
        self.TaskFrame.setGeometry(QtCore.QRect(200, 40, 1000, 800))
        self.TaskFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.TaskFrame.setMaximumSize(QtCore.QSize(1000, 800))
        self.TaskFrame.setAutoFillBackground(False)
        self.TaskFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.TaskFrame.setText("")
        self.TaskFrame.setAlignment(QtCore.Qt.AlignCenter)
        self.TaskFrame.setObjectName("TaskFrame")

        font = QtGui.QFont("Gill Sans MT", pointSize = 36, weight = 50)

        self.TaskValLevel = QtWidgets.QLabel(self)
        self.TaskValLevel.setGeometry(QtCore.QRect(10, 50, 80, 50))
        self.TaskValLevel.setFont(font)
        self.TaskValLevel.setAlignment(QtCore.Qt.AlignCenter)
        self.TaskValLevel.setObjectName("TaskValLevel")

        self.TaskValCnt = QtWidgets.QLabel(self)
        self.TaskValCnt.setGeometry(QtCore.QRect(10, 140, 80, 50))
        self.TaskValCnt.setFont(font)
        self.TaskValCnt.setAlignment(QtCore.Qt.AlignCenter)
        self.TaskValCnt.setObjectName("TaskValCnt")

        # Define HUD Frame
        self.HUDFrame = QtWidgets.QWidget(self)
        self.HUDFrame.setGeometry(QtCore.QRect(1400, 0, 200, 900))
        self.HUDFrame.setMaximumSize(QtCore.QSize(1600, 900))
        #self.HUDFrame.setAutoFillBackground(False)
        self.HUDFrame.setObjectName("HUDFrame")
        self.HUDFrame.setStyleSheet("background-color: rgba(0,0,0,15%)")

        # Define Value Display
        font = QtGui.QFont("Gill Sans MT", pointSize = 48, weight = 50)

        self.HUDValTime = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValTime.setGeometry(QtCore.QRect(0, 45, 200, 85))
        self.HUDValTime.setFont(font)
        self.HUDValTime.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValTime.setObjectName("HUDValTime")

        self.HUDValHR = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValHR.setGeometry(QtCore.QRect(0, 155, 200, 85))
        self.HUDValHR.setFont(font)
        self.HUDValHR.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValHR.setObjectName("HUDValHR")

        self.HUDValSpd = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValSpd.setGeometry(QtCore.QRect(0, 265, 200, 85))
        self.HUDValSpd.setFont(font)
        self.HUDValSpd.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValSpd.setObjectName("HUDValSpd")

        self.HUDValInstCad = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValInstCad.setGeometry(QtCore.QRect(0, 375, 200, 85))
        self.HUDValInstCad.setFont(font)
        self.HUDValInstCad.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValInstCad.setObjectName("HUDValInstCad")

        self.HUDValAccPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValAccPwr.setGeometry(QtCore.QRect(0, 485, 200, 85))
        self.HUDValAccPwr.setFont(font)
        self.HUDValAccPwr.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValAccPwr.setObjectName("HUDValAccPwr")

        self.HUDValInstPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValInstPwr.setGeometry(QtCore.QRect(0, 595, 200, 85))
        self.HUDValInstPwr.setFont(font)
        self.HUDValInstPwr.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValInstPwr.setObjectName("HUDValInstPwr")

        self.HUDValPBalR = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValPBalR.setGeometry(QtCore.QRect(100, 705, 100, 85))
        self.HUDValPBalR.setFont(font)
        self.HUDValPBalR.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValPBalR.setObjectName("HUDValPBalR")

        self.HUDValPBalL = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValPBalL.setGeometry(QtCore.QRect(0, 705, 100, 85))
        self.HUDValPBalL.setFont(font)
        self.HUDValPBalL.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValPBalL.setObjectName("HUDValPBalL")

        # Define Labels
        font = QtGui.QFont("Gill Sans MT", pointSize = 14)

        self.TaskLabLevel = QtWidgets.QLabel(self)
        self.TaskLabLevel.setGeometry(QtCore.QRect(10, 20, 80, 25))
        self.TaskLabLevel.setFont(font)
        self.TaskLabLevel.setScaledContents(False)
        self.TaskLabLevel.setObjectName("TaskLabLevel")

        self.TaskLabCnt = QtWidgets.QLabel(self)
        self.TaskLabCnt.setGeometry(QtCore.QRect(10, 110, 80, 25))
        self.TaskLabCnt.setFont(font)
        self.TaskLabCnt.setScaledContents(False)
        self.TaskLabCnt.setObjectName("TaskLabCnt")

        self.HUDLabPedBal = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabPedBal.setGeometry(QtCore.QRect(10, 680, 200, 25))
        self.HUDLabPedBal.setFont(font)
        self.HUDLabPedBal.setScaledContents(False)
        self.HUDLabPedBal.setObjectName("HUDLabPedBal")

        self.HUDLabInstPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabInstPwr.setGeometry(QtCore.QRect(10, 570, 200, 25))
        self.HUDLabInstPwr.setFont(font)
        self.HUDLabInstPwr.setScaledContents(False)
        self.HUDLabInstPwr.setObjectName("HUDLabInstPwr")

        self.HUDLabInstCad = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabInstCad.setGeometry(QtCore.QRect(10, 350, 200, 25))
        self.HUDLabInstCad.setFont(font)
        self.HUDLabInstCad.setScaledContents(False)
        self.HUDLabInstCad.setObjectName("HUDLabInstCad")

        self.HUDLabTime = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabTime.setGeometry(QtCore.QRect(10, 20, 200, 25))
        self.HUDLabTime.setFont(font)
        self.HUDLabTime.setScaledContents(False)
        self.HUDLabTime.setObjectName("HUDLabTime")

        self.HUDLabHR = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabHR.setGeometry(QtCore.QRect(10, 130, 200, 25))
        self.HUDLabHR.setFont(font)
        self.HUDLabHR.setScaledContents(False)
        self.HUDLabHR.setObjectName("HUDLabHR")

        self.HUDLabSpd = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabSpd.setGeometry(QtCore.QRect(10, 240, 200, 25))
        self.HUDLabSpd.setFont(font)
        self.HUDLabSpd.setScaledContents(False)
        self.HUDLabSpd.setObjectName("HUDLabSpd")

        self.HUDLabAccPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabAccPwr.setGeometry(QtCore.QRect(10, 460, 200, 25))
        self.HUDLabAccPwr.setFont(font)
        self.HUDLabAccPwr.setScaledContents(False)
        self.HUDLabAccPwr.setObjectName("HUDLabAccPwr")

        # Define Force Balance Separator VLine
        self.HUDLabPedBalSpr = QtWidgets.QFrame(self.HUDFrame)
        self.HUDLabPedBalSpr.setGeometry(QtCore.QRect(100, 710, 3, 80))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HUDLabPedBalSpr.sizePolicy().hasHeightForWidth())
        self.HUDLabPedBalSpr.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.HUDLabPedBalSpr.setFont(font)
        self.HUDLabPedBalSpr.setFrameShape(QtWidgets.QFrame.VLine)
        self.HUDLabPedBalSpr.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.HUDLabPedBalSpr.setObjectName("HUDLabPedBalSpr")

        #Define Question Buttons
        QBtnfont = QtGui.QFont("Gill Sans MT", pointSize = 1)
        self.QuesBtn_Left = QtWidgets.QPushButton(self)
        self.QuesBtn_Left.setGeometry(QtCore.QRect(40, 440, 200, 200))
        self.QuesBtn_Left.setFont(QBtnfont)
        self.QuesBtn_Left.setFlat(True)
        self.QuesBtn_Left.setObjectName("QuesBtn_Left")
        self.QuesBtn_Left.hide()

        self.QuesBtn_Down = QtWidgets.QPushButton(self)
        self.QuesBtn_Down.setGeometry(QtCore.QRect(240, 640, 200, 200))
        self.QuesBtn_Down.setFont(QBtnfont)
        self.QuesBtn_Down.setFlat(True)
        self.QuesBtn_Down.setObjectName("QuesBtn_Down")
        self.QuesBtn_Down.hide()

        self.QuesBtn_Up = QtWidgets.QPushButton(self)
        self.QuesBtn_Up.setGeometry(QtCore.QRect(240, 240, 200, 200))
        self.QuesBtn_Up.setFont(QBtnfont)
        self.QuesBtn_Up.setFlat(True)
        self.QuesBtn_Up.setObjectName("QuesBtn_Up")
        self.QuesBtn_Up.hide()

        self.QuesBtn_Right = QtWidgets.QPushButton(self)
        self.QuesBtn_Right.setGeometry(QtCore.QRect(440, 440, 200, 200))
        self.QuesBtn_Right.setFont(QBtnfont)
        self.QuesBtn_Right.setFlat(True)
        self.QuesBtn_Right.setObjectName("QuesBtn_Right")
        self.QuesBtn_Right.hide()

        self.QuesBtn_X = QtWidgets.QPushButton(self)
        self.QuesBtn_X.setGeometry(QtCore.QRect(760, 440, 200, 200))
        self.QuesBtn_X.setFont(QBtnfont)
        self.QuesBtn_X.setFlat(True)
        self.QuesBtn_X.setObjectName("QuesBtn_X")
        self.QuesBtn_X.hide()

        self.QuesBtn_Y = QtWidgets.QPushButton(self)
        self.QuesBtn_Y.setGeometry(QtCore.QRect(960, 240, 200, 200))
        self.QuesBtn_Y.setFont(QBtnfont)
        self.QuesBtn_Y.setFlat(True)
        self.QuesBtn_Y.setObjectName("QuesBtn_Y")
        self.QuesBtn_Y.hide()

        self.QuesBtn_B = QtWidgets.QPushButton(self)
        self.QuesBtn_B.setGeometry(QtCore.QRect(1160, 440, 200, 200))
        self.QuesBtn_B.setFont(QBtnfont)
        self.QuesBtn_B.setFlat(True)
        self.QuesBtn_B.setObjectName("QuesBtn_B")
        self.QuesBtn_B.hide()

        self.QuesBtn_A = QtWidgets.QPushButton(self)
        self.QuesBtn_A.setGeometry(QtCore.QRect(960, 640, 200, 200))
        self.QuesBtn_A.setFont(QBtnfont)
        self.QuesBtn_A.setFlat(True)
        self.QuesBtn_A.setObjectName("QuesBtn_A")
        self.QuesBtn_A.hide()

        self.QuesBtn_ShldL = QtWidgets.QPushButton(self)
        self.QuesBtn_ShldL.setGeometry(QtCore.QRect(240, 20, 200, 200))
        self.QuesBtn_ShldL.setFont(QBtnfont)
        self.QuesBtn_ShldL.setFlat(True)
        self.QuesBtn_ShldL.setObjectName("QuesBtn_ShldL")
        self.QuesBtn_ShldL.hide()

        self.QuesBtn_ShldR = QtWidgets.QPushButton(self)
        self.QuesBtn_ShldR.setGeometry(QtCore.QRect(960, 20, 200, 200))
        self.QuesBtn_ShldR.setFont(QBtnfont)
        self.QuesBtn_ShldR.setFlat(True)
        self.QuesBtn_ShldR.setObjectName("QuesBtn_ShldR")
        self.QuesBtn_ShldR.hide()
        #root.setCentralWidget(self.centralwidget)
 
        self.retranslateUi(root)
        QtCore.QMetaObject.connectSlotsByName(root)

    # Set UI Default Text
    def retranslateUi(self, root):
        root.setWindowTitle(_translate("root", "Cognitive Cycling"))
        #level
        self.TaskLabLevel.setText(_translate("root", "<font color='White'>Level</font>"))
        self.TaskValLevel.setText(_translate("root", "<font color='White'>0</font>"))
        #counter
        self.TaskLabCnt.setText(_translate("root", "<font color='White'>Counter</font>"))
        self.TaskValCnt.setText(_translate("root", "<font color='White'>0</font>"))
        #time
        self.HUDValTime.setText(_translate("root", "<font color='White'>0</font>"))
        #Heart rate
        self.HUDValHR.setText(_translate("root", "<font color='White'>0</font>"))
        #Speed
        self.HUDValSpd.setText(_translate("root", "<font color='White'>0</font>"))
        #cadence
        self.HUDValInstCad.setText(_translate("root", "<font color='White'>0</font>"))
        #Accumulate Power
        self.HUDValAccPwr.setText(_translate("root", "<font color='White'>0</font>"))
        #Instanceous Power
        self.HUDValInstPwr.setText(_translate("root", "<font color='White'>0</font>"))
        self.HUDLabPedBal.setText(_translate("root", "<font color='White'>Pedal Balance L/R (%)</font>"))
        #BalanceL
        self.HUDValPBalL.setText(_translate("root", "<font color='White'>50</font>"))
        self.HUDLabInstPwr.setText(_translate("root", "<font color='White'>Inst. Power (W)</font>"))
        self.HUDLabInstCad.setText(_translate("root", "<font color='White'>Inst. Cadence (RPM)</font>"))
        #BalanceR
        self.HUDValPBalR.setText(_translate("root", "<font color='White'>50</font>"))
        self.HUDLabTime.setText(_translate("root", "<font color='White'>Elapsed Time (s)</font>"))
        self.HUDLabHR.setText(_translate("root", "<font color='White'>Heart Rate (BPM)</font>"))
        self.HUDLabSpd.setText(_translate("root", "<font color='White'>Speed (RPM)</font>"))
        self.HUDLabAccPwr.setText(_translate("root", "<font color='White'>Accum. Power (W)</font>"))
        #Start Btn
        self.StartBtn.setText(_translate("root", "Cycle Task"))
        #Game Btn
        self.GameBtn.setText(_translate("root", "Task Only"))
        self.QuesBtn_Left.setText(_translate("root", "L"))
        self.QuesBtn_Down.setText(_translate("root", "D"))
        self.QuesBtn_Up.setText(_translate("root", "U"))
        self.QuesBtn_Right.setText(_translate("root", "R"))
        self.QuesBtn_X.setText(_translate("root", "X"))
        self.QuesBtn_Y.setText(_translate("root", "Y"))
        self.QuesBtn_B.setText(_translate("root", "B"))
        self.QuesBtn_A.setText(_translate("root", "A"))
        self.QuesBtn_ShldL.setText(_translate("root", "L1"))
        self.QuesBtn_ShldR.setText(_translate("root", "R1"))

# Close Program Stuff
    def closeEvent(self, event):

        self.pedalBackend.terminate()
        self.daqbackend.terminate()
        event.accept()
        sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ui = Ui_root()    #Initalise UI
    ui.show()     #Show UI

    sys.exit(app.exec_())

    