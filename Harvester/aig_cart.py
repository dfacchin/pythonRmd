import copy
import time
import socket
import pickle
from aig_camera import *
from aig_scara import *
from utils import *
from aig_apple import *


config = {  #MECHANICAL FRAME OF THE SCARA ARM
            "framelimit":{"minX":-50.0 ,"maxX": 90.0,
                          "minY":-50.0 ,"maxY": 50.0,
                          "minZ": 0.0 ,"maxZ": 115.0},
            #SCARA SERVER 
            "scaraIp":"127.0.0.1", "scaraPort":20001,
            #GRIPPER MECHANICAL OFFSET
            "offsetGripper":{"x":0.0,"y":0.0,"z":0.0},
            #CAMERA SERVER
            "camera1Ip":"127.0.0.1", "camera1Port":20000,
            #CAMERA OFFSET
            "offsetCamera":{"x":0.0,"y":0.0,"z":0.0},
            #DISTANCE BETWEEN SCANS
            "scanStepCm":20.0,
            #DROP POSITION
            "dropPosition":{"x":50.0,"y":0.0,"z":50.0},
            #IDLE POSITION
            "idlePosition":{"x":50.0,"y":0.0,"z":0.0},
            #APPLE SIZE LIMIT 
            "appleSize":7.0,
            #PICK Sequence mode topDown, downTop, test
            "pickSequenceMode":"test"

         }

# aig_cart is connected to 
# ADAM2/python/RealTest3.py to control the RealSense camera 
#   camera1IP -> IP of the nano with the realsense
#   camera1Port -> 20000 for the first camera, second camera it will be  a second IP
#   this module reports the coordinate, size , refernce time and unique id 
#   for each "scanned" apple, also on the device with the camera the RGB, depth
#   and each scanned info is stored
#   data = self.camera.singleDetection("AppleDetection","save")


# PythonRMD/Harvester/aig_scara_server.py
# This module is performing all the scara movements
# messages are exchanged with dictionaries
# Read -> (scara) if True reports the entire dic of the scara
#         this is used to query state or position
# command -> (scara) change state to the machine
#            (calibrate) from BOOT, IDLE -> CALIBRATING -> IDLE
#            (idle) from BOOT -> IDLE
#            (pick) from IDLE -> PICKING -> IDLE (pickComplete = True)
#                   entire pick sequece, requires:
#                   {"pickX","pickY","PickZ"}
#                   {"dropX","dropY","dropZ"}
#                   {"requestTime"} ????
#            (moveto) from IDLE -> MOVINGTO -> IDLE (positionReached = True)
#            (grab) 
#            (release)


#Reference frame is always the mechanical frame.
# 0 is the low limit switch
# when we scan we get apples from all the surroundings
# an apple is reachable if
# apple position - offset gripper to reference is in the reference limits
# offset limits are added to transform reference to offesett limit
# (reference position Apple) = referene Position + offset Gripper
# when taking picure
# picture taken has an offset
# real position = taken picture + offset camera + global position
# assume the camera has an offset of x = 2, y = -10, z = 15 
# it means that every picutre fill be 
# 2 cm closer to the object
# shiftet to the left of 10 cm
# and taken higher of 15 cm
# if we are in position 0,0,0 and we take a picutre that has an object at 100,0,0
# in global coordinate this object will be
# 102, -10, 15
# Now we want to take it with the gripper that has 8,0,20 
# to reach this object the position that we need to reach is
# 94, -10, -5
# if this position is inside the "limits" of the system, we are "fine", else it's not reachable


class aig_cart:
    def __init__(self,loadFile):
        #read form load files the settings of this cart
        #Cart state machine
        self.state = "BOOT"
        self.cmd = "None"
        #Cart config
        self.framelimit = loadFile["framelimit"]
        self.scanStepCm = loadFile["scanStepCm"]
        #Apple container
        self.apples = apples()
        #Apple size limit
        self.apples.sizeLimit = loadFile["appleSize"]

        self.arms = []
        #1 Single arm
        #Offset vertical Gripper
        #Drop position
        offsetGripper = loadFile["offsetGripper"] # {"x":0.0, "y":0.0, "z":0.0}
        self.drop = loadFile["dropPosition"]      # {"x":0.0, "y":50.0, "z":0.0}
        #Robot definition
        self.scara = scara(loadFile["scaraIp"], loadFile["scaraPort"], offsetGripper, self.framelimit, self.drop)
        #define Camera Offset
        self.offsetCamera = loadFile["offsetCamera"] # {"x":0.0,"y":0.0,"z":0.0}
        #Idle Position
        self.idlePosition = loadFile["idlePosition"] #{"x":0.0,"y":0.0,"z":0.0}
        #Camera
        self.camera = aig_Camera(loadFile["camera1Ip"], loadFile["camera1Port"])
        self.debugLevel = 0xFF
        #Pick sequence mode
        self.pickSequenceMode = loadFile["pickSequenceMode"]    
    
    def run(self):
        print(self.state,self.cmd)
        if self.state == "BOOT":
            if self.cmd == "CALIBRATE":
                self.state = "CALIBRATION"
            if self.cmd == "IDLE":
                self.state = "IDLE"

        elif self.state == "ERROR":
            if self.cmd == "RESET":
                self.state = "RESETTING"

        elif self.state == "IDLE":
            if self.cmd == "CALIBRATE":
                self.state = "CALIBRATION"
            if self.cmd == "SCAN":
                self.state = "SCANNING"
            elif self.cmd == "PICK":
                self.state = "PICKING"

        elif self.state == "RESETTING":
            #Clear errors and restart like new
            pass

        elif self.state == "CALIBRATION":
            #Calibrate Vertical
            self.scara.calibrate()
            self.goIdle()
            self.state = "IDLE"

        elif self.state == "SCANNING":
            #reach idle position
            aigPrint(DBG_SCAN,"Reach idle Position")

            if self.goIdle() == False:
                aigPrint(DBG_ERROR,"Error Reaching idle Position")
                self.state = "ERROR"
                return

            #clear all previous data
            aigPrint(DBG_SCAN,"Clear Apple list")
            self.apples.clearAll()
            #Generate Vertical scanning points
            scanPoints = [self.framelimit["minZ"]]
            while scanPoints[-1] < self.framelimit["maxZ"]:
                step = scanPoints[-1] + self.scanStepCm
                if step < self.framelimit["maxZ"]:
                    scanPoints.append(step)
                else:
                    scanPoints.append(self.framelimit["maxZ"])

            #Reach each point and then scan
            aigPrint(DBG_SCAN,scanPoints)
            for point in scanPoints:
                aigPrint(DBG_SCAN,"Go scan position {}".format(str(point)))
                # Make a copy of the idle position
                pos = copy.deepcopy(self.idlePosition)
                # Change the Vertical position
                pos["z"] = point
                if self.scara.go(pos) == False:
                    aigPrint(DBG_ERROR,"Error Reaching idle Position {}".format(str(pos)))
                    self.state = "ERROR"
                    return                
                #Scan and pass the actual position
                aigPrint( DBG_CRITICAL, "WARNING: using the scan request, not the actual position, change when scara is complete")
                #self.scan(self.scara.getPosition())
                self.scan(pos)

            #Filter Scan data
            self.filterScan()

            if self.goIdle() == False:
                aigPrint(DBG_ERROR,"Error Reaching idle Position")
                self.state = "ERROR"
                return

            self.state = "IDLE"

        elif self.state == "PICKING":
            if self.pickSequenceMode == "test":
                if self.goIdle() == False:
                    aigPrint(DBG_ERROR,"Error Reaching idle Position")
                    self.state = "ERROR"
                    return

                #picking movement is elaborated in the scara low level
                self.scara.pick({"x":80.4, "y":23, "z":100})

                if self.goIdle() == False:
                    aigPrint(DBG_ERROR,"Error Reaching idle Position")
                    self.state = "ERROR"
                    return

            if self.pickSequenceMode == "topDown":
                if self.goIdle() == False:
                    aigPrint(DBG_ERROR,"Error Reaching idle Position")
                    self.state = "ERROR"
                    return             
                #For each apple try to pick it
                picking = True
                while picking:
                    el = self.apples.popLowest()
                    if el == None:
                        aigPrint(DBG2,"No more elements to pick")
                        picking = False
                    else:
                        #picking movement is elaborated in the scara low level
                        if self.isReachable(el):
                            if self.scara.pick(el) == False:
                                aigPrint(DBG_ERROR,"Error picking phase")
                                self.state = "ERROR"
                                return                                

                if self.goIdle() == False:
                    aigPrint(DBG_ERROR,"Error Reaching idle Position")
                    self.state = "ERROR"
                    return  
            else:
                #Go top using idle "XY", and highest point Z
                topIdle = copy.deepcopy(self.idlePosition)
                # set the top position 5 cm lower than max limit
                topIdle["z"] = self.framelimit["z"] - 5.0 
                #Check if the top position is lower than regular idle position, go idle
                if topIdle["z"] < self.idlePosition["z"]:
                    topIdle["z"] = self.idlePosition["z"]
                #Go Top position
                
                if self.scara.goWait(self.topIdle) == False:
                    aigPrint(DBG_ERROR,"Error Reaching Top idle Position")
                    self.state = "ERROR"
                    return                
                #For each apple try to pick it
                picking = True
                while picking:
                    el = self.apples.popHighest()
                    if el == None:
                        aigPrint(DBG2,"No more elements to pick")
                        picking = False
                    else:
                        #picking movement is elaborated in the scara low level
                        if self.isReachable(el):
                            if self.scara.pick(el) == False:
                                aigPrint(DBG_ERROR,"Error picking phase")
                                self.state = "ERROR"
                                return                                

                if self.goIdle() == False:
                    aigPrint(DBG_ERROR,"Error Reaching idle Position")
                    self.state = "ERROR"
                    return  

            self.state = "IDLE"
        self.cmd = "None"

    def isReachable(self,pos):
        #check if the Vertical limit and the gripper offset are ok
        #to reach this point
        if self.scara.isReachable(pos) == True:
            return True
        return False

    def goIdle(self):
        #Move retract scara
        return self.scara.goWait(self.idlePosition)

    def scan(self,position):
        data = self.camera.singleDetection("AppleDetection","save")
        if data["response"] == "Error":
            text = "Error Scanning:" + data["errorCode"]
            aigPrint(DBG_ERROR,text)
            return False

        #For each element we need to add the actual position of the machine, just the vertical in our case
        for idx in range(len(data["elements"])):
            data["elements"][idx]["z"] = data["elements"][idx]["z"] + position["z"]
            #push to apple data array
            self.apples.data.append(copy.deepcopy(data["elements"][idx]))
        return True
        

    def filterScan(self):
        for el in self.apples.data:
            print(el)

        #1 Remove all the apples that are smaller than desired size
        #def remove_values_from_list(the_list, key, val):
        #    return [value for value in the_list if value[key] != val]
        self.apples.data = [value for value in self.apples.data if value["sizeHeight"] >= self.apples.sizeLimit]
        self.apples.data = [value for value in self.apples.data if value["sizeWidth"] >= self.apples.sizeLimit]

        print("After size control")

        for el in self.apples.data:
            print(el)


        #For each data we have:
        # Pos X,Y,Z
        # UUID
        # camera position (we want to prioritize position that are close to camera
        # vertical center)

        #1 Remove all the element that are not pickable
        self.apples.data = [value for value in self.apples.data if self.scara.isReachable({"x":value["x"],"y":value["y"],"z":value["z"]}) ]
        pass

    def pickAndDrop(self,el):
        #Ask the scara system to pick the apple at the desired coordinate
        pass

    def pickAndDropControlled(self,el):
        #Reach front of apples
        #ask for pick or not
        #if not save info of UUID and not pick for Color/size
        #else
        #pick apple
        #move to picture position
        #take picture
        #save pciture RGB
        #Ask if picciolo / pick
        #in case drop to convorybelt
        pass


aigPrint( DBG2, "Start")
robot1 = aig_cart(config)
while True:
    robot1.run()
    robot1.cmd = input().replace("\r","").replace("\n","")

aigPrint( DBG2, "Stop")
