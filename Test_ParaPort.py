#!/usr/bin/env python

from psychopy import parallel
import time

port = parallel.ParallelPort(address=0x0278)

# Should be able to see it in the monitor in device manager.
port.setData(200)
port.setData(0)
'''
with parallel.ParallelPort(address=0x0278) as port:
    port.setData(200)
    port.setData(0)
'''