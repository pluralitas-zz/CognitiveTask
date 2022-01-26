from PyQt5 import QtCore, QtTest
import random

class workmemVerb_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _ansshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)

    def __init__(self):
        super(workmemVerb_main, self).__init__()
        # Array Position to Buttons: A(Bottom),B(Right),X(Left),Y(Top),Up,Down,Left,Right,L1,R1
        self.questions = ["VerbAirport.png", "VerbChurch.png","VerbHospital.png","VerbLibrary.png","VerbMarket.png","VerbPharmacy.png","VerbRestaurant.png","VerbSalon.png","VerbSchool.png","VerbStation.png"]
        self.blankans = ["Blank.png","Blank.png","Blank.png","Blank.png"]
        self.dispcount = 0
        self.anscount = 0
        self.taskarr = []
        self.anspadarr =[]
        self.ansarr = []
        self.anstimelim = 10
        self.answerworkmemVerb = False
        self.level = 0
        self.speed = 0
        self.pausespd = 10
        
    def run_task(self,count):
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self.anspadarr.clear()
        self._ansdisp.emit(self.blankans)

        # Determine difficulty
        blanktime = 1000
        if count >= 80:
            self.anscount = 4
            self.dispcount = 7
            self.level = 10
            self.anstimelim = 25
            showtime = 500
        elif count >= 70:
            self.anscount = 4
            self.dispcount = 7
            self.level = 9
            self.anstimelim = 30
            showtime = 700
        elif count >= 60:
            self.anscount = 4
            self.dispcount = 6
            self.level = 8
            self.anstimelim = 25
            showtime = 700
        elif count >= 50:
            self.anscount = 4
            self.dispcount = 5
            self.level = 7
            self.anstimelim = 20
            showtime = 700
        elif count >= 40:
            self.anscount = 4
            self.dispcount = 4
            self.level = 6
            self.anstimelim = 15
            showtime = 700
        elif count >= 30:
            self.anscount = 4
            self.dispcount = 4
            self.level = 5
            self.anstimelim = 15
            showtime = 700
        elif count >= 20:
            self.anscount = 4
            self.dispcount = 3
            self.level = 4
            self.anstimelim = 15
            showtime = 700
        elif count >= 10:
            self.anscount = 2
            self.dispcount = 3
            self.level = 3
            self.anstimelim = 10
            showtime = 1000
        elif count >= 5:
            self.anscount = 2
            self.dispcount = 2
            self.level = 2
            self.anstimelim = 10
            showtime = 1000
        else:
            self.anscount = 2
            self.dispcount = 2
            self.level = 1
            self.anstimelim = 10
            showtime = 1500

        self._level.emit(self.level) 
        self._paraport.emit(20) #Task 2
        QtTest.QTest.qWait(2000)

        # Show center point
        self._qnsdisp.emit("Center.png",800,150) 
        QtTest.QTest.qWait(500)
        self._qnsdisp.emit("Blank.png",800,150)

        # Delay before questions start showing on screen
        task_delay = random.randrange(1000,3000)
        QtTest.QTest.qWait(task_delay)

        # hold task in while loop while user isnt cycling
        while self.speed < self.pausespd: 
            QtTest.QTest.qWait(1000)
        
        # generate correct answers
        while len(self.taskarr) < self.dispcount:
            self.disp = random.choice(self.questions)
            if self.disp not in self.taskarr:
                self.taskarr.append(self.disp)
                self._qnsdisp.emit(self.disp,800,150)
                self._paraport.emit(21)
                QtTest.QTest.qWait(showtime)
                self._qnsdisp.emit("Blank.png",800,150)
                QtTest.QTest.qWait(blanktime)

        self._ansshowhide.emit(1) #show the answer buttons
        self.ran_ans() #randomise answer

        timeCount = 0
        while len(self.ansarr) < len(self.taskarr): #While loop to hold code till answered or time passes
            QtTest.QTest.qWait(100)
            timeCount += 1
            if timeCount == (self.anstimelim*10):
                break

        self.answerworkmemVerb = False

        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self.anspadarr.clear()
        self._ansshowhide.emit(0) #hide the answer buttons

    def ran_ans(self): # Determine which right answer sequence it is and pad it to difficulty
        self.anspadarr = [self.taskarr[len(self.ansarr)]] # append right answer into array
        while len(self.anspadarr) != self.anscount: # pad array for displaying on answers
            self.ran_disp = random.choice(self.questions)
            if self.ran_disp not in self.anspadarr: #check for recurring values
                self.anspadarr.append(self.ran_disp)

        random.shuffle(self.anspadarr) #shuffle array around
        self._ansdisp.emit(self.anspadarr) #emit answers into buttons
        self._paraport.emit(23)
        QtTest.QTest.qWait(100)
        self._ansshowhide.emit(1) #show the answer buttons
        self.answerworkmemVerb = True

    #Append answers from main.py by user to determine if values are correct + randomise next answer
    def append_ans(self,data):
        if self.answerworkmemVerb == True:
            self._ansdisp.emit(self.blankans)
            self.ansarr.append(data)

            if data == self.taskarr[len(self.ansarr)-1]: #Check if answered correctly or not
                # print("Correct")
                self._counter.emit(1)
                self._paraport.emit(25)
            else:
                # print("Wrong")
                self._counter.emit(0)
                self._paraport.emit(26)
    
            self.answerworkmemVerb = False
            if len(self.ansarr) < self.dispcount:
                self.ran_ans() # Run randomise answer

    def current_speed(self,data,data2):
        self.speed = data
        self.pausespd = data2

    def diffdisp(self,numb):
        numb = abs(numb)
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
        elif numb is 6:
            self._qnsdisp.emit("cd6.png",800,150)
        elif numb is 7:
            self._qnsdisp.emit("cd7.png",800,150)  
        elif numb is 8:
            self._qnsdisp.emit("cd8.png",800,150)
        elif numb is 9:
            self._qnsdisp.emit("cd9.png",800,150)
        elif numb is 10:
            self._qnsdisp.emit("cd10.png",800,150)              
        else:
            pass


class workmemSpace_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _ansshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)

    def __init__(self):
        super(workmemSpace_main, self).__init__()
        # Array Position to Buttons: A(Bottom),B(Right),X(Left),Y(Top),Up,Down,Left,Right,L1,R1
        self.questions = ["SpaceN.png", "SpaceE.png","SpaceS.png","SpaceW.png","SpaceNE.png","SpaceNW.png","SpaceSE.png","SpaceNW.png"]
        self.blankans = ["Blank.png","Blank.png","Blank.png","Blank.png"]
        self.dispcount = 0
        self.anscount = 0
        self.taskarr = []
        self.anspadarr =[]
        self.ansarr = []
        self.anstimelim = 10
        self.answerworkmemSpace = False
        self.level = 0
        self.speed = 0
        self.pausespd = 10
        
    def run_task(self,count):
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self.anspadarr.clear()
        self._ansdisp.emit(self.blankans)

        # Determine difficulty            
        blanktime = 1000
        if count >= 80:
            self.anscount = 4
            self.dispcount = 7
            self.level = 10
            self.anstimelim = 25
            showtime = 500
        elif count >= 70:
            self.anscount = 4
            self.dispcount = 7
            self.level = 9
            self.anstimelim = 30
            showtime = 700
        elif count >= 60:
            self.anscount = 4
            self.dispcount = 6
            self.level = 8
            self.anstimelim = 25
            showtime = 700
        elif count >= 50:
            self.anscount = 4
            self.dispcount = 5
            self.level = 7
            self.anstimelim = 20
            showtime = 700
        elif count >= 40:
            self.anscount = 4
            self.dispcount = 4
            self.level = 6
            self.anstimelim = 15
            showtime = 700
        elif count >= 30:
            self.anscount = 4
            self.dispcount = 4
            self.level = 5
            self.anstimelim = 15
            showtime = 700
        elif count >= 20:
            self.anscount = 4
            self.dispcount = 3
            self.level = 4
            self.anstimelim = 15
            showtime = 700
        elif count >= 10:
            self.anscount = 2
            self.dispcount = 3
            self.level = 3
            self.anstimelim = 10
            showtime = 1000
        elif count >= 5:
            self.anscount = 2
            self.dispcount = 2
            self.level = 2
            self.anstimelim = 10
            showtime = 1000
        else:
            self.anscount = 2
            self.dispcount = 2
            self.level = 1
            self.anstimelim = 10
            showtime = 1500

        self._level.emit(self.level)
        self._paraport.emit(30) #Task 3
        QtTest.QTest.qWait(2000)

        # Show center point
        self._qnsdisp.emit("Center.png",800,150) 
        QtTest.QTest.qWait(500)
        self._qnsdisp.emit("Blank.png",800,150)
        
        # Delay before questions start showing on screen
        task_delay = random.randrange(1000,3000)
        QtTest.QTest.qWait(task_delay)

        # hold task in while loop while user isnt cycling
        while self.speed < self.pausespd: 
            QtTest.QTest.qWait(1000)
        
        # generate correct answers
        while len(self.taskarr) < self.dispcount:
            self.disp = random.choice(self.questions)
            if self.disp not in self.taskarr:
                self.taskarr.append(self.disp)
                self._qnsdisp.emit(self.disp,500,500)
                self._paraport.emit(31)
                QtTest.QTest.qWait(showtime)
                self._qnsdisp.emit("Blank.png",800,150)
                QtTest.QTest.qWait(blanktime)
        self._ansshowhide.emit(1) #show the answer buttons
        self.ran_ans() #randomise answer

        timeCount = 0
        while len(self.ansarr) < len(self.taskarr): #While loop to hold code till answered or time passes
            QtTest.QTest.qWait(100)
            timeCount += 1
            if timeCount == (self.anstimelim*10):
                break

        self.answerworkmemSpace = False

        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array
        self.anspadarr.clear()
        self._ansshowhide.emit(0) #hide the answer buttons

    def ran_ans(self): # Determine which right answer sequence it is and pad it to difficulty
        
        self.anspadarr = [self.taskarr[len(self.ansarr)]] # append right answer into array
        while len(self.anspadarr) != self.anscount: # pad array for displaying on answers
            self.ran_disp = random.choice(self.questions)
            if self.ran_disp not in self.anspadarr: #check for recurring values
                self.anspadarr.append(self.ran_disp)

        random.shuffle(self.anspadarr) #shuffle array around
        self._ansdisp.emit(self.anspadarr) #emit answers into buttons
        self._paraport.emit(33)
        QtTest.QTest.qWait(100)
        self._ansshowhide.emit(1) #show the answer buttons
        self.answerworkmemSpace = True

    #Append answers from main.py by user to determine if values are correct + randomise next answer
    def append_ans(self,data):
        if self.answerworkmemSpace == True:
            self.ansarr.append(data)
            self._ansdisp.emit(self.blankans)

            if data == self.taskarr[len(self.ansarr)-1]: #Check if answered correctly or not
                # print("Correct")
                self._counter.emit(1)
                self._paraport.emit(35)
            else:
                # print("Wrong")
                self._counter.emit(0)
                self._paraport.emit(36)
    
            self.answerworkmemSpace = False
            if len(self.ansarr) < self.dispcount:
                self.ran_ans() # Run randomise answer

    def current_speed(self,data,data2):
        self.speed = data
        self.pausespd = data2

    def diffdisp(self,numb):
        numb = abs(numb)
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
        elif numb is 6:
            self._qnsdisp.emit("cd6.png",800,150)
        elif numb is 7:
            self._qnsdisp.emit("cd7.png",800,150)  
        elif numb is 8:
            self._qnsdisp.emit("cd8.png",800,150)
        elif numb is 9:
            self._qnsdisp.emit("cd9.png",800,150)
        elif numb is 10:
            self._qnsdisp.emit("cd10.png",800,150)              
        else:
            pass