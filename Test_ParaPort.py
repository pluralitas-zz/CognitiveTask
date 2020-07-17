#!/usr/bin/env python

# Emulation Tab:
#   Emulated port address:378h(888, LPT1)
#   LPT enchancement mode: SPP
# Select "Debug register trap"

# Port Settings Tab:
#   Select "Never use an interrupt"
#   Select "Enable legacy Plug and Play dection"
#   LPT Port Number:LPT1

# Ensure that the h#s USB to LPT converter in Device Manager is "LPT1"

from psychopy import parallel
import time

port = parallel.ParallelPort(address=0x0378)

# Should be able to see it in the monitor in device manager.
for i in range(10):
    port.setData(2)
    time.sleep(1)
    port.setData(0)
    time.sleep(1)
