# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WidGraphVideoItem.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
import sys
import os
import random
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimediaWidgets, QtMultimedia
import main

class MainWid(QtWidgets.QWidget):
    def __init__(self,parent):
        self.playstate = 0
        self.videos = "Videos" #location of videos relative to main.py
        self.vidd = os.path.join(os.getcwd(),self.videos) # actual path of folders
        self.vidFile = [files for files in os.listdir(vidd) if files.endswith(".mp4")] #find all video files in video folder
        super(MainWid,self).__init__(parent)

        self.setupUi(self)
        self.vidScene = QtWidgets.QGraphicsScene(self)
        self.graphView = QtWidgets.QGraphicsView(self.vidScene)
        self.graphView.setGeometry(QtCore.QRect(0,0,800,450))
        self.graphView.setStyleSheet("background-color: rgba(0,0,0,0); color:rgb(0,255,0)")
        self.graphView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.graphView.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)
        self.graphView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphView.setAutoFillBackground(False)
        
        self.vidFrame = QtMultimediaWidgets.QGraphicsVideoItem()
        self.vidScene.addItem(self.vidFrame)
        self.vidPlayer = QtMultimedia.QMediaPlayer(self,QtMultimedia.QMediaPlayer.VideoSurface)
        self.vidPlayer.stateChanged.connect(self.on_stateChanged)
        self.vidPlayer.setVideoOutput(self.vidFrame)
        self.graphView.fitInView(self.vidFrame,QtCore.Qt.KeepAspectRatio)
        
        file = os.path.join(self.vidd, random.choice(self.vidFile))
        self.vidPlayer.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file)))
        self.parent = parent
        #self.vidPlayer.stop()
        #self.button = QtWidgets.QPushButton("Play")
        #self.button.clicked.connect(lambda:self.startVid())
        
        #Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.graphView)
        #layout.addWidget(self.button)   

    def restartVid(self):
        self.vidPlayer.stop()
        file = os.path.join(os.path.dirname(__file__), random.choice(self.vidFile))
        self.vidPlayer.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file)))
        self.vidPlayer.play()
        self.graphView.fitInView(self.vidFrame,QtCore.Qt.KeepAspectRatioByExpanding)

    def pauseVid(self):
        if self.playstate == 1:
            self.vidPlayer.pause()

    def startVid(self):
        if self.playstate == 2:
            self.vidPlayer.play()
            self.graphView.fitInView(self.vidFrame,QtCore.Qt.KeepAspectRatioByExpanding)
        elif self.playstate == 0:
            file = os.path.join(os.path.dirname(__file__), random.choice(self.vidFile))
            self.vidPlayer.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file)))
            self.vidPlayer.play()
            self.graphView.fitInView(self.vidFrame,QtCore.Qt.KeepAspectRatioByExpanding)
        else:
            pass

    def setupUi(self, MainWin):
        MainWin.setObjectName("MainWin")
        MainWin.resize(1600, 900)

        self.retranslateUi(MainWin)
        QtCore.QMetaObject.connectSlotsByName(MainWin)

    def retranslateUi(self, MainWin):
        _translate = QtCore.QCoreApplication.translate
        MainWin.setWindowTitle(_translate("MainWin", "Cognitive"))

    @QtCore.pyqtSlot(QtMultimedia.QMediaPlayer.State)
    def on_stateChanged(self, state):
        print(state)
        self.playstate = state
        if state == QtMultimedia.QMediaPlayer.PlayingState:
            self.graphView.fitInView(self.vidFrame, QtCore.Qt.KeepAspectRatioByExpanding)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    w = MainWid()
    w.show()
    #w.startVid()
    sys.exit(app.exec_())