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
        self.answers = ["FlankR.png","Blank.png","Blank.png","Blank.png",  "Blank.png","FlankL.png","Blank.png","Blank.png"  ,"Blank.png","Blank.png"]
        self.taskarr = []
        self.ansarr = []
        self.answerflank = False
        self.level = 0

    def run_task(self,count):
        self.ansarr.clear()     #clear array
        self.taskarr.clear()    #clear array

        # Show center point
        self._qnsdisp.emit("Center.png",800,150) 
        QtTest.QTest.qWait(500)
        self._qnsdisp.emit("Blank.png",800,150)

        ##Determine difficulty
        if count >= 10: 
            showtime = 500
            self.questions2 = self.questions
            self.level = 3
        elif count >=5:
            showtime = 500
            self.questions2 = self.questions[:2]
            self.level = 2
        else:
            showtime = 1000
            self.questions2 = self.questions[:2]
            self.level = 1
        self._level.emit(self.level)

        self._ansdisp.emit(self.answers) #emit answers into buttons

        #Delay before questions start showing on screen
        task_delay = random.randrange(1000,3000)
        QtTest.QTest.qWait(task_delay)

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
            if timeCount == 100:
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
        #self._qnsshowhide.emit(0) #hide the answer buttons

        #QtTest.QTest.qWait(10000) #wait between next test after everything is done

    #Append answers from main.py by user to determine if values are correct
    def append_ans(self,data):
        if self.answerflank == True:
            self.ansarr.append(data[:6])
            #print(self.ansarr)

