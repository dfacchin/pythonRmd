#Testversion 0



import socket
import pickle
import copy
import struct
import time

tipoConverter = {"uint8":"B","uint16":"<H","uint32":"<I","int8":"b","int16":"<h","int32":"<l","float":"<f"}


CameraServerPort = 502

class MTG_controlWord:
    def __init__(self,sock):
        self.sock = sock

    def set(self, so = False, ev = False, qs = False, eo = False, oms1 = False, oms2 = False,  oms3 = False, fr = False, h = False, oms4 = False, r = False, ms1 = False, ms2 = False, ms3 = False, ms4 = False, ms5 = False):
        self.data  = 0
        self.controlWord = {}
        self.controlWord["so"] = so
        self.data  += so * 0x1
        self.controlWord["ev"] = ev
        self.data  += ev * 0x2
        self.controlWord["qs"] = qs
        self.data  += qs * 0x4
        self.controlWord["eo"] = eo
        self.data  += eo * 0x8
        self.controlWord["oms1"] = oms1
        self.data  += oms1 * 0x10
        self.controlWord["oms2"] = oms2
        self.data  += oms2 * 0x20
        self.controlWord["oms3"] = oms3
        self.data  += oms3 * 0x40
        self.controlWord["fr"] = fr
        self.data  += fr * 0x80
        self.controlWord["h"] = h
        self.data  += h * 0x100
        self.controlWord["oms4"] = oms4
        self.data  += oms4 * 0x200
        self.controlWord["r"] = r
        self.data  += r * 0x400
        self.controlWord["ms1"] = ms1
        self.data  += ms1 * 0x800
        self.controlWord["ms2"] = ms2
        self.data  += ms2 * 0x1000
        self.controlWord["ms3"] = ms3
        self.data  += ms3 * 0x2000
        self.controlWord["ms4"] = ms4
        self.data  += ms4 * 0x4000
        self.controlWord["ms5"] = ms5
        self.data  += ms5 * 0x8000
        self.dataOut = struct.pack("<H",self.data)

    def write(self):
        MTG_reqres(self.sock,0x6040,0,"uint16",self.data) #Read Object Dictionary 6041 Status Word that is unsigned int 16



        

class MTG_statusWord:
    def __init__(self,sock):
        self.sock = sock

    def refresh(self):
        data = MTG_reqres(self.sock,0x6041,0,"uint16") #Read Object Dictionary 6041 Status Word that is unsigned int 16
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

    def print(self):
        print(self.statusWord)

def tipoPack(value, tipo):
    return struct.pack(tipoConverter[tipo],value)

def tipoUnpack(data,tipo):
    return struct.unpack(tipoConverter[tipo],data)[0]

def MTG_request(obj,idx,tipo,writeData = None ):
    #bj += 1
    buffer = [0,0,0,0,0]
    readSize = 0
    writeSize = 0
    if writeData != None:
        writeBuffer = tipoPack(writeData,tipo)
        writeSize = len(writeBuffer)
    else:
        readSize = len(tipoPack(0,tipo))
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

def MTG_response(request,data,tipo):
    #check response code of byte 7 
    if data[7] >= 0x80:
        print("Rensponse code Error" + hex(data[7]))
        return None
    #check if read data is all available
    if request[9] == 0:
        if len(data) != 19 + request[18]:    
            return None
        else:
            return tipoUnpack(data[19::],tipo)
    #check if write data is all available
    else:
        if len(data) != 19:
            return None
        else:
            return 0


def MTG_reqres(sock,obj,idx,tipo,writeData = None):
    try:
        dataOut = MTG_request(obj,idx,tipo,writeData)
        sock.send( dataOut )
        dataIn = sock.recv(1024)
        return MTG_response(dataOut,dataIn,tipo)
    except:
        return None




    


#Create and connect to socket to Camera server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ("10.170.43.149", CameraServerPort)
print("Connect to server")
sock.connect(server_address)
sock.settimeout(15)
sw = MTG_statusWord(sock)
sw.refresh()
sw.print()

cw = MTG_controlWord(sock)

for a in range(100):
    print( MTG_reqres(sock,0x2000,1,"uint16") )
    cw.set(fr = True)
    cw.write()
    sw.refresh()
    sw.print()
    time.sleep(4)
    print( MTG_reqres(sock,0x2000,1,"uint16") )
    cw.set(fr = False)
    cw.write()
    sw.refresh()
    sw.print()
    time.sleep(4)
 

sock.close()

        


