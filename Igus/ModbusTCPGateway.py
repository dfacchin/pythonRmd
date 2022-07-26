import socket
import pickle
import copy
import struct
import time

from cv2 import TermCriteria_COUNT
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

homeSpeed = 5
homeAcceleration = 20
homeType = 17
maxSpeed = 50
maxAcceleration = 20


class MTG_controlWord:
    def __init__(self,mtg):
        self.mtg = mtg

    def set(self, so = False, ev = False, qs = False, eo = False, oms1 = False, oms2 = False,  oms3 = False, fr = False, h = False, oms4 = False, r = False, ms1 = False, ms2 = False, ms3 = False, ms4 = False, ms5 = False):
        self.data  = 0
        self.controlWord = {}
        #0 Switch On
        self.controlWord["so"] = so
        self.data  += so * 0x1
        #1 Enable Voltage
        self.controlWord["ev"] = ev
        self.data  += ev * 0x2
        #2 Quick Stop
        self.controlWord["qs"] = qs
        self.data  += qs * 0x4
        #3 Enable Operation
        self.controlWord["eo"] = eo
        self.data  += eo * 0x8
        #4 Mode specific 1
        self.controlWord["oms1"] = oms1
        self.data  += oms1 * 0x10
        #5 Mode specific 2
        self.controlWord["oms2"] = oms2
        self.data  += oms2 * 0x20
        #6 Mode specific 3
        self.controlWord["oms3"] = oms3
        self.data  += oms3 * 0x40
        #7 Fault Reset
        self.controlWord["fr"] = fr
        self.data  += fr * 0x80
        #8 Halt
        self.controlWord["h"] = h
        self.data  += h * 0x100
        #9 Mode specific 4
        self.controlWord["oms4"] = oms4
        self.data  += oms4 * 0x200
        #10 Reserver
        self.controlWord["r"] = r
        self.data  += r * 0x400
        #11 Manufacturer Specific 1
        self.controlWord["ms1"] = ms1
        self.data  += ms1 * 0x800
        #12 Manufacturer Specific 2
        self.controlWord["ms2"] = ms2
        self.data  += ms2 * 0x1000
        #13 Manufacturer Specific 3
        self.controlWord["ms3"] = ms3
        self.data  += ms3 * 0x2000
        #14 Manufacturer Specific 4
        self.controlWord["ms4"] = ms4
        self.data  += ms4 * 0x4000
        #15 Manufacturer Specific 5
        self.controlWord["ms5"] = ms5
        self.data  += ms5 * 0x8000
        #Save packet data
        self.dataOut = struct.pack("<H",self.data)

    def write(self):
        return self.mtg.MTG_reqres(0x6040, 0, "uint16", self.data) #Read Object Dictionary 6041 Status Word that is unsigned int 16   

class MTG_statusWord:
    def __init__(self, mtg):
        self.mtg = mtg

    def refresh(self):
        data = self.mtg.MTG_reqres(0x6041, 0, "uint16") #Read Object Dictionary 6041 Status Word that is unsigned int 16
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

    def print(self):
        print(self.statusWord)

class MTG:
    def __init__(self, serverip, port):
        #Create and connect to socket to Camera server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = (serverip, port)
        self.sock.connect(server_address)
        self.sock.settimeout(15)
        self.sw = MTG_statusWord(self)
        self.cw = MTG_controlWord(self)
    
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
        if self.mtg.MTG_reqres(0x6098, 0, "uint8", 17) == None:
            return False
        #Homing Speed
        if self.mtg.MTG_reqres(0x6099, 1, "uint32", homeSpeed*100) == None:
            return False
        if self.mtg.MTG_reqres(0x6099, 2, "uint32", homeSpeed*100) == None:
            return False
        #Homing Acceleration
        if self.mtg.MTG_reqres(0x609A, 0, "uint32", homeAcceleration*100) == None:
            return False

    def DI7(self,state):
        #we use the Dout 1 to control to DI7
        if state == True:
            if self.mtg.MTG_reqres(0x60FE, 1, "uint32", 0x10000) == None:
                return False
        else:
            if self.mtg.MTG_reqres(0x60FE, 1, "uint32", 0x00000) == None:
                return False
        return True
    
    def clearError(self):
        if self.sw.refresh() == False:
            return False        
        #if fault is present, clear it
        if self.sw.statusWord["f"] == True:
            self.cw.controlWord["fr"] = True
            if self.cw.write() == None:
                return False
                    #SW refresh
            if self.sw.refresh() == False:
                return False        
            time.sleep(0.2)
            self.cw.controlWord["fr"] = False
            time.sleep(0.2)
            if self.sw.refresh() == False:
                return False        
            if self.sw.statusWord["f"]:
                return False
        return True

    def boot(self):
        #SW refresh
        if self.sw.refresh() == False:
            return False

        #Set bitmask for digital output
        #We set only bit16 (DOUT 1)
        if self.mtg.MTG_reqres(0x60FE, 2, "uint32", 0x10000) == None:
            return False
        #SW refresh
        if self.sw.refresh() == False:
            return False

        #SET DI7 LOW
        if self.DI7(False) == False:
            return False

        #Homing methond 17
        if self.mtg.MTG_reqres(0x6098, 0, "uint8", 17) == None:
            return False
        #Homing Speed
        if self.mtg.MTG_reqres(0x6099, 1, "uint32", homeSpeed*100) == None:
            return False
        if self.mtg.MTG_reqres(0x6099, 2, "uint32", homeSpeed*100) == None:
            return False
        #Homing Acceleration
        if self.mtg.MTG_reqres(0x609A, 0, "uint32", homeAcceleration*100) == None:
            return False
        #Max speed
        #Max acceleration
        #linear movement
        #this data are written with the WEB interface

        #DI7 HIGH
        if self.DI7(True) == False:
            return False

        #Wait Bit9 remote High
        for a in range(50):
            #SW refresh
            if self.sw.refresh() == False:
                return False
            if self.sw.statusWord["rm"]:
                break
            time.sleep(0.1)

        #Write Shutdown (page100 Operatin Manual)
        self.cw.set(ev = True, qs = True)
        if self.cw.write() == None:
            return False
                #SW refresh
        if self.sw.refresh() == False:
            return False
        
        #Wait swith On bit
        for a in range(50):
            #SW refresh
            if self.sw.refresh() == False:
                return False
            if self.sw.statusWord["rtso"]:
                break
            time.sleep(0.1)

        #Switch On        
        self.cw.controlWord["qs"] = True
        if self.cw.write() == None:
            return False
                #SW refresh
        if self.sw.refresh() == False:
            return False

        #Wait swithed On bit
        for a in range(50):
            #SW refresh
            if self.sw.refresh() == False:
                return False
            if self.sw.statusWord["so"]:
                break
            time.sleep(0.1)

        #Enable Operation
        self.cw.controlWord["eo"] = True
        if self.cw.write() == None:
            return False
                #SW refresh
        if self.sw.refresh() == False:
            return False

        #Wait swithed On bit
        for a in range(50):
            #SW refresh
            if self.sw.refresh() == False:
                return False
            if self.sw.statusWord["eo"]:
                break
            time.sleep(0.1)

        #Ready for Operation
        return True     

    def MTG_home(self):
        #Clear Error
        self.clearError()

        if self.sw.refresh() == False:
            return False
        #Set Operation Mode 
        if self.mtg.MTG_reqres(0x6060, 0, "uint8", 6) == None:
            return False   
        #Wait 1 Second     
        for a in range(10):
            if self.sw.refresh() == False:
                return False
            time.sleep(0.1)
        #Read Operation Mode 
        if self.mtg.MTG_reqres(0x6061, 0, "uint8") == 6:
            print("Homing mode not set")
            return False   

        #Go Home
        self.cw.controlWord["oms1"] = True
        if self.cw.write() == None:
            return False
                #SW refresh
        if self.sw.refresh() == False:
            return False   
        #Remove start home flag
        self.cw.controlWord["oms1"] = False
        #Wait 500ms to be sure command is accepted
        time.sleep(0.5)

        #Wait until bit 10 target reached  - 12 oms
        for a in range(1200):
            if self.sw.refresh() == False:
                return False   
            if ((self.sw.statusWord["oms1"]) == False) and \
               ((self.sw.statusWord["oms2"]) == False) and \
               ((self.sw.statusWord["tr"]) == False):
               #Homing is being executed
               pass
            elif ((self.sw.statusWord["oms1"]) == False) and \
                 ((self.sw.statusWord["oms2"]) == False) and \
                 ((self.sw.statusWord["tr"]) == True):
                 #homing interrupted or not yet started
                 return False
            elif ((self.sw.statusWord["oms1"]) == False) and \
                 ((self.sw.statusWord["oms2"]) == True) and \
                 ((self.sw.statusWord["tr"]) == False):
                 #Still moving to homing
                 pass
            elif ((self.sw.statusWord["oms1"]) == False) and \
                 ((self.sw.statusWord["oms2"]) == True) and \
                 ((self.sw.statusWord["tr"]) == True):
                 #Home complete
                 break
            elif ((self.sw.statusWord["oms1"]) == False) and \
                 ((self.sw.statusWord["oms2"]) == False) and \
                 ((self.sw.statusWord["tr"]) == True):
                 pass
            elif ((self.sw.statusWord["oms1"]) == True) and \
                 ((self.sw.statusWord["oms2"]) == False) and \
                 ((self.sw.statusWord["tr"]) == False):
                 #Homing Error
                 return False
            elif ((self.sw.statusWord["oms1"]) == True) and \
                 ((self.sw.statusWord["oms2"]) == False) and \
                 ((self.sw.statusWord["tr"]) == True):
                 #Homing Error
                 return False
            elif ((self.sw.statusWord["oms1"]) == True) and \
                 ((self.sw.statusWord["oms2"]) == True) and \
                 ((self.sw.statusWord["tr"]) == False):
                 #reserved
                 pass
            time.sleep(0.1)
        #if reached the 120sec timeout
        if a >= 1999:
            return False
        #Homing Reached
        return True

    def positionMode(self):
        #Clear Error
        self.clearError()

        if self.sw.refresh() == False:
            return False
        #Set Operation Mode 
        if self.mtg.MTG_reqres(0x6060, 0, "uint8", 1) == None:
            return False   
        #Wait 1 Second     
        for a in range(10):
            if self.sw.refresh() == False:
                return False
            time.sleep(0.1)
        #Read Operation Mode 
        if self.mtg.MTG_reqres(0x6061, 0, "uint8") == 1:
            print("Position mode not set")
            return False   

        #bit6 Oms2 set to 0 means absolute moveements
        self.cw.controlWord["oms3"] = False
        if self.cw.write() == None:
            return False
        #SW refresh
        if self.sw.refresh() == False:
            return False   
        #Remove start home flag
        time.sleep(0.5)

        #Position mode enabled
        return True        

    def moveTo(self, posMm):
        #remove Errors
        self.clearError()

        #set destination position
        if self.mtg.MTG_reqres(0x607A, 0, "uint32", posMm*100) == None:
            return False   
        if self.sw.refresh() == False:
            return False  
        #start command
        #bit6 Oms2 set to 0 means absolute moveements
        self.cw.controlWord["eo"] = True
        if self.cw.write() == None:
            return False
        #SW refresh
        if self.sw.refresh() == False:
            return False  
        self.cw.controlWord["eo"] = False

        for a in range(1200):
            if self.sw.refresh() == False:
                return False           
            if self.sw.statusWord["tr"]:
                break
            time.sleep(0.1)
        #if reached the 120sec timeout
        if a >= 1999:
            return False
        #Homing Reached
        return True

        
        


vertical1 = MTG("10.170.43.149", CameraServerPort)
        


