#!/usr/bin/env python3
from time import sleep

from libAnt.drivers.serial import SerialDriver
from libAnt.drivers.usb import USBDriver
from libAnt.node import Node


def callback(msg):
    raw=str(msg)
    

    
    
    if(int(raw[6:8],16)==16):
      

        #Balance
        raw=int(raw[12:14],16)
        raw=bin(raw)
        lastBit=raw[2]
        if lastBit=='1':
            raw = int(raw[3:10],2)
            print(raw)
            print(lastBit)
 


def eCallback(e):
    print(e)

# for USB driver
while True:
    with Node(USBDriver(vid=0x0FCF, pid=0x1008), 'MyNode') as n:

    # for serial driver
    #with Node(SerialDriver("/dev/ttyUSB0"), 'MyNode') as n:
        n.enableRxScanMode()
        n.start(callback, eCallback)
        sleep(3)  # Listen for 30sec
