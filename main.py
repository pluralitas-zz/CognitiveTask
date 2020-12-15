# Created by: PyQt5 UI code generator 5.6, Form implementation generated from reading ui file 'task.ui'
# Run on Anaconda3-4.3.0-Windows-x86_64, Python Version 3.6.10

# -*- coding: utf-8 -*-

import sys, os, time, threading, numpy as np, random
import VideoPlayer, BackendThread
import task_cdown, task_flank, task_workmem, task_nback, task_divAttn, task_major, task_trngComplete, task_PurchaseMission, task_stroop
from writeout import wrttask, paraout
from xinput3_KeyboardControll_NES_Shooter_addGameTask import sample_first_joystick
from PyQt5 import Qt, QtCore, QtGui, QtWidgets, QtTest
from pynput.keyboard import Key, Controller

_translate = QtCore.QCoreApplication.translate
class Ui_root(QtWidgets.QMainWindow):
    _answer = QtCore.pyqtSignal(str) #QtSlot for answering questions in task subpy
    _speed = QtCore.pyqtSignal(int,int) #QtSlot for speed
    _time = QtCore.pyqtSignal(int)

# Define your USER ID/NAME HERE
    UserIDNAME = "Test"
    assess = True #Run assessment mode
    game = False #True for Game, False for Tasks, ignore self.dotask and self.hiit if True.
    dotask = False #Put true to do task, else False to just cycle
    hiit = False #True to do HIIT, False to do MICT
    cycle = False #Put False if do not want minimal cycling

# Define your Counter scores HERE
    counter = [0,0,0,0,0,0,0,0,0] #Flank, WrkMemVerb, WrkMemSpace, nBckVerb, nBackSpace, mjr, purchaseMission

# Define TRAINING TIME HERE
    traintime = QtCore.QTime(0,0,0) #(hours, minutes, seconds)
    traintimemax = QtCore.QTime(0,30,0)
    trainsec = QtCore.QTime(0,0,0).secsTo(traintimemax) #change to seconds
    tasknumnow = 0 #Task number now
    #tasknum = 0 #Task number sequence

# Define ALL YOUR TASKS FUNCTION HERE
    # tasksnum = random.sample(range(0, 5), 5) # randomise tasks
    tasksnum = [0,1,2,3,4,5,6,7,8]
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
        elif numb is 6:
            self.stroop.run_task(self.count[6])
        else:
            pass

    def tasknameshow(self,numb): #show task names before the task begin
        if numb is 0:
            self.cd.run_cd("NameFlank.png") #10 seconds count down, 7 secs show task name
        elif numb is 1:
            self.cd.run_cd("NameNbackSpace.png") #10 seconds count down, 7 secs show task name
        elif numb is 2:
            self.cd.run_cd("NameMajor.png") #10 seconds count down, 7 secs show task name
        elif numb is 3:
            self.cd.run_cd("NameStroop.png") #10 seconds count down, 7 secs show task name
        else:
            pass

    def tasknumset(self,num):
        self.tasknumnow = self.tasksnum[num]
        self.CntDisplay()
        self.tasknameshow(self.tasknumnow)

# Define YOUR CYCLE TASK EVENT HERE
    def cycle_run(self):
        ################################################### 
        ###############     RUN TASKS     #################
        
        while self.timecount < self.trainsec:
            QtTest.QTest.qWait(100)

        self.complet.run_com(1)
        ###################################################

# Define YOUR HIIT/MCIT RUN TASK EVENT HERE
    def hiit_run(self):
        ################################################### 
        ###############     RUN TASKS     #################
        self.firsttaskone = True
        self.firsttasktwo = True
        self.firsttaskthree = True
        self.firsttaskfour = True
        self.firsttaskfive = True

        while self.timecount < self.trainsec:
                        
            if 330 >= self.timecount > (90-10): #in seconds
                if self.firsttaskone == True:
                    self.tasknumset(0)
                    self.firsttaskone = False

                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)

            elif 500 >= self.timecount > (420-10) or 650 >= self.timecount > (570-10):
                if self.firsttasktwo == True:
                    self.tasknumset(1)
                    self.firsttasktwo = False

                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)

            elif (1020+10) >= self.timecount > 720:                
                if self.firsttaskthree == True:
                    self.tasknumset(2)
                    self.firsttaskthree = False

                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)

            elif 1220 >= self.timecount > (1140-10) or 1370 >= self.timecount > (1290-10):
                if self.firsttaskfour == True:
                    self.tasknumset(3)
                    self.firsttaskfour = False

                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)

            elif 1740 >= self.timecount > (1440-10):
                if self.firsttaskfive == True:
                    self.tasknumset(4)
                    self.firsttaskfive = False

                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)
            else:
                pass
            QtTest.QTest.qWait(100)

        self.complet.run_com(1)
        ###################################################

    def mcit_run(self):
        ################################################### 
        ###############     RUN TASKS     #################
        self.firsttaskone = True
        self.firsttasktwo = True
        self.firsttaskthree = True
        self.firsttaskfour = True
        self.firsttaskfive = True

        while self.timecount < self.trainsec:
            
            if self.timecount == 10:
                self.tasknumnow = 6
                self.purmistask = self.purmis.gen_task(self.counter[6])

            elif 420 >= self.timecount > (120-10): #in seconds
                if self.firsttaskone == True:
                    self.tasknumset(0)
                    self.firsttaskone = False

                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)

            elif self.timecount == 470:
                self.tasknumnow = 6
                self.purmis.ans_task(1,self.counter[6],self.purmistask)

            elif 840 >= self.timecount > (540-10):
                if self.firsttasktwo == True:
                    self.tasknumset(1)
                    self.firsttasktwo = False

                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)

            elif self.timecount == 880:
                self.tasknumnow = 6
                self.purmis.ans_task(2,self.counter[6],self.purmistask)

            elif 1260 >= self.timecount > (960-10):                
                if self.firsttaskthree == True:
                    self.tasknumset(2)
                    self.firsttaskthree = False

                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)
            
            elif self.timecount == 1300:
                self.tasknumnow = 6
                self.purmis.ans_task(3,self.counter[6],self.purmistask)
            
            elif 1680 >= self.timecount > (1380-10):
                if self.firsttaskfour == True:
                    self.tasknumset(3)
                    self.firsttaskfour = False
                    
                self.wouttask("Do Task " + str(self.tasknumnow))
                self.tasks(self.tasknumnow)
           
            elif self.timecount == 1700:
                self.purmis.ans_task(4,self.counter[6],self.purmistask)

            QtTest.QTest.qWait(100)

        self.complet.run_com(1)
        ###################################################
    
# Define YOUR ASSESSMENT RUN TASK EVENT HERE
    def assess_run(self):

        self.disp_qns("Center.png",800,150)
        QtTest.QTest.qWait(120*1000) # Wait 2 minutes

        self.taskflow = [1]*60 + [2]*60
        random.shuffle(self.taskflow)
        self.tasknumset(0)
        for i in range(len(self.taskflow)):
            self.flnk.run_task(self.taskflow[i])

        self.nbckflow = [1,2]
        random.shuffle(self.nbckflow)
        self.tasknumset(1)
        for i in range(len(self.nbckflow)):
            self.nbckSpace.run_task(self.nbckflow[i])

        QtTest.QTest.qWait(180*1000) # Wait 3 minutes

        self.mjrflow = [5]*60 + [4]*60 + [3]*60
        random.shuffle(self.mjrflow)
        self.tasknumset(2)
        for i in range(len(self.mjrflow)):
            self.mjr.run_task(self.mjrflow[i])

        random.shuffle(self.taskflow)
        self.tasknumset(3)
        for i in range(len(self.taskflow)):
            self.stroop.run_task(self.taskflow[i])

        QtTest.QTest.qWait(120*1000) # Wait 2 minutes

        self.complet.run_com(1)

# Define YOUR DEMO TASK EVENT HERE
    def demo_run(self):
        self.tasknumnow = 6
        self.purmistask = self.purmis.gen_task(self.counter[6])
        QtTest.QTest.qWait(1000)

        self.purmis.ans_task(1,self.counter[6],self.purmistask)
        QtTest.QTest.qWait(1000)
        self.purmis.ans_task(2,self.counter[6],self.purmistask)
        QtTest.QTest.qWait(1000)
        self.purmis.ans_task(3,self.counter[6],self.purmistask)
        QtTest.QTest.qWait(1000)
        self.purmis.ans_task(4,self.counter[6],self.purmistask)
        QtTest.QTest.qWait(1000)
        
        QtTest.QTest.qWait(5000)

        self.tasknumset(0)
        for i in range(3):
            self.tasks(0)

        self.tasknumset(1)
        for i in range(3):
            self.tasks(1)

        self.tasknumset(2)
        for i in range(3):
            self.tasks(2)

        self.tasknumset(3)
        for i in range(1):
            self.tasks(3)

        self.tasknumset(4)
        for i in range(1):
            self.tasks(4)

        self.tasknumset(5)
        for i in range(3):
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
        self.pausespd = 10 #Pause/Play Threshold Speed
        self.ansdict={}
        self.timecount = 0
        self.timems = 0 
        self.timer = False
        self.pictures = "Pictures" #location of pictures in folder "Pictures"
        #self.picd = os.path.join(os.getcwd(),self.pictures)
        self.picd = os.path.join(os.path.dirname(__file__),self.pictures)

        self.setupUi(self)
        self.StartBtn.clicked.connect(lambda:self.StartBtnPress())
        self.DemoBtn.clicked.connect(lambda:self.DemoBtnPress())
        self.GameBtn.clicked.connect(lambda:self.GameBtnPress())

        if self.game == True:
            self.dotask = False
            self.GameBtn.show()
        else:
            self.StartBtn.show()
            self.DemoBtn.show()

        self.initTaskSigSlot() #Connect signal slots used for Tasks

        #self.vidFrame.startVid() #Start Video

# Task Stuff
    def initTaskSigSlot(self): #Initialise Task Stuff
      
        #connect countdown
        self.cd = task_cdown.countdown_main()
        self.cd._qnsdisp.connect(self.disp_qns)

        #connect training complete screen
        self.complet = task_trngComplete.trngCom_main()
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
        self.mjr._qnsmultidisp.connect(self.disp_qnsmulti)
        self.mjr._ansdisp.connect(self.disp_ans)
        self.mjr._counter.connect(self.counter_add)
        self.mjr._level.connect(self.LevelDisplay)
        self.mjr._ansshowhide.connect(self.showhideAnswers)
        self.mjr._paraport.connect(self.parwrite)
        self.mjr._wouttask.connect(self.wouttask)
        self._answer.connect(self.mjr.append_ans)
        self._speed.connect(self.mjr.current_speed)

        #connect stroop task
        self.stroop = task_stroop.stroop_main()
        self.stroop._qnsdisp.connect(self.disp_qns)
        self.stroop._textdisp.connect(self.disp_text)
        self.stroop._ansdisp.connect(self.disp_ans)
        self.stroop._counter.connect(self.counter_add)
        self.stroop._level.connect(self.LevelDisplay)
        self.stroop._ansshowhide.connect(self.showhideAnswers)
        self.stroop._paraport.connect(self.parwrite)
        self.stroop._wouttask.connect(self.wouttask)
        self._answer.connect(self.stroop.append_ans)
        self._speed.connect(self.stroop.current_speed)

        #connect Purchase Mission tasl
        self.purmis = task_PurchaseMission.PurchaseMission_main()
        self.purmis._qnsdisp.connect(self.disp_qns)
        self.purmis._qnsmultidisp.connect(self.disp_qnsmulti)
        self.purmis._ansdisp.connect(self.disp_ans)
        self.purmis._counter.connect(self.counter_add)
        self.purmis._level.connect(self.LevelDisplay)
        self.purmis._ansshowhide.connect(self.showhideAnswers)
        self.purmis._wouttask.connect(self.wouttask)
        self.purmis._paraport.connect(self.parwrite)
        self._answer.connect(self.purmis.append_ans)

        #create shortcut for buttons
        self.AnsBtn_Cl.setShortcut("v")
        self.AnsBtn_Sq.setShortcut("d")
        self.AnsBtn_Left.setShortcut(QtCore.Qt.Key_Left)
        self.AnsBtn_Right.setShortcut(QtCore.Qt.Key_Right)

        #connect the buttons to answering definition
        self.AnsBtn_Cl.clicked.connect(lambda:self.answer())
        self.AnsBtn_Sq.clicked.connect(lambda:self.answer())
        self.AnsBtn_Left.clicked.connect(lambda:self.answer())
        self.AnsBtn_Right.clicked.connect(lambda:self.answer())

    def showhideAnswers(self,value): #Show/Hide UI buttons for displaying answers
        if value == 0:
            self.AnsBtn_Left.hide()
            self.AnsBtn_Right.hide()
            self.AnsBtn_Sq.hide()
            self.AnsBtn_Cl.hide()

        elif value == 1:
            self.AnsBtn_Left.show()
            self.AnsBtn_Right.show()

            self.AnsBtn_Sq.show()
            self.AnsBtn_Cl.show()

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
        # print(self.counter)
        # if self.counter in (3, 5, 7): #change videos if counter reached X value(s)
        #     #self.vidFrame.restartVid()
        #     pass

    def counter_reset(self):
        self.counter = [0,0,0,0,0,0]
        QtTest.QTest.qWait(100)
        self.CntDisplay()

    def disp_qns(self,data,wid,hei): #Display list of Questions in Ques_Center
        pixmap = QtGui.QPixmap(os.path.join(self.picd, data))
        #pixmap = pixmap.scaled(self.Ques_Center.width(),self.Ques_Center.height(),QtCore.Qt.KeepAspectRatio)
        pixmap = pixmap.scaled(wid,hei,QtCore.Qt.KeepAspectRatio)

        if data == "Blank.png" or data =="Center.png" or data == "Complete.png" or "neg" in data or "Name" in data or "Inst" in data or "cd" in data:
            pass
        else:
            self.wouttask("Question Shown")
        self.Ques_Center.setPixmap(pixmap)

    def disp_text(self,data,col):
        self.Ques_Text.setText("<font color='" + col + "'>" + data + "</font>")

    def disp_qnsmulti(self,data):
        self.wouttask("Question Shown")
        if len(data) < 5:
            [data.append('Blank.png') for i in range(5 - len(data))] #append to 5 data with 'Blank.png'

        pixmap = QtGui.QPixmap(os.path.join(self.picd, data[0]))
        pixmap = pixmap.scaled(200,200,QtCore.Qt.KeepAspectRatio)
        self.Ques_N.setPixmap(pixmap)

        pixmap = QtGui.QPixmap(os.path.join(self.picd, data[1]))
        pixmap = pixmap.scaled(200,200,QtCore.Qt.KeepAspectRatio)
        self.Ques_NE.setPixmap(pixmap)

        pixmap = QtGui.QPixmap(os.path.join(self.picd, data[2]))
        pixmap = pixmap.scaled(200,200,QtCore.Qt.KeepAspectRatio)
        self.Ques_SE.setPixmap(pixmap)

        pixmap = QtGui.QPixmap(os.path.join(self.picd, data[3]))
        pixmap = pixmap.scaled(200,200,QtCore.Qt.KeepAspectRatio)
        self.Ques_SW.setPixmap(pixmap)

        pixmap = QtGui.QPixmap(os.path.join(self.picd, data[4]))
        pixmap = pixmap.scaled(200,200,QtCore.Qt.KeepAspectRatio)
        self.Ques_NW.setPixmap(pixmap)

    def disp_ans(self,data): #Display Answers in relevant buttons
        
        if len(data) == 2: #if value is 2, allow all left 2(LR) and right 2(SqCl) buttons to do the same thing
            data.insert(1,data[0])
            data.insert(4,data[2])
            self.ansdict = {'Cl':data[0],'Sq':data[1],'L':data[2],'R':data[3]} #dictionary to compare button to picture displayed
            # Change other values except 'Cl' and 'L' "Blank.png" for display
            data[0] = 'Blank.png' 
            data[2] = 'Blank.png'
            # for i in range(len(data)): #Change all values to "Blank.png" for display
            #     data[i] = 'Blank.png'

        elif len(data) != 2 and len(data) < 4: #append to fit the list of buttons if list of values are not enough

            [data.append('Blank.png') for i in range(4 - len(data))] #append to 5 data with 'Blank.png'
            self.ansdict = {'Cl':data[0],'Sq':data[1],'L':data[2],'R':data[3]} #dictionary to compare button to picture displayed

        elif len(data) > 4:
            data = random.sample(data,10)
            self.ansdict = {'Cl':data[0],'Sq':data[1],'L':data[2],'R':data[3]} #dictionary to compare button to picture displayed

        else:
            self.ansdict = {'Cl':data[0],'Sq':data[1],'L':data[2],'R':data[3]} #dictionary to compare button to picture displayed

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[0])))
        self.AnsBtn_Cl.setIcon(icon)
        self.AnsBtn_Cl.setIconSize(QtCore.QSize(300,300))
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[1])))
        self.AnsBtn_Sq.setIcon(icon)
        self.AnsBtn_Sq.setIconSize(QtCore.QSize(300,300))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[2])))
        self.AnsBtn_Left.setIcon(icon)
        self.AnsBtn_Left.setIconSize(QtCore.QSize(300,300))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.picd,data[3])))
        self.AnsBtn_Right.setIcon(icon)
        self.AnsBtn_Right.setIconSize(QtCore.QSize(300,300))

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
    def wouttask(self,data):
        try:
            self.taskcomb = str(np.round(time.time(),decimals=2)) + ',' + str(data) #time, data value
            self.writetask.appendfile(self.taskcomb) #write task data to file
        except: pass

    def parwrite(self,data):
        try:
            self.para.parawrite(data)
        except: pass

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
            self.timer = False
        else: #start video if speed >=pausespd
            self.playVid()
            self.timer = True

# Start Task Button, Demo Button & Game Start Button Stuff
    def StartBtnPress(self): #Start Video/Task Mode
        self.StartBtn.hide()
        self.DemoBtn.hide()
        self.GameBtn.hide()

        self.TaskFrame.show()
        if self.assess == True:
            self.HUDFrame.hide()
        elif self.dotask == False:
            self.vidFrame.startVid() #Start video

        #start Backend signal slot connection
        self.initBackendThread()
        self.pedalBackend.start()
        self.daqbackend.start()
        self.timer = True

        #Initialise and create Writeout file with username
        self.writetask=wrttask(self.UserIDNAME)

        if self.assess == True:
            self.assess_run()
        else:
            if self.dotask == True:
                if self.hiit == False:
                    self.mcit_run()
                else:
                    self.hiit_run()
            else:
                self.cycle_run()

        #Reset
        self.TimeReset()
        self.vidFrame.pauseVid()
        if self.pedalBackend.isRunning():
            self.pedalBackend.terminate()
            self.pedalBackend.wait()
        if self.daqbackend.isRunning():
            self.daqbackend.terminate()
            self.daqbackend.wait()

        self.firsttaskone = True
        self.firsttasktwo = True
        self.firsttaskthree = True
        self.firsttaskfour = True
        self.firsttaskfive = True

        if self.game == True:
            self.GameBtn.show()
        else:
            self.StartBtn.show()
            self.DemoBtn.show()
        
    def DemoBtnPress(self): #Start No Hardware Task mode
        self.StartBtn.hide()
        self.DemoBtn.hide()
        self.GameBtn.hide()
        self.vidFrame.startVid() #Start video 
        self.TaskFrame.show()

        #start Backend signal slot connection
        self.initBackendThread()
        # self.pedalBackend.start()
        self.EncSpeed(999) #set dummy speed as 999
        # self.daqbackend.start()

        #do task
        self.HUDFrame.hide()
        # self.demo_run()
        self.assess_run()

        #Reset
        self.TimeReset()
        self.counter_reset()
        self.vidFrame.pauseVid()
        if self.pedalBackend.isRunning():
            self.pedalBackend.terminate()
            self.pedalBackend.wait()

        self.firsttaskone = True
        self.firsttasktwo = True
        self.firsttaskthree = True
        self.firsttaskfour = True
        self.firsttaskfive = True

        if self.game == True:
            self.GameBtn.show()
        else:
            self.StartBtn.show()
            self.DemoBtn.show()

    def GameBtnPress(self): #Start Game mode
        self.StartBtn.hide()
        self.DemoBtn.hide()
        self.GameBtn.hide()

        #Hide tasks stuff
        self.vidFrame.hide()
        self.TaskFrame.hide()
        self.TaskLabCnt.hide()
        self.TaskValCnt.hide()
        self.TaskLabLevel.hide()
        self.TaskValLevel.hide()

        #start Backend signal slot connection
        self.initBackendThread()
        self.pedalBackend.start()
        self.daqbackend.start()
        self.timer = True
        #self.daqbackend._encoderSpeed.connect(self.Controller_Game) #Pass Speed to controller slot for pressing buttons with Encoder

        #Do Task
        self.cycle_run()

        #Reset
        self.TimeReset()
        self.vidFrame.pauseVid()
        if self.pedalBackend.isRunning():
            self.pedalBackend.terminate()
            self.pedalBackend.wait()
        if self.daqbackend.isRunning():
            self.daqbackend.terminate()
            self.daqbackend.wait()

        if self.game == True:
            self.GameBtn.show()
        else:
            self.StartBtn.show()
            self.DemoBtn.show()

# HUD Stuff
    def TimeDisplay(self,data):
        if self.timer == True:
            self.timecount = self.timecount + int(data-self.timems)/1000 #ms
            self.timeleft = self.traintime.addSecs(self.timecount).toString() #seconds
            self._time.emit(self.timecount*1000)
            self.HUDValTime.setText("<font color='White'>"+ self.timeleft[3:] +"</font>")
        else: pass
        self.timems = data
        
    def TimeReset(self):
        self.timecount = 0
        self._time.emit(0)
        self.timeleft = self.traintime.addSecs(self.timecount)
        self.timedisp = self.timeleft.toString() 
        self.HUDValTime.setText("<font color='White'>"+ self.timedisp[3:] +"</font>")        

    def HRDisplay(self,data):
        if data == 0:
            self.HUDValHR.setText("<font color='Red'>"+ str("NULL") +"</font>")
        else:
            self.HUDValHR.setText("<font color='White'>"+ str(data) +"</font>")

    def EncSpeed(self, data): # UI Slot to recieve Encoder Speed Value
        self.speed=data
        if self.cycle ==True:
            self._speed.emit(data,self.pausespd)
        else:
            self._speed.emit(50,self.pausespd)
        self.HUDValSpd.setText("<font color='White'>"+ str(data)+"</font>")

    def PedalDisplay(self,data): #InstPower, AccumPower, InstCadence, pedalBalRight
        self.HUDValInstPwr.setText(_translate("root","<font color='White'>" + str(data[0]) + "</font>"))
        self.HUDValAvgPwr.setText(_translate("root","<font color='White'>" + str(data[1]) + "</font>"))
        self.HUDValInstCad.setText(_translate("root","<font color='White'>"+ str(data[2]*2) + "</font>"))

        if 255 > data[3] > 128:
            self.HUDValPBalR.setText(_translate("root","<font color='White'>"+ str(data[3]-128)+"</font>"))
            self.HUDValPBalL.setText(_translate("root","<font color='White'>"+ str(100-(data[3]-128))+"</font>"))
        if 0 < data[3] < 128:
            self.HUDValPBalR.setText(_translate("root","<font color='White'>"+ str(100-data[3])+"</font>"))
            self.HUDValPBalL.setText(_translate("root","<font color='White'>"+ str(data[3])+"</font>"))
        else:
            pass

# Game Stuff
    def Controller_Game(self,data): #Controller Slot to recieve Encoder Speed and translate to button inputs
        self.speed=data
        keyboard = Controller()
        
        if self.speed>30: #acceleration, pressed
            keyboard.press('z')            
            QtTest.QTest.qWait(100)                  
        elif 30>=self.speed>10: #acceleration, tapping
            keyboard.press('z')
            QtTest.QTest.qWait(100)
            keyboard.release('z')
        elif 10>=self.speed>=0: #deceleration, not pressed
            keyboard.release('z')
            QtTest.QTest.qWait(100)
        elif self.speed<0:
            keyboard.press('a')
            QtTest.QTest.qWait(100)
            keyboard.release('a') 
    
# Initialize Signal Slots for Backend Threads
    def initBackendThread(self): 
        # Create backend Threads
        self.pedalBackend=BackendThread.PedalThread()
        self.daqbackend=BackendThread.EncDAQBackThread(self.UserIDNAME)

        #Initialize Controller
        self.controller=self.Controller()        
        self.th_Controller=threading.Thread(target=self.controller.thread_Controller, args=(),daemon=True)
        self.th_Controller.start()

        #Initialise and start Parallel port write to LPT
        self.para=paraout()

        # Signal connect to Slots for Data
        self._time.connect(self.daqbackend.Timercv)     #Pass time for writeout
        self.daqbackend._encoderSpeed.connect(self.EncSpeed)  #Pass Speed to UI label2 
        if self.cycle == True:
            self.daqbackend._encoderSpeed.connect(self.videoStartPause) #Encoder Speed control Start/Pause video
        self.daqbackend._etime.connect(self.TimeDisplay)
        self.pedalBackend._HeartRate.connect(self.HRDisplay)       #Pass Heart Rate to UI label 3
        self.pedalBackend._pedalValue.connect(self.PedalDisplay)    #Pass all pedal values
        self.pedalBackend._ANTwrtout.connect(self.daqbackend.ANTrcv) #Pass HR, pedal values for writeout

# Setup UI Stuff
    def setupUi(self, root):
        root.setObjectName("MainWindow")
        root.resize(1600, 900)
        root.setMinimumSize(QtCore.QSize(1900, 1000))
        root.setMaximumSize(QtCore.QSize(1900, 1000))
        if self.game == True:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)  #make window transparent/stay always on top, for Games only
        root.setAttribute(QtCore.Qt.WA_TranslucentBackground,on=True)
        root.closeEvent = self.closeEvent

        # Define Video Task as centralwidget
        self.vidFrame = VideoPlayer.MainWid(self)
        self.setCentralWidget(self.vidFrame)
        #self.vidFrame.hide() #hide video frame
        #self.centralwidget.setObjectName("centralwidget")

        # Define Start Button
        self.StartBtn = QtWidgets.QPushButton(self)
        self.StartBtn.setGeometry(QtCore.QRect(1400, 800, 100, 40))
        self.StartBtn.setFlat(False)
        self.StartBtn.setObjectName("StartBtn")
        self.StartBtn.hide()

        # Define Demo Button
        self.DemoBtn = QtWidgets.QPushButton(self)
        self.DemoBtn.setGeometry(QtCore.QRect(1290, 800, 100, 40))
        self.DemoBtn.setFlat(False)
        self.DemoBtn.setObjectName("DemoBtn")
        self.DemoBtn.hide()
        
        # Define Game Button
        self.GameBtn = QtWidgets.QPushButton(self)
        self.GameBtn.setGeometry(QtCore.QRect(1290, 800, 100, 40))
        self.GameBtn.setFlat(False)
        self.GameBtn.setObjectName("GameBtn")
        self.GameBtn.hide()

        # Define Warning Frame
        self.WarnFrame = QtWidgets.QLabel(self)
        self.WarnFrame.setGeometry(QtCore.QRect(450,100,800,100))
        self.WarnFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.WarnFrame.setMaximumSize(QtCore.QSize(1000, 800))    
        self.WarnFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.WarnFrame.setText("")
        self.WarnFrame.setAlignment(QtCore.Qt.AlignCenter)
        self.WarnFrame.setObjectName("Ques_Center")
        pixmap = QtGui.QPixmap(os.path.join(self.picd, "Pause.png"))
        self.WarnFrame.setPixmap(pixmap)
        self.WarnFrame.hide()

        # Define Task Frame/Question Frame
        self.TaskFrame = QtWidgets.QWidget(self)
        self.TaskFrame.setGeometry(QtCore.QRect(150, 50, 1600, 1000))
        self.TaskFrame.setMaximumSize(QtCore.QSize(1600, 1000))
        #self.HUDFrame.setAutoFillBackground(False)
        self.TaskFrame.setObjectName("HUDFrame")
        self.TaskFrame.setStyleSheet("background-color: rgba(0,0,0,0%)")
        self.TaskFrame.hide()

        self.Ques_N = QtWidgets.QLabel(self.TaskFrame)
        self.Ques_N.setGeometry(QtCore.QRect(700, 30, 200, 200))
        self.Ques_N.setMinimumSize(QtCore.QSize(0, 0))
        self.Ques_N.setMaximumSize(QtCore.QSize(300, 300))
        self.Ques_N.setAutoFillBackground(False)
        self.Ques_N.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Ques_N.setText("")
        self.Ques_N.setAlignment(QtCore.Qt.AlignCenter)
        self.Ques_N.setObjectName("Ques_N")

        self.Ques_NW = QtWidgets.QLabel(self.TaskFrame)
        self.Ques_NW.setGeometry(QtCore.QRect(450, 280, 200, 200))
        self.Ques_NW.setMinimumSize(QtCore.QSize(0, 0))
        self.Ques_NW.setMaximumSize(QtCore.QSize(300, 300))
        self.Ques_NW.setAutoFillBackground(False)
        self.Ques_NW.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Ques_NW.setText("")
        self.Ques_NW.setAlignment(QtCore.Qt.AlignCenter)
        self.Ques_NW.setObjectName("Ques_NW")

        self.Ques_NE = QtWidgets.QLabel(self.TaskFrame)
        self.Ques_NE.setGeometry(QtCore.QRect(950, 280, 200, 200))
        self.Ques_NE.setMinimumSize(QtCore.QSize(0, 0))
        self.Ques_NE.setMaximumSize(QtCore.QSize(300, 300))
        self.Ques_NE.setAutoFillBackground(False)
        self.Ques_NE.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Ques_NE.setText("")
        self.Ques_NE.setAlignment(QtCore.Qt.AlignCenter)
        self.Ques_NE.setObjectName("Ques_NE")

        self.Ques_SW = QtWidgets.QLabel(self.TaskFrame)
        self.Ques_SW.setGeometry(QtCore.QRect(580, 530, 200, 200))
        self.Ques_SW.setMinimumSize(QtCore.QSize(0, 0))
        self.Ques_SW.setMaximumSize(QtCore.QSize(300, 300))
        self.Ques_SW.setAutoFillBackground(False)
        self.Ques_SW.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Ques_SW.setText("")
        self.Ques_SW.setAlignment(QtCore.Qt.AlignCenter)
        self.Ques_SW.setObjectName("Ques_NW")

        self.Ques_SE = QtWidgets.QLabel(self.TaskFrame)
        self.Ques_SE.setGeometry(QtCore.QRect(820, 530, 200, 200))
        self.Ques_SE.setMinimumSize(QtCore.QSize(0, 0))
        self.Ques_SE.setMaximumSize(QtCore.QSize(300, 300))
        self.Ques_SE.setAutoFillBackground(False)
        self.Ques_SE.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Ques_SE.setText("")
        self.Ques_SE.setAlignment(QtCore.Qt.AlignCenter)
        self.Ques_SE.setObjectName("Ques_NE")

        self.Ques_Center = QtWidgets.QLabel(self.TaskFrame)
        self.Ques_Center.setGeometry(QtCore.QRect(300, 0, 1000, 800))
        self.Ques_Center.setMinimumSize(QtCore.QSize(0, 0))
        self.Ques_Center.setMaximumSize(QtCore.QSize(1000, 800))
        self.Ques_Center.setAutoFillBackground(False)
        self.Ques_Center.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Ques_Center.setText("")
        self.Ques_Center.setAlignment(QtCore.Qt.AlignCenter)
        self.Ques_Center.setObjectName("Ques_Center")

        font = QtGui.QFont("Gill Sans MT", pointSize = 300, weight = 50)

        self.Ques_Text = QtWidgets.QLabel(self.TaskFrame)
        self.Ques_Text.setGeometry(QtCore.QRect(300, 0, 1000, 800))
        self.Ques_Text.setMinimumSize(QtCore.QSize(0, 0))
        self.Ques_Text.setMaximumSize(QtCore.QSize(1000, 800))
        self.Ques_Text.setAutoFillBackground(False)
        self.Ques_Text.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Ques_Text.setFont(font)
        self.Ques_Text.setText("")
        self.Ques_Text.setAlignment(QtCore.Qt.AlignCenter)
        self.Ques_Text.setObjectName("Ques_Text")

        font = QtGui.QFont("Gill Sans MT", pointSize = 36, weight = 50)

        # Task Values
        self.TaskValLevel = QtWidgets.QLabel(self)
        self.TaskValLevel.setGeometry(QtCore.QRect(10, 50, 80, 60))
        self.TaskValLevel.setFont(font)
        self.TaskValLevel.setAlignment(QtCore.Qt.AlignCenter)
        self.TaskValLevel.setObjectName("TaskValLevel")
        self.TaskValLevel.setStyleSheet("background-color: rgba(0,0,0,30%)")

        self.TaskValCnt = QtWidgets.QLabel(self)
        self.TaskValCnt.setGeometry(QtCore.QRect(10, 140, 80, 60))
        self.TaskValCnt.setFont(font)
        self.TaskValCnt.setAlignment(QtCore.Qt.AlignCenter)
        self.TaskValCnt.setObjectName("TaskValCnt")
        self.TaskValCnt.setStyleSheet("background-color: rgba(0,0,0,30%)")

        # Define HUD Frame
        self.HUDFrame = QtWidgets.QWidget(self)
        self.HUDFrame.setGeometry(QtCore.QRect(1700, 20, 200, 770))
        self.HUDFrame.setMaximumSize(QtCore.QSize(1900, 1000))
        #self.HUDFrame.setAutoFillBackground(False)
        self.HUDFrame.setObjectName("HUDFrame")
        self.HUDFrame.setStyleSheet("background-color: rgba(0,0,0,15%)")

        # Define Value Display
        font = QtGui.QFont("Gill Sans MT", pointSize = 48, weight = 50)

        self.HUDValTime = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValTime.setGeometry(QtCore.QRect(0, 25, 200, 85))
        self.HUDValTime.setFont(font)
        self.HUDValTime.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValTime.setObjectName("HUDValTime")

        self.HUDValHR = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValHR.setGeometry(QtCore.QRect(0, 135, 200, 85))
        self.HUDValHR.setFont(font)
        self.HUDValHR.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValHR.setObjectName("HUDValHR")

        self.HUDValSpd = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValSpd.setGeometry(QtCore.QRect(0, 245, 200, 85))
        self.HUDValSpd.setFont(font)
        self.HUDValSpd.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValSpd.setObjectName("HUDValSpd")

        self.HUDValInstCad = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValInstCad.setGeometry(QtCore.QRect(0, 355, 200, 85))
        self.HUDValInstCad.setFont(font)
        self.HUDValInstCad.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValInstCad.setObjectName("HUDValInstCad")

        self.HUDValAvgPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValAvgPwr.setGeometry(QtCore.QRect(0, 465, 200, 85))
        self.HUDValAvgPwr.setFont(font)
        self.HUDValAvgPwr.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValAvgPwr.setObjectName("HUDValAvgPwr")

        self.HUDValInstPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValInstPwr.setGeometry(QtCore.QRect(0, 575, 200, 85))
        self.HUDValInstPwr.setFont(font)
        self.HUDValInstPwr.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValInstPwr.setObjectName("HUDValInstPwr")

        self.HUDValPBalR = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValPBalR.setGeometry(QtCore.QRect(100, 685, 100, 85))
        self.HUDValPBalR.setFont(font)
        self.HUDValPBalR.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValPBalR.setObjectName("HUDValPBalR")

        self.HUDValPBalL = QtWidgets.QLabel(self.HUDFrame)
        self.HUDValPBalL.setGeometry(QtCore.QRect(0, 685, 100, 85))
        self.HUDValPBalL.setFont(font)
        self.HUDValPBalL.setAlignment(QtCore.Qt.AlignCenter)
        self.HUDValPBalL.setObjectName("HUDValPBalL")

        # Define Labels
        font = QtGui.QFont("Gill Sans MT", pointSize = 14)

        self.TaskLabLevel = QtWidgets.QLabel(self)
        self.TaskLabLevel.setGeometry(QtCore.QRect(10, 20, 80, 30))
        self.TaskLabLevel.setFont(font)
        self.TaskLabLevel.setScaledContents(False)
        self.TaskLabLevel.setObjectName("TaskLabLevel")
        self.TaskLabLevel.setStyleSheet("background-color: rgba(0,0,0,30%)")

        self.TaskLabCnt = QtWidgets.QLabel(self)
        self.TaskLabCnt.setGeometry(QtCore.QRect(10, 110, 80, 30))
        self.TaskLabCnt.setFont(font)
        self.TaskLabCnt.setScaledContents(False)
        self.TaskLabCnt.setObjectName("TaskLabCnt")
        self.TaskLabCnt.setStyleSheet("background-color: rgba(0,0,0,30%)")

        self.HUDLabPedBal = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabPedBal.setGeometry(QtCore.QRect(0, 660, 200, 25))
        self.HUDLabPedBal.setFont(font)
        self.HUDLabPedBal.setScaledContents(False)
        self.HUDLabPedBal.setObjectName("HUDLabPedBal")

        self.HUDLabInstPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabInstPwr.setGeometry(QtCore.QRect(0, 550, 200, 25))
        self.HUDLabInstPwr.setFont(font)
        self.HUDLabInstPwr.setScaledContents(False)
        self.HUDLabInstPwr.setObjectName("HUDLabInstPwr")

        self.HUDLabInstCad = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabInstCad.setGeometry(QtCore.QRect(0, 330, 200, 25))
        self.HUDLabInstCad.setFont(font)
        self.HUDLabInstCad.setScaledContents(False)
        self.HUDLabInstCad.setObjectName("HUDLabInstCad")

        self.HUDLabTime = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabTime.setGeometry(QtCore.QRect(0, 0, 200, 25))
        self.HUDLabTime.setFont(font)
        self.HUDLabTime.setScaledContents(False)
        self.HUDLabTime.setObjectName("HUDLabTime")

        self.HUDLabHR = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabHR.setGeometry(QtCore.QRect(0, 110, 200, 25))
        self.HUDLabHR.setFont(font)
        self.HUDLabHR.setScaledContents(False)
        self.HUDLabHR.setObjectName("HUDLabHR")

        self.HUDLabSpd = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabSpd.setGeometry(QtCore.QRect(0, 220, 200, 25))
        self.HUDLabSpd.setFont(font)
        self.HUDLabSpd.setScaledContents(False)
        self.HUDLabSpd.setObjectName("HUDLabSpd")

        self.HUDLabAvgPwr = QtWidgets.QLabel(self.HUDFrame)
        self.HUDLabAvgPwr.setGeometry(QtCore.QRect(0, 440, 200, 25))
        self.HUDLabAvgPwr.setFont(font)
        self.HUDLabAvgPwr.setScaledContents(False)
        self.HUDLabAvgPwr.setObjectName("HUDLabAvgPwr")

        # Define Force Balance Separator VLine
        self.HUDLabPedBalSpr = QtWidgets.QFrame(self.HUDFrame)
        self.HUDLabPedBalSpr.setGeometry(QtCore.QRect(100, 690, 3, 80))
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

        # Define Answer Buttons
        QBtnfont = QtGui.QFont("Gill Sans MT", pointSize = 1)
        self.AnsBtn_Left = QtWidgets.QPushButton(self.TaskFrame)
        self.AnsBtn_Left.setGeometry(QtCore.QRect(0, 650, 300, 300))
        self.AnsBtn_Left.setFont(QBtnfont)
        self.AnsBtn_Left.setStyleSheet("background-color: rgba(0,0,0,15%)")
        #self.AnsBtn_Left.setFlat(True)
        self.AnsBtn_Left.setObjectName("AnsBtn_Left")
        self.AnsBtn_Left.hide()

        self.AnsBtn_Right = QtWidgets.QPushButton(self.TaskFrame)
        self.AnsBtn_Right.setGeometry(QtCore.QRect(400, 650, 300, 300))
        self.AnsBtn_Right.setFont(QBtnfont)
        self.AnsBtn_Right.setStyleSheet("background-color: rgba(0,0,0,15%)")
        #self.AnsBtn_Right.setFlat(True)
        self.AnsBtn_Right.setObjectName("AnsBtn_Right")
        self.AnsBtn_Right.hide()

        self.AnsBtn_Sq = QtWidgets.QPushButton(self.TaskFrame)
        self.AnsBtn_Sq.setGeometry(QtCore.QRect(900, 650, 300, 300))
        self.AnsBtn_Sq.setFont(QBtnfont)
        self.AnsBtn_Sq.setStyleSheet("background-color: rgba(0,0,0,15%)")
        #self.AnsBtn_Sq.setFlat(True)
        self.AnsBtn_Sq.setObjectName("AnsBtn_Sq")
        self.AnsBtn_Sq.hide()

        self.AnsBtn_Cl = QtWidgets.QPushButton(self.TaskFrame)
        self.AnsBtn_Cl.setGeometry(QtCore.QRect(1300, 650, 300, 300))
        self.AnsBtn_Cl.setFont(QBtnfont)
        self.AnsBtn_Cl.setStyleSheet("background-color: rgba(0,0,0,15%)")
        #self.AnsBtn_Cl.setFlat(True)
        self.AnsBtn_Cl.setObjectName("AnsBtn_Cl")
        self.AnsBtn_Cl.hide()
 
        self.retranslateUi(root)
        QtCore.QMetaObject.connectSlotsByName(root)

# Set UI Default Text
    def retranslateUi(self, root):
        root.setWindowTitle(_translate("root", "Cognitive Cycling"))
        #level
        self.TaskLabLevel.setText(_translate("root", "<font color='White'>&nbsp;Level</font>"))
        self.TaskValLevel.setText(_translate("root", "<font color='White'>0</font>"))
        #counter
        self.TaskLabCnt.setText(_translate("root", "<font color='White'>&nbsp;Counter</font>"))
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
        self.HUDLabPedBal.setText(_translate("root", "<font color='White'>&nbsp;&nbsp;Pedal Balance L/R (%)</font>"))
        #BalanceL
        self.HUDValPBalL.setText(_translate("root", "<font color='White'>50</font>"))
        self.HUDLabInstPwr.setText(_translate("root", "<font color='White'>&nbsp;&nbsp;Inst. Power (W)</font>"))
        self.HUDLabInstCad.setText(_translate("root", "<font color='White'>&nbsp;&nbsp;Inst. Cadence (RPM)</font>"))
        #BalanceR
        self.HUDValPBalR.setText(_translate("root", "<font color='White'>50</font>"))
        self.HUDLabTime.setText(_translate("root", "<font color='White'>&nbsp;&nbsp;Elapsed Time (s)</font>"))
        self.HUDLabHR.setText(_translate("root", "<font color='White'>&nbsp;&nbsp;Heart Rate (BPM)</font>"))
        self.HUDLabSpd.setText(_translate("root", "<font color='White'>&nbsp;&nbsp;Speed (RPM)</font>"))
        self.HUDLabAvgPwr.setText(_translate("root", "<font color='White'>&nbsp;&nbsp;Avg. Power (W)</font>"))
        #Start Btn
        self.StartBtn.setText(_translate("root", "Cycle Task"))
        #Demo Btn
        self.DemoBtn.setText(_translate("root", "Demo"))
        #Game Btn
        self.GameBtn.setText(_translate("root","Start"))
        #Answer Btn
        self.AnsBtn_Left.setText(_translate("root", "L"))
        self.AnsBtn_Right.setText(_translate("root", "R"))
        self.AnsBtn_Sq.setText(_translate("root", "Sq"))
        self.AnsBtn_Cl.setText(_translate("root", "Cl"))

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