import numpy as np


# Initial Conditions (i.c.):
# Define (time,pose,vel) for each path point
time = [0, 2, 4, 8, 10] # [s]
theta = [10, 20, 0, 30, 40] # [deg]
theta_d = [0] # [deg/s]

# Velocity in each segment
v = [] # create an empty list
for index, (elem_t,elem_theta) in enumerate(zip(time,theta)):
    if (index+1 < len(time)): # compute only until the second to last value
        v.append((theta[index+1]-theta[index])/(time[index+1]-time[index]))

# Velocity at each path point
for index, elem in enumerate(v):
    if (index+1 < len(v)):
        if np.sign(v[index]) == np.sign(v[index+1]):
            theta_d.append((v[index]+v[index+1])/2)
        elif np.sign(v[index]) != np.sign(v[index+1]):
            theta_d.append(0)
theta_d.append(0) # this represents the endpoint-velocity (i.c.)


# ----------------------------------------------------------
# Solve the Cubic Polinomial for each step:

for index, (el_time,el_theta,el_theta_d) in enumerate(zip(time,theta,theta_d)):
    t = np.linspace(time[index], time[index+1], steps) # [s] Time
    delta_theta_S = theta[index+1] - theta[index] # Delta value
    sum_theta_d_S = theta_d[index+1] + theta_d[index] # Sum

    # c-coefficients
    c0_S = theta[index]
    c1_S = theta_d[index]
    c2_S = ((3*delta_theta_S)/(time[index+1]-time[index])**2) - ((2*theta_d[index])/(time[index+1]-time[index])) - (theta_d[index]/(time[index+1]-time[index]))
    c3_S = (-(2*delta_theta_S)/(time[index+1]-time[index])**3) + (sum_theta_d_S/(time[index+1]-time[index])**2)

    # Cubic Polinomial [Trajectory of angular displacement]
    theta_S = c0_S + (c1_S*(t-time[index])) + (c2_S*(t-time[index])**2) + (c3_S*(t-time[index])**3) # [deg] Shoulder
    # Cubic Polinomial [Trajectory of angular velocity]
    theta_d_S = c1_S + (2*c2_S*(t-time[index])) + (3*c3_S*(t-time[index])**2) # [deg/s] Shoulder

    # Note: the variables that this function returns are arrays
    #return theta_S, theta_d_S
