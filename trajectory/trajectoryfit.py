""" Trajectory fit takes a list of points in space, and based on acceleration and speed 
    constraints will assign a time to each point at which constraints are maintained true

    First and last point of the path (x,y) are set to be at 0 velocity

    vectorV is the sqrt(Vx^2+Vy^2)
    vectorA is the sqrt(Ax^2+Ay^2)
"""
import time
import logging
import math

CORRECTION_MARGIN = 0.999
REDUCTION_FACTOR = 0.9

STATE_INIT = "INIT"
STATE_DONE = "DONE"
STATE_NEXT = "NEXT"
STATE_BACKFIRE = "BACKFIRE"
STATE_ERROR_ACC = "ERROR_ACC"

#logging.basicConfig(level=logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG)

def calc_time(d,a,v):
    try:
        t = (math.sqrt((2*d)/a + v*v)-v)/a
    except:
        t = 0
    return t
def calc_a(d,vi,vf):
    a = (vf*vf-vi*vi)/(2*d)
    return a 
def calc_t(vi,vf,a):
    t = (vf-vi)/a
    return t
def calc_t_dva(d,vi,a):
    try:
        t = (math.sqrt((2*d*a) + (vi*vi)) - vi) / a
    except:
        t = 0
    return t
def cald_d(vi,a,t):
    d = vi*t + (a*t*t)/2
    return d
def calc_a_dvt(d,v,t):
    a = (d-v*t)*(2/(t*t))
    return a
def calc_vf_dva(d,vi,a):
    #works if it "goes" straight
    try:
        vf = math.sqrt(2*a*d+vi*vi)
    except:
        vf = 0
    return vf

# Calculate the time and final speed
# to cover a distance, with a starting speed
# 
def calcAB(A,B):
    """
    IF state OK always make sure
    A.acc.value  #REQ1
    B.vel.value  #REQ2
    B.vel.max    #REQ3
    B.time.value #REQ4
    are set
    """
    d = B.pos.value - A.pos.value
    A.state = STATE_INIT
    B.state = STATE_INIT    
    #if d is 0 Velocity must be 0
    if d == 0:
        if A.vel.value != 0:
            A.vel.max = 0
            A.state = STATE_BACKFIRE
            B.state = STATE_INIT
            return A,B
        #REQ1 No need for acceleration
        A.acc.value = 0
        #REQ2 No change in velocity
        B.vel.value = 0
        #REQ3 max velocity is limited to 0
        B.vel.max = 0
        #REQ4 No time constraint        
        B.time.value = 0 
    else:
        #check if we need to change speed
        if A.vel.value == B.vel.max:
            #REQ1 No need for acceleration
            #moving already at the right speed, no acceleration            
            A.acc.value = 0
            #REQ2 No change in velocity
            B.vel.value = A.vel.value
            #REQ3 max velocity does not change
            B.vel.max = B.vel.max
            #REQ4 time is space dived by constat speed        
            try:
                B.time.value = d/A.vel.value
            except:
                B.time.value = 0.0

        else:
            #calculate the max acceleration required to reach speed at B
            #with final speed Vmax
            velf = B.vel.max*CORRECTION_MARGIN
            acc = calc_a(d, A.vel.value, velf)
            #if the acceleration exceeds max acceleration
            if abs(acc) > B.acc.max:
                #ideal acceleration leads to speed exceeding limit
                #if the desired acceleration is negative set -Amax
                if acc < 0:
                    acc = -B.acc.max*CORRECTION_MARGIN
                else:
                    acc = B.acc.max*CORRECTION_MARGIN
                #with the new acceleration the max speed will be lower                 
                velf = calc_vf_dva(d, A.vel.value, acc)
            if acc != 0:
                #with know initial Velocity, max speed, and acceleration we can calculate time
                tim = calc_t(A.vel.value, velf, acc)
                #just for test knowing distance, initial speed and acceleration
                t1 = calc_t_dva(d, A.vel.value, acc)
                #print(B.time.value, t1)
            else:
                tim = d/A.vel.value

            #Check if time is negative something is not right
            if tim < 0:
                if d>0:
                    vmax = calc_vf_dva(d, B.vel.max, A.acc.max*CORRECTION_MARGIN)
                else:
                    vmax = calc_vf_dva(d, B.vel.max, -A.acc.max*CORRECTION_MARGIN)
                A.vel.max = vmax
                A.state = STATE_BACKFIRE
                B.state = STATE_INIT
                return A,B                    
            #Need to check the if the final speed in in between the limits
            if abs(velf) > B.vel.max:
                #Set in A the max speed it can have to reach B with its max acceleration
                # Dont use all the max acceleration otherwise we will play on the variable precision
                vmax = calc_vf_dva(d, B.vel.max, A.acc.max*CORRECTION_MARGIN)
                A.vel.max = vmax
                A.state = STATE_BACKFIRE
                B.state = STATE_INIT
                return A,B
            #REQ1 
            A.acc.value = acc
            #REQ2 
            B.vel.value = velf
            #REQ3 no change to the max possibile speed
            B.vel.max = B.vel.max
            #REQ4 
            B.time.value = tim 
    A.state = STATE_DONE
    B.state = STATE_NEXT             
    return A,B


def calcAB_t(A,B,t):
    """
    IF state OK always make sure
    A.acc.value  #REQ1
    B.vel.value  #REQ2
    B.vel.max    #REQ3
    B.time.value is fixed
    are set
    """
    d = B.pos.value - A.pos.value
    #calc acceleration
    acc = calc_a_dvt(d,A.vel.value,t)
    #This should not happend, we ask for longer time respect to the first acceleration tested
    if (acc>B.acc.max):
        print("ERROR")
        return A,B
    vel = calc_vf_dva(d, A.vel.value, acc)
    #REQ1 
    A.acc.value = acc
    #REQ2 
    B.vel.value = vel
    #REQ3 no change to the max possibile speed
    B.vel.max = B.vel.max
    #REQ4 
    B.time.value = t
    return A,B


def calcTime(A,B):
    tx = B.x.time.value
    ty = B.y.time.value
    if tx < ty:
        A.x,B.x = calcAB_t(A.x,B.x,ty)
    elif ty < tx:
        A.y,B.y = calcAB_t(A.y,B.y,tx)
    return A,B

def infoNode(pointName,point,level):
    strA =  "\n"+str(level)
    strA += "\t"*(1+level)+pointName+"\n"
    strA += point.string(pad=" "*len(str(level))+"\t"*(1+level)+"  ")
    return strA

def infoStep(A,B):
    stra  = "\n--- X\n"
    stra += "P:"+str(A.x.pos.value)+"->"+str(B.x.pos.value)+"\n"
    stra += "S:"+str(A.x.vel.value)+"->"+str(B.x.vel.value)+"_"+str(A.x.vel.max)+"->"+str(B.x.vel.max)+"\n"
    stra += "A:"+str(A.x.acc.value)+"->"+str(B.x.acc.value)+"_"+str(A.x.acc.max)+"->"+str(B.x.acc.max)+"\n"
    stra += "t:"+str(A.x.time.value)+"->"+str(B.x.time.value)+"_"+str(A.x.time.max)+"->"+str(B.x.time.max)+"\n"
    stra += "--- Y\n"
    stra += "P:"+str(A.y.pos.value)+"->"+str(B.y.pos.value)+"\n"
    stra += "S:"+str(A.y.vel.value)+"->"+str(B.y.vel.value)+"_"+str(A.y.vel.max)+"->"+str(B.y.vel.max)+"\n"
    stra += "A:"+str(A.y.acc.value)+"->"+str(B.y.acc.value)+"_"+str(A.y.acc.max)+"->"+str(B.y.acc.max)+"\n"
    stra += "t:"+str(A.y.time.value)+"->"+str(B.y.time.value)+"_"+str(A.y.time.max)+"->"+str(B.y.time.max)+"\n"
    stra += "---\n"
    return stra

def calc(A,B,level):
    #logging.debug(infoNode("Ain",A,level) + infoNode("Bin",B,level))
    level +=1
    logging.info(infoStep(A,B))
    #A has a starting V
    #A B both have a Vxmax Vymax velocity that starts with Vmax

    #1 Find the distance between the point in x and y

    #2 Search for right acceleration for each axis.
    ##1 Step 1 consider each axis indipendetly
    A.x,B.x = calcAB(A.x,B.x)
    A.y,B.y = calcAB(A.y,B.y)
    # if we found no "solution" step to previous element
    # we call it backfire, means the element A has a new constraint
    # either acceleration limit or speed limit
    if A.noBackfire() == False:
        logging.info("Fail\n"+infoStep(A,B))
        return False,A,B

    logging.info("Intermediate1 \n"+infoStep(A,B))

    #find the longest time of the 2 elements
    A,B = calcTime(A,B)

    logging.info("Intermediate1 \n"+infoStep(A,B))


    #Now the 2 elements are aligned in time
    #let's check that the max acceleration and max speed are ok
    while A.checkAcc() == False:
        #Acceleration constraing are not met
        #reduce max acceleration on both axes
        B.x.acc.max *= REDUCTION_FACTOR
        B.y.acc.max *= REDUCTION_FACTOR
        ret,A,B = calc(A,B,level)
        if ret == False:
            logging.info("Fail\n"+infoStep(A,B))
            return False,A,B


    while B.checkVel() == False:
        B.x.vel.max *= REDUCTION_FACTOR
        B.y.vel.max *= REDUCTION_FACTOR
        ret,A,B = calc(A,B,level)
        if ret == False:
            logging.info("Fail\n"+infoStep(A,B))
            return False,A,B
        
    #Solution found, return True and the values
    #logging.debug(infoNode("Aou",A,level-1) + infoNode("Bou",A,level-1))
    logging.info("Sucseed \n"+infoStep(A,B))
    return True,A,B

        
    


class element:
    def __init__(self,value,max):
        self.value = value
        self.max = max
    
    def string(self):
        stringa = "[value:"+str(self.value)+", max:"+str(self.max)+"]"
        return stringa

    def test(self):
        return abs(self.value) <= abs(self.max)
class Axis:
    def __init__(self,value,Vmax,Amax):
        self.pos = element(value,None)
        self.vel = element(0,Vmax)
        self.acc = element(0,Amax)
        self.time = element(0,0)
        self.state = STATE_INIT

    def string(self):
        stringa = "[pos:"+self.pos.string()+", vel"+self.vel.string()+", acc"+self.acc.string()+", state:"+self.state+"]"
        return stringa

class myPoint:
    def __init__(self, x, y, Vmax = 2, Amax = 1):
        self.x = Axis(x,Vmax,Amax)
        self.y = Axis(y,Vmax,Amax)
        self.Vmax = Vmax
        self.Amax = Amax
    
    def string(self,pad=""):
        stringa  = pad+"x"+self.x.string()+"\n"
        stringa += pad+"y"+self.y.string()+"\n"
        stringa += pad+"Vmax:"+str(self.Vmax)+",Amax:"+str(self.Amax)+"\n"
        return stringa
    
    
    def noBackfire(self):
        ret = True
        if self.x.state == STATE_BACKFIRE:
            #Speed is the output of backfire
            #we can restore the max acceleration limit
            self.x.acc.max = self.Amax
            ret = False
        if self.y.state == STATE_BACKFIRE:
            #Speed is the output of backfire
            #we can restore the max acceleration limit
            self.y.acc.max = self.Amax
            ret = False
        return ret

    
    def checkVel(self):
        #check if velocity of the 2 axis in lower than the velocity Max
        if self.x.vel.test() and self.y.vel.test():
            value = math.pow(self.x.vel.value,2) + math.pow(self.y.vel.value,2)
            if math.pow(self.Vmax,2) >= value:
                return True
        return False

    def checkAcc(self):
        #check if acc of the 2 axis in lower than the velocity Max
        if self.x.acc.test() and self.y.acc.test():
            value = math.pow(self.x.acc.value,2) + math.pow(self.y.acc.value,2)
            if math.pow(self.Amax,2) >= value:
                return True
        return False
   
    def setMaxVel(self,Vmax):
        self.x.vel.max = Vmax
        self.y.vel.max = Vmax

    def setMaxAcc(self,Amax):
        self.x.acc.max = Amax
        self.y.acc.max = Amax
    def setTargetVel(self,Vtarget):
        self.x.vel.value = Vtarget
        self.x.vel.max = Vtarget
        self.y.vel.value = Vtarget
        self.y.vel.max = Vtarget


class trajectoryFit:
    def __init__(self, listPoints):
        self.Points = []
        self.Vmax = 0
        self.Max = 0
        self.executionTime = 0
        for el in listPoints:
            self.Points.append(myPoint(el[0],el[1]))
    
    #Set the max velocity for the trajectory
    def setMaxVel(self, Vmax):
        self.Vmax = Vmax
        for el in self.Points:
            el.setMaxVel(Vmax)

    #Get the max velocity for the trajectory
    def getMaxVel(self):        
        return self.Vmax
    
    #Get the max acceleration for the trajectory
    def getMaxAcc(self):
        return self.Amax
        
    #Set the max acceleration for the entire trajectory
    def setMaxAcc(self, Amax):
        self.Amax = Amax
        for el in self.Points:
            el.setMaxAcc(Amax)
    
    def evaluate(self):
        #Set a reference time
        timex = time.time()
        #First and last points have target 0 speed
        #All other points we want to go as fast as possible
        #previously setMaxAcc and setMaxVel must be used
        self.Points[0].setTargetVel(0)
        self.Points[-1].setTargetVel(0)

        #We evaluate 2 point at the timne
        #A  to B
        #last point B is end of line so do not evaluate it (array -1)
        idx = 0
        while idx < (len(self.Points)-1):
            if idx == 10:
                print("start debug")
            logging.info("IDX:" +str(idx))
            #Check if thre is a valid fit for A->B
            ret,A,B = calc(self.Points[idx],self.Points[idx+1],0)
            #Found a solution move to next point
            if ret == True:
                idx+=1
            #No solution, revaluate the previous step if possible
            else:
                if (idx>0):
                    idx -= 1
                #If we fall back to the first element evaluation failed
                else:
                    print("ERROR")
                    return False
        #Store execution time
        self.executionTime = time.time() - timex
        return True


if __name__ == "__main__":
    #list of points
    a = []
    for b in range(10):
        a.append([b*0.1,b*0.2])
    for b in range(10):
        a.append([1-b*0.1,1-b*0.2])

    #create the trajectory using the list [[x1,y1]..]
    tf = trajectoryFit(a)

    #set max acceleration along the entire trajectory
    tf.setMaxAcc(1)

    #set max velocity along the entire trajectory
    tf.setMaxVel(2)

    #evalute the trajectory 
    ret = tf.evaluate()

    #Print out all the POS xy and their velocity
    if ret:
        for a in tf.Points:
            print("Pos:\n\t"+ str(a.x.pos.value)+" Vel:" + str(a.x.vel.value)+"\n\t"+ str(a.y.pos.value)+" Vel:" + str(a.y.vel.value))    
    else:
        print("Point calculation fail")

    #Tell the execution time
    print("Execution time:",tf.executionTime)