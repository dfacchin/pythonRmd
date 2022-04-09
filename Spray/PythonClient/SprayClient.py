import socket
import time

host = "10.170.43.10"
port = 8893

time.sleep(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

t =100
request = "G:"+str(t)

# send the message
data = bytes(str(request).encode("utf8"))
print (data)
timex = time.time()
sock.sendto(data, (host, port))

# empty buffer
dataret = sock.recv(1024)
print(dataret)
print(time.time()-timex)

# sleep for 0.3 seconds to ensure the pressure is stable
time.sleep(0.3)
print("End")
