import socketserver as SocketServer
import threading
import os
import struct
import time
import pickle

class Scara:
    #Init
    def __init__(self):
        self.scara = {"state":"idle","command":"none"}
        pass

    def moveCtrl(self):
        #Here all the logic for controlling

        #Idle State
        if self.scare["state"] == "idle":
            pass

        #Calibrating State
        elif self.scare["state"] == "calibrating":
            pass
        pass

myScara = Scara()

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global myScara
        socket = self.request[1]
        #Get data
        data = self.request[0].strip()
        #Unpickle it
        req = pickle.loads(data)

        dataOut = {"state":"Idle"}
        res = pickle.dumps(dataOut)
        socket.sendto(res, self.client_address)


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8891

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        #print("Server started at {} port {}".format(HOST, PORT))
        while True:
            while 1:
                myScara.moveCtrl()
                time.sleep(0.01)


            # Close port
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()

        exit()
