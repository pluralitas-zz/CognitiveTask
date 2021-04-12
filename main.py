# Created by: PyQt5 UI code generator 5.6, Form implementation generated from reading ui file 'task.ui'
# Run on Anaconda3-4.3.0-Windows-x86_64, Python Version 3.6.10
import sys, os, time, threading, numpy as np, random
import task_cdown, task_flank, task_workmem, task_nback, task_divAttn, task_major, task_trngComplete, task_PurchaseMission, task_stroop
from writeout import paraout, wrttask
from xinput3_KeyboardControll_NES_Shooter_addGameTask import sample_first_joystick
from PyQt5 import Qt, QtCore, QtGui, QtWidgets, QtTest
from pynput.keyboard import Key, Controller

_translate = QtCore.QCoreApplication.translate
class Ui_root(QtWidgets.QMainWindow):
    _answer = QtCore.pyqtSignal(str) #QtSlot for answering questions in task subpy

# Define your USER ID/NAME HERE
    UserIDNAME = "Test"

# Define YOUR ASSESSMENT RUN TASK EVENT HERE
    def assess_run(self):
        self.taskflow = [1]*60 + [2]*60
        random.shuffle(self.taskflow)

        # #Fixation
        self.disp_qns("Center.png",800,150)
        QtTest.QTest.qWait(180*1000) # Wait 3 minutes

        # #Flanker
        # for i in range(len(self.taskflow)):
        #     self.flnk.run_task(self.taskflow[i])

        # #n-back
        # self.nbckflow = [1] #2
        # random.shuffle(self.nbckflow)
        # for i in range(len(self.nbckflow)):
        #     self.nbckSpace.run_task(self.nbckflow[i])

        # #Stroop
        # random.shuffle(self.taskflow)
        # for i in range(len(self.taskflow)):
        #     self.stroop.run_task(self.taskflow[i])

        self.complet.run_com(1)

# Define YOUR DEMO TASK EVENT HERE
    def demo_run(self):
        QtTest.QTest.qWait(5000)

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
        self.ansdict={}
        self.pictures = "Pictures" #location of pictures in folder "Pictures"
        #self.picd = os.path.join(os.getcwd(),self.pictures)
        self.picd = os.path.join(os.path.dirname(__file__),self.pictures)
        
        self.setupUi(self)
        self.StartBtn.clicked.connect(lambda:self.StartBtnPress())
        self.DemoBtn.clicked.connect(lambda:self.DemoBtnPress())

        self.StartBtn.show()
        # self.DemoBtn.show()

        self.initTaskSigSlot() #Connect signal slots used for Tasks

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

        self.divattn._ansshowhide.connect(self.showhideAnswers)
        self.divattn._paraport.connect(self.parwrite)
        self._answer.connect(self.divattn.append_ans)

        #connect flank task
        self.flnk = task_flank.flank_main()
        self.flnk._qnsdisp.connect(self.disp_qns)
        self.flnk._ansdisp.connect(self.disp_ans)
        self.flnk._ansshowhide.connect(self.showhideAnswers)
        self.flnk._paraport.connect(self.parwrite)
        self._answer.connect(self.flnk.append_ans)

        #connect working memory Verbal task
        self.wrkVerb = task_workmem.workmemVerb_main()
        self.wrkVerb._qnsdisp.connect(self.disp_qns)
        self.wrkVerb._ansdisp.connect(self.disp_ans)
        self.wrkVerb._ansshowhide.connect(self.showhideAnswers)
        self.wrkVerb._paraport.connect(self.parwrite)
        self._answer.connect(self.wrkVerb.append_ans)

        #connect n-back verbal task
        self.nbckVerb = task_nback.nbackVerb_main()
        self.nbckVerb._qnsdisp.connect(self.disp_qns)
        self.nbckVerb._ansdisp.connect(self.disp_ans)
        self.nbckVerb._ansshowhide.connect(self.showhideAnswers)
        self.nbckVerb._paraport.connect(self.parwrite)
        self._answer.connect(self.nbckVerb.append_ans)

        #connect nback task
        self.nbckSpace = task_nback.nbackSpace_main()
        self.nbckSpace._qnsdisp.connect(self.disp_qns)
        self.nbckSpace._ansdisp.connect(self.disp_ans)
        self.nbckSpace._ansshowhide.connect(self.showhideAnswers)
        self.nbckSpace._paraport.connect(self.parwrite)
        self._answer.connect(self.nbckSpace.append_ans)

        #connect working memory Spatial task
        self.wrkSpace = task_workmem.workmemSpace_main()
        self.wrkSpace._qnsdisp.connect(self.disp_qns)
        self.wrkSpace._ansdisp.connect(self.disp_ans)
        self.wrkSpace._ansshowhide.connect(self.showhideAnswers)
        self.wrkSpace._paraport.connect(self.parwrite)
        self._answer.connect(self.wrkSpace.append_ans)

        #connect majority task
        self.mjr = task_major.major_main()
        self.mjr._qnsdisp.connect(self.disp_qns)
        self.mjr._qnsmultidisp.connect(self.disp_qnsmulti)
        self.mjr._ansdisp.connect(self.disp_ans)
        self.mjr._ansshowhide.connect(self.showhideAnswers)
        self.mjr._paraport.connect(self.parwrite)
        self._answer.connect(self.mjr.append_ans)

        #connect stroop task
        self.stroop = task_stroop.stroop_main()
        self.stroop._qnsdisp.connect(self.disp_qns)
        self.stroop._textdisp.connect(self.disp_text)
        self.stroop._ansdisp.connect(self.disp_ans)
        self.stroop._ansshowhide.connect(self.showhideAnswers)
        self.stroop._paraport.connect(self.parwrite)
        self._answer.connect(self.stroop.append_ans)

        #connect Purchase Mission tasl
        self.purmis = task_PurchaseMission.PurchaseMission_main()
        self.purmis._qnsdisp.connect(self.disp_qns)
        self.purmis._qnsmultidisp.connect(self.disp_qnsmulti)
        self.purmis._ansdisp.connect(self.disp_ans)
        self.purmis._ansshowhide.connect(self.showhideAnswers)
        self.purmis._paraport.connect(self.parwrite)

        #create shortcut for buttons
        self.AnsBtn_Left.setShortcut("v")
        self.AnsBtn_Right.setShortcut("b")
        self.AnsBtn_Sq.setShortcut("n")
        self.AnsBtn_Cl.setShortcut("m")

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
        else:
            pass

    def disp_qns(self,data,wid,hei): #Display list of Questions in Ques_Center
        pixmap = QtGui.QPixmap(os.path.join(self.picd, data))
        #pixmap = pixmap.scaled(self.Ques_Center.width(),self.Ques_Center.height(),QtCore.Qt.KeepAspectRatio)
        pixmap = pixmap.scaled(wid,hei,QtCore.Qt.KeepAspectRatio)

        self.Ques_Center.setPixmap(pixmap)

    def disp_text(self,data,col):
        self.Ques_Text.setText("<font color='" + col + "'>" + data + "</font>")

    def disp_qnsmulti(self,data):
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
        self._answer.emit(ans)

# Write out to file Stuff
    def parwrite(self,data):
        try:
            self.para.parawrite(data)
        except: pass
        self.taskcomb = str(np.round(time.time(),decimals=2)) + ',' + str(data) + ";" #time, data value
        self.writetask.appendfile(self.taskcomb) #write task data to file

# Start Task Button, Demo Button & Game Start Button Stuff
    def StartBtnPress(self): #Start Video/Task Mode
        self.StartBtn.hide()
        self.DemoBtn.hide()
        self.TaskFrame.show()

        #Initialise and create Writeout file with username
        self.writetask=wrttask(self.UserIDNAME)
        #Initialise and start Parallel port write to LPT
        self.para = paraout()
        
        self.assess_run()

        #Reset
        self.StartBtn.show()
        # self.DemoBtn.show()
        
    def DemoBtnPress(self): #Start No Hardware Task mode
        self.StartBtn.hide()
        self.DemoBtn.hide()
        self.TaskFrame.show()
        
        #Initialise and create Writeout file with username
        self.writetask=wrttask(self.UserIDNAME)
        #Initialise and start Parallel port write to LPT
        self.para = paraout()
        
        self.demo_run()

        #Reset
        self.StartBtn.show()
        # self.DemoBtn.show()

# Setup UI Stuff
    def setupUi(self, root):
        root.setObjectName("MainWindow")
        root.resize(1600, 900)
        root.setMinimumSize(QtCore.QSize(1900, 1000))
        root.setMaximumSize(QtCore.QSize(1900, 1000))
        root.setAttribute(QtCore.Qt.WA_TranslucentBackground,on=True)
        root.closeEvent = self.closeEvent

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
        
        # Define Task Frame/Question Frame
        self.TaskFrame = QtWidgets.QWidget(self)
        self.TaskFrame.setGeometry(QtCore.QRect(150, 50, 1600, 1000))
        self.TaskFrame.setMaximumSize(QtCore.QSize(1600, 1000))
        #self.HUDFrame.setAutoFillBackground(False)
        self.TaskFrame.setObjectName("HUDFrame")
        self.TaskFrame.setStyleSheet("background-color: rgba(0,0,0,0%)")
        self.TaskFrame.hide()

        self.Ques_Center = QtWidgets.QLabel(self.TaskFrame)
        self.Ques_Center.setGeometry(QtCore.QRect(300, 0, 1000, 800))
        self.Ques_Center.setMinimumSize(QtCore.QSize(0, 0))
        self.Ques_Center.setMaximumSize(QtCore.QSize(1000, 800))
        self.Ques_Center.setAutoFillBackground(False)
        self.Ques_Center.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Ques_Center.setText("")
        self.Ques_Center.setAlignment(QtCore.Qt.AlignCenter)
        self.Ques_Center.setObjectName("Ques_Center")

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
        root.setWindowTitle(_translate("root", "EEG Task"))
        #Start Btn
        self.StartBtn.setText(_translate("root", "Start"))
        #Demo Btn
        self.DemoBtn.setText(_translate("root", "Demo"))
        #Answer Btn
        self.AnsBtn_Left.setText(_translate("root", "L"))
        self.AnsBtn_Right.setText(_translate("root", "R"))
        self.AnsBtn_Sq.setText(_translate("root", "Sq"))
        self.AnsBtn_Cl.setText(_translate("root", "Cl"))

# Close Program Stuff
    def closeEvent(self, event):
        event.accept()
        sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ui = Ui_root()    #Initalise UI
    ui.show()     #Show UI

    sys.exit(app.exec_())