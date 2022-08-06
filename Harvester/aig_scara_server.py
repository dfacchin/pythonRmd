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

        self.scara["executePath"] = False
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

        # Reach the stop condition from moving
        # if some movements fails, we trigger stopping and after stop
        # from stop we exit with and idle command
        elif self.scara["state"] == "stop":
            if self.scara["command"] == "calibrate":
              self.scara["state"] = "calibrating"
            if self.scara["state"] == "idle":
              self.scara["state"] = "idle"

        #Calibrating State
        elif self.scara["state"] == "calibrating":
            if (time.time()-self.calibrateStartTime) > 10:
                self.scara["calibrate"] = True
                self.scara["state"] = "idle"

        #Picking State
        #This is the picking commands
        #command = {"command":"pick"}
        #command["pickX"] = el["x"]
        #command["pickY"] = el["x"]
        #command["pickZ"] = el["x"]
        #command["dropX"] = self.drop["x"]
        #command["dropY"] = command["dropX"] = self.drop["x"]
        #command["dropZ"] = command["dropX"] = self.drop["x"]
        #1 Be sure to move out of the dropping zone
        #2 Once out, move vertical to picking position, at that point we need to be with the horizontal in the limit of the safe are
        #3 Enter and pick the apple
        #4 retract to the safe area
        #5 start moving to the drop position vertical, horizontal must stop in fron of the dropping area
        #6 when the vertical is done, enter e drop the apple
        elif self.scara["state"] == "picking":
            
            #Check if inside collision zone, move out of it
            if self.scara["pickState"] == 0:
                if self.scara["actualX"] < 10:
                    self.scara["pickState"] = 2
                    #Keep X and move to B "safe" position with shulder, elbow, wrist, open finger, right twist
                    self.scara["positionReached"] = False
                    self.scara["moveTimeout"] = time.time() + 5
                else:
                    #Already out of critical position, go to state 3
                    self.scara["pickState"] = 3

            # Move out of critical zone 
            elif self.scara["pickState"] == 2:
                if self.scara["positionReached"] == False:
                    if time.time() > self.scara["moveTimeout"]:
                        self.scara["state"] == "stopping"
                        self.scara["stopState"] = 0
                else:
                    self.scara["pickState"] = 3
            
            #Path planning to pick the apple
            elif self.scara["pickState"] == 3:               
                #Prepare path to pick the apple 
                Points = []
                timeRef = 0.0
                # 1 firt point is to reach safe zone in front of apple with longer time between:
                # vertical or horizontal time
                timeVertical = 3.0   #getFromToVerticalTiming()
                timeHorizontal = 2.0 #getFromToHorizontalTiming()
                timeStep = min(timeVertical, timeHorizontal)
                timeRef += timeStep
                if (self.scara["pickX"] -10.0) > 60.0:
                    safeX = 60.0
                else:
                    safeX = self.scara["pickX"]
                Points.add[ {"x": safeX, "y":self.scara["pickY"], "z":self.scara["pickZ"], "time": timeRef, "gripper": "open", "twist": "right", "orientation":"tree"} ]         


                #2 Now we are in front of the apple, enter 
                timeRef += 0.5
                Points.add[ {"x":self.scara["pickX"], "y":self.scara["pickY"], "z":self.scara["pickZ"], "time": timeRef, "gripper": "close", "twist": "right", "orientation":"tree"} ]         

                #3 Close the apple 
                timeRef += 0.3
                Points.add[ {"x":self.scara["pickX"], "y":self.scara["pickY"], "z":self.scara["pickZ"], "time": timeRef, "gripper": "close", "twist": "right", "orientation":"tree"} ]         

                #3 Retract a little + keep close and turn left the gripper
                timeRef += 0.3
                retractOffset = 3.0
                Points.add[ {"x":self.scara["pickX"] - retractOffset, "y":self.scara["pickY"], "z":self.scara["pickZ"], "time": timeRef, "gripper": "close", "twist": "left", "orientation":"tree"} ]         

                #4 Reach safe zone
                timeRef += 0.3
                retractOffset = 3.0
                Points.add[ {"x":safeX, "y":self.scara["pickY"], "z":self.scara["pickZ"], "time": timeRef, "gripper": "close", "twist": "left", "orientation":"tree"} ] 

                #5 Move in front of dropping position 
                timeVertical = 3.0   #getFromToVerticalTiming()
                timeHorizontal = 2.0 #getFromToHorizontalTiming()
                timeStep = min(timeVertical, timeHorizontal)
                timeRef += timeStep
                safeX = 10.0
                Points.add[ {"x":safeX, "y":self.scara["dropY"], "z":self.scara["dropZ"], "time": timeRef, "gripper": "close", "twist": "left", "orientation":"machine"} ] 

                # Prepare next subState
                # Generate path planning using Points

                self.scara["pickState"] = 4
                self.scara["executePath"] = True
                self.scara["positionReached"] = False
                self.scara["moveTimeout"] = timeRef + 5

            # Execute the path planning
            elif self.scara["pickState"] == 5:
                if self.scara["positionReached"] == False:
                    if time.time() > self.scara["moveTimeout"]:
                        self.scara["state"] == "stopping"
                        self.scara["stopState"] = 0
                else:
                    self.scara["pickState"] = 6

            #Path planning to drop the apple and exit critical area
            elif self.scara["pickState"] == 6:               
                #Prepare path to pick the apple 
                Points = []
                timeRef = 0.0
                # 1 Enter overt the convory belt
                # vertical or horizontal time
                timeRef  = 1.0
                Points.add[ {"x": self.scara["dropX"], "y":self.scara["dropY"], "z":self.scara["dropZ"], "time": timeRef, "gripper": "close", "twist": "right", "orientation":"machine"} ]         

                #2 Open the fingers
                timeRef += 0.3
                Points.add[ {"x": self.scara["dropX"], "y":self.scara["dropY"], "z":self.scara["dropZ"], "time": timeRef, "gripper": "open", "twist": "right", "orientation":"machine"} ]         

                #3 retract keep facing the machine
                timeRef += 0.7
                safeX = 10.0
                Points.add[ {"x":safeX, "y":self.scara["dropY"], "z":self.scara["dropZ"], "time": timeRef, "gripper": "close", "twist": "left", "orientation":"machine"} ] 

                # Prepare next subState
                # Generate path planning using Points

                self.scara["pickState"] = 7
                self.scara["executePath"] = True
                self.scara["positionReached"] = False
                self.scara["moveTimeout"] = timeRef + 5
            
            # Execute the path planning
            elif self.scara["pickState"] == 7:
                if self.scara["positionReached"] == False:
                    if time.time() > self.scara["moveTimeout"]:
                        self.scara["state"] == "stopping"
                        self.scara["stopState"] = 0

                else:
                    self.scara["positionReached"] = True
                    self.scara["state"] = "idle"
            
            #Not possible conditionss
            else:
                self.scara["state"] == "stopping"
                self.scara["stopState"] = 0



        #Stopping
        elif self.scara["state"] == "stopping":
            if self.scara["stopState"] == 0:
                self.scara["stopState"] = 1
                self.scara["moveTimeout"] = timeRef + 5
                #Emergency STOP to all motors
            elif self.scara["stopState"] == 1:
                if time.time > self.scara["moveTimeout"]:
                    #Check if all motors are stopped
                    self.scara["state"] = "stop"
                    
        #Update path if running        
        #Update Vertical
        #Update Dynamixel
        #Uppdate RMD

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
