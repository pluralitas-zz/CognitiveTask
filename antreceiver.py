from PyQt5 import QtTest
from libAnt.drivers.usb import USBDriver
from libAnt.loggers.pcap import PcapLogger
from libAnt.node import Node
from libAnt.profiles.factory import Factory
from PyQt5 import QtTest
import numpy as np

class antrcv:
    raw = []
    heartrate = []
    powermeter = []
    
    def __init__(self):
        pass
            
    def callback(self,msg): 
        ''' PowerTap P1 = [instantaneousPower, avgPower, instantaneousCadence, pedalBalanceValue, eventCount] 
            Polar H10 = [heartRate]
        '''
        self.raw = str(msg) #Change to string
        self.raw = self.raw.split(",") #Split into array
        self.raw = [int(i) for i in self.raw] # Change to int
        if len(self.raw) == 5:
            self.powermeter = self.raw
        else:
            self.heartrate = self.raw

        # print(self.raw)

    def eCallback(self,e):
        print(e) #print "device is closed""

    def antacq(self):
        self.heartrate = []
        self.powermeter = []
        self.counter = 0
        while True: #while loop to acquire ANT raw data input
            with Node(USBDriver(vid=0x0FCF, pid=0x1008), 'MyNode') as n:
                f = Factory(self.callback)
                n.enableRxScanMode() 
                n.start(f.parseMessage, self.eCallback) #print "USB OPENSTART""USB OPEN SUCCESS" & "USB CLOSE START" & "USB CLOSE END"
                QtTest.QTest.qWait(3000) # keep Listening for 30sec

            if self.counter == 2:
                self.counter = 0
                self.heartrate = [0] 

            if (bool(self.powermeter) and bool(self.heartrate)): #break while loop if filled
                # print("broken")
                break
            else:
                self.counter +=1
        
        return [self.powermeter, self.heartrate] #return assembled data
'''
self.pedalRead[0][0] = Inst. Power
self.pedalRead[0][1] = Avg Power
self.pedalRead[0][2] = Instant Cadence
self.pedalRead[0][3] = Pedal Balance Right
self.pedalRead[1][0] = HeartRate (From Polar H10)
'''
if __name__ == "__main__":
    
    ant = antrcv()
    while True:
        out = ant.antacq()
        print("output........................................")
        print([out[1][0],out[0][0],out[0][1],out[0][2],int(round(out[0][3]))])