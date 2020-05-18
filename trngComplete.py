from PyQt5 import QtCore, QtTest
import random

class trngCom_main(QtCore.QThread):
    _qnsdisp = QtCore.pyqtSignal(str,int,int)

    def __init__(self):
        super(trngCom_main, self).__init__()
        
    def run_com(self,time):
        # Show center point
        self._qnsdisp.emit("Complete.png",800,400)
        QtTest.QTest.qWait(60000) 