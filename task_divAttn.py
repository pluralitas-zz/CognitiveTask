from PyQt5 import QtCore, QtTest
import random

class divattn_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _qnsshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)

    def __init__(self):
        super(divattn_main, self).__init__()
        self.question = "Divattn.png"
        self.taskarr = []
        self.ansarr = []
        self.answerdivattn = False
        self.level = 0
        self.speed = 0
        self.pausespd = 10

    def run_task(self,count):
        self.ansarr.clear()     #clear array
        self.taskarr.clear()

        # randomise where the self.question image is going to show on self.answers
        qnsloc = random.randrange(0,9)
        self.answers = []
        for i in range(10):
            self.answers.append('Blank.png')
        
        self.answers[qnsloc] = self.question
        self.taskarr.append(self.question)

        ##Determine difficulty
        if count >= 10:
            waittime = 200
        else:
            waittime = 500

        #Delay before questions start showing on screen
        QtTest.QTest.qWait(100)
        self._level.emit(99)

        self._ansdisp.emit(self.answers) #emit answers into buttons
        QtTest.QTest.qWait(100)
        
        self.answerdivattn = True
        self._qnsshowhide.emit(1) #show the answer buttons

        timeCount = 0
        while len(self.ansarr) < len(self.taskarr): #While loop to hold code till answered or time passes
            QtTest.QTest.qWait(100)
            timeCount += 1
            if timeCount == 100:
                break

        self.answerdivattn = False

        if self.ansarr == self.taskarr: #Check if answered correctly or not
            print("Correct")
            self._counter.emit(1)
        else:
            print("Wrong")
            self._counter.emit(0)

        print("finished test")
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self._qnsshowhide.emit(0)

    #Append answers from main.py by user to determine if values are correct
    def append_ans(self,data):
        if self.answerdivattn == True:
            self.ansarr.append(data)
            # print(self.ansarr)

    def current_speed(self,data,data2):
        self.speed = data
        self.pausespd = data2