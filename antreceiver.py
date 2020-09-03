#!/usr/bin/env python3
import time
#from libAnt.drivers.serial import SerialDriver
from libAnt.drivers.usb import USBDriver
from libAnt.loggers.pcap import PcapLogger
from libAnt.node import Node
from libAnt.profiles.factory import Factory
import numpy as np

class antrcv:
    raw = np.array([])
    heartrate = np.array([])
    powermeter = np.array([])
    bl = np.zeros(2) # baseline: [power, count] for avg power calculation

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
            # if not self.bl.all(): # create initial value for accumPower
            #     self.bl[0] = self.raw[1]
            #     self.bl[1] = self.raw[4] - 1
            #     self.raw[1] = 0 #replace accum power with 0
            # else:
            #     self.bl[0] = divmod((self.raw[1] - self.bl[0]),65536)[1] #prevent overflows, take only remainder
            #     self.bl[1] = divmod((self.raw[1] - self.bl[0]),255)[1] #prevent overflows, take only remainder
            #     self.raw[1] = int(self.bl[0]/self.bl[1])

            self.powermeter = self.raw
        else:
            self.heartrate = self.raw
        
        #print(self.raw)

    def eCallback(self,e):
        print(e) #print "device is closed""

    def antacq(self):
        self.heartrate = np.array([])
        self.powermeter = np.array([])
        while True: #while loop to acquire ANT raw data input
            with Node(USBDriver(vid=0x0FCF, pid=0x1008), 'MyNode') as n:
                f = Factory(self.callback)
                n.enableRxScanMode() 
                n.start(f.parseMessage, self.eCallback) #print "USB OPENSTART""USB OPEN SUCCESS" & "USB CLOSE START" & "USB CLOSE END"
                time.sleep(1) # keep Listening for 30sec

            if (bool(self.powermeter) and bool(self.heartrate)): #break while loop if filled
                #print("broken")
                break
        
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
        print(out[0])
        print(out[1][0])