from PyQt5 import QtCore, QtTest
import random

class workmemVerb_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _qnsshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)

    def __init__(self):
        super(workmemVerb_main, self).__init__()
        # Array Position to Buttons: A(Bottom),B(Right),X(Left),Y(Top),Up,Down,Left,Right,L1,R1
        self.questions = ["VerbAirport.png", "VerbChurch.png","VerbHospital.png","VerbLibrary.png","VerbMarket.png","VerbPharmacy.png","VerbRestaurant.png","VerbSalon.png","VerbSchool.png","VerbStation.png"]
        self.dispcount = 0
        self.anscount = 0
        self.taskarr = []
        self.anspadarr =[]
        self.ansarr = []
        self.answerworkmemVerb = False
        self.level = 0

    def run_task(self,count):
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self.anspadarr.clear()

        # Show center point
        self._qnsdisp.emit("Center.png",800,150) 
        QtTest.QTest.qWait(500)
        self._qnsdisp.emit("Blank.png",800,150)
        
        # Determine difficulty
        showtime = 1000
        blanktime = 1000
        if count >= 10:
            self.anscount = 10
            self.dispcount = 5
            self.level = 3
        elif count >= 5:
            self.anscount = 7
            self.dispcount = 4
            self.level = 2
        else:
            self.anscount = 5
            self.dispcount = 3
            self.level = 1
        self._level.emit(self.level)        
        #Delay before questions start showing on screen
        task_delay = random.randrange(1000,3000)
        QtTest.QTest.qWait(task_delay)
        
        # generate correct answers
        for i in range(self.dispcount):
            self.disp = random.choice(self.questions)
            self.taskarr.append(self.disp)
            self._qnsdisp.emit(self.disp,800,150)
            QtTest.QTest.qWait(showtime)
            self._qnsdisp.emit("Blank.png",800,150)
            QtTest.QTest.qWait(blanktime)

        self._qnsshowhide.emit(1) #show the answer buttons
        self.ran_ans() #randomise answer

        timeCount = 0
        while len(self.ansarr) < len(self.taskarr): #While loop to hold code till answered or time passes
            QtTest.QTest.qWait(100)
            timeCount += 1
            if timeCount == 100:
                break
            
        self.answerworkmemVerb = False
        if self.ansarr == self.taskarr: #Check if answered correctly or not
            print("Correct")
            self._counter.emit(1)
        else:
            print("Wrong")
            self._counter.emit(0)

        print("finished test")
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self.anspadarr.clear()
        self._qnsshowhide.emit(0) #hide the answer buttons

    def ran_ans(self): # Determine which right answer sequence it is and pad it to difficulty
        self.anspadarr = [self.taskarr[len(self.ansarr)]] # append right answer into array
        
        while len(self.anspadarr) != self.anscount: # pad array for displaying on answers
            self.ran_disp = random.choice(self.questions)
            if self.ran_disp not in self.anspadarr: #check for recurring values
                self.anspadarr.append(self.ran_disp)

        random.shuffle(self.anspadarr) #shuffle array around
        self._ansdisp.emit(self.anspadarr) #emit answers into buttons
        QtTest.QTest.qWait(100)
        self.answerworkmemVerb = True

    #Append answers from main.py by user to determine if values are correct + randomise next answer
    def append_ans(self,data):
        if self.answerworkmemVerb == True:
            self.ansarr.append(data)
            self.answerworkmemVerb = False
            #print(self.ansarr)
            if len(self.ansarr) < self.dispcount:
                self.ran_ans() # Run randomise answer

class workmemSpace_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _qnsshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)
    
    def __init__(self):
        super(workmemSpace_main, self).__init__()
        # Array Position to Buttons: A(Bottom),B(Right),X(Left),Y(Top),Up,Down,Left,Right,L1,R1
        self.questions = ["SpaceN.png", "SpaceE.png","SpaceS.png","SpaceW.png","SpaceNE.png","SpaceNW.png","SpaceSE.png","SpaceNW.png"]
        self.dispcount = 0
        self.anscount = 0
        self.taskarr = []
        self.anspadarr =[]
        self.ansarr = []
        self.answerworkmemSpace = False
        self.level = 0
        
    def run_task(self,count):
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self.anspadarr.clear()

        # Show center point
        self._qnsdisp.emit("Center.png",800,150) 
        QtTest.QTest.qWait(500)
        self._qnsdisp.emit("Blank.png",800,800)
        
        # Determine difficulty
        showtime = 1000
        blanktime = 1000
        if count >= 10:
            self.anscount = 10
            self.dispcount = 2
            self.level = 3
        elif count >= 5:
            self.anscount = 7
            self.dispcount = 2
            self.level = 2
        else:
            self.anscount = 5
            self.dispcount = 2
            self.level = 1
        self._level.emit(self.level)
        #Delay before questions start showing on screen
        task_delay = random.randrange(1000,3000)
        QtTest.QTest.qWait(task_delay)
        
        # generate correct answers
        for i in range(self.dispcount):
            self.disp = random.choice(self.questions)
            self.taskarr.append(self.disp)
            self._qnsdisp.emit(self.disp,600,600)
            QtTest.QTest.qWait(showtime)
            self._qnsdisp.emit("Blank.png",800,800)
            QtTest.QTest.qWait(blanktime)

        self._qnsshowhide.emit(1) #show the answer buttons
        self.ran_ans() #randomise answer

        timeCount = 0
        while len(self.ansarr) < len(self.taskarr): #While loop to hold code till answered or time passes
            QtTest.QTest.qWait(100)
            timeCount += 1
            if timeCount == 100:
                break

        self.answerworkmemSpace = False
        if self.ansarr == self.taskarr: #Check if answered correctly or not
            print("Correct")
            self._counter.emit(1)
        else:
            print("Wrong")
            self._counter.emit(0)

        print("finished test")
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self.anspadarr.clear()
        self._qnsshowhide.emit(0) #hide the answer buttons

    def ran_ans(self): # Determine which right answer sequence it is and pad it to difficulty
        self.anspadarr = [self.taskarr[len(self.ansarr)]] # append right answer into array
        
        while len(self.anspadarr) != self.anscount: # pad array for displaying on answers
            self.ran_disp = random.choice(self.questions)
            if self.ran_disp not in self.anspadarr: #check for recurring values
                self.anspadarr.append(self.ran_disp)

        random.shuffle(self.anspadarr) #shuffle array around
        self._ansdisp.emit(self.anspadarr) #emit answers into buttons
        QtTest.QTest.qWait(100)
        self.answerworkmemSpace = True

    #Append answers from main.py by user to determine if values are correct + randomise next answer
    def append_ans(self,data):
        if self.answerworkmemSpace == True:
            self.ansarr.append(data)
            #print(self.ansarr)
            self.answerworkmemSpace = False
            if len(self.ansarr) < self.dispcount:
                self.ran_ans() # Run randomise answer