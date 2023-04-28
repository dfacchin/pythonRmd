""" Trajectory fit takes a list of points in space, and based on acceleration and speed 
    constraints will assign a time to each point at which constraints are maintained true

    First and last point of the path (x,y) are set to be at 0 velocity

    vectorV is the sqrt(Vx^2+Vy^2)
    vectorA is the sqrt(Ax^2+Ay^2)
"""

def calcAtoB(pointA,pointB):
    """
    #A and B are two myPoint in space xy
    #A is the starting point of the sequence going to B
    #A has a Vx Vy component
    
    #Rule to apply
    1) NEVER have a vecotor velocity higher than the Vmax
    2) NEVER apply acceleration higher Amax between the 2 points

    Results:
    1 move on a straight line with constant velocity keeping Vvecotr costant from the starting point      
    2 move from A to B with a uniform accelerated acceleration

    result will be:
    time needed to reach point B
    V at point B (Vx, Vy)


    How to perform the calc:
    if I were to move on 1 dimension we can use the formula
    t = (sqrt((2d/a) + (v_i^2)) - v_i) / a
    this gives us the time with time we can fill the B time and V
    if V is higher than the expected we need to reduce the acceleration
        if we were accelerating 
            we can decrees the acceleration
        if we were deccelerating
            we need to reduce the previous target velocity and redu the calcs, otherwise we will not fit into the curve
    if V is lower than the expected:
        if we were accelerating 
            we need to increase the previous target velocity and redu the calcs, otherwise we will not fit into the curve
        if we were deccelerating (-)
            we can decrees the acceleration (less decceleration)
    What when we start point 0 is V0
    Point 1 is set to be MAX velocity
    We accelerate at max, but at point 1 velocity is lower than maxV
    we are lower and are accelerating, in this case we need to "increase previous point"
    this is not possible start is 0, we should be able to accept this.

    Vmax should not be the target velocity
    we should just check if we can reach the point from 0 to 1 using at max vectorA
    for example if from point A to point B
    A is still and we go to point B, it must be "physically" possible to do so
    A-B:
    Av=0 time is based on distance and acceleration
    imposing max acceleration we have a time

    """
    pass

"""
The formula to calculate time taken to cover a specific distance with starting speed and constant acceleration is given by:

t = (sqrt(2 * s / a + u^2) - u) / a

where

t is the time taken to cover the distance
s is the distance covered
u is the initial velocity
a is the acceleration
This formula can be derived from the kinematic equation:

s = ut + 1/2 at^2

where

s is the distance covered
u is the initial velocity
a is the acceleration
t is the time taken to cover the distance
I hope this helps! Let me know if you have any other questions.
"""
import math

STATE_INIT = 0
STATE_DONE = 1
STATE_NEXT = 2
STATE_BACKFIRE = 3
STATE_ERROR_ACC = 4

def calc_time(d,a,v):
    t = (math.sqrt((2*d)/a + v*v)-v)/a
    return t
def calc_a(d,vi,vf):
    a = (vf*vf-vi*vi)/(2*d)
    return a 
def calc_t(vi,vf,a):
    t = (vf-vi)/a
    return t
def calc_t_dva(d,vi,a):
    t = (math.sqrt((2*d*a) + (vi*vi)) - vi) / a
    return t
def cald_d(vi,a,t):
    d = vi*t + (a*t*t)/2
    return d
def calc_a_dvt(d,v,t):
    a = (d-v*t)*(2/(t*t))
    return a
def calc_vf_dva(d,vi,a):
    #works if it "goes" straight
    vf = math.sqrt(2*a*d+vi*vi)
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
            B.time.value = d/A.vel.value

        else:
            #calculate the max acceleration required to reach speed at B
            #with final speed Vmax
            acc = calc_a(d, A.vel.value, B.vel.max)
            #if the acceleration exceeds max acceleration
            if abs(acc) > B.acc.max:
                #ideal acceleration leads to speed exceeding limit
                #if the desired acceleration is negative set -Amax
                if acc < 0:
                    acc = -B.acc.max
                else:
                    acc = B.acc.max
                #with the new acceleration the max speed will be lower                 
                vel = calc_vf_dva(d, A.vel.value, acc)
            if acc != 0:
                #with know initial Velocity, max speed, and acceleration we can calculate time
                tim = calc_t(A.vel.value, vel, acc)
                #just for test knowing distance, initial speed and acceleration
                #t1 = calc_t_dva(d, A.vel.value, acc)
                #print(B.time.value, t1)
            else:
                tim = d/A.vel.value

            #REQ1 
            A.acc.value = acc
            #REQ2 
            B.vel.value = vel
            #REQ3 no change to the max possibile speed
            B.vel.max = B.vel.max
            #REQ4 
            B.time.value = tim 
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

def calc(A,B):
    #A has a starting V
    #A B both have a Vxmax Vymax velocity that starts with Vmax

    #1 Find the distance between the point in x and y

    #2 Search for right acceleration for each axis.
    ##1 Step 1 consider each axis indipendetly
    A.x,B.x = calcAB(A.x,B.x)
    A.x,B.x = calcAB(A.y,B.y)
    #if we found no "solution" step to previous element
    if A.noBackfire() == False:
        return False,A,B

    #find the longest time of the 2 elements
    A,B = calcTime(A,B)

    #Now the 2 elements are aligned in time
    #let's check that the max acceleration and max speed are ok
    if A.checkAcc() == False:
        ret = False
        while ret == False:
            #Too much acceleration 
            #reduce limit by 10%
            B.x.acc.max = A.x.acc.value * 0.9
            B.y.acc.max = A.y.acc.value * 0.9
            ret,A,B = calc(A,B)

    if B.checkSpeed() == False:
        ret = False
        while ret == False:
            #Reduce axis speed 
            #reduce limit by 10%
            B.x.vel.max = A.x.acc.value * 0.9
            B.y.vel.max = A.y.acc.value * 0.9
            ret,A,B = calc(A,B)
    
    #Solution found, return True and the values
    return True,A,B

        
    


class element:
    def __init__(self,value,max):
        self.value = value
        self.max = max

    def test(self):
        return abs(self.value) <= abs(self.max)
class Axis:
    def __init__(self,value,Vmax,Amax):
        self.pos = element(value,None)
        self.vel = element(0,Vmax)
        self.acc = element(0,Amax)
        self.time = element(0,0)
        self.state = STATE_INIT

class myPoint:
    def __init__(self, x, y, Vmax = 2, Amax = 1):
        self.x = Axis(x,Vmax,Amax)
        self.y = Axis(y,Vmax,Amax)
        self.Vmax = Vmax
        self.Amax = Amax
    
    
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
            value = self.x.vel.value^2 + self.y.vel.value^2
            if (self.Vmax^2) > value:
                return True
        return False

    def checkAcc(self):
        #check if acc of the 2 axis in lower than the velocity Max
        if self.x.acc.test() and self.y.acc.test():
            value = self.x.acc.value^2 + self.y.acc.value^2
            if (self.Amax^2) > value:
                return True
        return False
   
    def setMaxSpeed(self,Vmax):
        self.x.vel.max = Vmax
        self.y.vel.max = Vmax

    def setMaxAcceleration(self,Amax):
        self.x.acc.max = Amax
        self.y.acc.max = Amax
    def setTargetSpeed(self,Vtarget):
        self.x.vel.value = Vtarget
        self.x.vel.max = Vtarget
        self.y.vel.value = Vtarget
        self.y.vel.max = Vtarget


class trajectoryFit:
    def __init__(self, listPoints):
        self.Points = []
        for el in listPoints:
            self.Points.append(el)
    
    def setMaxSpeed(self, Vmax):
        for el in self.Points:
            el.setMaxSpeed(Vmax)

    def setMaxVelocity(self, Amax):
        for el in self.Points:
            el.setMaxAcceleration(Amax)
    
    def evaluate(self):
        #First and last points have target 0 speed
        #All other points we want to go as fast as possible
        self.Points[0].setTargetSpeed(0)
        self.Points[-1].setTargetSpeed(0)
        for el in self.Points[1:-1]:
            el.setTargetSpeed(el.getMaxSpeed())


            



def trajectoryToPoints(distance):
    a = [[0,0],[1,0],[2,0],[3,0],[3,1],[3,2],[2,2]]
    return a





if __name__ == "__main__":
    """
    while True:
        try:
            a = float(input("a:"))
            b = float(input("b:"))
            Vi = float(input("Vi:"))
            Vmax = float(input("Vmax:"))
            Amax = float(input("Amax:"))
            print(calcAB(a,b,Vi,Vmax,Amax))
        except:
            pass
    """
    a = [[0,0],[1,0],[2,0],[3,0],[3,1],[3,2],[2,2]]
    A = myPoint(a[0][0],a[0][1])
    B = myPoint(a[1][0],a[1][1])

    calc(A,B)
    """
    # Get a list of points from a trajectory
    # points must be of a specified distance between them
    listPoints = trajectoryToPoints(5)
    myTrajectory = trajectoryFit(listPoints)
    """