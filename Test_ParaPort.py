#!/usr/bin/env python

from psychopy import parallel
import time

port = parallel.ParallelPort(address=0x0278)

# Should be able to see it in the monitor in device manager.
for i in range(10):
    port.setData(2)
    port.setData(0)
    time.sleep(1)
    port.setData(1)
    port.setData(0)
    time.sleep(1)


