import socket
import pickle
import copy
import struct
import time

"""
HOM
- Homing Method (p. 58) selection
- Feed Rate
- Max Velocity
- Jog Velocity (≤ Max. Velocity)
- Max. Acceleration
- Set DI 7 “Enable”
- “Ready” signal at DO 1
- No "Active" signal at DO 2
- No "Error" signal at DO 5
REL, ARO, ADR, ROT
- Feed Rate
- Max Velocity
- Jog Velocity (≤ Max. Velocity)
- Max. Acceleration
- Set DI 7 “Enable”
- “Ready” signal at DO 1
- No "Active" signal at DO 2
- No "Error" signal at DO 5
ABS, APS
- Available Stroke - from SettingFile
- Feed Rate        - from SettingFile
- Max Velocity     - from SettingFile
- Jog Velocity (≤ Max. Velocity)
- Max. Acceleration
- Set DI 7 “Enable”
- “Ready” signal at DO 1
- No "Active" signal at DO 2
- No "Error" signal at DO 5
"""
tipoConverter = {"uint8":"B","uint16":"<H","uint32":"<I","int8":"b","int16":"<h","int32":"<l","float":"<f"}
CameraServerPort = 502

homeSpeed = 50
homeAcceleration = 200
homeType = 17
maxSpeed = 140 #Looks like 140 is the fastest we can without "arm"
maxAcceleration = 400 #400 works good

class MTG:
    def __init__(self, serverip, port):
        #Create and connect to socket to Camera server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = (serverip, port)
        try:
            self.sock.connect(server_address)
        except socket.error:
            print("open socketError")
            return 
        print("Connection Open")
        self.sock.settimeout(15)
        self.cwset()
        self.swrefresh()
    
    def run(self):
        while True:
            pass

    def referenced(self):
        ret = self.MTG_reqres(0x2014, 0, "uint32")
        if ret == None:
            return False
        if ret & 0x1:
            return True
        else:
            return False
    
    def errorCode(self):
        return self.MTG_reqres(0x603F, 0, "uint16")
    
    def temperature(self):
        return self.MTG_reqres(0x2013, 0, "float")

    def getPosition(self):
        return self.MTG_reqres(0x6064, 0, "int32")
    def swrefresh(self):
        data = self.MTG_reqres(0x6041, 0, "uint16") #Read Object Dictionary 6041 Status Word that is unsigned int 16
        if data == None:
            return False
        # Turn data from array 2 byte litte endian
        self.dataIn = data
        self.statusWord = {}
        #0 ready to switch on
        self.statusWord["rtso"] = (data & 0x1) ==  0x01
        #1 Sitched On
        self.statusWord["so"]   = (data & 0x2) ==  0x2
        #2 Operation Enabled
        self.statusWord["oe"]   = (data & 0x4) ==  0x4
        #3 Fault
        self.statusWord["f"]    = (data & 0x8) ==  0x8
        #4 Voltage Enable
        self.statusWord["ve"]   = (data & 0x10) ==  0x10
        #5 QuickStop
        self.statusWord["qs"] = (data & 0x20) ==  0x20
        #6 Switch On Disable 
        self.statusWord["sod"] = (data & 0x40) ==  0x40
        #7 Warning
        self.statusWord["w"] = (data & 0x80) ==  0x80
        #8 Manufacturer Specific 1
        self.statusWord["ms1"] = (data & 0x100) ==  0x100
        #9 Remote
        self.statusWord["rm"] = (data & 0x200) ==  0x200
        #10 Target Reached
        self.statusWord["tr"] = (data & 0x400) ==  0x400
        #11 Internal Limit Active
        self.statusWord["ila"] = (data & 0x800) ==  0x800
        #12 Operation Mode Specific 1
        self.statusWord["oms1"] = (data & 0x1000) ==  0x1000
        #13 Operation Mode Specific 2
        self.statusWord["oms2"] = (data & 0x2000) ==  0x2000
        #14 Manufacturer Specific 2
        self.statusWord["ms2"] = (data & 0x4000) ==  0x4000
        #15 Manufacturer Specific 3
        self.statusWord["ms3"] = (data & 0x8000) ==  0x8000
        return True

    def cwset(self, so = False, ev = False, qs = False, eo = False, oms1 = False, oms2 = False,  oms3 = False, fr = False, h = False, oms4 = False, r = False, ms1 = False, ms2 = False, ms3 = False, ms4 = False, ms5 = False):
        self.cwdata  = 0
        self.controlWord = {}
        #0 Switch On
        self.controlWord["so"] = so
        self.cwdata  += so * 0x1
        #1 Enable Voltage
        self.controlWord["ev"] = ev
        self.cwdata  += ev * 0x2
        #2 Quick Stop
        self.controlWord["qs"] = qs
        self.cwdata  += qs * 0x4
        #3 Enable Operation
        self.controlWord["eo"] = eo
        self.cwdata  += eo * 0x8
        #4 Mode specific 1
        self.controlWord["oms1"] = oms1
        self.cwdata  += oms1 * 0x10
        #5 Mode specific 2
        self.controlWord["oms2"] = oms2
        self.cwdata  += oms2 * 0x20
        #6 Mode specific 3
        self.controlWord["oms3"] = oms3
        self.cwdata  += oms3 * 0x40
        #7 Fault Reset
        self.controlWord["fr"] = fr
        self.cwdata  += fr * 0x80
        #8 Halt
        self.controlWord["h"] = h
        self.cwdata  += h * 0x100
        #9 Mode specific 4
        self.controlWord["oms4"] = oms4
        self.cwdata  += oms4 * 0x200
        #10 Reserver
        self.controlWord["r"] = r
        self.cwdata  += r * 0x400
        #11 Manufacturer Specific 1
        self.controlWord["ms1"] = ms1
        self.cwdata  += ms1 * 0x800
        #12 Manufacturer Specific 2
        self.controlWord["ms2"] = ms2
        self.cwdata  += ms2 * 0x1000
        #13 Manufacturer Specific 3
        self.controlWord["ms3"] = ms3
        self.cwdata  += ms3 * 0x2000
        #14 Manufacturer Specific 4
        self.controlWord["ms4"] = ms4
        self.cwdata  += ms4 * 0x4000
        #15 Manufacturer Specific 5
        self.controlWord["ms5"] = ms5
        self.cwdata  += ms5 * 0x8000
        #Save packet data
        self.cwdataOut = struct.pack("<H",self.cwdata)

    def cwwrite(self):
        self.cwdata  = 0
        #0 Switch On
        self.cwdata  += self.controlWord["so"] * 0x1
        #1 Enable Voltage
        self.cwdata  += self.controlWord["ev"] * 0x2
        #2 Quick Stop
        self.cwdata  += self.controlWord["qs"] * 0x4
        #3 Enable Operation
        self.cwdata  += self.controlWord["eo"] * 0x8
        #4 Mode specific 1
        self.cwdata  += self.controlWord["oms1"] * 0x10
        #5 Mode specific 2
        self.cwdata  += self.controlWord["oms2"] * 0x20
        #6 Mode specific 3
        self.cwdata  += self.controlWord["oms3"] * 0x40
        #7 Fault Reset
        self.cwdata  += self.controlWord["fr"] * 0x80
        #8 Halt
        self.cwdata  += self.controlWord["h"] * 0x100
        #9 Mode specific 4
        self.cwdata  += self.controlWord["oms4"] * 0x200
        #10 Reserver
        self.cwdata  += self.controlWord["r"] * 0x400
        #11 Manufacturer Specific 1
        self.cwdata  += self.controlWord["ms1"] * 0x800
        #12 Manufacturer Specific 2
        self.cwdata  += self.controlWord["ms2"] * 0x1000
        #13 Manufacturer Specific 3
        self.cwdata  += self.controlWord["ms3"] * 0x2000
        #14 Manufacturer Specific 4
        self.cwdata  += self.controlWord["ms4"]  * 0x4000
        #15 Manufacturer Specific 5
        self.cwdata  += self.controlWord["ms5"] * 0x8000
        return self.MTG_reqres(0x6040, 0, "uint16", self.cwdata) #Read Object Dictionary 6041 Status Word that is unsigned int 16   


    
    def close(self):
        self.sock.close()
        

    def tipoPack(self, value, tipo):
        return struct.pack(tipoConverter[tipo],value)

    def tipoUnpack(self, data,tipo):
        return struct.unpack(tipoConverter[tipo],data)[0]

    def MTG_request(self, obj,idx,tipo,writeData = None ):
        #bj += 1
        buffer = [0,0,0,0,0]
        readSize = 0
        writeSize = 0
        if writeData != None:
            writeBuffer = self.tipoPack(writeData,tipo)
            writeSize = len(writeBuffer)
        else:
            readSize = len(self.tipoPack(0,tipo))
        #Add size of read
        if readSize > 0:
            buffer.append(13)
        else:
            buffer.append((13 + writeSize) %256)
        #Fix request
        buffer = buffer + [0,43,13]
        #1 if write, 0 if read
        if readSize > 0:
            buffer.append(0)
        else:
            buffer.append(1)
        #Fix request
        buffer = buffer + [0,0]
        #Add Object Dictionary
        #High byte
        buffer = buffer + [(obj>>8)&0xFF]
        #Low byte
        buffer = buffer + [obj & 0xFF] 
        #SubIndex
        buffer.append(idx%256)
        #Fix request
        buffer = buffer + [0,0,0]
        #Set Size of read or write variable
        if readSize > 0:
            buffer.append(readSize%256)
        else:
            buffer.append(len(writeBuffer)%256)
        ret = bytes(buffer)
        #Add write data
        if writeSize > 0:
            ret = ret + writeBuffer
        return ret

    def MTG_response(self, request,data,tipo):
        #check response code of byte 7 
        if data[7] >= 0x80:
            print("Rensponse code Error" + hex(data[7]))
            return None
        #check if read data is all available
        if request[9] == 0:
            if len(data) != 19 + request[18]:    
                return None
            else:
                return self.tipoUnpack(data[19::],tipo)
        #check if write data is all available
        else:
            if len(data) != 19:
                return None
            else:
                return 0


    def MTG_reqres(self, obj,idx,tipo,writeData = None):
        try:
            dataOut = self.MTG_request(obj,idx,tipo,writeData)
            self.sock.send( dataOut )
            dataIn = self.sock.recv(1024)
            return self.MTG_response(dataOut,dataIn,tipo)
        except:
            return None

    def configure(self):
        #Toggle DI7 to Disable
        # is this possible from "Code" ? we could wire a Digital Out ? 

        #Homing methond 17
        if self.MTG_reqres(0x6098, 0, "uint8", 17) == None:
            return False
        #Homing Speed
        if self.MTG_reqres(0x6099, 1, "uint32", homeSpeed*100) == None:
            return False
        if self.MTG_reqres(0x6099, 2, "uint32", homeSpeed*100) == None:
            return False
        #Homing Acceleration
        if self.MTG_reqres(0x609A, 0, "uint32", homeAcceleration*100) == None:
            return False

    def DI7(self,state):
        #we use the Dout 1 to control to DI7
        if state == True:
            if self.MTG_reqres(0x60FE, 1, "uint32", 0x30000) == None:
                return False
        else:
            if self.MTG_reqres(0x60FE, 1, "uint32", 0x00000) == None:
                return False
        return True
    
    def clearError(self):
        if self.swrefresh() == False:
            return False        
        #if fault is present, clear it
        if self.statusWord["f"] == True:
            self.controlWord["fr"] = True
            if self.cwwrite() == None:
                return False
            #SW refresh
            if self.swrefresh() == False:
                return False        
            time.sleep(0.2)
            self.controlWord["fr"] = False
            time.sleep(0.2)
            if self.cwwrite() == None:
                return False
            if self.swrefresh() == False:
                return False        
            if self.statusWord["f"]:
                return False
        return True

    def boot(self):
        #SW refresh
        if self.swrefresh() == False:
            return False

        #Set bitmask for digital output
        #We set only bit16 (DOUT 1)
        if self.MTG_reqres(0x60FE, 2, "uint32", 0x30000) == None:
            return False
        #SW refresh
        if self.swrefresh() == False:
            return False

        #SET DI7 LOW
        if self.DI7(False) == False:
            return False

        #Set the Heart beat consumer to 0
        if self.MTG_reqres(0x1016, 1, "uint32", 0) == None:
            return False        

        #Homing methond 17
        if self.MTG_reqres(0x6098, 0, "uint8", 17) == None:
            return False
        #Homing Speed
        if self.MTG_reqres(0x6099, 1, "uint32", homeSpeed*100) == None:
            return False
        if self.MTG_reqres(0x6099, 2, "uint32", homeSpeed*100) == None:
            return False
        #Homing Acceleration
        if self.MTG_reqres(0x609A, 0, "uint32", homeAcceleration*100) == None:
            return False
        #Max Velocity
        if self.MTG_reqres(0x607F, 0, "uint32", maxSpeed*100) == None:
            return False
        #Profile Velocity
        if self.MTG_reqres(0x6081, 0, "uint32", maxSpeed*100) == None:
            return False
        #Profile Acceleration 
        if self.MTG_reqres(0x6083, 0, "uint32", maxAcceleration*100) == None:
            return False
        #Profile Deceleration
        if self.MTG_reqres(0x6084, 0, "uint32", maxAcceleration*100) == None:
            return False

        #Clear Error
        self.clearError()

        #DI7 HIGH
        if self.DI7(True) == False:
            return False

        #Clear Error
        self.clearError()

        #Wait Bit9 remote High
        for a in range(50):
            #SW refresh
            if self.swrefresh() == False:
                return False
            if self.statusWord["rm"]:
                break
            time.sleep(0.1)

        #Write Shutdown (page100 Operatin Manual)
        self.cwset(ev = True, qs = True)
        if self.cwwrite() == None:
            return False
                #SW refresh
        if self.swrefresh() == False:
            return False
        
        self.clearError()

        #Wait swith On bit
        for a in range(50):
            #SW refresh
            if self.swrefresh() == False:
                return False
            if self.statusWord["rtso"]:
                break
            time.sleep(0.1)

        #Switch On        
        self.controlWord["so"] = True
        if self.cwwrite() == None:
            return False
                #SW refresh
        if self.swrefresh() == False:
            return False

        #Wait swithed On bit
        for a in range(50):
            #SW refresh
            if self.swrefresh() == False:
                return False
            if self.statusWord["so"]:
                break
            time.sleep(0.1)

        #Enable Operation
        self.controlWord["eo"] = True
        if self.cwwrite() == None:
            return False
                #SW refresh
        if self.swrefresh() == False:
            return False

        #Wait swithed On bit
        for a in range(50):
            #SW refresh
            if self.swrefresh() == False:
                return False
            if self.statusWord["oe"]:
                break
            time.sleep(0.1)

        #Ready for Operation
        return True     

    def MTG_home(self):
        #Clear Error
        self.clearError()

        if self.swrefresh() == False:
            return False
        #Set Operation Mode 
        if self.MTG_reqres(0x6060, 0, "uint8", 6) == None:
            return False   
        #Wait 1 Second     
        for a in range(10):
            if self.swrefresh() == False:
                return False
            time.sleep(0.1)
        #Read Operation Mode 
        if self.MTG_reqres(0x6061, 0, "uint8") != 6:
            print("Homing mode not set")
            return False   

        #Go Home
        self.controlWord["oms1"] = True
        if self.cwwrite() == None:
            return False
                #SW refresh
        if self.swrefresh() == False:
            return False   

        #Wait until bit 10 target reached  - 12 oms
        for a in range(1200):
            if self.swrefresh() == False:
                return False 
            if ((self.statusWord["oms1"]) == True) and \
               ((self.statusWord["tr"]) == True):
               break
            time.sleep(0.1)
        #if reached the 120sec timeout
        if a >= 1999:
            return False
        #Homing Reached

        #Remove start home flag
        self.controlWord["oms1"] = False
        if self.cwwrite() == None:
            return False
                #SW refresh

        return True

    def positionMode(self):
        #Clear Error
        self.clearError()
        #Set speed and all the other parameters
        if self.swrefresh() == False:
            return False
        #Set Operation Mode 
        if self.MTG_reqres(0x6060, 0, "uint8", 1) == None:
            return False   
        #SW refresh
        if self.swrefresh() == False:
            return False   

        for a in range(200):
        #Read Operation Mode 
            if self.MTG_reqres(0x6061, 0, "uint8") == 1:
                break
            time.sleep(0.1)
        if a >= 199:
            print("Position mode not set")
            return False   

        #bit6 Oms2 set to 0 means absolute moveements
        self.controlWord["oms3"] = False
        if self.cwwrite() == None:
            return False
        #SW refresh
        if self.swrefresh() == False:
            return False   
        #Remove start home flag
        time.sleep(0.5)

        #Position mode enabled
        return True        

    def moveTo(self, posMm):
        #remove Errors
        self.clearError()

        #Check if homing is referenced
        if self.referenced() == False:
            print("Not reference home")
            return False   

        #Read Operation Mode 
        if self.MTG_reqres(0x6061, 0, "uint8") != 1:
            print("Position mode not set")
            return False         

        #set destination position
        if self.MTG_reqres(0x607A, 0, "uint32", posMm*100) == None:
            return False   
        if self.swrefresh() == False:
            return False  

        #start command
        self.controlWord["oms1"] = True
        #self.controlWord["oms2"] = True
        if self.cwwrite() == None:
            return False
                #SW refresh
        if self.swrefresh() == False:
            return False   
        
        for a in range(1200):
            if self.swrefresh() == False:
                return False           
            if self.statusWord["tr"]:
                break
            time.sleep(0.1)
        #if reached the 120sec timeout
        if a >= 1999:
            return False

        #Position Reached
        #Remove start home flag
        self.controlWord["oms1"] = False
        if self.cwwrite() == None:
            return False
                #SW refresh

        return True

        
vertical1 = MTG("10.170.43.149", CameraServerPort)

print(vertical1.swrefresh())
print("Boot")
print(vertical1.boot())
print("Home")
print(vertical1.MTG_home())
print("Position mode")
input()
print(vertical1.positionMode())
print("Move to 400")
timex = time.time()
print(vertical1.moveTo(400))
input()
print(time.time() - timex)
print("Move to 100")
print(vertical1.moveTo(100))
print("Move to 350")
print(vertical1.moveTo(350))
print("Move to 300")
print(vertical1.moveTo(300))
print("Move to 410")
print(vertical1.moveTo(50))