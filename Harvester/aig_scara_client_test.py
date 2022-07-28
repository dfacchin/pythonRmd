import socket
import time
import pickle
#host = "10.170.43.10"
host = "127.0.0.1"
port = 20001


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

t =100
request = {"Nome":"Cognome"}
# send the message
data = pickle.dumps(request)
print (data)
timex = time.time()
sock.sendto(data, (host, port))

# empty buffer
dataret = sock.recv(1024)
print(pickle.loads(dataret))
print(time.time()-timex)

"""
for a in range(100):
    request = "Q"
    data = bytes(str(request).encode("utf8"))
    print (data)
    timex = time.time()
    sock.sendto(data, (host, port))

    # empty buffer
    dataret = sock.recv(1024)
    print(dataret)
    print(time.time()-timex)
    time.sleep(0.1)


# sleep for 0.3 seconds to ensure the pressure is stable
"""
print("End")
