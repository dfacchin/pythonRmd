import copy

#Class gripper
class gripper:
    def __init__(self):
        pass
    def calibrate(self):
        pass

#Class arms
class scara:
    def __init__(self,offsetGripper,framelimit,Drop):
        self.offsetGripper = offsetGripper
        self.framelimit = framelimit
        self.gripper = gripper()
        pass

    def calibrate(self):
        #Calibrate vertical
        pass
        #Calibrate arm
        pass
        #Calibrate gripper
        self.gripper.calibrate()

    def go(self,el):
        pass

    def goWait(self,el):
        self.go(el)

    def pick(self,el):
        if (self.isReachable(el)):
            #remove the Vertical offset of the gripper
            el["z"] = el["z"] - self.offsetGripper["z"]

    def isReachable(self,pos):
        if pos["x"] < (self.framelimit["minX"] + self.offsetGripper["x"]):
            return False
        if pos["x"] > (self.framelimit["maxX"] + self.offsetGripper["x"]):
            return False
        if pos["y"] < (self.framelimit["minY"] + self.offsetGripper["y"]):
            return False
        if pos["y"] > (self.framelimit["maxY"] + self.offsetGripper["y"]):
            return False
        if pos["z"] < (self.framelimit["minZ"] + self.offsetGripper["z"]):
            return False
        if pos["z"] > (self.framelimit["maxZ"] + self.offsetGripper["z"]):
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
        drop = {"x":0.0, "y":50.0, "z":0.0}
        #Robot definition
        self.scara = scara(offsetGripper,self.framelimit,drop)
        #define Camera Offset
        self.offsetCamera = {"x":0.0,"y":0.0,"z":0.0}
        #Idle Position
        self.idlePosition = {"x":0.0,"y":0.0,"z":0.0}

    def run(self):
        print(self.state,self.cmd)
        if self.state == "BOOT":
            if self.cmd == "CALIBRATE":
                self.state = "CALIBRATION"
                self.cmd = "None"
            if self.cmd == "IDLE":
                self.state = "IDLE"
                self.cmd = "None"
        elif self.state == "CALIBRATION":
            #Calibrate Vertical
            self.scara.calibrate()
            self.goIdle()
            self.state = "IDLE"

        elif self.state == "IDLE":
            if self.cmd == "SCAN":
                self.state = "SCANNING"
                self.cmd = "None"
            elif self.cmd == "PICK":
                self.state = "PICKING"
                self.cmd = "None"

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
            while (self.apples.findLowest() != None):
                el = self.apples.popLowest()
                #picking movement is elaborated in the scara low level
                self.pickAndDrop(self,el)
            self.goIdle()
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
robot1 = aig_cart("none")
while True:
    robot1.run()
    robot1.cmd = input().replace("\r","").replace("\n","")

print("Stop")
