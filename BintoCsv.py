import os, numpy as np
# from psychopy import parallel


col = 13
datatype = 'uint16'
savepath = "C:\\Users\\CyclingSystem\\OneDrive - The Chinese University of Hong Kong\\MCI Cycling\\Data Evaluation\\D\\DTC062" #data savepath

files=[]
for root, dirnames, filenames in os.walk(savepath, topdown=True):
    for file in filenames:
        if file.endswith('.dat'):
            files.append(os.path.join(root,file))

for i in range(len(files)):

    fpathin = files[i]#os.path.join(savepath, fname + ".dat")
    fpathout = files[i][:-4] + ".csv" #os.path.join(savepath, fname + ".csv")
    head = 'Time*1000,ElapsedTime,Deg*10,Speed,QCLeft*1000,HSLeft*1000,QCRight*1000,HSRight*1000,HeartRate,InstPower,AvgPower,InstCad,Balance' #header
    comms = "Data File datatype = 'uint16'\r\n1000Hz sampling rate, 10samples from DAQ for EMG(s)\r\nEncoder angle w.r.t. LEFT crank angle is synchronised to DAQ once every 10 samples(100Hz)\r\nBalance is R if more than 128, else Balance = L. 100% = L% + R%\r\nHeart Rate Data, Pedal Data at 1 Hz\r\n\r\n" #comments

    # if "task" in fname:
    #     test = np.fromfile(fpathin,dtype=np.str)
    #     print(len)
    # else:
    test = np.fromfile(fpathin,dtype=datatype)
    testlen = int(len(test)/col)
    print(len(test))
    print(testlen)
    test = test.reshape(testlen,col)

    np.savetxt(fpathout, test, delimiter=',', fmt="%d", header=comms + head) #fmt = formatting(3 decimal places float), delimiter is comma cause csv
