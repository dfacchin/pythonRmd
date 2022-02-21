import math
import numpy as np


def IK(target, len1=497.0, len2=500.0, elbow=0):
    """Compute two inverse kinematics solutions for a target end position.  The
    target is a Cartesian position vector (two-element ndarray) in world
    coordinates, and the result vectors are joint angles as ndarrays [q0, q1].
    If the target is out of reach, returns the closest pose.

    :param target: two-element list or ndarray with [x, y] target position
    :param len1: optional proximal link length
    :param len2: optional distal link length
    :return: tuple (solution1, solution2) of two-element ndarrays with q1, q2 angles
    """

    # find the position of the point in polar coordinates
    radiussq = np.dot(target, target)
    radius   = math.sqrt(radiussq)

    # theta is the angle of target point w.r.t. X axis, same origin as arm
    theta    = math.atan2(target[1], target[0]) 

    # use the law of cosines to compute the elbow angle
    #   R**2 = l1**2 + l2**2 - 2*l1*l2*cos(pi - elbow)
    #   both elbow and -elbow are valid solutions
    acosarg = (radiussq - len1**2 - len2**2) / (-2 * len1 * len2)
    if acosarg < -1.0:  elbow_supplement = math.pi
    elif acosarg > 1.0: elbow_supplement = 0.0
    else:               elbow_supplement = math.acos(acosarg)

    # use the law of sines to find the angle at the bottom vertex of the triangle defined by the links
    #  radius / sin(elbow_supplement)  = l2 / sin(alpha)
    if radius > 0.0:
        alpha = math.asin(len2 * math.sin(elbow_supplement) / radius)
    else:
        alpha = 0.0

    #  compute the two solutions with opposite elbow sign
    theta1_1 = np.rad2deg(theta - alpha)
    theta2_1 = np.rad2deg(math.pi - elbow_supplement)
    theta1_1 = round(theta1_1,2)
    theta2_1 = round(theta2_1,2)
    soln1 = np.array((theta1_1, theta2_1))
    
    theta1_2 = np.rad2deg(theta + alpha)
    theta2_2 = np.rad2deg(elbow_supplement - math.pi)
    theta1_2 = round(theta1_2,2)
    theta2_2 = round(theta2_2,2)
    soln2 = np.array((theta1_2, theta2_2))
 
	# Solutions in rad:
#    soln1 = np.array((theta - alpha, math.pi - elbow_supplement))
#    soln2 = np.array((theta + alpha, elbow_supplement - math.pi))

    if elbow==1:
        return soln1
    else:
        return soln2

'''
################################################################
# When run as a script, try a sample problem:
if __name__ == "__main__":

    # choose a sample target position to test IK
	x = float(input("x-axis [mm]: "))
	y = float(input("y-axis [mm]: "))
	target = np.array((x, y))
	ik = IK(target)
	print("The following solutions should reach endpoint position %s: %s" % (target, ik))
'''
