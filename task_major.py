from PyQt5 import QtCore, QtTest
import random

class major_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _ansshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)
    _wouttask = QtCore.pyqtSignal(str)
    _qnsmultidisp = QtCore.pyqtSignal(list)

    def __init__(self):
        super(major_main, self).__init__()
        self.questions = ["Right.png","Left.png"]
        self.blanktask = ["Blank.png","Blank.png","Blank.png","Blank.png","Blank.png"]
        self.taskarr = []
        self.ansarr = []
        self.answermajor = False
        self.level = 0
        self.speed = 0
        self.pausespd = 10

    def run_task(self, count):
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array

        # Determine difficulty
        self.showtime = 1000 #ms
        self.level = 5-(abs(count)-1)
        self.showtotal = 5 #total number of questions show
        self.showratio = abs(count) #number of questions in the same side, must be more than half of showtotal
        self.cutofftime = 100 #multiplies of 100ms

        # Show Difficulty
        self._level.emit(self.level)
        self._paraport.emit(60+ self.level) #Task 6
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

        self._ansdisp.emit(self.questions) #emit answers into buttons

        # generate correct answers
        self.showoppo = self.showtotal - self.showratio # Number of questions showing opposite
        self.taskchange = random.sample(range(0,4),self.showoppo) #array values to change to wrong
        self.taskcorrect = random.sample(self.questions,2) #First is wrong, 2nd is correct
        self.taskarr = self.blanktask.copy() #create taskarr all blank tasks

        for i in range(self.showtotal): #append correct answers to taskarr
            self.taskarr[i] = self.taskcorrect[1]

        for i in range(len(self.taskchange)): #change correct to wrong answers
            self.taskarr[self.taskchange[i]] = self.taskcorrect[0]

        self._wouttask.emit("Question Shown")
        self._qnsmultidisp.emit(self.taskarr) #emit taskarr into buttons

        self.answermajor = True
        QtTest.QTest.qWait(self.showtime)
        self._qnsmultidisp.emit(self.blanktask) #hide the answers buttons
        self._paraport.emit(64)
        self._ansshowhide.emit(1) #show the answer buttons
        
        timeCount = 0
        while len(self.ansarr) < 1: #While loop to hold code till answered or time passes
            QtTest.QTest.qWait(100)
            timeCount += 1
            if timeCount == self.cutofftime:
                break
        
        self.answermajor = False
        if self.ansarr == [self.taskcorrect[1]]: #Check if answered correctly or not
            # print("Correct")
            self._counter.emit(1)
            self._paraport.emit(65)
        else:
            # print("Wrong")
            self._counter.emit(0)
            self._paraport.emit(66)

        # print("finished test")
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self._ansshowhide.emit(0) #hide the answer buttons

    #Append answers from main.py by user to determine if values are correct
    def append_ans(self,data):
        if self.answermajor == True:
            self.ansarr.append(data)

    def current_speed(self,data,data2):
        self.speed = data
        self.pausespd = data2