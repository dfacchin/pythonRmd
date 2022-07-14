import socket
import pickle

def aig_Camera_getRgbDepth(sock):
    data = pickle.dumps({"cmd":"RgbDepth"})
    sock.send(data)
    #wait for response
    res = sock.recv(1024*1024*20)
    print(len(res))
    dataOut = pickle.loads(res)
    print(len(dataOut))


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 8009)
sock.connect(server_address)
sock.settimeout(15)

#get RgbDepth
aig_Camera_getRgbDepth(sock)
sock.close()
