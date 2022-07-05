import socketserver as SocketServer
import threading
import os
import struct
import time

state = "r"

def Go():
    global state
    #custom implement
    state = "g"

def Pick():
    global state
    #custom implement
    state = "p"

def Calibrate():
    global state
    #custom implement
    state = "c"


def moveCtrl():
    global desPosX,desPosY,desPosZ,desTempo;
    global actPosX,actPosY,actPosZ,actTempo;
    global ctrlTime1,ctrlPathIdx,ctrlPathSize
    global pathPlanned
    global state
    #query current position
    if state == "g":
        ctrlTime1 = time.time() + 1.0
        state = "G"
    elif state == "G":
        if (time.time() > ctrlTime1):
            state = "h"

    if state == "p":
        ctrlTime1 = time.time() + 10.0
        state = "P"
    elif state == "P":
        if (time.time() > ctrlTime1):
            state = "h"

    if state == "c":
        ctrlTime1 = time.time() + 10.0
        state = "C"
    elif state == "C":
        if (time.time() > ctrlTime1):
            state = "h"

    elif state == "h":
        # Enter every 100ms
        # If all path planning is complete --> exit
        if (time.time() > ctrlTime1):
            state = "H"




def decodeMessage(cmdMsg):
    global desPosX,desPosY,desPosZ,desTempo
    global state

    ret = "K"
    if (cmdMsg[0] == "Q"):
        #print("Query")
        pass
    # G:x,y,z,sec
    # x - toward the trees
    # y - towards the left, looking at the camera
    # z - up
    elif (cmdMsg[0] == "G"): #G:x:y:z:sec
        # Split cmd into position and velocity
        # G:pos:vel
        # G:pos
        print("Go")
        values = cmdMsg.split(":")
        if len(values) == 5:
            desPosX = float(values[1])
            desPosY = float(values[2])
            desPosZ = float(values[3])
            #desTempo = float(values[4])
        Go()
    elif (cmdMsg[0] == "P"): #P:x:y:z:UUID
        print("Pick")
        values = cmdMsg.split(":")
        if len(values) == 5:
            desPosX = float(values[1])
            desPosY = float(values[2])
            desPosZ = float(values[3])
            uuid =  values[4]
        Pick()
    else:
        print("Unknown")
        ret = "N"
    return ret

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global state
        data = self.request[0].strip()
        socket = self.request[1]
        for el in data:
            print(el)

        cmdMsg = data.decode("utf-8")
        ret = decodeMessage(cmdMsg)
        #print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        #old python
        #socket.sendto(ret + state + ":" + str(-position), self.client_address)
        socket.sendto(bytes(ret + state,"utf8"), self.client_address)


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
                moveCtrl()
                time.sleep(0.01)


            # Close port
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()

        exit()
