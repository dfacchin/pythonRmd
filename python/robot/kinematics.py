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
    #x = round(x, 2)  # round to 2 decimal numbers
    #y = round(y, 2)
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


def linear_path(x1, y1, x2, y2, steps=20):
    steps_x = np.linspace(x1, x2, steps, endpoint=True)  # (start, stop, steps)
    steps_y = np.linspace(y1, y2, steps, endpoint=True)

    xy_coords = []

    if x1 == x2:
        for y in steps_y:
            x = x1
            #x = round(x, 2)
            #y = round(y, 2)
            soln = [x, y]
            xy_coords.append(soln)
    elif y1 == y2:
        for x in steps_x:
            y = y1
            #x = round(x, 2)
            #y = round(y, 2)
            soln = [x, y]
            xy_coords.append(soln)
    else:
        for x in steps_x:
            y = (((x-x1)/(x2-x1))*(y2-y1))+y1
            #x = round(x, 2)
            #y = round(y, 2)
            soln = [x, y]
            xy_coords.append(soln)
    return xy_coords


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
