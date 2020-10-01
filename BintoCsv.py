import os, numpy as np
from psychopy import parallel

savepath = "C:\\Data" #data savepath
fname = "testt__2020-10-01T165452_14col_int32"
fpathin = os.path.join(savepath, fname + ".dat")
fpathout = os.path.join(savepath, fname + ".csv")
head = 'Time*1000,ElapsedTime,Deg*100,Speed,QCLeft*1000,HSLeft*1000,QCRight*1000,HSRight*1000,PPGRaw*1000,HeartRate,InstPower,AvgPower,InstCad,BalanceR' #header
comms = "Data File datatype = 'int32'\r\n1000Hz sampling rate, 10samples from DAQ for EMG(s)\r\nEncoder angle w.r.t. LEFT crank angle is synchronised to DAQ once every 10 samples(100Hz)\r\nHeart Rate Data, Pedal Data at 1 Hz\r\n\r\n" #comments

test = np.fromfile(fpathin,dtype='int32')
testlen = int(len(test)/13)
print(len(test))
print(testlen)
test = test.reshape(testlen,13)

np.savetxt(fpathout, test, delimiter=',', fmt="%d", header=comms + head) #fmt = formatting(3 decimal places float), delimiter is comma cause csv
