from PyQt5 import QtCore, QtTest
import random

class countdown_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)

    def __init__(self):
        super(countdown_main, self).__init__()
        self.timedisp = ["cd1.png","cd2.png","cd3.png"]

    def run_cd(self,*inst):
        # Show center point
        if "Inst" in inst and ".png" in inst:
            self.dispfile = inst
        else:
            self.dispfile = "Center.png"

        self._qnsdisp.emit(self.dispfile,800,150)
        QtTest.QTest.qWait(7000)
        self._qnsdisp.emit("Blank.png",800,150)
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit(self.timedisp[2],800,150)
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit(self.timedisp[1],800,150) 
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit(self.timedisp[0],800,150)
        QtTest.QTest.qWait(1000)
        self._qnsdisp.emit("Blank.png",800,150)