# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtTest
import random

class stroop_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _textdisp = QtCore.pyqtSignal(str,str)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _ansshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)
    _wouttask = QtCore.pyqtSignal(str)

    def __init__(self):
        super(stroop_main, self).__init__()
        self.questions = ["red.png","yellow.png","green.png","blue.png"]
        self.questext = [u"紅", u"黃", u"綠", u"藍"]
        self.quescolour = ["red", "yellow", "green","blue"]
        self.blank = ["Blank.png","Blank.png","Blank.png","Blank.png","Blank.png"]
        self.taskarr = []
        self.ansarr = []
        self.answerstroop = False
        self.level = 0
        self.speed = 0
        self.pausespd = 10

    def run_task(self, count):
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array

        # Determine difficulty
        self.level = count
        self.cutofftime = 50 #multiplies of 100ms
        self.showtime = 500
        self.blanktime = 500

        # Show Difficulty
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

        self._ansdisp.emit(self.questions) #emit answers into buttons

        #Randomly select word to display
        self.dispnum = list(range(len(self.quescolour)))
        random.shuffle(self.dispnum) 
        if count == 2:
            self._textdisp.emit(self.questext[self.dispnum[1]],self.quescolour[self.dispnum[0]])
            self.taskarr.append(self.quescolour[self.dispnum[0]])
            self._paraport.emit(72)
            self._wouttask.emit("Question Shown-InCon")
        else:
            self._textdisp.emit(self.questext[self.dispnum[0]],self.quescolour[self.dispnum[0]])
            self.taskarr.append(self.quescolour[self.dispnum[0]])
            self._paraport.emit(71)
            self._wouttask.emit("Question Shown-Con")
        
        QtTest.QTest.qWait(self.showtime)
        self._textdisp.emit("","white")
        self.answerstroop = True
        QtTest.QTest.qWait(self.blanktime)

        self._ansshowhide.emit(1) #show the answer buttons

        timeCount = 0
        while len(self.ansarr) < len(self.taskarr): #While loop to hold code till answered or time passes
            QtTest.QTest.qWait(100)
            timeCount += 1
            if timeCount == self.cutofftime:
                break
        
        self.answerstroop = False
        self._ansshowhide.emit(0) #hide the answer buttons

        if self.ansarr == self.taskarr:
            print("Correct")
            self._counter.emit(1)
            self._paraport.emit(75)
        else:
            print("Wrong")
            self._counter.emit(0)
            self._paraport.emit(76)

        # print("finished test")
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self._ansshowhide.emit(0) #hide the answer buttons


    #Append answers from main.py by user to determine if values are correct
    def append_ans(self,data):
        if self.answerstroop == True:
            self.ansarr.append(data[:-4])
            # print(self.ansarr)

    def current_speed(self,data,data2):
        self.speed = data
        self.pausespd = data2