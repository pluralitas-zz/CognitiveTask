import serial
import binascii as ba
import numpy as np
import time
def acqenc(old,sam,enc):
   enc.flushInput()
   encraw=enc.readline(5) # read 5 btyes of data {1: 0xff, 2: 0x81, 3: 2bits high [4pos], 4: 8bits low [255pos]}
   enc.flushInput()
   #enchex=struct.unpack("h", encraw)
   enchex = ba.hexlify(encraw) #decode to ascii
   encdat = enchex.decode('utf-8').split('ff81') #convert to string from bytes and split using the 0xff81 data
   encdat2 = encdat[1] if len(encdat) == 2 else old #checker if encoder data is correct else output old
   enchigh = int((str(encdat2[0:2])),16) #split upper and change to decimals
   #print(encdat2[2:4])
   enclow = int((str(encdat2[2:4])),16) #lower
   #print(enclow)
   #print(type(encdat2))
   #print(encdat2[0:2])
   #print(encdat2[2:4])
   encdeg = round((enchigh*90) + (enclow*90/256),1) #calculate angles from encoder data
   return (encdeg,encdat2)


def SPD_Call(enc):
   #global enc 
   global SPD
   SPDarr = np.array(list())
   #SPDper_in = np.array(list())
   samp_rate = 1000 #for DAQ (Hz)
   samples = 10 #per acquisition
   period = 1/samp_rate * samples ## determines while loop sampling rate
   tcheck = time.time()
   HRcaltime = 2
   

   enc.flushInput()
   intraw = enc.readline(5)
   inthex = ba.hexlify(intraw)
   intdat = inthex.decode('utf-8')
   encold = intdat.split('ff81')
   flag =0
   while (flag ==0):
      tcheck+=period
      encdeg,encdat2 = acqenc(encold,2,enc)
      encold = encdat2 #record for use in checker

      #print(encdeg)
   
      if len(SPDarr) != 20:
         SPDarr = np.append(SPDarr,encdeg)
         
         #return 0
      else:
         SPDarrdiff = np.diff(SPDarr)
         #print(SPDarrdiff)
         SPDper_in = SPDarrdiff[np.all([SPDarrdiff>-100,SPDarrdiff<100],axis=0)]
         #print(SPDper_in)
         SPDdeg = np.sum(SPDper_in)
         SPD = int(SPDdeg/HRcaltime*60/360) #rpm
         SPDarr = np.array(list())
         SPDper_in = np.array(list())
         flag =1
         return SPD

      time.sleep(max(0,tcheck-time.time()))

if __name__ == "__main__":
    global enc
    enc = serial.Serial(port='COM6',baudrate=38400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,rtscts=True) #Optical Encoder config E1090BK25 chang chun hua te guang dian
    x=acqenc(enc)  
    print("speed")
    print(type(x))
     