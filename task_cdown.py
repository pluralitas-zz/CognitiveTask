from PyQt5 import QtCore, QtTest
import random

class countdown_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)

    def __init__(self):
        super(countdown_main, self).__init__()
        self.timedisp = ["cd1.png","cd2.png","cd3.png"]

    def run_cd(self,*inst):
        # Show center point
        if len(inst) > 0:
            self._qnsdisp.emit(inst[0],800,400)
        else:
            pass
        
        QtTest.QTest.qWait(4000)
        self._qnsdisp.emit("Center.png",800,150)
        QtTest.QTest.qWait(2000)
        self._qnsdisp.emit("Blank.png",800,150)
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit(self.timedisp[2],800,150)
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit(self.timedisp[1],800,150) 
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit(self.timedisp[0],800,150)
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit("Blank.png",800,150)