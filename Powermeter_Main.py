from Powermeter_Test2 import *
import numpy
import timer

global lasttime
lasttime=time.time()
start=time.time()

#while (lasttime-start)<3000 :
baseline_init=main()
print(baseline_init)
while 1:
    pedal=DAQfunc(baseline_init[0],baseline_init[1])
    print("Pedal: ")
    print(pedal)
    lasttime=time.time

    
    

