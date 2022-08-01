import copy
import time
import socket
import pickle
from aig_camera import *

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

DBG1 = 0x1
DBG2 = 0x2
DBG3 = 0x4
DBG4 = 0x8
DBG5 = 0x10
DBG6 = 0x20
DBG7 = 0x40
DBG7 = 0x80

DBG_SCAN = DBG1
DBG_CRITICAL = DBG7


DBGLVL = 0xFF

def aigPrint(dbglvl, stringa):
    global DBGLVL
    if DBGLVL & dbglvl:
        print(stringa)


config = {  #MECHANICAL FRAME OF THE SCARA ARM
            "framelimit":{"minX":-50.0 ,"maxX": 150.0,
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
            "appleSize":7.0

         }


#Class arms
class scara:
    def __init__(self, scaraIp , scaraPort, offsetGripper,framelimit,drop):
        #Open socket connection with the SCARA 
        self.drop = drop
        self.scaraIp = scaraIp
        self.scaraPort = scaraPort
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.offsetGripper = offsetGripper
        self.framelimit = framelimit
    
    #Generate a request and get the response
    def reqres(self,data):
        dataOut = pickle.dumps(data)
        try:
            self.sock.sendto(dataOut, (self.scaraIp, self.scaraPort))
            # empty buffer
            res = self.sock.recv(1024)
        except:
            return None
        return pickle.loads(res) 

    #req = string with request code
    #condition = {"condition":conditionValue}
    #timeout = timout in seconds to exit with timeout error
    #frequency = 1/frequency sleep time between requests
    def waitCondition(self,conditions,timeout,frequency,text="."):
        timestart = time.time()
        while (time.time() - timestart) < timeout:
            result = {}
            #Make a request with Read query command, it's simple read
            res = self.reqres({"Read":True})
            #check if response is valid
            if res == None:
                return False
            #for each condition
            for el in conditions:
                #be sure the condition is in the response
                #add the result to the response
                if el in res:
                    if res[el] == conditions[el]:
                        result[el] = True
                    else:
                        result[el] = False
            #if all conditions are met return true, else continue
            test = True
            for el in result:
                if result[el] == False:
                    test = False
            if test:
                return True
            #sleep
            #with frequency == 0 1 try only
            if (frequency == 0):
                return False
            print(text,end="")
            time.sleep(1.0/frequency)         
        #timeout
        return False
    
    def checkIs(self,conditions):
        return self.waitCondition(conditions,999,0,text="")

    def calibrate(self):
        #send socket request to SCARA to calibrate
        #wait for response of type 
        # "calibration complete" or "idle"
        #if error state, quit with error
        self.waitCondition({"state":"idle","pending":False}, 5, 10)
        # empty buffer
        if self.reqres({"command":"calibrate"}) != None:
            aigPrint( DBG2, "Calibrate")
            if self.waitCondition({"state":"calibrating","pending":False}, 5, 10):
                aigPrint( DBG2, "calibrating..")
                if self.waitCondition({"state":"idle","calibrate":True}, 50, 10) == True:
                    aigPrint( DBG2, "Calibrate Complete")
                    return True
        aigPrint(DBG_CRITICAL,"Calibration Fail")
        return False

    def getPosition(self):
        #do I need to deep copy this ?
        res = self.reqres({"Read":True})
        #check if response is valid
        if res == None:
            return False        
        return {"x":res["actual"]["x"],"y":res["actual"]["y"],"z":res["actual"]["z"]}

    def go(self,el):
        aigPrint( DBG2, "go")
        aigPrint( DBG2, el)
        #send 
        pass

    def goWait(self,el):
        self.go(el)
        #wait for idle state or error state
        time.sleep(2)
        return True

    def grips(self):
        #send command to close the gripper and twist back and forth
        time.sleep(0.5)
        return True

    def release(self):
        time.sleep(0.5)
        return True
        #open the gripper and 

    def pick(self,el):
        #send socket request to SCARA to calibrate
        #wait for response of type 
        # "calibration complete" or "idle"
        #if error state, quit with error
        self.waitCondition({"state":"idle","pending":False}, 5, 10)
        if self.checkIs({"calibrate":False}):
            aigPrint( DBG2, "Calibrate before picking")
            return False
        # empty buffer
        command = {"command":"pick"}
        command["pickX"] = el["x"]
        command["pickY"] = el["x"]
        command["pickZ"] = el["x"]
        command["dropX"] = self.drop["x"]
        command["dropY"] = command["dropX"] = self.drop["x"]
        command["dropZ"] = command["dropX"] = self.drop["x"]
        if self.reqres(command) != None:
            aigPrint(DBG2,"Pick ")
            if self.waitCondition({"state":"picking","pending":False}, 5, 10):
                if self.waitCondition({"state":"idle","pickComplete":True}, 15, 10) == True:
                    aigPrint("DBG2","pick compelte")
                    return True
        aigPrint( DBG2, "Pick Fail")
        return False

        #remove the 
        if (self.isReachable(copy.deepcopy(el))):
            #remove the Vertical offset of the gripper
            #send pick request
            #wait for response 
            #idle state
            #if error state, quit with error
            time.wait(5)
            return True
        return True

    def isReachable(self,pos):
        pos["x"] = pos["x"] - self.offsetGripper["x"]
        pos["y"] = pos["y"] - self.offsetGripper["y"]
        pos["z"] = pos["z"] - self.offsetGripper["z"]
        if pos["x"] < (self.framelimit["minX"] - self.offsetGripper["x"]):
            return False
        if pos["x"] > (self.framelimit["maxX"] - self.offsetGripper["x"]):
            return False
        if pos["y"] < (self.framelimit["minY"] - self.offsetGripper["y"]):
            return False
        if pos["y"] > (self.framelimit["maxY"] - self.offsetGripper["y"]):
            return False
        if pos["z"] < (self.framelimit["minZ"] - self.offsetGripper["z"]):
            return False
        if pos["z"] > (self.framelimit["maxZ"] - self.offsetGripper["z"]):
            return False
        return True


#Cart class
class apples:
    def __init__(self):
        self.data = []
        self.sizeLimit = 8.0

    def clearAll(self):
        self.data = []

    def findLowest(self):
        #Logic, serve first the "lowest" apple and than start going up
        if len(self.data) == 0:
            return None
        return min(self.data, key=lambda x:x['y'])

    def removeElement(self,element):
        # each element is identified by an UUID,
        # search for the UUID in the list of data and remove it
        searchUuid = element["uuid"]
        popIdx = -1
        for el in self.data:
            if  el["uuid"] == searchUuid:
                popIdx = self.data.index(el)
                break
        if popIdx >= 0:
            self.data.pop(popIdx)

    def popLowest(self):
        el = self.findLowest()
        if el != None:
            self.removeElement(el)




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
        #Apple size limit
    
    
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
            self.goIdle()
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
                self.scara.go(pos)
                aigPrint(DBG_SCAN,"Position Reached, SCAN")
                #Scan and pass the actual position
                aigPrint( DBG_CRITICAL, "WARNING: using the scan request, not the actual position, change when scara is complete")
                #self.scan(self.scara.getPosition())
                self.scan(pos)

            #Filter Scan data
            self.filterScan()
            self.goIdle()
            self.state = "IDLE"

        elif self.state == "PICKING":
            self.goIdle()
            #picking movement is elaborated in the scara low level
            self.scara.pick({"x":80.4, "y":23, "z":100})
            self.goIdle()
            """
            self.goIdle()
            while (self.apples.findLowest() != None):
                el = self.apples.popLowest()
                #picking movement is elaborated in the scara low level
                self.scara.pick(self,el)
            self.goIdle()
            """
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
        self.scara.goWait(self.idlePosition)

    def scan(self,position):
        data = self.camera.singleDetection("AppleDetection","save")
        #For each element we need to add the actual position of the machine, just the vertical in our case
        for idx in range(len(data["elements"])):
            data["elements"][idx]["z"] = data["elements"][idx]["z"] + position["z"]
            #push to apple data array
            self.apples.data.append(copy.deepcopy(data["elements"][idx]))
        

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
