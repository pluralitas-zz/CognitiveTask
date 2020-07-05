from PyQt5 import QtCore, QtTest
import random

class flank_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _qnsshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)
    
    def __init__(self):
        super(flank_main, self).__init__()
        # Array Position to Buttons: A(Bottom),B(Right),X(Left),Y(Top),Up,Down,Left,Right,L1,R1
        self.questions = ["FlankLCon.png", "FlankRCon.png","FlankLIncon.png","FlankRIncon.png"]
        self.answers = ["FlankR.png","FlankL.png"]
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
        if count >= 20:
            showtime = 300
            self.questions2 = self.questions
            self.level = 5
            self.cutofftime = 20 #multiplies of 100ms
        elif count >= 20:
            showtime = 300
            self.questions2 = self.questions
            self.level = 4
            self.cutofftime = 30 #multiplies of 100ms
        elif count >= 10:
            showtime = 500
            self.questions2 = self.questions
            self.level = 3
            self.cutofftime = 50 #multiplies of 100ms
        elif count >=5:
            showtime = 700
            self.questions2 = self.questions[:2]
            self.level = 2
            self.cutofftime = 70 #multiplies of 100ms
        else:
            showtime = 1000
            self.questions2 = self.questions[:2]
            self.level = 1
            self.cutofftime = 100 #multiplies of 100ms

        # Show Difficulty
        #self.diffdisp(self.level)
        self._level.emit(self.level)
        QtTest.QTest.qWait(2000)
        
        # Show center point
        self._qnsdisp.emit("Center.png",800,150)
        QtTest.QTest.qWait(500)
        self._qnsdisp.emit("Blank.png",800,150)

        #Delay before questions start showing on screen
        task_delay = random.randrange(1000,3000)
        QtTest.QTest.qWait(task_delay)

        #Hold task in while loop while user isnt cycling
        while self.speed < self.pausespd: 
            QtTest.QTest.qWait(100)

        self._ansdisp.emit(self.answers) #emit answers into buttons

        #Randomise and display the answer
        self.disp = random.choice(self.questions2)
        self.taskarr.append(self.disp[:6])
        #print(self.taskarr)

        self._qnsdisp.emit(self.disp,800,150)
        QtTest.QTest.qWait(showtime)
        self._qnsdisp.emit("Blank.png",800,150) #wait time from displaying the answers to actually able to answer
        

        QtTest.QTest.qWait(100) # Wait before allowing user to answer
        self.answerflank = True
        self._qnsshowhide.emit(1) #show the answer buttons
        timeCount = 0
        while len(self.ansarr) < len(self.taskarr): #While loop to hold code till answered or time passes
            QtTest.QTest.qWait(100)
            timeCount += 1
            if timeCount == self.cutofftime:
                break
        
        self.answerflank = False
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

        #QtTest.QTest.qWait(10000) #wait between next test after everything is done

    #Append answers from main.py by user to determine if values are correct
    def append_ans(self,data):
        if self.answerflank == True:
            self.ansarr.append(data[:6])
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