#Testversion 0

import socket
import pickle
import copy

def aig_Camera_getRgbDepth(sock):
    data = pickle.dumps({"cmd":"RgbDepth"})
    try:
        sock.send(data)
        #wait for response
        res = sock.recv(1024*1024*20)
        data = pickle.loads(res)
    except:
        data = {"response":"Error"}
        
    return copy.deepcopy(data)


#Get image and saves it
#return an arrya of detected elements
def aig_singleDetection(serverIp = "localhost"):
    returnElements = []
    #Create and connect to socket to Camera server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = (serverIp, 8009)
    sock.connect(server_address)
    sock.settimeout(15)
    #get RgbDepth
    data = aig_Camera_getRgbDepth(sock)
    sock.close()
    if data["response"] != "Error":
        #Save timestamp
        #Save RGB 
        #Save Depth
        #Save Robot Position
        #Save Robot offset

        #Run Detection
        #Remove touching limits
        #Find 3d Position
        el = {"x":0.0,"y":0.0,"z":0.0,"bbx":((100,100),(200,200))}
    returnElements.append(copy.deepcopy(el))
    return returnElements

        


