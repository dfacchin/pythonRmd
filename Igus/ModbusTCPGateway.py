#Testversion 0


import socket
import pickle
import copy
import struct

CameraServerPort = 502


def MTG_request(obj,idx,readSize,writeBuffer):
    obj += 1
    buffer = [0,0,0,0,0]
    #Add size of read
    if readSize > 0:
        buffer.append(13)
    else:
        buffer.append((13+len(writeBuffer))%256)
    buffer = buffer + [0,43,13]
    if readSize > 0:
        buffer.append(0)
    else:
        buffer.append(1)
    buffer = buffer + [0,0]
    #Add Object Dictionary
    #High byte
    buffer = buffer + [(obj>>8)&0xFF]
    #Low byte
    buffer = buffer + [obj & 0xFF] 
    buffer.append(idx%256)
    buffer = buffer + [0,0,0]
    if readSize > 0:
        buffer.append(readSize%256)
    else:
        buffer.append(len(writeBuffer)%256)
        buffer = buffer + writeBuffer
    return bytes(buffer)

def MTG_response(request,data):
    #check if read data is all available
    if request[9] == 0:
        if len(data) != 19 + request[18]:    
            return None
        else:
            return data[19::]
    #check if write data is all available
    else:
        if len(data) != 19:
            return None
        else:
            return []            


def MTG_reqres(sock,obj,idx,readSize,writeBuffer):
    try:
        dataOut = MTG_request(obj,idx,readSize,writeBuffer)
        sock.send( dataOut )
        dataIn = sock.recv(1024)
        return MTG_response(dataOut,dataIn)
    except:
        return None




    


#Create and connect to socket to Camera server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ("10.170.43.149", CameraServerPort)
print("Connect to server")
sock.connect(server_address)
sock.settimeout(15)
print( len (MTG_reqres(sock,0x6040,0,2,[]) ) )

sock.close()

        


