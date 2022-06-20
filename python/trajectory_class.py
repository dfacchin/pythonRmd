import numpy as np

'''
Index:
i = initial, f = final
S = shoulder, E = elbow
d = dot (derivative)
'''

# Variables

# time
dt = 0.1 # [s] time step
tEnd = 4 # [s] time in which we want the motion to be executed
t = np.linspace(0, dt, tEnd) # [s]

class Trajectory:

    def __init__(self, theta_i, theta_f, theta_d_i, theta_d_f):
        self.theta_i = theta_i

# Known conditions
# Use the IK (xi,yi) (xf,yf) to get --> (theta_i_S,theta_i_E) (theta_f_S,theta_f_E)

# initial position [deg]
theta_i_S = 45 
theta_i_E = 90 
# final position [deg]
theta_f_S = 90
theta_f_E = 0

# initial velocity [deg/s]
theta_d_i_S = 0
theta_d_i_E = 0
# final position [deg/s]
theta_d_f_S = 0
theta_d_f_E = 0

# Delta values
delta_theta = theta_f - theta_i
theta_d_sum = theta_d_f + theta_d_i

# c-coefficients
# Shoulder
c0 = theta_i
c1 = theta_d_i
c2 = ((3*delta_theta)/tEnd**2) - ((2*theta_d_i)/tEnd) - (theta_d_f/tEnd)
c3 = (-(2*delta_theta)/tEnd**3) + (theta_d_sum/tEnd**2)
# Elbow
c0 = theta_i
c1 = theta_d_i
c2 = ((3*delta_theta)/tEnd**2) - ((2*theta_d_i)/tEnd) - (theta_d_f/tEnd)
c3 = (-(2*delta_theta)/tEnd**3) + (theta_d_sum/tEnd**2)

print("c0: " + str(c0))
print("c1: " + str(c1))
print("c2: " + str(c2))
print("c3: " + str(c3))

# Cubic Polinomial [Trajectory of angular displacement]

theta = c0 + (c1*t) +(c2*t**2) + (c3*t**3)

# Cubic Polinomial [Trajectory of angular velocity]

theta_d = c1 + (2*c2*t) +(3*c3*t**2)
