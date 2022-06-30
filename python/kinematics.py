import math
import numpy as np


'''
Direct kinematics [DK]:
Transforms joint angles (theta1,theta2) in eef coordinates (x,y))
'''


def DK(target, len1=497.0, len2=500.0):
    # target = [theta1, theta2] or
    # target = np.array((theta1, theta2))
    target[0] = np.deg2rad(target[0])
    target[1] = np.deg2rad(target[1])
    x = len1*np.cos(target[0]) + len2*np.cos(target[0]+target[1])
    y = len1*np.sin(target[0]) + len2*np.sin(target[0]+target[1])
    x = round(x, 2)  # round to 2 decimal numbers
    y = round(y, 2)
    return x, y


'''
Inverse kinematics [IK]:
Transforms eef coordinates (x,y) in joint angles (theta1,theta2)
'''


def IK(target, len1=497.0, len2=500.0, elbow=0, elbow_limit=30):

    # radius = distance from the origin to the eef
    radiussq = np.dot(target, target)
    radius = math.sqrt(radiussq)

    # theta is the angle of target point w.r.t. X axis
    theta = math.atan2(target[1], target[0])

    # use the law of cosines to compute the elbow angle theta2
    #   R**2 = l1**2 + l2**2 - 2*l1*l2*cos(pi - theta2)
    #   beta = pi - theta2
    #   both theta2 and -theta2 are valid solutions
    cos_beta = (radiussq - len1**2 - len2**2) / (-2 * len1 * len2)
    if cos_beta < -1.0:
        beta = math.pi
    elif cos_beta > 1.0:
        beta = 0.0
    else:
        beta = math.acos(cos_beta)

    # Limit the beta value to set elbow joint constraints
    elbow_limit = np.deg2rad(elbow_limit)
    if beta < elbow_limit:
        beta = elbow_limit
        # compute the new radius
        radius = math.sqrt(len1**2 + len2**2 - 2*len1*len2*math.cos(beta))

    # use the law of sines to compute the angle alpha
    #  radius / sin(beta)  = l2 / sin(alpha)
    if radius > 0.0:
        alpha = math.asin(len2 * math.sin(beta) / radius)
    else:
        alpha = 0.0

    #  compute the two solutions with opposite elbow sign
    theta1_1 = np.rad2deg(theta - alpha)
    theta2_1 = np.rad2deg(math.pi - beta)
    theta1_1 = round(theta1_1, 2)
    theta2_1 = round(theta2_1, 2)
    soln1 = np.array((theta1_1, theta2_1))

    theta1_2 = np.rad2deg(theta + alpha)
    theta2_2 = np.rad2deg(beta - math.pi)
    theta1_2 = round(theta1_2, 2)
    theta2_2 = round(theta2_2, 2)
    soln2 = np.array((theta1_2, theta2_2))

    if elbow == 1:
        return soln1
    else:
        return soln2


'''
Linear Path Planning:
Calculates the vector passing through the 'start' and the 'end' point.
Splits the vector in multiple points that define the path to follow.
'''


def path(x1, y1, x2, y2, steps=20):
    steps_x = np.linspace(x1, x2, steps, endpoint=True)  # (start, stop, steps)
    steps_y = np.linspace(y1, y2, steps, endpoint=True)

    solt = []

    if x1 == x2:
        for y in steps_y:
            x = x1
            x = round(x, 2)
            y = round(y, 2)
            soln = np.array((x, y))
            solt.append(soln)
    elif y1 == y2:
        for x in steps_x:
            y = y1
            x = round(x, 2)
            y = round(y, 2)
            soln = np.array((x, y))
            solt.append(soln)
    else:
        for x in steps_x:
            y = (((x-x1)/(x2-x1))*(y2-y1))+y1
            x = round(x, 2)
            y = round(y, 2)
            soln = np.array((x, y))
            solt.append(soln)
    return solt


'''
Trajectory Planning:
Ensure a smooth variation of the joint angles while following a desired path
using the (Cubic) Polinomial Trajectory Function
'''


def cubic_trajectory(time, theta_S, theta_S_d, theta_E, theta_E_d, steps=6):
    # Velocity in each segment
    v_S = [] # Shoulder
    for index, (elem_t,elem_theta_S) in enumerate(zip(time,theta_S)):
        if (index+1 < len(time)): # compute only until the second to last value
            v_S.append((theta_S[index+1]-theta_S[index])/(time[index+1]-time[index]))

    v_E = [] # Elbow
    for index, (elem_t,elem_theta_E) in enumerate(zip(time,theta_E)):
        if (index+1 < len(time)): # compute only until the second to last value
            v_E.append((theta_E[index+1]-theta_E[index])/(time[index+1]-time[index]))

    # Velocity at each path point (Shoulder)
    for index, elem in enumerate(v_S):
        if (index+1 < len(v_S)):
            if np.sign(v_S[index]) == np.sign(v_S[index+1]):
                theta_S_d.append((v_S[index]+v_S[index+1])/2)
            elif np.sign(v_S[index]) != np.sign(v_S[index+1]):
                theta_S_d.append(0)
    theta_S_d.append(0) # this represents the endpoint-velocity (i.c.)

    # Velocity at each path point (Elbow)
    for index, elem in enumerate(v_E):
        if (index+1 < len(v_E)):
            if np.sign(v_E[index]) == np.sign(v_E[index+1]):
                theta_E_d.append((v_E[index]+v_E[index+1])/2)
            elif np.sign(v_E[index]) != np.sign(v_E[index+1]):
                theta_E_d.append(0)
    theta_E_d.append(0) # this represents the endpoint-velocity (i.c.)

    # Solve the Cubic Polinomial for each step:
    # Shoulder
    for index, (el_time,el_theta,el_theta_d) in enumerate(zip(time,theta_S,theta_S_d)):
        if (index+1 < len(theta_S)):
            t = np.linspace(time[index], time[index+1], steps) # [s] Time

            # c-coefficients
            c0_S = theta_S[index]
            c1_S = theta_S_d[index]
            c2_S = ((-3*(theta_S[index]-theta_S[index+1])) - (2*theta_S_d[index] + theta_S_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**2
            c3_S = ((2*(theta_S[index]-theta_S[index+1])) + (theta_S_d[index] + theta_S_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**3

            # Cubic Polinomial [Trajectory of angular displacement]
            theta_S_t = c0_S + (c1_S*(t-time[index])) + (c2_S*(t-time[index])**2) + (c3_S*(t-time[index])**3) # [deg] Shoulder
            # Cubic Polinomial [Trajectory of angular velocity]
            theta_S_d_t = c1_S + (2*c2_S*(t-time[index])) + (3*c3_S*(t-time[index])**2) # [deg/s] Shoulder

    # Elbow
    for index, (el_time,el_theta,el_theta_d) in enumerate(zip(time,theta_E,theta_E_d)):
        if (index+1 < len(theta_E)):
            t = np.linspace(time[index], time[index+1], steps) # [s] Time

            # c-coefficients
            c0_E = theta_E[index]
            c1_E = theta_E_d[index]
            c2_E = ((-3*(theta_E[index]-theta_E[index+1])) - (2*theta_E_d[index] + theta_E_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**2
            c3_E = ((2*(theta_E[index]-theta_E[index+1])) + (theta_E_d[index] + theta_E_d[index+1]) * (time[index+1]-time[index])) / (time[index+1]-time[index])**3

            # Cubic Polinomial [Trajectory of angular displacement]
            theta_E_t = c0_E + (c1_E*(t-time[index])) + (c2_E*(t-time[index])**2) + (c3_E*(t-time[index])**3) # [deg] Elbow
            # Cubic Polinomial [Trajectory of angular velocity]
            theta_E_d_t = c1_E + (2*c2_E*(t-time[index])) + (3*c3_E*(t-time[index])**2) # [deg/s] Elbow


    # Note: the variables that this function returns are arrays
    return theta_S_t, theta_E_t, theta_S_d_t, theta_E_d_t


def cubic_trajectory_1dof(time, theta, theta_d, steps=6):

    # Velocity in each segment
    v = []
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

    # Solve the Cubic Polinomial for each step
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

            print("theta_S: " + str(theta_S))
            print("theta_d_S: " + str(theta_d_S))

            # Note: the variables that this function returns are arrays
            #return theta_S, theta_d_S



'''
Trajectory Planning:
Follow the desired path in a linear manner. Parabolic blends are used to
smoothen the direction changes at each defined path point (via point).
The Linear Trajectory Function with Parabolic Blends is used.
'''

def linear_trajectory(pos_target_i, pos_target_f, vel_target_i, vel_target_f, accel, ti, tf, steps):
    # pos_target = [theta_S, theta_E] or np.array((theta_S,theta_E))
    # vel_target = [theta_d_S, theta_d_E] or np.array((theta_d_S,theta_d_E))
    # accel = [theta_dd_S, theta_dd_E] or np.array((theta_dd_S,theta_dd_E))

    # Time
    t = np.linspace(ti, tf, steps) # [s]

    # Variables:
    # Blend time (tb_i = tb_f)
    tb = (t/2)- (np.sqrt()/(2*accel[0]))
    # Joint angles at the end of the blend region
    theta_b_S = pos_target_i[0] + (0.5*accel[0]*tb)

    pass


'''
########################### For debugging #############################
# When run as a script, try a sample problem:
if __name__ == "__main__":
    # choose a sample target position to test IK
	x = float(input("x-axis [mm]: "))
	y = float(input("y-axis [mm]: "))
	target = np.array((x, y))
	ik = IK(target)
	print("The following solutions should reach endpoint position %s: %s" % (target, ik))
    # choose sample joint angles to test DK
    theta1 = float(input("MT shoulder [deg]: "))
    theta2 = float(input("MT elbow [deg]: "))
    target = np.array((theta1, theta2))
    dk = DK(target)
    print("The following x,y coord returns angles %s: %s" % (target, dk))
'''
