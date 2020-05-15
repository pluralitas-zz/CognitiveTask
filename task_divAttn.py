from PyQt5 import QtCore, QtTest
import random

# run_task(task="")
# tasks = flank, nback-verbal, nback-visual, working-verbal, working-visual

class divattn_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)
    _ansdisp = QtCore.pyqtSignal(list)
    _counter = QtCore.pyqtSignal(int)
    _qnsshowhide = QtCore.pyqtSignal(int)
    _level = QtCore.pyqtSignal(int)
    _paraport = QtCore.pyqtSignal(int)
    blankanswer = ["Blank.png","Blank.png","Blank.png","Blank.png",  "Blank.png","Blank.png","Blank.png","Blank.png"  ,"Blank.png","Blank.png"]
    qns_flank = ["FlankLCon.png", "FlankRCon.png"]
    qns_verb = ["VerbAirport.png", "VerbChurch.png","VerbHospital.png","VerbLibrary.png","VerbMarket.png","VerbPharmacy.png","VerbRestaurant.png","VerbSalon.png","VerbSchool.png","VerbStation.png"]
    qns_nbackvis = ["SpaceN.png", "SpaceE.png","SpaceS.png","SpaceW.png","SpaceNE.png","SpaceNW.png","SpaceSE.png","SpaceNW.png"]
    qns_wrkmemvis = ["SpaceN.png", "SpaceE.png","SpaceS.png","SpaceW.png","SpaceNE.png","SpaceNW.png","SpaceSE.png","SpaceNW.png"]

    def __init__(self):
        super(divattn_main, self).__init__()
        self.question = "Divattn.png"
        self.taskarr = []
        self.ansarr = []
        self.answerdivattn = False
        self.level = 0
        self.speed = 0
        self.pausespd = 10

    def run_task(self,count,**tskname):
        self.ansarr.clear()     #clear array
        self.taskarr.clear()

        # randomise where the self.question image is going to show on self.answers
        qnsloc = random.randrange(0,9)
        self.answers = self.blankanswer.copy() #.copy() to prevent linkage which changes both variables.
        
        self.answers[qnsloc] = self.question
        self.taskarr.append(self.question)

        
        self._level.emit(99)
        ##Determine difficulty
        if count >= 10:
            waittime = 200
        else:
            waittime = 500
        
        # Optional displaying of "Tasks" to fake other tasks.
        if 'task' in tskname.keys():
            # Show center point
            self._qnsdisp.emit("Center.png",800,150)
            QtTest.QTest.qWait(500)
            self._qnsdisp.emit("Blank.png",800,150)

            #Delay before questions start showing on screen
            task_delay = random.randrange(1000,3000)
            QtTest.QTest.qWait(task_delay)

            #Show selective fake task
            if tskname['task'] == "flank":
                self._qnsdisp.emit(random.choice(self.qns_flank),800,150)
            elif tskname['task'] == "nback-verbal" or tskname['task'] == "working-verbal":
                self._qnsdisp.emit(random.choice(self.qns_verb),800,150)
            elif tskname['task'] == "nback-visual":
                self._qnsdisp.emit(random.choice(self.qns_nbackvis),800,150)
            elif tskname['task'] == "working-visual":
                self._qnsdisp.emit(random.choice(self.qns_wrkmemvis),800,150)
            else:
                self._qnsdisp.emit("Blank".png,800,150)

            QtTest.QTest.qWait(500)
            self._qnsdisp.emit("Blank.png",800,150) 

        #Delay before questions start showing on screen
        QtTest.QTest.qWait(100)
        

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