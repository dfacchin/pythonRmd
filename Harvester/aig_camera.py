
import socket
import pickle
import copy
import time
from utils import *

#Connect to the Realsesne "server" and retrive the infomration
# aig_singleDetection(IP,"AppleDetection","save") will return a list of dic with apple position, and save them on the remote server

CameraServerPort = 20000
class aig_Camera:
    def __init__(self,serverIp = "localhost",serverPort = "20000", offsetCamera = {"x":0.0,"y":0.0,"z":0.0}):
        self.serverIp = serverIp
        self.offsetCamera = offsetCamera


    def getRgbDepth(self, sock, mode):
        data = pickle.dumps({"command":"RgbAndAlignDepth","mode":mode})
        try:
            sock.send(data)
        except:        
            data = {"response":"Error"}
        if mode == "raw":
            return fileTransferReceive(sock)
        else:
            return fileTransferReceiveCompress(sock)

    def getAppleDetection(self, sock, mode):
        data = pickle.dumps({"command":"AppleDetection","mode":mode})
        try:
            sock.send(data)
        except:        
            data = {"response":"Error"}
        try:
            return pickle.loads(sock.recv(1024*16))
        except:        
            data = {"response":"Error"}

    #Get image and saves it
    #return an arrya of detected elements
    def singleDetection(self,request = "AppleDetection", mode = "raw"):
        #Create and connect to socket to Camera server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        try:
            server_address = (self.serverIp, CameraServerPort)
            sock.connect(server_address)
            sock.settimeout(15)
        except:
            print("Connection Error")
            return returnElements
        #get RgbDepth
        if request == "RgbAndAlignDepth":
            data = self.getRgbDepth(sock,mode)
        #get Apple detection
        if request == "AppleDetection":
            data = self.getAppleDetection(sock,mode)
        try:
            sock.close()
        except:
            print("already closed")
        if data["response"] != "Error":
            #for each data we need to apply the camera offset
            for idx in range(len(data["elements"])):
                data["elements"][idx]["x"] = data["elements"][idx]["x"] + self.offsetCamera["x"]
                data["elements"][idx]["y"] = data["elements"][idx]["y"] + self.offsetCamera["y"]
                data["elements"][idx]["z"] = data["elements"][idx]["z"] + self.offsetCamera["z"]

        else:
            data = {"response":"Error","elements":[]}

        return copy.deepcopy(data)

"""
print("get Raw Image")
timex= time.time()
dati = aig_singleDetection()
print(time.time()-timex)

print("get Raw Compressed Image")
timex= time.time()
dati = aig_singleDetection(mode="compress")
print(time.time()-timex)


print("get detection Frame")
timex= time.time()
dati = aig_singleDetection(mode="save")
"""

"""
timex= time.time()
cam = aig_Camera("localhost")
print( cam.singleDetection() )
print("get detection Frame")
"""