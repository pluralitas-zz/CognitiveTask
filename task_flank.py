from PyQt5 import QtCore, QtTest
import random

class flank_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _ansshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)
    _wouttask = QtCore.pyqtSignal(str)
    
    def __init__(self):
        super(flank_main, self).__init__()
        # Array Position to Buttons: A(Bottom),B(Right),X(Left),Y(Top),Up,Down,Left,Right,L1,R1
        self.questions = ["FlankLConL.png", "FlankRConR.png","FlankLInconR.png","FlankRInconL.png"]
        self.flankprep = ["FlankL.png","FlankR.png"]
        self.answers = ["Right.png","Left.png"]
        self.taskarr = []
        self.ansarr = []
        self.answerflank = False
        self.level = 0
        self.speed = 0
        self.pausespd = 10

    def run_task(self,count):
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array

        # Determine difficulty
        self.level = 1
        self.cutofftime = 50 #multiplies of 100ms
        self.showtime = 500

        # Show Difficulty
        #self.diffdisp(self.level)
        self._level.emit(self.level)
        # QtTest.QTest.qWait(2000)
        
        # Show center point
        self._qnsdisp.emit("Center.png",800,150)
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit("Blank.png",800,150)

        #Delay before questions start showing on screen
        task_delay = random.randrange(1000,2000)
        QtTest.QTest.qWait(task_delay)

        #Hold task in while loop while user isnt cycling
        while self.speed < self.pausespd: 
            QtTest.QTest.qWait(1000)

        self._ansdisp.emit(self.answers) #emit answers into buttons

        #Randomise and display the flankprep
        self.disp = random.choice(self.flankprep)
        # self._paraport.emit(10) #Task 1
        self._qnsdisp.emit(self.disp,800,150) #display Flankprep
        QtTest.QTest.qWait(500)
        self.answerflank = True
        
        #Find relevancy in flankprep and select REAL question
        if count == 2:
            self.questions2 = [s for s in self.questions[2:4] if self.disp[:6] in s] #find elements in self.questions containing self.disp[:6]
        else:
            self.questions2 = [s for s in self.questions[0:2] if self.disp[:6] in s] #find elements in self.questions containing self.disp[:6]

        self.disp = self.questions2[0]
        self.taskarr.append(self.disp[-5])
        self._qnsdisp.emit(self.disp,800,150)
        if "Incon" in self.disp:
            self._paraport.emit(12)
            self._wouttask.emit("Question Shown-InCon")
        else:
            self._paraport.emit(11)
            self._wouttask.emit("Question Shown-Con")

        QtTest.QTest.qWait(self.showtime)
        self._qnsdisp.emit("Blank.png",800,150) #wait time from displaying the answers to actually able to answer
        QtTest.QTest.qWait(1000)
        self._ansshowhide.emit(1) #show the answer buttons

        timeCount = 0
        while len(self.ansarr) < len(self.taskarr): #While loop to hold code till answered or time passes
            QtTest.QTest.qWait(100)
            timeCount += 1
            if timeCount == self.cutofftime:
                break
        
        self.answerflank = False
        if self.ansarr == self.taskarr: #Check if answered correctly or not
            # print("Correct")
            self._counter.emit(1)
            self._paraport.emit(15)
        else:
            # print("Wrong")
            self._counter.emit(0)
            self._paraport.emit(16)

        # print("finished test")
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self._ansshowhide.emit(0) #hide the answer buttons

        #QtTest.QTest.qWait(10000) #wait between next test after everything is done

    #Append answers from main.py by user to determine if values are correct
    def append_ans(self,data):
        if self.answerflank == True:
            self.ansarr.append(data[0])
            #print(self.ansarr)

    def current_speed(self,data,data2):
        self.speed = data
        self.pausespd = data2

    def diffdisp(self,numb):
        if numb is 1:
            self._qnsdisp.emit("cd1.png",800,150)
        elif numb is 2:
            self._qnsdisp.emit("cd2.png",800,150)
        elif numb is 3:
            self._qnsdisp.emit("cd3.png",800,150)
        elif numb is 4:
            self._qnsdisp.emit("cd4.png",800,150)
        elif numb is 5:
            self._qnsdisp.emit("cd5.png",800,150)
        else:
            pass