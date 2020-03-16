import nidaqmx, numpy as np

class daq:
    def acqdaq(self,rate,sam):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0:4") #ai0 = PPG Digital Out, ai1:4 = EEG
            task.timing.cfg_samp_clk_timing(rate=rate, sample_mode=nidaqmx.constants.AcquisitionType.FINITE)
            raw_in = task.read(number_of_samples_per_channel=sam)
        arr_out = np.array(raw_in)
        arr_out = np.transpose(arr_out)
        return arr_out

if __name__ == "__main__":
    
    #Parameters
    samp_rate = 1000 #for DAQ (Hz)
    samples = 10 #per acquisition

    daqq = daq()
    arrdaq = daqq.acqdaq(samp_rate,samples)
    
    #print column
    col = arrdaq[:,0]
    print(col)
    test = arrdaq[:,1:]
    # print()
    print(len(test))
    comb = np.column_stack([test,col])
    print(comb)


