""" Trajectory fit takes a list of points in space, and based on acceleration and speed 
    constraints will assign a time to each point at which constraints are maintained true

    First and last point of the path (x,y) are set to be at 0 velocity

    vectorV is the sqrt(Vx^2+Vy^2)
    vectorA is the sqrt(Ax^2+Ay^2)
"""
import time
import logging
import math
from trajectoryfunctions import *

CORRECTION_MARGIN = 0.98
REDUCTION_FACTOR = 0.98
VEL_TOLLERANCE = 0.05
ACC_TOLLERANCE = 0.05

STATE_INIT = "INIT"
STATE_DONE = "DONE"
STATE_NEXT = "NEXT"
STATE_BACKFIRE = "BACKFIRE"
STATE_ERROR_ACC = "ERROR_ACC"

#logging.basicConfig(level=logging.CRITICAL)
logging.basicConfig(level=logging.INFO)

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
    sign = 1
    if d < 0:
        sign = -1
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
        if (A.vel.value == B.vel.max) and (sign > 0):
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
        if (A.vel.value == -B.vel.max) and (sign < 0):
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

            # 1 initial speed and final speed must be of the same "sign"
            # speed sign must be of the same sign of the direction
            if sign == 1:
                if A.vel.value >= 0:                    
                    velf = abs(B.vel.max*CORRECTION_MARGIN)
                    acc = calc_a(d, A.vel.value, velf)
                else:
                    #start velocity can't be of opposite direction
                    A.vel.max = 0.0
                    A.state = STATE_BACKFIRE
                    B.state = STATE_INIT
                    return A,B
            elif sign == -1:
                if A.vel.value <= 0:
                    velf = abs(B.vel.max*CORRECTION_MARGIN) * -1
                    #due to the direction negative the acceleration will flip sign as expected
                    acc = calc_a(d, A.vel.value, velf)
                else:
                    #start velocity can't be of opposite direction
                    A.vel.max = 0.0
                    A.state = STATE_BACKFIRE
                    B.state = STATE_INIT
                    return A,B


            #if the acceleration exceeds max acceleration
            if abs(acc) > abs(A.acc.max):
                #ideal acceleration leads to speed exceeding limit
                #if the desired acceleration is negative set -Amax
                if acc < 0:
                    acc = -A.acc.max*CORRECTION_MARGIN
                else:
                    acc = A.acc.max*CORRECTION_MARGIN
                                
                #with the new acceleration the max speed will be lower  
                if sign == 1:               
                    velf = calc_vf_dva(d, A.vel.value, acc)
                else:
                    #invert all the signs
                    velf = -calc_vf_dva(-d, -A.vel.value, -acc)
            if acc != 0:
                #with know initial Velocity, max speed, and acceleration we can calculate time
                tim = calc_t(A.vel.value, velf, acc)
                #just for test knowing distance, initial speed and acceleration
                t1 = calc_t_dva(d, A.vel.value, acc)
                #print(B.time.value, t1)
            else:
                try:
                    tim = d/A.vel.value
                except:
                    tim = 0.0

            #Check if time is negative something is not right
            if tim < 0:
                if d>0:
                    vmax = calc_vf_dva(d, B.vel.max, A.acc.max*CORRECTION_MARGIN)
                else:
                    vmax = calc_vf_dva(d, B.vel.max, -A.acc.max*CORRECTION_MARGIN)
                A.vel.max = abs(vmax)
                A.state = STATE_BACKFIRE
                B.state = STATE_INIT
                return A,B                    
            #Need to check the if the final speed in in between the limits
            if sign == 1:
                if velf > B.vel.max:
                    vmax = calc_vf_dva(d, B.vel.max, A.acc.max*CORRECTION_MARGIN)
                    A.vel.max = abs(vmax)
                    A.state = STATE_BACKFIRE
                    B.state = STATE_INIT
                    return A,B        
            if sign == -1:
                if velf < -B.vel.max:
                    vmax = -calc_vf_dva(-d, B.vel.max, A.acc.max*CORRECTION_MARGIN)
                    A.vel.max = abs(vmax)
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
    To reach B in t having a specific speed in A
    B has a max speed limit
    A has a max acceleration limit

    If in B there is a tight constraing on velocity there is only a solution:
    Ex1:
    From A(p:0,v:0) to B(p:1,v:<=33) t = 2
    the distance is 1, we can tune the acceleration to cover the distance in t=2 having a final speed
    a = (d-v*t)*(2/(t*t))
    vf = math.sqrt(2*a*d+vi*vi)    
    if a is in the acceleration limit and vf is in the permitted range of final velocity we have a solution
    a = 0.5 v = 1.0 all stays in the limit

    Ex2:
    (A(p:0,v=3),B(p:1,v<=1)) t=2
    in this case  
    a = (d-v*t)*(2/(t*t))
    a = -2.5 v=2.0 
    too much acceleration is need

    """
    d = B.pos.value - A.pos.value
    sign = 1
    if d < 0:
        sign = -1
    
    if sign == 1:
        if A.vel.value < 0: 
            print("ERROR velocity is negative when moving to")
            input()
        a = calc_a_dvt(d,A.vel.value,t)
        if (a <= A.acc.max) and (a >= -A.acc.max):
            vf = calc_vf_dvt(d,A.vel.value,t)
            if abs(vf)<0.01:
                vf = 0.0
            if (vf <= B.vel.max):# and (vf >=0):
                B.vel.value = vf
                A.acc.value = a
                B.time.value = t
                A.state = STATE_DONE
                B.state = STATE_NEXT
                return A,B
            else:
                #Out of velocity
                #What is the velocity in A that with max acc fits vel constraint in B?
                #it also means we were decelerating
                vf = calc_vf_dvt(d,B.vel.max,t)
                A.vel.max = abs(vf)
                A.state = STATE_BACKFIRE
                B.state = STATE_INIT
                return A,B
        else:
            #too much acceleration
            #Actual velocity is not compatible with 
            #distance and time constraint
            if a > 0:
                v= calc_vi_dat(d,A.acc.max,t)
            if a < 0:
                v= calc_vi_dat(d,-A.acc.max,t)
            A.vel.max = abs(v)
            A.state = STATE_BACKFIRE
            B.state = STATE_INIT
            return A,B            
    if sign == -1:
        if A.vel.value > 0: 
            print("ERROR velocity is negative when moving to")
            input()
        a = -calc_a_dvt(-d,-A.vel.value,t)
        if (a <= A.acc.max) and (a >= -A.acc.max):
            vf = -calc_vf_dvt(-d,-A.vel.value,t)
            if abs(vf)<0.01:
                vf = 0.0
            if (vf > -B.vel.max):# and (vf <= 0):
                B.vel.value = vf
                A.acc.value = a
                B.time.value = t
                A.state = STATE_DONE
                B.state = STATE_NEXT
                return A,B
            else:
                #Out of velocity
                #What is the velocity in A that with max acc fits vel constraint in B?
                #it also means we were decelerating
                vf = -calc_vf_dvt(-d,B.vel.max,t)
                A.vel.max = abs(vf)
                A.state = STATE_BACKFIRE
                B.state = STATE_INIT
                return A,B
        else:
            #too much acceleration
            #Actual velocity is not compatible with 
            #distance and time constraint
            if a > 0:
                v= calc_vi_dat(-d,A.acc.max,t)
            if a < 0:
                v= calc_vi_dat(-d,-A.acc.max,t)            
            A.vel.max = abs(v)
            A.state = STATE_BACKFIRE
            B.state = STATE_INIT
            return A,B  

def calcTime(A,B):
    tx = B.x.time.value
    ty = B.y.time.value
    #time clould be a little different
    tx = round(tx,2)
    ty = round(ty,2)
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

def infoStepold(A,B):
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
    stra += "--- SUM\n"
    stra += "S:"+str(A.xy.vel.value)+"->"+str(B.xy.vel.value)+"_"+str(A.xy.vel.max)+"->"+str(B.xy.vel.max)+"\n"
    stra += "A:"+str(A.xy.acc.value)+"->"+str(B.xy.acc.value)+"_"+str(A.xy.acc.max)+"->"+str(B.xy.acc.max)+"\n"
    stra += "---\n"
    return stra

def infoStep(A,B):
    stra = str(B.x.pos.value - A.x.pos.value)+"->"+str(A.x.vel.value)+"_"+str(A.x.acc.max)+"->"+str(B.x.vel.max)+"\n"
    stra += str(B.y.pos.value - A.y.pos.value)+"->"+str(A.y.vel.value)+"_"+str(A.y.acc.max)+"->"+str(B.y.vel.max)+"\n"
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
    #Check if the speed in B is not exceeding the imposed limit
    #if it's the case, set the max A state that will permit B to reach it's condition
    if A.noBackfire() == False:
        logging.info("Fail\n"+infoStep(A,B))
        return False,A,B

    logging.info("Intermediate1 \n"+infoStep(A,B))


    #Now the 2 elements are aligned in time
    #let's check that the max acceleration and max speed are ok
    A.update()
    B.update()
    while A.checkAcc() == False:
        #Acceleration constraing are not met
        #reduce max acceleration on both axes by normalizing the combined acceleration
        ratio = A.xy.acc.max / A.xy.acc.value
        #apply a reduction factor for safety
        ratio *= REDUCTION_FACTOR
        A.x.acc.max = abs(A.x.acc.value * ratio)
        A.y.acc.max = abs(A.y.acc.value * ratio)
        ret,A,B = calc(A,B,level)
        A.update()
        B.update()
        if ret == False:
            logging.info("Fail\n"+infoStep(A,B))
            return False,A,B

    A.update()
    B.update()
    while B.checkVel() == False:
       #reduce max acceleration on both axes by normalizing the combined acceleration
        ratio = B.xy.vel.max / B.xy.vel.value
        #apply a reduction factor for safety
        ratio *= REDUCTION_FACTOR
        B.x.vel.max = abs(B.x.vel.value * ratio)
        B.y.vel.max = abs(B.y.vel.value * ratio)
        ret,A,B = calc(A,B,level)
        A.update()
        B.update()
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
        #combined value
        self.xy = Axis(y,Vmax,Amax)
        self.update()
        self.Vmax = Vmax
        self.Amax = Amax
    
    def update(self):
        self.xy.vel.value = math.sqrt(math.pow(self.x.vel.value,2)+math.pow(self.y.vel.value,2))
        self.xy.acc.value = math.sqrt(math.pow(self.x.acc.value,2)+math.pow(self.y.acc.value,2))

    def string(self,pad=""):
        stringa  = pad+"x"+self.x.string()+"\n"
        stringa += pad+"y"+self.y.string()+"\n"
        stringa += pad+"Vmax:"+str(self.Vmax)+",Amax:"+str(self.Amax)+"\n"
        return stringa
    
    
    def noBackfire(self):
        ret = True
        if self.x.state == STATE_BACKFIRE:
            logging.info("X axis backfire")
            #Speed is the output of backfire
            #we can restore the max acceleration limit
            self.x.acc.max = self.Amax
            ret = False
        if self.y.state == STATE_BACKFIRE:
            logging.info("Y axis backfire")
            #Speed is the output of backfire
            #we can restore the max acceleration limit
            self.y.acc.max = self.Amax
            ret = False
        return ret

    
    def checkVel(self):
        #check if velocity of the 2 axis in lower than the velocity Max
        if self.xy.vel.value <= (self.xy.vel.max+VEL_TOLLERANCE):
            return True
        return False

    def checkAcc(self):
        #check if acc of the 2 axis in lower than the velocity Max
        if self.xy.acc.value <= (self.xy.acc.max+ACC_TOLLERANCE):
            return True
        return False
   
    def setMaxVel(self,Vmax):
        self.x.vel.max = Vmax
        self.y.vel.max = Vmax
        self.xy.vel.max = Vmax
    def setMaxAcc(self,Amax):
        self.x.acc.max = Amax
        self.y.acc.max = Amax
        self.xy.acc.max = Amax
    def setTargetVel(self,Vtarget):
        self.x.vel.value = Vtarget
        self.x.vel.max = Vtarget
        self.y.vel.value = Vtarget
        self.y.vel.max = Vtarget
        self.xy.vel.value = Vtarget
        self.xy.vel.max = Vtarget


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
        count = 0
        while idx < (len(self.Points)-1):
            if idx == 31:
                print("start debug")
            if count == 104:
                print("start debug")
            logging.critical("IDX:" +str(idx))
            #logging.critical("count:" +str(count))
            count+=1
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
                    #print("ERROR")
                    #return False
                    print("Revalate the first point")
        #Store execution time
        self.executionTime = time.time() - timex
        return True



from trajectory import *

if __name__ == "__main__":

    #Points = [[0,0],[0,200],[0,400],[200,400],[500,400],[800,400],[400,405]]
    #Points = [[0,200], [-300,400], [0,502],[300,600], [0,600], [0,800], [0,1000], [0,1200]]
    #Points = [[0,200], [-300,400],[300,600], [0,600], [0,800]]
    #Points = [[0,200], [-300,400], [300,600], [0,800], [0,1000], [0,1200], [0,1500]]
    #Points = [[0,200], [0,400], [150,400], [300,400], [300,100], [800, 600], [0, 1000], [500, 1000]]
    #Points = [[0,200], [0,400], [300,400], [300,-300],[-300,-400], [0, 1000], [500, 1000],[0,200], [-300,400], [300,600]]
    Points = [[0,0],[-400,400],[0,600]]
    #Points = [[0,0],[500,800]]


    # Generate the trajectory
    traj1 = TrajectoryPlanner(Points)
    traj1.parabolic_path()
  
    # Generate equally spaced lines
    traj1.equally_spaced_lines()

    """
    # Plot
    import matplotlib.pyplot as plt
    
    # path points
    for pp in traj1.pp:
        plt.plot(pp[0],pp[1], marker=(5,0), label="pp")

    # # parabola start
    # for s in traj1.p_start:
    #     plt.plot(s[0],s[1], marker=".", label="p_start")

    # # parabola end
    # for e in traj1.p_end:
    #     plt.plot(e[0],e[1], marker=(5,2), label="p_end")

    # parabola vertex
    #plt.plot(, marker=(5,2), label="p_vertex")


    plt.plot(traj1.equal_traj_x, traj1.equal_traj_y, marker=(5,2), label="lin")

    # Set equal axis aspect
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    
    plt.xlabel("x")
    plt.ylabel("y")

    plt.legend()
    plt.show()
    """
    a = traj1.equal_traj_xy

    #sinmple trajectory
    a = []
    steps = 50
    for c in range(steps):
        a.append([0.1*c,0.2*c])
    # for c in range(steps):
    #     a.append([steps*0.1-0.1*c,steps*0.2-0.2*c])

    #create the trajectory using the list [[x1,y1]..]
    tf = trajectoryFit(a)

    #set max acceleration along the entire trajectory
    tf.setMaxAcc(1)

    #set max velocity along the entire trajectory
    tf.setMaxVel(2)

    #evalute the trajectory 
    ret = tf.evaluate()

    # variables
    t = []
    x = []
    y = []
    vx = []
    vy = []
    ax = []
    ay = []


    #Print out all the POS xy and their velocity
    if ret:
        prev_t = 0

        for idx,a in enumerate(tf.Points):
            #print("Pos: t("+str(a.x.time.value)+")\n\t"+ str(a.x.pos.value)+" Vel:" + str(a.x.vel.value)+"\n\t"+ str(a.y.pos.value)+" Vel:" + str(a.y.vel.value)+"\n\tAcc"+ str(a.x.acc.value)+" Vel:" + str(a.y.acc.value))    
            
            multip = 1
            if idx == 0:
                t.append(round(a.x.time.value,3))
                x.append(round(a.x.pos.value,3) * multip)
                y.append(round(a.y.pos.value,3) * multip)
                vx.append(round(a.x.vel.value,3) * multip)
                vy.append(round(a.y.vel.value,3) * multip)
                ax.append(round(a.x.acc.value,3) * multip)
                ay.append(round(a.y.acc.value,3) * multip)
                prev_t += a.x.time.value

            else:
                t.append(round(prev_t + a.x.time.value,3))  
                x.append(round(a.x.pos.value,3) * multip)
                y.append(round(a.y.pos.value,3) * multip)
                vx.append(round(a.x.vel.value,3) * multip)
                vy.append(round(a.y.vel.value,3) * multip)
                ax.append(round(a.x.acc.value,3) * multip)
                ay.append(round(a.y.acc.value,3) * multip)
                prev_t += a.x.time.value
    
    else:
        print("Point calculation fail")

    import numpy as np

    # ti = np.linspace(0,29.3,100)
    # ti = list(ti)

    print("t: \n", t, "\n len t: ", len(t))

    print("x: \n", x, "\n len x: ", len(x))
    print("y: \n", y, "\n len y: ", len(y))

    print("vx: \n", vx, "\n len vx: ", len(vx))
    print("vy: \n", vy, "\n len vy: ", len(vy))

    print("ax: \n", ax, "\n len ax: ", len(ax))
    print("ay: \n", ay, "\n len ay: ", len(ay))

    #Tell the execution time
    print("Execution time:",tf.executionTime)