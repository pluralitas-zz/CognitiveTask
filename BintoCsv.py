import os, numpy as np
from psychopy import parallel

col = 13
datatype = 'uint16'
fname = "Test__2020-10-02T061059_13col_uint16"


savepath = "C:\\Data" #data savepath
fpathin = os.path.join(savepath, fname + ".dat")
fpathout = os.path.join(savepath, fname + ".csv")
head = 'Time*1000,ElapsedTime,Deg*10,Speed,QCLeft*1000,HSLeft*1000,QCRight*1000,HSRight*1000,PPGRaw*1000,HeartRate,InstPower,AvgPower,InstCad,BalanceR' #header
comms = "Data File datatype = 'uint16'\r\n1000Hz sampling rate, 10samples from DAQ for EMG(s)\r\nEncoder angle w.r.t. LEFT crank angle is synchronised to DAQ once every 10 samples(100Hz)\r\nHeart Rate Data, Pedal Data at 1 Hz\r\n\r\n" #comments



test = np.fromfile(fpathin,dtype=datatype)
testlen = int(len(test)/col)
print(len(test))
print(testlen)
test = test.reshape(testlen,col)

np.savetxt(fpathout, test, delimiter=',', fmt="%d", header=comms + head) #fmt = formatting(3 decimal places float), delimiter is comma cause csv
