import copy
import time
import socket
import pickle

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

config = {"scaraIp":"127.0.0.1", "scaraPort":20001}

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
            print("Calibrate")
            if self.waitCondition({"state":"calibrating","pending":False}, 5, 10):
                print("calibrating..")
                if self.waitCondition({"state":"idle","calibrate":True}, 50, 10) == True:
                    print("Calibrate Complete")
                    return True
        print("Calibration Fail")
        return False

    def getPosition(self):
        #do I need to deep copy this ?
        return {"x":0.0,"y":0.0,"z":0.0}

    def go(self,el):
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
            print("Calibrate before picking")
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
            print("Pick")
            if self.waitCondition({"state":"picking","pending":False}, 5, 10):
                print("picking phase calibrating.. 1")
                if self.waitCondition({"state":"idle","pickComplete":True}, 15, 10) == True:
                    return True
        print("Pick Fail")
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
        self.framelimit = {}
        self.framelimit["minX"] = -50.0
        self.framelimit["maxX"] = 50.0
        self.framelimit["minY"] = 50.0
        self.framelimit["maxY"] = 90.0
        self.framelimit["minZ"] = 0.0
        self.framelimit["maxZ"] = 115.0
        self.scanStepCm = 20
        #Apple container
        self.apples = apples()
        self.arms = []
        #1 Single arm
        #Offset vertical Gripper
        #Drop position
        offsetGripper = {"x":0.0, "y":0.0, "z":0.0}
        self.drop = {"x":0.0, "y":50.0, "z":0.0}
        #Robot definition
        self.scara = scara(loadFile["scaraIp"], loadFile["scaraPort"], offsetGripper, self.framelimit, self.drop)
        #define Camera Offset
        self.offsetCamera = {"x":0.0,"y":0.0,"z":0.0}
        #Idle Position
        self.idlePosition = {"x":0.0,"y":0.0,"z":0.0}

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
            self.goIdle()
            #clear all previous data
            self.apples.clearAll()
            #Generate Vertical scanning points
            scanPoints = [self.framelimit["minZ"]]
            while scanPoints[-1] < self.framelimit["minZ"]:
                step = scanPoints[-1] + self.scanStepCm
                if step < self.framelimit["maxZ"]:
                    scanPoints.append(step)
                else:
                    scanPoints.append(self.framelimit["maxZ"])
            #Reach each point and then scan
            for point in scanPoints:
                self.scara.go({"z":point})
                self.scan()
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
        posXYIntermediate = copy.deepcopy(self.idlePosition)
        print(posXYIntermediate)
        posZIntermediate= posXYIntermediate.pop("y")
        self.scara.goWait(posXYIntermediate)
        self.scara.goWait(posZIntermediate)

    def scan(self):
        #Get the real vertical Position
        #Get the Frame RGB/DEPTH
        #GET BBOX
        #Clear BBOX
        #GET APPLE Position
        #For each APPLE
        ##x,y,z Position
        ##uuid
        ##camera pixel coordinate of bbox center RGB
        ##grade of confidance
        ##e BBox
        #Save apples info
        #SAVE RGB image
        #SAVE DEPTH frame
        #push to apple data array
        pass

    def filterScan(self):
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


print("Start")
robot1 = aig_cart(config)
while True:
    robot1.run()
    robot1.cmd = input().replace("\r","").replace("\n","")

print("Stop")
