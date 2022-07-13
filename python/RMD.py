"""
RMD class implementation


Run command line for can interface
sudo ip link set can0 type can bitrate 1000000
sudo ip link set up can0

"""

#Python library to be intalled with ù
#requires python 3.9 >
#pip install python-can
import can
import struct
import time

class RMD:


    #init the Motor
    def __init__(self,nodeID,canbus,ratio=9):
        self.ratio = ratio
        self.nodeID = nodeID
        self.bus = canbus
        #init used variables
        self.encoderPosition = 0
        self.multiTurn = 0
        self.singleTurn = 0
        self.multiTurnG = 0
        self.singleTurnG = 0
        self.PidPosKp  = 0
        self.PidPosKi  = 0
        self.PidVelKp  = 0
        self.PidVelKi  = 0
        self.PidTrqKp  = 0
        self.PidTrqKi  = 0
        self.acceleration  = 0
        #clear all can messages in queue
        msg = self.bus.recv(0.2)
        msg = self.bus.recv(0.2)
        msg = self.bus.recv(0.2)
        msg = self.bus.recv(0.2)
        msg = self.bus.recv(0.2)
        msg = self.bus.recv(0.2)
        msg = self.bus.recv(0.2)
        msg = self.bus.recv(0.2)
        msg = self.bus.recv(0.2)

    def info(self):
        print("######### INFO ########")
        print("\tPID:")
        stringa = "\t\tPosKp/i:"+str(self.PidPosKp)+":"+str(self.PidPosKi)+"\n"
        stringa += "\t\tVelKp/i:"+str(self.PidVelKp)+":"+str(self.PidVelKi)+"\n"
        stringa += "\t\tTrqKp/i:"+str(self.PidTrqKp)+":"+str(self.PidTrqKi)+"\n"
        print(stringa)
        print("\tAcceleration:")
        print("\t\t",self.acceleration)

    def print(self):
        stringa = "#POSITION "+ str(self.nodeID) +"     RAW:" + str(self.encoderPosition) +"\t"
        stringa += "M" + "{:.2f}".format(self.multiTurn) +"\t"
        stringa += "S" + "{:.2f}".format(self.singleTurn) +"\t"
        stringa += "MG" + "{:.2f}".format(self.multiTurnG)+"\t"
        stringa += "SG" + "{:.2f}".format(self.singleTurnG)
        print(stringa)

    def get_current_theta(self):
        stringa = "#POSITION     RAW:" + str(self.encoderPosition) +"\t"
        stringa += "M" + "{:.2f}".format(self.multiTurn) +"\t"
        stringa += "S" + "{:.2f}".format(self.singleTurn) +"\t"
        stringa += "MG" + "{:.2f}".format(self.multiTurnG)+"\t"
        stringa += "SG" + "{:.2f}".format(self.singleTurnG)
        print(stringa)

    def encoderInfo(self):

        stringa = "#POSITION\n\tRAW:" + str(self.encoderPosition)
        stringa += "\n\t" + str(self.encoderOriginalPosition)
        stringa += "\n\t" + str(self.encoderOffset)
        print(stringa)


      #write and receive RAW data
    def wr(self,data):
        msg = can.Message(arbitration_id=self.nodeID,
                      data=data,
                      is_extended_id=False)
        #try to send the message on the bus
        try:
            self.bus.send(msg)
        except can.CanError:
            print("Message NOT sent")
            return (False,[])

        #read the response, no timeout on this action without arguments in the recv function
        try:
            msg = self.bus.recv(1.0)
        except:
            print("Message NOT rev")
            return (False,[22,0,0,0,0,0,0,0])
        return (True,msg.data)

    #read internal encoder position and off set
    def Fn90(self):
        data = [0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        ret = self.wr(data)
        if (ret[0]) and (ret[1][0] == 0x90):
            self.encoderPosition  = struct.unpack("<H",ret[1][2:4])[0]
            self.encoderOriginalPosition = struct.unpack("<H",ret[1][4:6])[0]
            self.encoderOffset = struct.unpack("<H",ret[1][6:8])[0]
            #print(self.encoderPosition, self.encoderOriginalPosition, self.encoderOffset)
        else:
            print("ERRORE",data)
            for el in ret[1]:
                print(el)

    #Calibrate offset to specific angle
    def Fn91(self,angle = 180):
        #Our offset is the actual original postion, shifted of 180degrees
        #180degres for this encoder are 0x8000 in hex
        #we can add the value and mod with 0x1000
        """
        We run in a stupid problem from the driver
        the offset is a unsigned value, and the output of the
        RAW after offset is always a unsigned 16bit value
        The problem raises when the multiturn is taking place
        this is because the internal system works like this:
        it "subtracts" the offset to the RAW sensor data
        but then it's used in the signed positioning value
        and it goes instead of 0 to 360
        """
        value = self.encoderOriginalPosition + 0x8000
        value = value%0x10000
        data = [0x91,0x00,0x00,0x00,0x00,0x00]
        data2 = struct.pack("<H",value)
        for el in data2:
            data.append(el)
        ret = self.wr(data)
        if (ret[0]) and (ret[1][0] == 0x91):
            self.encoderOffset = struct.unpack("<H",ret[1][6:8])[0]
            #print(self.encoderPosition, self.encoderOriginalPosition, self.encoderOffset)
        else:
            print("ERRORE",data)
            for el in ret[1]:
                print(el)

    #Calibrate offset to specific angle
    def Fn19(self):
        #Our offset is the actual original postion, shifted of 180degrees
        #180degres for this encoder are 0x8000 in hex
        #we can add the value and mod with 0x1000
        """
        We run in a stupid problem from the driver
        the offset is a unsigned value, and the output of the
        RAW after offset is always a unsigned 16bit value
        The problem raises when the multiturn is taking place
        this is because the internal system works like this:
        it "subtracts" the offset to the RAW sensor data
        but then it's used in the signed positioning value
        and it goes instead of 0 to 360
        """
        data = [0x19,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        ret = self.wr(data)
        if (ret[0]) and (ret[1][0] == 0x19):
            pass
        else:
            print("ERRORE",data)
            for el in ret[1]:
                print(el)


    #read multi run angle
    def Fn92(self):
        data = [0x92,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        ret = self.wr(data)
        if (ret[0]) and (ret[1][0] == 0x92):
            data = []
            for el in ret[1][1:]:
                data.append(el)
            data.append(data[-1])
            self.multiTurn  = struct.unpack("<q",bytes(data))[0]
            #print("multiBeforeChange",self.nodeID,self.multiTurn)
            #print(data)
            #self.multiTurn  += 18000
            self.multiTurn  /= 100
            self.multiTurnG = self.multiTurn/self.ratio
            self.multiTurnG = int(self.multiTurnG)
            print(self.multiTurnG)
        else:
            print("ERRORE",data)
            for el in ret[1]:
                print(el)

    #read single turn angle
    def Fn94(self):
        data = [0x94,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        ret = self.wr(data)
        if (ret[0]) and (ret[1][0] == 0x94):
            self.singleTurn = struct.unpack("<H",ret[1][6:8])[0]/100
            self.singleTurnG = self.singleTurn/self.ratio
            self.singleTurnG = int(self.singleTurnG)
            print("FN94",self.singleTurn)
        else:
            print("ERRORE",data)
            for el in ret[1]:
                print(el)

    #Motor OFF
    def Fn80(self):
        data = [0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        ret = self.wr(data)
        if (ret[0]) and (ret[1][0] == 0x80):
            print("Motor OFF")
        else:
            print("ERRORE",data)
            for el in ret[1]:
                print(el)

    #Motor STOP
    def Fn81(self):
        data = [0x81,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        ret = self.wr(data)
        if (ret[0]) and (ret[1][0] == 0x81):
            print("Motor STOP")
        else:
            print("ERRORE",data)
            for el in ret[1]:
                print(el)

    #read PIDs
    def Fn30(self):
        data = [0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        ret = self.wr(data)
        if (ret[0]) and (ret[1][0] == 0x30):
            print("Decode Pids")
            self.PidPosKp  = struct.unpack("B",ret[1][2:3])[0]
            self.PidPosKi  = struct.unpack("B",ret[1][3:4])[0]
            self.PidVelKp  = struct.unpack("B",ret[1][4:5])[0]
            self.PidVelKi  = struct.unpack("B",ret[1][5:6])[0]
            self.PidTrqKp  = struct.unpack("B",ret[1][6:7])[0]
            self.PidTrqKi  = struct.unpack("B",ret[1][7:8])[0]
        else:
            print("ERRORE",data)
            for el in ret[1]:
                print(el)

    #write PIDs RAM
    def Fn31(self):
        data = [0x31,0x00]
        data2 = struct.pack("BBBBBB",self.PidPosKp,self.PidPosKi,self.PidVelKp,self.PidVelKi,self.PidTrqKp,self.PidTrqKi)
        for el in data2:
            data.append(el)
        ret = self.wr(data)
        if (ret[0]) and (ret[1][0] == 0x31):
            self.PidPosKp  = struct.unpack("B",ret[1][2:3])[0]
            self.PidPosKi  = struct.unpack("B",ret[1][3:4])[0]
            self.PidVelKp  = struct.unpack("B",ret[1][4:5])[0]
            self.PidVelKi  = struct.unpack("B",ret[1][5:6])[0]
            self.PidTrqKp  = struct.unpack("B",ret[1][6:7])[0]
            self.PidTrqKi  = struct.unpack("B",ret[1][7:8])[0]
        else:
            print("ERRORE",data)
            for el in ret[1]:
                print(el)

    #read Acceleration
    def Fn33(self):
        data = [0x33,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        ret = self.wr(data)
        if (ret[0]) and (ret[1][0] == 0x33):
            self.acceleration  = struct.unpack("<l",ret[1][4:8])[0]
        else:
            print("ERRORE",data)
            for el in ret[1]:
                print(el)

    #write Acceleration RAM
    def Fn34(self):
        data = [0x34,0x00,0x00,0x00]
        data2 = struct.pack("<l",self.acceleration)
        for el in data2:
            data.append(el)
        ret = self.wr(data)
        if (ret[0]) and (ret[1][0] == 0x34):
            self.acceleration  = struct.unpack("<l",ret[1][4:8])[0]
        else:
            print("ERRORE",data)
            for el in ret[1]:
                print(el)

    #Position Velocity Cmd
    def FnA4(self,desiredPosition,maxSpeed):
        data = [0xA4,0x00]
        #self.desiredPosition = desiredPosition +18000
        self.desiredPosition = desiredPosition
        self.maxSpeed = maxSpeed
        #print("GO TO",desiredPosition,self.desiredPosition)
        data2 = struct.pack("<Hl",maxSpeed,self.desiredPosition)
        #print("SPACCEHTTA",struct.unpack("<Hl",data2))
        for el in data2:
            data.append(el)
        ret = self.wr(data)
        if (ret[0]) and (ret[1][0] == 0xA4):
            pass
        else:
            print("ERRORE",data)
            for el in ret[1]:
                print(el)

    #go to a specific position and print actual position
    def go(self,pos,speed):
        self.print()
        self.FnA4(pos*100,speed)
        for a in range(1000):
            self.Fn90()
            self.Fn92()
            self.Fn94()
            self.print()

    #go to a specific position and print actual position
    def goG(self,pos,speed):
        #self.print()
        self.FnA4(int(pos*100*self.ratio), int(speed*self.ratio))
        #for a in range(1):
        #    #self.Fn90()
        #    self.Fn92()
        #    #self.Fn94()
        #    self.print()
