#Testversion 0


import socket
import pickle
import copy

CameraServerPort = 20000

def aig_Camera_getRgbDepth(sock):
    data = pickle.dumps({"command":"RgbAndAlignDepth","mode":"demo"})
    try:
        sock.send(data)
    except:
        print("OUT")
        data = {"response":"Error"}
        #wait for response
    try:
        sock.send(data)
        res = sock.recv(1980*1024*4*100)
        data = pickle.loads(res)
    except:
        print("IN")
        data = {"response":"Error"}
        
    return copy.deepcopy(data)


#Get image and saves it
#return an arrya of detected elements
def aig_singleDetection(serverIp = "localhost"):
    returnElements = []
    #Create and connect to socket to Camera server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = (serverIp, CameraServerPort)
    sock.connect(server_address)
    sock.settimeout(15)
    #get RgbDepth
    data = aig_Camera_getRgbDepth(sock)
    sock.close()
    print("Dimensione",len(data))
    for a in data:
        print(a)
    print("YYYYY")
    print(data["response"])
    if data["response"] != "Error":
        print("XXXXXX")
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

        

print(aig_singleDetection())
