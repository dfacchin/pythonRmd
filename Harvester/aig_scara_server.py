import socketserver as SocketServer
import threading
import os
import struct
import time
import pickle

#Initialize scara

class Scara:
    #Init
    def __init__(self):
        self.scara = { "state":"idle", 
                       "command":"none",
                       "pending":False,
                       "calibrate":False,
                       "actual":{"x":0,"y":0,"z":0}
                     }
        pass

    def moveCtrl(self):
        #Here all the logic for controlling

        #Idle State
        if self.scara["state"] == "idle":
            if self.scara["command"] == "calibrate":
              self.scara["state"] = "calibrating"
              self.calibrateStartTime = time.time() #use timer for state control
            if self.scara["command"] == "pick":
              self.scara["state"] = "picking"
              self.scara["pickState"] = 0           #use internal state for state control
              self.scara["pickComplete"] = False
            if self.scara["command"] == "moveto":
              self.scara["state"] = "movingto"
              self.scara["positionReached"] = False
              self.moveToTimer = time.time()
            
            #Remove command and pending value
            if self.scara["command"] != "None":
                self.scara["command"] = "None"
                self.scara["pending"] = False
            pass

        #Calibrating State
        elif self.scara["state"] == "calibrating":
            if (time.time()-self.calibrateStartTime) > 10:
                self.scara["calibrate"] = True
                self.scara["state"] = "idle"

        #Picking State
        elif self.scara["state"] == "picking":
            #Prepare path, test it and launch to command for the vertical
            if self.scara["pickState"] == 0:
                self.pickTime = time.time()
                self.scara["pickState"] = 1 
            #If the vertical position is in the range to move the horizontal, start moving the horizontal
            elif self.scara["pickState"] == 1:
                if (time.time() - self.pickTime) > 1:
                    self.pickTime = time.time()
                    self.scara["pickState"] = 2
            #Position to close the gripper reached, close it       
            elif self.scara["pickState"] == 2:
                if (time.time() - self.pickTime) > 1:
                    self.pickTime = time.time()
                    self.scara["pickState"] = 3       
            #Move out to drop position first move to point "B" horizonta
            #Start moving the vertial for drop position
            elif self.scara["pickState"] == 3:
                self.scara["pickComplete"] = True
                self.scara["state"] = "idle"
            #If the vertical permits it, now move to drop position
            #drop reached, ok drop!

        #Go position X, Y, Z
        elif self.scara["state"] == "movingto":
            if (time.time()-self.moveToTimer) > 5:
                self.scara["positionReached"] = True
                self.scara["state"] = "idle"

        #Refresh scara single element
        self.scara["actualX"] = "idle"

        pass


class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global myScara
        print("Request")
        socket = self.request[1]
        #Get data
        data = self.request[0].strip()
        #Unpickle it
        req = pickle.loads(data)
        print(req)
        #write to the Dictionary only if the request is not a read
        if req.get("Read",False) != True:
            for el in req:
                myScara.scara[el] = req[el]
        res = pickle.dumps(myScara.scara)
        print("Response",myScara.scara)
        socket.sendto(res, self.client_address)


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


myScara = Scara()

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 20001

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print("Server Running 20001")
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
