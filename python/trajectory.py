import numpy as np

'''
Index:
i = initial, f = final
S = shoulder, E = elbow
d = dot (derivative)
'''

# Variables

# time
dt = 1 # [s] time step
tEnd = 4 # [s] time in which we want the motion to be executed
t = np.linspace(0, dt, tEnd) # [s]

# Known conditions
# Use the IK (xi,yi) (xf,yf) to get --> (theta_i_S,theta_i_E) (theta_f_S,theta_f_E)

# initial position [deg]
theta_i_S = 20
theta_i_E = 90 
# final position [deg]
theta_f_S = 80
theta_f_E = 20

# initial velocity [deg/s]
theta_d_i_S = 0
theta_d_i_E = 0
# final position [deg/s]
theta_d_f_S = 0
theta_d_f_E = 0

# Delta values (Shoulder)
delta_theta_S = theta_f_S - theta_i_S
theta_d_sum_S = theta_d_f_S + theta_d_i_S
# Delta values (Elbow)
delta_theta_E = theta_f_E - theta_i_E
theta_d_sum_E = theta_d_f_E + theta_d_i_E

# c-coefficients
# Shoulder
c0_S = theta_i_S
c1_S = theta_d_i_S
c2_S = ((3*delta_theta_S)/tEnd**2) - ((2*theta_d_i_S)/tEnd) - (theta_d_f_S/tEnd)
c3_S = (-(2*delta_theta_S)/tEnd**3) + (theta_d_sum_S/tEnd**2)
# Elbow
c0_E = theta_i_E
c1_E = theta_d_i_E
c2_E = ((3*delta_theta_E)/tEnd**2) - ((2*theta_d_i_E)/tEnd) - (theta_d_f_E/tEnd)
c3_E = (-(2*delta_theta_E)/tEnd**3) + (theta_d_sum_E/tEnd**2)

print("Shoulder")
print("c0: " + str(c0_S))
print("c1: " + str(c1_S))
print("c2: " + str(c2_S))
print("c3: " + str(c3_S))
print("Elbow")
print("c0: " + str(c0_E))
print("c1: " + str(c1_E))
print("c2: " + str(c2_E))
print("c3: " + str(c3_E))

# Cubic Polinomial [Trajectory of angular displacement]

# Shoulder
theta_S = c0_S + (c1_S*t) +(c2_S*t**2) + (c3_S*t**3)
# Elbow
theta_E = c0_E + (c1_E*t) +(c2_E*t**2) + (c3_E*t**3)

# Cubic Polinomial [Trajectory of angular velocity]

# Shoulder
theta_d_S = c1_S + (2*c2_S*t) +(3*c3_S*t**2)
# Elbow
theta_d_E = c1_E + (2*c2_E*t) +(3*c3_E*t**2)

print("theta_S: " + str(theta_S))
print("theta_E: " + str(theta_E))
print("theta_d_S: " + str(theta_d_S))
print("theta_d_E: " + str(theta_d_E))