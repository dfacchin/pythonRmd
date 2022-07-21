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
print("v: " + str(v))

# Velocity at each path point
for index, elem in enumerate(v):
    if (index+1 < len(v)):
        if np.sign(v[index]) == np.sign(v[index+1]):
            theta_d.append((v[index]+v[index+1])/2)
        elif np.sign(v[index]) != np.sign(v[index+1]):
            theta_d.append(0)
theta_d.append(0) # this represents the endpoint-velocity (i.c.)
print("theta_d: " + str(theta_d))

# ----------------------------------------------------------
# Solve the Cubic Polinomial for each step:
steps = 6
for index, (el_time,el_theta,el_theta_d) in enumerate(zip(time,theta,theta_d)):
    if (index+1 < len(theta)):
        t = np.linspace(time[index], time[index+1], steps) # [s] Time

        print("theta[index]: " + str(theta[index]))
        print("theta[index+1]: " + str(theta[index+1]))
        print("theta_d[index]: " + str(theta_d[index]))
        print("theta_d[index+1]: " + str(theta_d[index+1]))

        # c-coefficients
        c0_S = theta[index]
        c1_S = theta_d[index]
        c2_S = ((-3*(theta[index]-theta[index+1])) - (2*theta_d[index] + theta_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**2
        c3_S = ((2*(theta[index]-theta[index+1])) + (theta_d[index] + theta_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**3

        print("c0_S: " + str(c0_S))
        print("c1_S: " + str(c1_S))
        print("c2_S: " + str(c2_S))
        print("c3_S: " + str(c3_S))
        # Cubic Polinomial [Trajectory of angular displacement]
        theta_S = c0_S + (c1_S*(t-time[index])) + (c2_S*(t-time[index])**2) + (c3_S*(t-time[index])**3) # [deg] Shoulder
        # Cubic Polinomial [Trajectory of angular velocity]
        theta_d_S = c1_S + (2*c2_S*(t-time[index])) + (3*c3_S*(t-time[index])**2) # [deg/s] Shoulder

        # Note: the variables that this function returns are arrays
        #return theta_S, theta_d_S

        print("theta_S: " + str(theta_S))
        print("theta_d_S: " + str(theta_d_S))