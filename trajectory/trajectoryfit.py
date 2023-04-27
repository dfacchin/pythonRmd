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
def calcAB(posA,posB,Vi,Vmax,Amax):
    d = posB-posA
    #check if we need to change speed
    if Vi == Vmax:
        #moving already at the right speed, no acceleration
        a = 0
        #time is space divide by speed
        t = d/Vi
    else:
        #calculate the max acceleration required to reach speed at B
        #with final speed Vmax
        a = calc_a(d,Vi,Vmax)
        #if the acceleration exceeds max acceleration
        if abs(a) > Amax:
            #ideal acceleration leads to speed exceeding limit
            #if the desired acceleration is negative set -Amax
            if a < 0:
                a = -Amax
            else:
                a = Amax
            #with the new acceleration the max speed will be lower
            Vmax = calc_vf_dva(d,Vi,a)
        if a!=0:
            #with know initial Velocity, max speed, and acceleration we can calculate time
            t = calc_t(Vi, Vmax, a)
            #just for test knowing distance, initial speed and acceleration
            t1 = calc_t_dva(d,Vi,a)
            print(t,t1)
        else:
            t = d/Vi
    return (Vmax,t)


def calc(A,B):
    #A has a starting V
    #A B both have a Vxmax Vymax velocity that starts with Vmax

    #1 Find the distance between the point in x and y
    d = B-A

    #2 Search for right acceleration for each axis.

    #check if we need to change speed
    if A.Vx == B.Vxmax:
        ax = 0
        tx = d[a]/A.Vx
    else:
        #calculate the max acceleration required to reach speed at B
        ax = calc_a(d[0],A.Vx,B.Vxmax)
        #if the acceleration exceeds max acceleration
        if abs(ax) > B.Axmax:
            ax = B.Axmax
            B.Vxmax = calc_vf_dva(d[0],A.Vx,ax)
        tx = calc_t(A.Vx,B.Vxmax,ax)

        
    





class myPoint:
    def __init__(self, x, y, Vmax = 100, Amax = 50):
        self.x = x
        self.y = y
        self.Vmax = Vmax
        self.Vxmax = Vmax
        self.Vymax = Vmax
        self.Amax = Amax
        self.Axmax = Amax
        self.Aymax = Amax
        self.Vx = 0
        self.Vy = 0
        self.Vtarget = 0
    
    def setMaxSpeed(self,Vmax):
        self.Vmax = Vmax
    def getMaxSpeed(self):
        return self.Vmax
    def setMaxAcceleration(self,Amax):
        self.Vmax = Amax
    def setTargetSpeed(self,Vtarget):
        self.Vtarget = self.Vmax

    def __sub__(self,other):
        x = self.x - other.x
        y = self.y - other.y
        return (x,y)

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
    print(B-A)
    # Get a list of points from a trajectory
    # points must be of a specified distance between them
    listPoints = trajectoryToPoints(5)
    myTrajectory = trajectoryFit(listPoints)
    """