from PyQt5 import QtCore, QtGui, QtWidgets, QtTest, QtMultimedia, QtMultimediaWidgets
import random, sys, time

class countdown_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)

    def __init__(self):
        super(countdown_main, self).__init__()
        self.timedisp = ["cd1.png","cd2.png","cd3.png"]

    def run_cd(self,time):
        # Show center point
        self._qnsdisp.emit("Center.png",800,150) 
        QtTest.QTest.qWait((time-3)*1000)
        self._qnsdisp.emit(self.timedisp[2],800,150)
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit(self.timedisp[1],800,150) 
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit(self.timedisp[0],800,150)
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit("Blank.png",800,150)