import numpy as np

# Variables
'''
pos_target_i
pos_target_f
vel_target_i
vel_target_f
ti
tf
steps
'''

# Initial Conditions (i.c.):
# Define (time,pose,vel) for each path point
t = [0, 2, 4, 8, 10] # [s]
theta = [10, 20, 0, 30, 40] # [deg]
theta_d = [0] # [deg/s]

# Velocity in each segment
v = [] # create an empty list
for index, (elem_t,elem_theta) in enumerate(zip(t,theta)):
    if (index+1 < len(t)): # compute only until the second to last value
        v.append((theta[index+1]-theta[index])/(t[index+1]-t[index]))

# Velocity at each path point
for index, elem in enumerate(v):
    if (index+1 < len(v)):
        if np.sign(v[index]) == np.sign(v[index+1]):
            theta_d.append((v[index]+v[index+1])/2)
        elif np.sign(v[index]) != np.sign(v[index+1]):
            theta_d.append(0)
theta_d.append(0) # this represents the endpoint-velocity (i.c.)



'''
# ----------------------------------------------------------
# Solve the Cubic Polinomial for each step:
# Time
t = np.linspace(ti, tf, steps) # [s]

# Delta values (Shoulder)
delta_theta_S = pos_target_f[0] - pos_target_i[0]
theta_d_sum_S = vel_target_f[0] + vel_target_i[0]
# c-coefficients
# Shoulder
c0_S = pos_target_i[0]
c1_S = vel_target_i[0]
c2_S = ((3*delta_theta_S)/(tf-ti)**2) - ((2*vel_target_i[0])/(tf-ti)) - (vel_target_f[0]/(tf-ti))
c3_S = (-(2*delta_theta_S)/(tf-ti)**3) + (theta_d_sum_S/(tf-ti)**2)

# Cubic Polinomial [Trajectory of angular displacement]
theta_S = c0_S + (c1_S*(t-ti)) + (c2_S*(t-ti)**2) + (c3_S*(t-ti)**3) # [deg] Shoulder
# Cubic Polinomial [Trajectory of angular velocity]
theta_d_S = c1_S + (2*c2_S*(t-ti)) + (3*c3_S*(t-ti)**2) # [deg/s] Shoulder

# Note: the variables that this function returns are arrays
return theta_S, theta_d_S
'''