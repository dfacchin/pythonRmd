import numpy as np


# Initial Conditions (i.c.):
# Define (time,pose,vel) for each path point
time = [0, 2, 4, 8, 10] # [s]
theta_S = [10, 20, 0, 30, 40] # [deg]
theta_S_d = [0] # [deg/s]
theta_E = [10, 20, 0, 30, 40] # [deg]
theta_E_d = [0] # [deg/s]


# Velocity in each segment
v_S = [] # Shoulder
for index, (elem_t,elem_theta_S) in enumerate(zip(time,theta_S)):
    if (index+1 < len(time)): # compute only until the second to last value
        v_S.append((theta_S[index+1]-theta_S[index])/(time[index+1]-time[index]))
print("v_S: " + str(v_S))

v_E = [] # Elbow
for index, (elem_t,elem_theta_E) in enumerate(zip(time,theta_E)):
    if (index+1 < len(time)): # compute only until the second to last value
        v_E.append((theta_E[index+1]-theta_E[index])/(time[index+1]-time[index]))
print("v_E: " + str(v_E))

# Velocity at each path point (Shoulder)
for index, elem in enumerate(v_S):
    if (index+1 < len(v_S)):
        if np.sign(v_S[index]) == np.sign(v_S[index+1]):
            theta_S_d.append((v_S[index]+v_S[index+1])/2)
        elif np.sign(v_S[index]) != np.sign(v_S[index+1]):
            theta_S_d.append(0)
theta_S_d.append(0) # this represents the endpoint-velocity (i.c.)
print("theta_S_d: " + str(theta_S_d))

# Velocity at each path point (Elbow)
for index, elem in enumerate(v_E):
    if (index+1 < len(v_E)):
        if np.sign(v_E[index]) == np.sign(v_E[index+1]):
            theta_E_d.append((v_E[index]+v_E[index+1])/2)
        elif np.sign(v_E[index]) != np.sign(v_E[index+1]):
            theta_E_d.append(0)
theta_E_d.append(0) # this represents the endpoint-velocity (i.c.)
print("theta_E_d: " + str(theta_E_d))

# ----------------------------------------------------------
# Solve the Cubic Polinomial for each step:
steps = 6

# Shoulder
for index, (el_time,el_theta,el_theta_d) in enumerate(zip(time,theta_S,theta_S_d)):
    if (index+1 < len(theta_S)):
        t = np.linspace(time[index], time[index+1], steps) # [s] Time

        print("theta_S[index]: " + str(theta_S[index]))
        print("theta_S[index+1]: " + str(theta_S[index+1]))
        print("theta_S_d[index]: " + str(theta_S_d[index]))
        print("theta_S_d[index+1]: " + str(theta_S_d[index+1]))

        # c-coefficients
        c0_S = theta_S[index]
        c1_S = theta_S_d[index]
        c2_S = ((-3*(theta_S[index]-theta_S[index+1])) - (2*theta_S_d[index] + theta_S_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**2
        c3_S = ((2*(theta_S[index]-theta_S[index+1])) + (theta_S_d[index] + theta_S_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**3

        print("c0_S: " + str(c0_S))
        print("c1_S: " + str(c1_S))
        print("c2_S: " + str(c2_S))
        print("c3_S: " + str(c3_S))
        # Cubic Polinomial [Trajectory of angular displacement]
        theta_S_t = c0_S + (c1_S*(t-time[index])) + (c2_S*(t-time[index])**2) + (c3_S*(t-time[index])**3) # [deg] Shoulder
        # Cubic Polinomial [Trajectory of angular velocity]
        theta_S_d_t = c1_S + (2*c2_S*(t-time[index])) + (3*c3_S*(t-time[index])**2) # [deg/s] Shoulder

        # Note: the variables that this function returns are arrays
        #return theta_S, theta_d_S

        print("theta_S_t: " + str(theta_S_t))
        print("theta_S_d_t: " + str(theta_S_d_t))

# Elbow
for index, (el_time,el_theta,el_theta_d) in enumerate(zip(time,theta_E,theta_E_d)):
    if (index+1 < len(theta_E)):
        t = np.linspace(time[index], time[index+1], steps) # [s] Time

        print("theta_E[index]: " + str(theta_E[index]))
        print("theta_E[index+1]: " + str(theta_E[index+1]))
        print("theta_E_d[index]: " + str(theta_E_d[index]))
        print("theta_E_d[index+1]: " + str(theta_E_d[index+1]))

        # c-coefficients
        c0_E = theta_E[index]
        c1_E = theta_E_d[index]
        c2_E = ((-3*(theta_E[index]-theta_E[index+1])) - (2*theta_E_d[index] + theta_E_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**2
        c3_E = ((2*(theta_E[index]-theta_E[index+1])) + (theta_E_d[index] + theta_E_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**3

        print("c0_E: " + str(c0_E))
        print("c1_E: " + str(c1_E))
        print("c2_E: " + str(c2_E))
        print("c3_E: " + str(c3_E))
        # Cubic Polinomial [Trajectory of angular displacement]
        theta_E_t = c0_E + (c1_E*(t-time[index])) + (c2_E*(t-time[index])**2) + (c3_E*(t-time[index])**3) # [deg] Elbow
        # Cubic Polinomial [Trajectory of angular velocity]
        theta_E_d_t = c1_E + (2*c2_E*(t-time[index])) + (3*c3_E*(t-time[index])**2) # [deg/s] Elbow

        # Note: the variables that this function returns are arrays
        #return theta_S, theta_d_S

        print("theta_E_t: " + str(theta_E_t))
        print("theta_E_d_t: " + str(theta_E_d_t))