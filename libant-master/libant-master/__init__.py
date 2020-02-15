from libAnt.core import lazyproperty
from libAnt.profiles.profile import ProfileMessage
#python setup.py install
#python Powermeter_Test.py

class PowerProfileMessage(ProfileMessage):
    """ Message from Power Meter """

    maxAccumulatedPower = 65536
    maxEventCount = 256

    def __str__(self):
        if self.dataPageNumber == 16 :   #Frances
            
            #return super().__str__() + ' P: {0:.0f}W '.format(self.instantaneousPower) + ' AvgP: {0:.0f}W '.format(self.averagePower) + ' Cadence: {0:.0f}rpm '.format(self.instantaneousCadence) + self.pedalBalanceRightLeft + '_Balance: '+ self.pedalBalanceValue
            return '{0:.0f}'.format(self.instantaneousPower)  #self.instantaneousCadence 
        else: #data page 0X13    #Frances
            return super().__str__() + ' LTorque: {0:.0f}N '.format(self.LeftTorqueEffectiveness) + ' RTorque: {0:.0f}N '.format(self.RightTorqueEffectiveness) 

    @lazyproperty
    def dataPageNumber(self):
        """
        :return: Data Page Number (int)
        """
        return self.msg.content[0]

    @lazyproperty
    def eventCount(self):
        """
        The update event count field is incremented each time the information in the message is updated.
        There are no invalid values for update event count.
        The update event count in this message refers to updates of the standard Power-Only main data page (0x10)
        :return: Power Event Count
        """
        return self.msg.content[1]
    @lazyproperty   #Frances
    def LeftTorqueEffectiveness(self): # 1/2% unit (range: 0-100%) for data page 0X13
        return self.msg.content[2]
    
    @lazyproperty   #Frances
    def RightTorqueEffectiveness(self): # 1/2% unit (range: 0-100%) for data page 0X13
        return self.msg.content[3]
    
    @lazyproperty   #Frances
    def LeftPedalSmoothness(self): # 1/2% unit (range: 0-100%) for data page 0X13
        return self.msg.content[4]
    
    @lazyproperty   #Frances
    def RightPedalSmoothness(self): # 1/2% unit (range: 0-100%) for data page 0X13
        return self.msg.content[5]

    @lazyproperty
    def instantaneousCadence(self):
        """
        The instantaneous cadence field is used to transmit the pedaling cadence recorded from the power sensor.
        This field is an instantaneous value only; it does not accumulate between messages.
        :return: Instantaneous Cadence (W)
        """
        return self.msg.content[3]
    
    @lazyproperty   #Frances
    def pedalBalanceValue(self):
        int_x = int(self.msg.content[2])
        cBinary =bin(int_x)
        cBinary_remove0b=cBinary[3:]

        cBinary2=int(cBinary_remove0b,2)
        Result=str(cBinary2/255 *100)
        return Result

    @lazyproperty   #Frances
    def pedalBalanceRightLeft(self):
        int_x = int(self.msg.content[2])
        cBinary=bin(int_x)

        #determine Right/Left Pedal by LefttMost Bit
        if cBinary[2] == "1":
            return "R"

        elif cBinary[2]== "0":
            return "L"

        else:
            return "Invalid number"
                
    @lazyproperty
    def accumulatedPower(self):
        """
        Accumulated power is the running sum of the instantaneous power data and is incremented at each update
        of the update event count. The accumulated power field rolls over at 65.535kW.
        :return:
        """
        return (self.msg.content[5] << 8) | self.msg.content[4]

    @lazyproperty
    def instantaneousPower(self):
        """ Instantaneous power (W) """
        return (self.msg.content[7] << 8) | self.msg.content[6]

    @lazyproperty
    def accumulatedPowerDiff(self):
        if self.previous is None:
            return None
        elif self.accumulatedPower < self.previous.accumulatedPower:
            # Rollover
            return (self.accumulatedPower - self.previous.accumulatedPower) + self.maxAccumulatedPower
        else:
            return self.accumulatedPower - self.previous.accumulatedPower

    @lazyproperty
    def eventCountDiff(self):
        if self.previous is None:
            return None
        elif self.eventCount < self.previous.eventCount:
            # Rollover
            return (self.eventCount - self.previous.eventCount) + self.maxEventCount
        else:
            return self.eventCount - self.previous.eventCount

    @lazyproperty
    def averagePower(self):
        """
        Under normal conditions with complete RF reception, average power equals instantaneous power.
        In conditions where packets are lost, average power accurately calculates power over the interval
        between the received messages
        :return: Average power (Watts)
        """
        if self.previous is None:
            return self.instantaneousPower
        if self.eventCount == self.previous.eventCount:
            return self.instantaneousPower
        return self.accumulatedPowerDiff / self.eventCountDiff
