#!/usr/bin/env python
# Created by: PyQt5 UI code generator 5.6, Form implementation generated from reading ui file 'task.ui'
# Run on Anaconda3-4.3.0-Windows-x86_64, Python Version 3.6.10
import sys, os, time, threading, numpy as np, random
import VideoPlayer, cdown, task_flank, task_workmem, task_nback, task_divAttn, task_major, trngComplete #custom .py
from xinput3_KeyboardControll_NES_Shooter_addGameTask import sample_first_joystick
from PyQt5 import Qt, QtCore, QtGui, QtWidgets, QtTest
from pynput.keyboard import Key, Controller
from BackendThread import EncDAQBackThread, PedalThread #Encoder=COM5, DAQ=Dev1
from writeout import wrtout, wrttask, paraout

_translate = QtCore.QCoreApplication.translate
class Ui_root(QtWidgets.QMainWindow):
    _answer = QtCore.pyqtSignal(str) #QtSlot for answering questions in task subpy
    _speed = QtCore.pyqtSignal(int,int) #QtSlot for speed

# Define your USER ID/NAME HERE
    UserIDNAME = "Test"
    dotask = True #Put true to do task, else False to just cycle

# Define your Counter scores HERE
    counter = np.array([0,0,0,0,0,0]) #Flank, WrkMemVerb, WrkMemSpace, nBckVerb, nBackSpace, mjr

# Define TRAINING TIME HERE 
    traintime = QtCore.QTime(0,0,0) #(hours, minutes, seconds)
    traintimemax = QtCore.QTime(0,30,0)
    trainsec = QtCore.QTime(0,0,0).secsTo(traintimemax) #change to seconds
    tasknumnow = 0 #Task number now
    tasknum = 0 #Task number sequence

    demosec = QtCore.QTime(0,0,0).secsTo(QtCore.QTime(0,6,0)) #Demo Time

# Define ALL YOUR TASKS FUNCTION HERE
    tasksnum = random.sample(range(0, 5), 4) # randomise tasks
    #tasksnum = [5, 5, 5, 5]
    def tasks(self,numb):
        if numb is 0:
            self.flnk.run_task(self.counter[0])
        elif numb is 1:
            self.wrkVerb.run_task(self.counter[1])
        elif numb is 2:
            self.wrkSpace.run_task(self.counter[2])
        elif numb is 3:
            self.nbckVerb.run_task(self.counter[3])
        elif numb is 4:
            self.nbckSpace.run_task(self.counter[4])
        elif numb is 5:
            self.mjr.run_task(self.counter[5])
        else:
            pass

    def tasknameshow(self,numb): #show task names before the task begin
        if numb is 0:
            self.cd.run_cd("NameFlank.png") #10 seconds count down, 7 secs show task name
        elif numb is 1:
            self.cd.run_cd("NameWrkMemVerb.png") #10 seconds count down, 7 secs show task name
        elif numb is 2:
            self.cd.run_cd("NameWrkMemVisual.png") #10 seconds count down, 7 secs show task name
        elif numb is 3:
            self.cd.run_cd("NameNbackVerb.png") #10 seconds count down, 7 secs show task name
        elif numb is 4:
            self.cd.run_cd("NameNbackVisual.png") #10 seconds count down, 7 secs show task name
        elif numb is 5:
            self.cd.run_cd("NameMajor.png") #10 seconds count down, 7 secs show task name
        else:
            pass

    def tasknumset(self,num):
        self.tasknumnow = self.tasksnum[num]
        self.CntDisplay()
        self.tasknameshow(self.tasknumnow)

# Define YOUR RUN TASK EVENT HERE
    def task_run(self):
        ################################################### 
        ###############     RUN TASKS     #################
        self.firsttaskone = True
        self.firsttasktwo = True
        self.firsttaskthree = True
        self.firsttaskfour = True
        
        while self.timecount < self.trainsec:
                        
            if 420 >= self.timecount > 120: #in seconds
                if self.firsttaskone == True:
                    self.tasknumset(0)
                    self.firsttaskone = False

                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)

            elif 840 >= self.timecount > 540:
                if self.firsttasktwo == True:
                    self.tasknumset(1)
                    self.firsttasktwo = False

                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)

            elif 1260 >= self.timecount > 960:                
                if self.firsttaskthree == True:
                    self.tasknumset(2)
                    self.firsttaskthree = False

                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)

            elif 1680 >= self.timecount > 1380:
                if self.firsttaskfour == True:
                    self.tasknumset(3)
                    self.firsttaskfour = False
                    
                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)

            else:
                pass
            QtTest.QTest.qWait(1000)

        self.complet.run_com(1)
        ###################################################

# Define YOUR DEMO TASK EVENT HERE
    def demo_run(self):
        self.tasknameshow(0)
        for i in range(10):
            self.tasks(0)

        self.tasknameshow(1)
        for i in range(5):
            self.tasks(1)

        self.tasknameshow(2)
        for i in range(5):
            self.tasks(2)

        self.tasknameshow(3)
        for i in range(2):
            self.tasks(3)

        self.tasknameshow(4)
        for i in range(2):
            self.tasks(4)

        self.tasknameshow(5)
        for i in range(5):
            self.tasks(5)

# Main.py Ui_root Init
    class Controller(): #Create Controller Class
        
        def __init__(self): #intialise controller
            self.speed=0 #speed value

        #Controller Threading
        def thread_Controller(self):
            sample_first_joystick()

    def __init__(self):
        #values    
        super(Ui_root,self).__init__()
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
        self.GameBtn.clicked.connect(lambda:self.DemoBtnPress())
        #self.GameBtn.clicked.connect(lambda:self.Gamebutton()) #Change 2nd Start button to Game Mode

        self.initTaskSigSlot() #Connect signal slots used for Tasks

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.TimeDisplay) #connect QtTimer for Elapsed Time
        #self.vidFrame.startVid() #Start Video

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
        self.divattn._ansshowhide.connect(self.showhideAnswers)
        self.divattn._paraport.connect(self.parwrite)
        self.divattn._wouttask.connect(self.wouttask)
        self._answer.connect(self.divattn.append_ans)
        self._speed.connect(self.divattn.current_speed)

        #connect flank task
        self.flnk = task_flank.flank_main()
        self.flnk._qnsdisp.connect(self.disp_qns)
        self.flnk._ansdisp.connect(self.disp_ans)
        self.flnk._counter.connect(self.counter_add)
        self.flnk._level.connect(self.LevelDisplay)
        self.flnk._ansshowhide.connect(self.showhideAnswers)
        self.flnk._paraport.connect(self.parwrite)
        self.flnk._wouttask.connect(self.wouttask)
        self._answer.connect(self.flnk.append_ans)
        self._speed.connect(self.flnk.current_speed)

        #connect working memory Verbal task
        self.wrkVerb = task_workmem.workmemVerb_main()
        self.wrkVerb._qnsdisp.connect(self.disp_qns)
        self.wrkVerb._ansdisp.connect(self.disp_ans)
        self.wrkVerb._counter.connect(self.counter_add)
        self.wrkVerb._level.connect(self.LevelDisplay)
        self.wrkVerb._ansshowhide.connect(self.showhideAnswers)
        self.wrkVerb._paraport.connect(self.parwrite)
        self.wrkVerb._wouttask.connect(self.wouttask)
        self._answer.connect(self.wrkVerb.append_ans)
        self._speed.connect(self.wrkVerb.current_speed)

        #connect n-back verbal task
        self.nbckVerb = task_nback.nbackVerb_main()
        self.nbckVerb._qnsdisp.connect(self.disp_qns)
        self.nbckVerb._ansdisp.connect(self.disp_ans)
        self.nbckVerb._counter.connect(self.counter_add)
        self.nbckVerb._level.connect(self.LevelDisplay)
        self.nbckVerb._ansshowhide.connect(self.showhideAnswers)
        self.nbckVerb._paraport.connect(self.parwrite)
        self.nbckVerb._wouttask.connect(self.wouttask)
        self._answer.connect(self.nbckVerb.append_ans)
        self._speed.connect(self.nbckVerb.current_speed)

        #connect nback task
        self.nbckSpace = task_nback.nbackSpace_main()
        self.nbckSpace._qnsdisp.connect(self.disp_qns)
        self.nbckSpace._ansdisp.connect(self.disp_ans)
        self.nbckSpace._counter.connect(self.counter_add)
        self.nbckSpace._level.connect(self.LevelDisplay)
        self.nbckSpace._ansshowhide.connect(self.showhideAnswers)
        self.nbckSpace._paraport.connect(self.parwrite)
        self.nbckSpace._wouttask.connect(self.wouttask)
        self._answer.connect(self.nbckSpace.append_ans)
        self._speed.connect(self.nbckSpace.current_speed)

        #connect working memory Spatial task
        self.wrkSpace = task_workmem.workmemSpace_main()
        self.wrkSpace._qnsdisp.connect(self.disp_qns)
        self.wrkSpace._ansdisp.connect(self.disp_ans)
        self.wrkSpace._counter.connect(self.counter_add)
        self.wrkSpace._level.connect(self.LevelDisplay)
        self.wrkSpace._ansshowhide.connect(self.showhideAnswers)
        self.wrkSpace._paraport.connect(self.parwrite)
        self.wrkSpace._wouttask.connect(self.wouttask)
        self._answer.connect(self.wrkSpace.append_ans)
        self._speed.connect(self.wrkSpace.current_speed)

        #connect majority task
        self.mjr = task_major.major_main()
        self.mjr._qnsdisp.connect(self.disp_qns)
        self.mjr._ansdisp.connect(self.disp_ans)
        self.mjr._counter.connect(self.counter_add)
        self.mjr._level.connect(self.LevelDisplay)
        self.mjr._ansshowhide.connect(self.showhideAnswers)
        self.mjr._paraport.connect(self.parwrite)
        self.mjr._wouttask.connect(self.wouttask)
        self._answer.connect(self.mjr.append_ans)
        self._speed.connect(self.mjr.current_speed)

        #create shortcut for buttons
        # self.AnsBtn_Cr.setShortcut("c")
        self.AnsBtn_Cl.setShortcut("v")
        self.AnsBtn_Sq.setShortcut("d")
        # self.AnsBtn_Tr.setShortcut("f")
        # self.AnsBtn_Up.setShortcut(QtCore.Qt.Key_Up)
        # self.AnsBtn_Down.setShortcut(QtCore.Qt.Key_Down)
        self.AnsBtn_Left.setShortcut(QtCore.Qt.Key_Left)
        self.AnsBtn_Right.setShortcut(QtCore.Qt.Key_Right)
        # self.AnsBtn_ShldL.setShortcut("e")
        # self.AnsBtn_ShldR.setShortcut("r")

        #connect the buttons to answering definition
        # self.AnsBtn_Cr.clicked.connect(lambda:self.answer())
        self.AnsBtn_Cl.clicked.connect(lambda:self.answer())
        self.AnsBtn_Sq.clicked.connect(lambda:self.answer())
        # self.AnsBtn_Tr.clicked.connect(lambda:self.answer())
        # self.AnsBtn_Up.clicked.connect(lambda:self.answer())
        # self.AnsBtn_Down.clicked.connect(lambda:self.answer())
        self.AnsBtn_Left.clicked.connect(lambda:self.answer())
        self.AnsBtn_Right.clicked.connect(lambda:self.answer())
        # self.AnsBtn_ShldL.clicked.connect(lambda:self.answer())
        # self.AnsBtn_ShldR.clicked.connect(lambda:self.answer())

    def showhideAnswers(self,value): #Show/Hide UI buttons for displaying answers
        if value == 0:
            self.AnsBtn_Left.hide()
            # self.AnsBtn_Down.hide()
            # self.AnsBtn_Up.hide()
            self.AnsBtn_Right.hide()

            self.AnsBtn_Sq.hide()
            # self.AnsBtn_Tr.hide()
            self.AnsBtn_Cl.hide()
            # self.AnsBtn_Cr.hide()

            # self.AnsBtn_ShldL.hide()
            # self.AnsBtn_ShldR.hide()
        elif value == 1:
            self.AnsBtn_Left.show()
            # self.AnsBtn_Down.show()
            # self.AnsBtn_Up.show()
            self.AnsBtn_Right.show()

            self.AnsBtn_Sq.show()
            # self.AnsBtn_Tr.show()
            self.AnsBtn_Cl.show()
            # self.AnsBtn_Cr.show()

            # self.AnsBtn_ShldL.show()
            # self.AnsBtn_ShldR.show()
            QtTest.QTest.qWait(100)
            self.wouttask("Answers Shown")
        else:
            pass

    def counter_add(self,boo): #Add/minus to counter
        if boo == 1:
            self.counter[self.tasknumnow] += 1
            self.wouttask("Correct: " + str(self.counter))
            QtTest.QTest.qWait(100)
        else:
            if self.counter[self.tasknumnow] > 0:
                self.counter[self.tasknumnow] -=1
            self.wouttask("Wrong: "+ str(self.counter))
            QtTest.QTest.qWait(100)
        self.CntDisplay()

        # if self.counter in (3, 5, 7): #change videos if counter reached X value(s)
        #     #self.vidFrame.restartVid()
        #     pass

    def counter_reset(self):
        self.counter = np.array([0,0,0,0,0,0])
        QtTest.QTest.qWait(100)
        self.CntDisplay()

    def disp_qns(self,data,wid,hei): #Display list of Questions in TaskFrame
        pixmap = QtGui.QPixmap(os.path.join(os.path.join(os.path.dirname(__file__),"Pictures"), data))
        #pixmap = pixmap.scaled(self.TaskFrame.width(),self.TaskFrame.height(),QtCore.Qt.KeepAspectRatio)
        pixmap = pixmap.scaled(wid,hei,QtCore.Qt.KeepAspectRatio)

        if data == "Blank.png" or data =="Center.png" or data == "Complete.png" or "neg" in data or "Name" in data or "Inst" in data or "cd" in data:
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
            # for i in range(4): #Change other values except data[0](Bottom Right) and data[5](Bottom Left) to "Blank.png" for display
                # data[i+1] = 'Blank.png' 
                # data[i+6] = 'Blank.png'
            for i in range(len(data)): #Change all values to "Blank.png" for display
                data[i] = 'Blank.png'

        elif "Right.png" in data or "Left.png" in data: #for use with task_major
            self.majorans = ["Right.png","Left.png","Blank.png"]
            self.ansdict = {'A':self.majorans[0],'B':self.majorans[0],'X':self.majorans[0],'Y':self.majorans[0],'U':self.majorans[1],'D':self.majorans[1],'L':self.majorans[1],'R':self.majorans[1],'L1':self.majorans[2],'R1':self.majorans[2]} #dictionary to compare button to picture displayed
        
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
        self.AnsBtn_Cr.setIcon(icon)
        self.AnsBtn_Cr.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[1])))
        self.AnsBtn_Cl.setIcon(icon)
        self.AnsBtn_Cl.setIconSize(QtCore.QSize(300,300))
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[2])))
        self.AnsBtn_Sq.setIcon(icon)
        self.AnsBtn_Sq.setIconSize(QtCore.QSize(300,300))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[3])))
        self.AnsBtn_Tr.setIcon(icon)
        self.AnsBtn_Tr.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[4])))
        self.AnsBtn_Up.setIcon(icon)
        self.AnsBtn_Up.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[5])))
        self.AnsBtn_Down.setIcon(icon)
        self.AnsBtn_Down.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[6])))
        self.AnsBtn_Left.setIcon(icon)
        self.AnsBtn_Left.setIconSize(QtCore.QSize(300,300))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[7])))
        self.AnsBtn_Right.setIcon(icon)
        self.AnsBtn_Right.setIconSize(QtCore.QSize(300,300))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[8])))
        self.AnsBtn_ShldL.setIcon(icon)
        self.AnsBtn_ShldL.setIconSize(QtCore.QSize(200,200))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[9])))
        self.AnsBtn_ShldR.setIcon(icon)
        self.AnsBtn_ShldR.setIconSize(QtCore.QSize(200,200))

    def answer(self): #emit answer to task subpy
        sender = self.sender()
        ans = self.ansdict[sender.text()] #check dict in disp_ans for correct value
        self.wouttask("User Answered")
        self._answer.emit(ans)

    def LevelDisplay(self, data):
        self.TaskValLevel.setText("<font color='White'>"+ str(data) +"</font>")

    def CntDisplay(self):
        self.TaskValCnt.setText("<font color='White'>"+ str(self.counter[self.tasknumnow]) +"</font>")

# Write out to file Stuff
    def writeout(self,data): #time, elapsed time, deg, speed, EMG x 4, PPGRaw, heartrate, InstPower, AccumPower, InstCadence, pedalBalRight
        self.comb = np.column_stack([ np.ones((self.daqbackend.samples,1))*time.time(), np.ones((self.daqbackend.samples,1))*self.timecount, data, self.heartratewoutarr, self.pedalwoutarr])
        self.writefile.appendfile(self.comb) #write data to file
    
    def wouttask(self,data):
        self.timenow = str(np.datetime64('now')).replace(":","")
        self.taskcomb = np.column_stack([self.timenow, str(data)]) #time, data value
        try:
            self.writetask.appendfile(self.taskcomb) #write task data to file
        except:
            pass

    def parwrite(self,data):
        self.para.parawrite(data)

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
            self.timer.stop()
        else: #start video if speed >=pausespd
            self.playVid()
            self.timer.start()

# Start Task Button, Demo Button & Game Start Button Stuff
    def StartBtnPress(self): #Start Video/Task Mode
        self.StartBtn.hide()
        self.GameBtn.hide()
        self.vidFrame.startVid() #Start video 

        #start Backend signal slot connection
        self.initBackendThread()

        #Initialise and create Writeout file with username
        self.writefile=wrtout(self.UserIDNAME)
        self.writetask=wrttask(self.UserIDNAME)

        # Start thread(s)
        self.pedalBackend.start()
        self.daqbackend.start()
        self.timer.start(1000)

        if self.dotask == True:
            self.task_run()

        self.timer.stop()
        self.TimeReset()
        self.vidFrame.pauseVid()
        if self.pedalBackend.isRunning():
            self.pedalBackend.terminate()
            self.pedalBackend.wait()
        if self.daqbackend.isRunning():
            self.daqbackend.terminate()
            self.daqbackend.wait()
        self.StartBtn.show()
        self.GameBtn.show()

    def DemoBtnPress(self): #Start No Hardware Task mode
        self.StartBtn.hide()
        self.GameBtn.hide()
        self.vidFrame.startVid() #Start video 

        #start Backend signal slot connection
        self.initBackendThread()
 
        # Start thread(s)
        self.pedalBackend.start()
        self.EncSpeed(999) #set dummy speed as 999
        self.timer.start(1000)

        self.demo_run()

        self.timer.stop()
        self.TimeReset()
        self.counter_reset()
        self.vidFrame.pauseVid()
        if self.pedalBackend.isRunning():
            self.pedalBackend.terminate()
            self.pedalBackend.wait()

        self.StartBtn.show()
        self.GameBtn.show()

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
        self.daqbackend._encoderSpeed.connect(self.Controller_Game) #Pass Speed to controller slot for pressing buttons with Encoder

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

    def TimeReset(self):
        self.timecount = 0
        self.timeleft = self.traintime.addSecs(self.timecount)
        self.timedisp = self.timeleft.toString() 
        self.HUDValTime.setText("<font color='White'>"+ self.timedisp[3:] +"</font>")        

    def HRDisplay(self,data):
        self.heartratewoutarr[0] = data
        self.HUDValHR.setText("<font color='White'>"+ str(data) +"</font>")

    def EncSpeed(self, data): # UI Slot to recieve Encoder Speed Value
        self.speed=data
        self._speed.emit(data,self.pausespd)
        self.HUDValSpd.setText("<font color='White'>"+ str(data)+"</font>")
        #self.HUDValSpd.setText(_translate("root", ("<font color='White'>"+str(data)+"</font>")))

    def PedalDisplay(self,data): #InstPower, AccumPower, InstCadence, pedalBalRight
        self.pedalwoutarr[0] = data #append into array for writeout
        self.HUDValInstPwr.setText(_translate("root","<font color='White'>" + str(data[0]) + "</font>"))
        self.HUDValAvgPwr.setText(_translate("root","<font color='White'>" + str(data[1]) + "</font>"))
        self.HUDValInstCad.setText(_translate("root","<font color='White'>"+ str(data[2]) + "</font>"))

        if data[3] > 0:
            self.HUDValPBalR.setText(_translate("root","<font color='White'>"+ str(data[3])+"</font>"))
            self.HUDValPBalL.setText(_translate("root","<font color='White'>"+ str(100-data[3])+"</font>"))

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
        self.heartratewoutarr = np.zeros((self.daqbackend.samples,1)) #blank array for use with writeout

        #Initialize Controller
        self.controller=self.Controller()        
        self.th_Controller=threading.Thread(target=self.controller.thread_Controller, args=(),daemon=True)
        self.th_Controller.start()

        #Initialise and start Parallel port write to LPT
        self.para=paraout()

        # Signal connect to Slots for Data
        self.daqbackend._encoderSpeed.connect(self.EncSpeed)  #Pass Speed to UI label2 
        self.daqbackend._encoderSpeed.connect(self.videoStartPause) #Encoder Speed control Start/Pause video
        self.daqbackend._woutBackEndArray.connect(self.writeout)    #Writeout
        self.pedalBackend._HeartRate.connect(self.HRDisplay)       #Pass Heart Rate to UI label 3
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
        self.GameBtn.setGeometry(QtCore.QRect(1140, 800, 100, 40))
        self.GameBtn.setFlat(False)
        self.GameBtn.setObjectName("GameBtn")

    # Define Warning Frame
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

    # Define Task Frame
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

        self.HUDValAvgPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValAvgPwr.setGeometry(QtCore.QRect(0, 485, 200, 85))
        self.HUDValAvgPwr.setFont(font)
        self.HUDValAvgPwr.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValAvgPwr.setObjectName("HUDValAvgPwr")

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

        self.HUDLabAvgPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabAvgPwr.setGeometry(QtCore.QRect(10, 460, 200, 25))
        self.HUDLabAvgPwr.setFont(font)
        self.HUDLabAvgPwr.setScaledContents(False)
        self.HUDLabAvgPwr.setObjectName("HUDLabAvgPwr")

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
        self.AnsBtn_Left = QtWidgets.QPushButton(self)
        self.AnsBtn_Left.setGeometry(QtCore.QRect(0, 600, 300, 300))
        self.AnsBtn_Left.setFont(QBtnfont)
        self.AnsBtn_Left.setStyleSheet("background-color: rgba(0,0,0,15%)")
        #self.AnsBtn_Left.setFlat(True)
        self.AnsBtn_Left.setObjectName("AnsBtn_Left")
        #self.AnsBtn_Left.hide()

        self.AnsBtn_Down = QtWidgets.QPushButton(self)
        self.AnsBtn_Down.setGeometry(QtCore.QRect(240, 640, 200, 200))
        self.AnsBtn_Down.setFont(QBtnfont)
        self.AnsBtn_Down.setFlat(True)
        self.AnsBtn_Down.setObjectName("AnsBtn_Down")
        self.AnsBtn_Down.hide()

        self.AnsBtn_Up = QtWidgets.QPushButton(self)
        self.AnsBtn_Up.setGeometry(QtCore.QRect(240, 240, 200, 200))
        self.AnsBtn_Up.setFont(QBtnfont)
        self.AnsBtn_Up.setFlat(True)
        self.AnsBtn_Up.setObjectName("AnsBtn_Up")
        self.AnsBtn_Up.hide()

        self.AnsBtn_Right = QtWidgets.QPushButton(self)
        self.AnsBtn_Right.setGeometry(QtCore.QRect(350, 600, 300, 300))
        self.AnsBtn_Right.setFont(QBtnfont)
        self.AnsBtn_Right.setStyleSheet("background-color: rgba(0,0,0,15%)")
        #self.AnsBtn_Right.setFlat(True)
        self.AnsBtn_Right.setObjectName("AnsBtn_Right")
        #self.AnsBtn_Right.hide()

        self.AnsBtn_Sq = QtWidgets.QPushButton(self)
        self.AnsBtn_Sq.setGeometry(QtCore.QRect(750, 600, 300, 300))
        self.AnsBtn_Sq.setFont(QBtnfont)
        self.AnsBtn_Sq.setStyleSheet("background-color: rgba(0,0,0,15%)")
        #self.AnsBtn_Sq.setFlat(True)
        self.AnsBtn_Sq.setObjectName("AnsBtn_Sq")
        #self.AnsBtn_Sq.hide()

        self.AnsBtn_Tr = QtWidgets.QPushButton(self)
        self.AnsBtn_Tr.setGeometry(QtCore.QRect(960, 240, 200, 200))
        self.AnsBtn_Tr.setFont(QBtnfont)
        self.AnsBtn_Tr.setFlat(True)
        self.AnsBtn_Tr.setObjectName("AnsBtn_Tr")
        self.AnsBtn_Tr.hide()

        self.AnsBtn_Cl = QtWidgets.QPushButton(self)
        self.AnsBtn_Cl.setGeometry(QtCore.QRect(1100, 600, 300, 300))
        self.AnsBtn_Cl.setFont(QBtnfont)
        self.AnsBtn_Cl.setStyleSheet("background-color: rgba(0,0,0,15%)")
        #self.AnsBtn_Cl.setFlat(True)
        self.AnsBtn_Cl.setObjectName("AnsBtn_Cl")
        #self.AnsBtn_Cl.hide()

        self.AnsBtn_Cr = QtWidgets.QPushButton(self)
        self.AnsBtn_Cr.setGeometry(QtCore.QRect(960, 640, 200, 200))
        self.AnsBtn_Cr.setFont(QBtnfont)
        self.AnsBtn_Cr.setFlat(True)
        self.AnsBtn_Cr.setObjectName("AnsBtn_Cr")
        self.AnsBtn_Cr.hide()

        self.AnsBtn_ShldL = QtWidgets.QPushButton(self)
        self.AnsBtn_ShldL.setGeometry(QtCore.QRect(240, 20, 200, 200))
        self.AnsBtn_ShldL.setFont(QBtnfont)
        self.AnsBtn_ShldL.setFlat(True)
        self.AnsBtn_ShldL.setObjectName("AnsBtn_ShldL")
        self.AnsBtn_ShldL.hide()

        self.AnsBtn_ShldR = QtWidgets.QPushButton(self)
        self.AnsBtn_ShldR.setGeometry(QtCore.QRect(960, 20, 200, 200))
        self.AnsBtn_ShldR.setFont(QBtnfont)
        self.AnsBtn_ShldR.setFlat(True)
        self.AnsBtn_ShldR.setObjectName("AnsBtn_ShldR")
        self.AnsBtn_ShldR.hide()
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
        #Average Power
        self.HUDValAvgPwr.setText(_translate("root", "<font color='White'>0</font>"))
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
        self.HUDLabAvgPwr.setText(_translate("root", "<font color='White'>Avg. Power (W)</font>"))
        #Start Btn
        self.StartBtn.setText(_translate("root", "Cycle Task"))
        #Game Btn
        self.GameBtn.setText(_translate("root", "Demo"))
        #Answer Btn
        self.AnsBtn_Left.setText(_translate("root", "L"))
        # self.AnsBtn_Down.setText(_translate("root", "D"))
        # self.AnsBtn_Up.setText(_translate("root", "U"))
        self.AnsBtn_Right.setText(_translate("root", "R"))
        self.AnsBtn_Sq.setText(_translate("root", "X"))
        # self.AnsBtn_Tr.setText(_translate("root", "Y"))
        self.AnsBtn_Cl.setText(_translate("root", "B"))
        # self.AnsBtn_Cr.setText(_translate("root", "A"))
        # self.AnsBtn_ShldL.setText(_translate("root", "L1"))
        # self.AnsBtn_ShldR.setText(_translate("root", "R1"))

# Close Program Stuff
    def closeEvent(self, event):
        if self.pedalBackend.isRunning():
            self.pedalBackend.terminate()
            self.pedalBackend.wait()
        if self.daqbackend.isRunning():
            self.daqbackend.terminate()
            self.daqbackend.wait()
        event.accept()
        sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ui = Ui_root()    #Initalise UI
    ui.show()     #Show UI

    sys.exit(app.exec_())

    