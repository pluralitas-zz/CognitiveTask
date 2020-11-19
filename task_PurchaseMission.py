from PyQt5 import QtCore, QtTest
import random

class PurchaseMission_main(QtCore.Qthread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _qnsmultidisp = QtCore.pyqtSignal(list)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _ansshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)
    _wouttask = QtCore.pyqtSignal(str)

    def __init__(self):
        super(PurchaseMission_main, self).__init__()
        self.questions = ["biscuits.png", "cola.png", "double.png", "drum.png", "eggpulf.png", "fishball.png","flower.png","milktea.png", "pcpudding.png","pineapple.png", "redbean.png","ringcandy.png","teaegg.png","waffle.png"]
        self.blanktask = ["Blank.png","Blank.png","Blank.png","Blank.png","Blank.png"]
        self.blankans = ["Blank.png","Blank.png","Blank.png","Blank.png"]
    
    def gen_task(self,count):
        self.taskarr = []
        self.anstimelim = 60000
        self.purchasemission = False

        self._ansdisp.emit(self.blankans)

        # Determine difficulty
        blanktime = 1000
        if count >= 10:
            showtime = 3000
            self.nval = 8
            self.level = 2
        else:
            showtime = 3000
            self.nval = 4
            self.level = 1

        self._level.emit(self.nval)
        QtTest.QTest.qWait(2000)

        # generate correct values
        for i in range(self.nval):
            self.disp = random.choice(self.questions)
            self.questions.remove(self.disp)
            self.taskarr.append(self.disp)

        # create 4 answers
        if self.nval == 8:
            self.quesone = self.taskarr[0:2]
            self.questwo = self.taskarr[2:4]
            self.questhree = self.taskarr[4:6]
            self.quesfour = self.taskarr[6:8]
        else 
            self.quesone = [self.taskarr[0]]
            self.questwo = [self.taskarr[1]]
            self.questhree = [self.taskarr[2]]
            self.quesfour = [self.taskarr[3]]

        while len(self.quesone) < 4:
            self.quesone.append(self.questions)
        while len(self.questwo) < 4:
            self.questwo.append(self.questions)
        while len(self.questhree) < 4:
            self.questhree.append(self.questions)
        while len(self.quesfour) < 4:
            self.quesfour.append(self.questions)

    #display for user to remember    
        
    #show 4 at one go
        if self.taskarr == 8:
            self.out = ["HOTITEM.png"]
            self.out.append(self.taskarr[0:4])
            self._qnsmultidisp.emit(self.out)
            QtTest.QTest.qWait(showtime)
            self._qnsmultidisp.emit(self.blanktask)
            QtTest.QTest.qWait(2000)

            self.out = ["HOTITEM.png"]
            self.out.append(self.taskarr[5:8])
            self._qnsmultidisp.emit(self.out)
            QtTest.QTest.qWait(showtime)
            self._qnsmultidisp.emit(self.blanktask)
            QtTest.QTest.qWait(2000)
        else:
            #show one at a time
            for i in range(len(self.taskarr)):
                self._qnsdisp.emit(self.taskarr[i-1],600,600)
                self._wouttask.emit("Mission Shown")
                QtTest.QTest.qWait(showtime)
                self._qnsdisp.emit("Blank.png",800,150)
                QtTest.QTest.qWait(2000)

        self.output = [self.taskarr,self.quesone,self.questwo,self.questhree,self.quesfour]

        return self.output

    def ans_task(self,quesno,count,input):
        if input[0] >= 8:
            self.answer = input[0][(quesno*2)-2:quesno*2]
            self.quesarr = input[quesno]
        else:
            self.answer = [input[0][quesno-1]]
            self.quesarr = input[quesno]

        self._ansdisp.emit(self.quesarr) #emit answers into buttons
        self._ansshowhide.emit(1)
        self.purchasemission = True
                    
        timeCount = 0

        while len(self.ansarr) < len(self.answer): #While loop to hold code till answered or time passes
            QtTest.QTest.qWait(100)
            timeCount += 1
            if timeCount == (self.anstimelim/100):
                break

        if quesno == 4:
            if count > len(self.taskarr)/2:
                self._qnsdisp.emit("happyending.png")
            else:
                self._qnsdisp.emit("sadending.png")

        self.purchasemission = False

        self.ansarr.clear()  #clear array
        self._ansdisp.emit(self.blankans)
        self._ansshowhide.emit(0)
        

    def append_ans(self,data):
        if self.purchasemission == True:
            self.ansarr.append(data)
            if data in self.answer: #Check if answered correctly or not
                self._counter.emit(1)
            else:
                self._counter.emit(0)

 

        








        