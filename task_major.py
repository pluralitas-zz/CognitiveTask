from PyQt5 import QtCore, QtTest
import random

class major_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _qnsshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)
    _wouttask = QtCore.pyqtSignal(str)

    def __init__(self):
        super(major_main, self).__init__()
        self.questions = ["FlankR.png","FlankL.png"]
        self.blanktask = ["Blank.png","Blank.png","Blank.png","Blank.png","Blank.png","Blank.png","Blank.png","Blank.png","Blank.png","Blank.png"]
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
        if count >= 30:
            self.showtime = 300 #ms
            self.level = 5
            self.showtotal = 7 #total number of questions show, must be odd number
            self.showratio = 4 #number of questions in the same side, must be more than half of showtotal
            self.cutofftime = 30 #multiplies of 100ms
        elif count >= 20:
            self.showtime = 500 #ms
            self.level = 4
            self.showtotal = 5 #total number of questions show
            self.showratio = 3 #number of questions in the same side, must be more than half of showtotal
            self.cutofftime = 50 #multiplies of 100ms
        elif count >= 10:
            self.showtime = 700 #ms
            self.level = 3
            self.showtotal = 5 #total number of questions show
            self.showratio = 4 #number of questions in the same side, must be more than half of showtotal
            self.cutofftime = 70 #multiplies of 100ms
        elif count >= 5:
            self.showtime = 700 #ms
            self.level = 2
            self.showtotal = 5 #total number of questions show
            self.showratio = 4 #number of questions in the same side, must be more than half of showtotal
            self.cutofftime = 70 #multiplies of 100ms
        else:
            self.showtime = 1000 #ms
            self.level = 1
            self.showtotal = 5 #total number of questions show
            self.showratio = 5 #number of questions in the same side, must be more than half of showtotal
            self.cutofftime = 100 #multiplies of 100ms

        # Show Difficulty
        self._level.emit(self.level)
        self._paraport.emit(60) #Task 6
        QtTest.QTest.qWait(2000)
        
        # Show center point
        self._qnsdisp.emit("Center.png",800,150)
        QtTest.QTest.qWait(500)
        self._qnsdisp.emit("Blank.png",800,150)

        # generate correct answers
        self.showoppo = self.showtotal - self.showratio # Number of questions showing opposite
        self.taskchange = random.sample(range(0,9),self.showtotal)
        self.taskcorrect = random.sample(self.questions,2) #First is wrong, 2nd is correct
        self.taskarr = self.blanktask.copy() #create taskarr all blank tasks

        if self.showoppo > 0: #if there are opposite to show
            for i in range(self.showoppo):
                self.taskarr[self.taskchange[i]] = self.taskcorrect[0]
        
        for i in range(self.showratio): #append correct answers to taskarr
            self.taskarr[self.taskchange[self.showoppo+i]] = self.taskcorrect[1]

        self._wouttask.emit("Question Shown")
        self._ansdisp.emit(self.taskarr) #emit taskarr into buttons

        #Delay before questions start showing on screen
        task_delay = random.randrange(1000,3000)
        QtTest.QTest.qWait(task_delay)

        #Hold task in while loop while user isnt cycling
        while self.speed < self.pausespd: 
            QtTest.QTest.qWait(100)

        self.answermajor = True
        self._qnsshowhide.emit(1) #show the answer buttons
        QtTest.QTest.qWait(showtime)
        self._qnsshowhide.emit(0) #hide the answers buttons
        self._ansdisp.emit(self.questions) #emit correct answering array
        
        timeCount = 0
        while len(self.ansarr) < len(self.taskarr): #While loop to hold code till answered or time passes
            QtTest.QTest.qWait(100)
            timeCount += 1
            if timeCount == self.cutofftime:
                break
        
        self.answermajor = False
        if self.ansarr == self.taskarr: #Check if answered correctly or not
            print("Correct")
            self._counter.emit(1)
        else:
            print("Wrong")
            self._counter.emit(0)

        print("finished test")
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self._qnsshowhide.emit(0) #hide the answer buttons

    #Append answers from main.py by user to determine if values are correct
    def append_ans(self,data):
        if self.answermajor == True:
            self.ansarr.append(data[:6])

    def current_speed(self,data,data2):
        self.speed = data
        self.pausespd = data2