import socket
import zlib
import pickle
import copy

DBG1 = 0x1
DBG2 = 0x2
DBG3 = 0x4
DBG4 = 0x8
DBG5 = 0x10
DBG6 = 0x20
DBG7 = 0x40
DBG8 = 0x80

DBG_SCAN = DBG1
DBG_CRITICAL = DBG7
DBG_ERROR = DBG8


DBGLVL = 0xFF

def aigPrint(dbglvl, stringa):
    global DBGLVL
    if DBGLVL & dbglvl:
        print(stringa)
        

#Transfer an entire file
def fileTransferSend(sock, data):
    try:
    #send the length of the data to the client
        sock.send( pickle.dumps( {"length":len(data)}))        
        load = True
        stepMax = 1024*20
        while load:
            remoteSize = pickle.loads(sock.recv(256))
            if (remoteSize < len(data)):
                step = min(stepMax,len(data)-remoteSize)
                sock.send(data[remoteSize:remoteSize+step])
            else:
                load = False
    except:
        #in case of error, just quit
        pass

#Transfer an entire file
def fileTransferSendCompress(sock, data):
    #compress it
    fileTransferSend(sock, zlib.compress(data))

def fileTransferReceiveRaw(sock):
    #get length of the file
    try:
        res = sock.recv(1024*20)
    except:
        print("receive problem")
    if(len(res)):
        #unload
        resp1 = pickle.loads(res)
        lunghezza = resp1.get("length",0)
        data = b''
        #get all the data
        while len(data)<lunghezza:
            #send the actual data size
            sock.send(pickle.dumps(len(data)))
            data = data + sock.recv(1024*20)
        #send last to close connection
        sock.send(pickle.dumps(len(data)))
        return data

def fileTransferReceive(sock):
        res = fileTransferReceiveRaw(sock)
        try:
            data = pickle.loads(res)
            return data
        except:
            data = {"response":"Error"}
            return copy.deepcopy(data)

def fileTransferReceiveCompress(sock):
        res = fileTransferReceiveRaw(sock)
        try:
            data = zlib.decompress(res)
            data = pickle.loads(data)
            return data
        except:
            data = {"response":"Error"}
            return copy.deepcopy(data)
