from PyQt5 import QtCore, QtTest
import random

class nbackVerb_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _ansshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)
    _wouttask = QtCore.pyqtSignal(str)

    def __init__(self):
        super(nbackVerb_main, self).__init__()
        # Array Position to Buttons: A(Bottom),B(Right),X(Left),Y(Top),Up,Down,Left,Right,L1,R1
        self.questions = ["VerbAirport.png", "VerbChurch.png","VerbHospital.png","VerbLibrary.png","VerbMarket.png","VerbPharmacy.png","VerbRestaurant.png","VerbSalon.png","VerbSchool.png","VerbStation.png"]
        self.answers = ["VerbTick.png","VerbCross.png"]
        self.dispcount = 0
        self.anscount = 0
        self.taskarr = []
        self.correctarr = []
        self.nval = 0
        self.answernbackVerb = False
        self.answerappended = True
        self.level = 0
        self.speed = 0
        self.pausespd = 10
        
    def run_task(self,count):
        self.taskarr.clear()    #clear array
        
        # Determine difficulty
        blanktime = 1000
        showtime = 1000
        self.nval = -abs(count)

        self._level.emit(self.nval)
        self.diffdisp(self.nval)
        # QtTest.QTest.qWait(1000)

        # Show center point
        self._qnsdisp.emit("Center.png",800,150) 
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit("Blank.png",800,150)

        # generate 60 values
        arraylen = 60
        for i in range(arraylen):
            self.disp = random.choice(self.questions)
            self.taskarr.append(self.disp)

        # Generate values to have X amount of correct answer
        correctval = 12
        for i in range(correctval):
            self.correctarr.append(random.randint(arraylen/correctval*i , arraylen/correctval*(i+1)-2))

        # correcting the answers
        for i in range(len(self.correctarr)):
            if self.correctarr[i]+self.nval >= 0:
                self.taskarr[self.correctarr[i]] = self.taskarr[self.correctarr[i]+self.nval]

        self._ansdisp.emit(self.answers)
        self._ansshowhide.emit(1) #show the answer buttons

        #Delay before questions start showing on screen
        task_delay = random.randrange(1000,2000)
        QtTest.QTest.qWait(task_delay)

        for i in range(len(self.taskarr)):
            self.answerappended = False

            while self.speed < self.pausespd: #hold task in while loop while user isnt cycling
                QtTest.QTest.qWait(1000)

            self.dispcount = i
            self._qnsdisp.emit(self.taskarr[i],800,150)
            try:
                self.dispback = self.taskarr[self.dispcount+self.nval]
            except:
                self.dispback = self.taskarr[self.dispcount]

            if self.taskarr[self.dispcount] == self.dispback and self.dispcount !=0:
                self._wouttask.emit("Question Shown-True")
                self._paraport.emit(49)
            else:
                self._wouttask.emit("Question Shown-False")
                self._paraport.emit(48)
            self.answernbackVerb = True
            

            QtTest.QTest.qWait(showtime)
            self._qnsdisp.emit("Blank.png",800,150)
            QtTest.QTest.qWait(blanktime)

            timeCount = 0
            while timeCount < (blanktime/100):
                QtTest.QTest.qWait(100)
                timeCount += 1
                if timeCount == (blanktime/100) or self.answerappended == True:
                    break

        self.answernbackVerb = False
        # print("finished test")
        self.taskarr.clear()    #clear array
        self._ansshowhide.emit(0) #hide the answer buttons
        
    #Append answers from main.py by user to determine if values are correct + randomise next answer
    def append_ans(self,data):
        if self.answernbackVerb == True:
            self.answerappended = True
            self.answernbackVerb = False

            # try:
            #     self.dispback = self.taskarr[self.dispcount+self.nval]
            # except:
            #     self.dispback = self.taskarr[self.dispcount]

            if data == "VerbTick.png":
                if self.taskarr[self.dispcount] == self.dispback and self.dispcount != 0: #Check if answered correctly or not
                    self.anscount +=1
                    #if self.anscount in (3,6,9,12):
                    #    self.anscount = 0
                    self._counter.emit(1)
                    # print("Correct: " + str(self.anscount))
                    
                else:
                    self._counter.emit(0)
                    # print("Wrong")
            elif data == "VerbCross.png":
                if self.taskarr[self.dispcount] != self.dispback and self.dispcount != 0: #Check if answered correctly or not
                    self.anscount +=1
                    #if self.anscount in (3,6,9,12):
                    #    self.anscount = 0
                    self._counter.emit(1)
                    # print("Correct: " + str(self.anscount))
                    
                else:
                    self._counter.emit(0)
                    # print("Wrong")

            else:
                self._counter.emit(0)
                # print("Wrong")
    
    def current_speed(self,data,data2):
        self.speed = data
        self.pausespd = data2

    def diffdisp(self,numb):
        if numb is -1:
            self._qnsdisp.emit("neg1.png",800,150)
            self._paraport.emit(41)
            self._wouttask.emit("Task n-1")
        elif numb is -2:
            self._qnsdisp.emit("neg2.png",800,150)
            self._paraport.emit(42)
            self._wouttask.emit("Task n-2")
        elif numb is -3:
            self._qnsdisp.emit("neg3.png",800,150)
            self._paraport.emit(43)
            self._wouttask.emit("Task n-3")
        else:
            pass


class nbackSpace_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _ansshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)
    _wouttask = QtCore.pyqtSignal(str)

    def __init__(self):
        super(nbackSpace_main, self).__init__()
        # Array Position to Buttons: A(Bottom),B(Right),X(Left),Y(Top),Up,Down,Left,Right,L1,R1
        self.questions = ["SpaceN.png", "SpaceE.png","SpaceS.png","SpaceW.png","SpaceNE.png","SpaceNW.png","SpaceSE.png","SpaceNW.png"]
        self.answers = ["VerbTick.png","VerbCross.png"]
        self.dispcount = 0
        self.anscount = 0
        self.taskarr = []
        self.correctarr = []
        self.nval = 0
        self.answernbackSpace = False
        self.answerappended = True
        self.level = 0
        self.speed = 0
        self.pausespd = 10

    def run_task(self,count):
        self.taskarr.clear()    #clear array

        # Determine difficulty
        self.blanktime = 500
        self.showtime = 600
        self.cutofftime = 50 #multiplies of 100ms
        self.nval = -abs(count)

        self._level.emit(self.nval)
        self.diffdisp(self.nval)
        # QtTest.QTest.qWait(1000)

        # Show center point
        self._qnsdisp.emit("Center.png",800,150) 
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit("Blank.png",800,150)

        # generate 60 values
        arraylen = 60
        for i in range(arraylen):
            self.disp = random.choice(self.questions)
            self.taskarr.append(self.disp)

        # Generate values to have X amount of correct answer
        correctval = 12
        for i in range(correctval):
            self.correctarr.append(random.randint(arraylen/correctval*i , arraylen/correctval*(i+1)-2))
        
        # correcting the answers
        for i in range(len(self.correctarr)):
            if self.correctarr[i]+self.nval >= 0:
                self.taskarr[self.correctarr[i]] = self.taskarr[self.correctarr[i]+self.nval]

        self._ansdisp.emit(self.answers)
        self._ansshowhide.emit(1) #show the answer buttons

        #Delay before questions start showing on screen
        task_delay = random.randrange(1000,2000)
        QtTest.QTest.qWait(task_delay)

        for i in range(len(self.taskarr)):
            self.answerappended = False

            while self.speed < self.pausespd: #hold task in while loop while user isnt cycling
                QtTest.QTest.qWait(1000)

            self.dispcount = i
            self._qnsdisp.emit(self.taskarr[i],600,600)
            try:
                self.dispback = self.taskarr[self.dispcount+self.nval]
            except:
                self.dispback = self.taskarr[self.dispcount]

            if self.taskarr[self.dispcount] == self.dispback and self.dispcount !=0:
                self._wouttask.emit("Question Shown-True")
                self._paraport.emit(59)
            else:
                self._wouttask.emit("Question Shown-False")
                self._paraport.emit(58)
            self.answernbackSpace = True

            QtTest.QTest.qWait(self.showtime)
            self._qnsdisp.emit("Blank.png",800,150)
            QtTest.QTest.qWait(self.blanktime)

            timeCount = 0
            while timeCount < (self.blanktime/100):
                QtTest.QTest.qWait(100)
                timeCount += 1
                if timeCount == (self.blanktime/100) or self.answerappended == True:
                    break

        self.answernbackSpace = False
        # print("finished test")
        self.taskarr.clear()    #clear array
        self._ansshowhide.emit(0) #hide the answer buttons
        
    #Append answers from main.py by user to determine if values are correct + randomise next answer
    def append_ans(self,data):
        if self.answernbackSpace == True:
            self.answerappended = True
            self.answernbackSpace = False

            # try:
            #     self.dispback = self.taskarr[self.dispcount+self.nval]
            # except:
            #     self.dispback = self.taskarr[self.dispcount]

            if data == "VerbTick.png":
                if self.taskarr[self.dispcount] == self.dispback and self.dispcount != 0: #Check if answered correctly or not
                    self.anscount +=1
                    #if self.anscount in (3,6,9,12):
                    #    self.anscount = 0
                    self._counter.emit(1)
                    # print("Correct: " + str(self.anscount))
                    
                else:
                    self._counter.emit(0)
                    # print("Wrong")
            elif data == "VerbCross.png":
                if self.taskarr[self.dispcount] != self.dispback and self.dispcount != 0: #Check if answered correctly or not
                    self.anscount +=1
                    #if self.anscount in (3,6,9,12):
                    #    self.anscount = 0
                    self._counter.emit(1)
                    # print("Correct: " + str(self.anscount))
                    
                else:
                    self._counter.emit(0)
                    # print("Wrong")

            else:
                self._counter.emit(0)
                # print("Wrong")
    
    def current_speed(self,data,data2):
        self.speed = data
        self.pausespd = data2

    def diffdisp(self,numb):
        if numb is -1:
            self._qnsdisp.emit("neg1.png",800,150)
            self._paraport.emit(51)
            self._wouttask.emit("Task n-1")
        elif numb is -2:
            self._qnsdisp.emit("neg2.png",800,150)
            self._paraport.emit(52)
            self._wouttask.emit("Task n-2")
        elif numb is -3:
            self._qnsdisp.emit("neg3.png",800,150)
            self._paraport.emit(53)
            self._wouttask.emit("Task n-3")
        else:
            pass