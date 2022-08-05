import copy
import time
import socket
import pickle
from utils import *


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
