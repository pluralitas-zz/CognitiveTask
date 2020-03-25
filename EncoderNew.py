import serial, time

class encoder:
    #for speed calculation
    def __init__(self):
        self.encfound = True
        try:
            self.enc = serial.Serial(port='COM6',baudrate=38400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,rtscts=True) #Optical Encoder config E1090BK25 chang chun hua te guang dian   
        except:
            self.encfound = False

    @property
    def deg(self):
        if self.encfound == True:
            self.enc.flushInput()
            self.encraw=self.enc.readline(5) # read 5 btyes of data {1: 0xff, 2: 0x81, 3: 2bits high [4pos], 4: 8bits low [255pos]}
            self.enc.flushInput()
                
            self.enchigh = int.from_bytes(self.encraw[2:3], byteorder='big')
            self.enclow = int.from_bytes(self.encraw[3:4], byteorder='big')
            self.encdeg = (self.enchigh*90) + round((self.enclow*90/256),1)
        else:
            self.encdeg = 0

        return self.encdeg


    @property
    def spd(self): #average speed over a period
        self.samp_rate = 100 #sample rate (hz)
        self.samp_period = 1 #period to collect signals sec
        self.degold = self.deg
        self.degtravelled = 0
        self.timecheck = time.time()
        self.newdiff=0

        for i in range(self.samp_rate*self.samp_period):
            self.timecheck += 1/self.samp_rate
            time.sleep(max(0,self.timecheck-time.time()))
            self.degnow = self.deg
            if ((self.degold - self.degnow) > 180):
                self.newdiff = self.degnow - self.degold + 360
            elif ((self.degold - self.degnow) < -180):
                self.newdiff = self.degnow - self.degold - 360  
            else:
                self.newdiff = self.degnow - self.degold

            self.degold = self.degnow
            self.degtravelled += self.newdiff

        self.speed = int(self.degtravelled/self.samp_period*60/360) #calculate rpm
        return self.speed

if __name__ == "__main__":
    enc = encoder()
    while 1:
        print(str(enc.spd))