#!/usr/bin/env python3
from time import sleep
import time
#from libAnt.drivers.serial import SerialDriver
from libAnt.drivers.usb import USBDriver
from libAnt.loggers.pcap import PcapLogger
from libAnt.node import Node
from libAnt.profiles.factory import Factory
import csv
import os
import numpy as np

#open file
raw=[0,0,0,0,0]
fpath = os.path.join(r"C:\Users\ipich\Desktop","testfile.txt") #output file name

def callback(msg):
    global raw 
    global count
    global avgPower_baseline , baseLine_count
    #fout = open(fpath,'a+')
    raw=str(msg)
    raw=raw.split(",")
    if not avgPower_baseline:
        avgPower_baseline=raw[1]
    if not baseLine_count:
        baseLine_count = int(raw[4])-1

    accum_power = int(raw[1])-int(avgPower_baseline)
    act_count = int(raw[4])-baseLine_count

    if accum_power <0:
        avgPower_baseline = avgPower_baseline-65536
        accum_power = int(raw[1])-int(avgPower_baseline)
    if act_count < 0:
        avgPower_baseline=raw[1]
        baseLine_count = int(raw[4])-1
        accum_power = int(raw[1])-int(avgPower_baseline)
        act_count = int(raw[4])-baseLine_count

    raw[1] = '{0:.0f}'.format(accum_power/act_count)
    raw = [int(i) for i in raw]
    #raw[1] = str((int(raw[1])-int(avgPower_baseline))/(int(raw[4])-baseLine_count))
    #fout.write(x+ "\n") #append to testfile
    #fout.close()   

def eCallback(e):
    print(e) #print "device is closed""

# for serial driver
#with Node(SerialDriver("/dev/ttyUSB0"), 'MyNode') as n:
# for USB driver

def main():
    global count
    global avgPower_baseline, baseLine_count
    global raw 
    avgPower_baseline =[]
    baseLine_count = []
    output_raw = [[] for _ in range(8)]
    count = 0
    flag = True
    while flag:
        with Node(USBDriver(vid=0x0FCF, pid=0x1008), 'MyNode') as n:
            f = Factory(callback)
            n.enableRxScanMode() 
            n.start(f.parseMessage, eCallback) #print "USB OPENSTART""USB OPEN SUCCESS" & "USB CLOSE START" & "USB CLOSE END"
            sleep(1.25)  # keep Listening for 30sec
            output_raw[count][0:4] = raw
            count = count+1
            #print("Baseline")
            #print (type(output_raw))
            if (bool(avgPower_baseline) & bool(baseLine_count)):
                flag = False
               

    return [avgPower_baseline,baseLine_count]

def DAQfunc(avgPower,baseCount):
    global avgPower_baseline, baseLine_count
    global raw 
    max_count =4
    baseLine_count = baseCount
    avgPower_baseline = avgPower
    output_raw = [[] for _ in range(max_count)]
    count = 0
    while count<max_count:
        with Node(USBDriver(vid=0x0FCF, pid=0x1008), 'MyNode') as n:
            f = Factory(callback)
            n.enableRxScanMode() 
            n.start(f.parseMessage, eCallback) #print "USB OPENSTART""USB OPEN SUCCESS" & "USB CLOSE START" & "USB CLOSE END"
            sleep(1.25)  # keep Listening for 1.25sec
            raw = [int(i) for i in raw]
            output_raw[count][0:4] = raw
            count = count+1
            #print (output_raw)
            #print(type(output_raw))
    return [np.median(np.array(output_raw),axis=0),avgPower_baseline,baseLine_count]

if __name__ == "__main__": 
    y=main()
    while 1:
        pedalRead=DAQfunc(y[0],y[1])
        print(pedalRead)
         