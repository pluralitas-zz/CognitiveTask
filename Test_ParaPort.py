#!/usr/bin/env python

from psychopy import parallel
import time

# JCCOCC
port = parallel.ParallelPort(address=0x3EFC) #JCCOCC

# Should be able to see it in the monitor in device manager.
for i in range(30):
    port.setData(69)
    time.sleep(1)
    port.setData(0)
    time.sleep(1)
'''
with parallel.ParallelPort(address=0x0278) as port:
    port.setData(200)
    port.setData(0)
'''