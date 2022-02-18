#!/usr/bin/env python3
"""two-link-ik.py: demonstration of forward and inverse kinematics for a two-link arm."""

# Standard library modules.
import math

# Third-party library modules.
import numpy as np

#================================================================
def two_link_forward_kinematics(q, len1=497.0, len2=500.0):
    """Compute the forward kinematics.  Returns the base-coordinate Cartesian
    position of the elbow and endpoint for a given joint angle vector.  Optional
    parameters l1 and l2 are the link lengths.  The base is assumed to be at the
    origin.

    :param q: two-element list or ndarray with [q1, q2] joint angles
    :param len1: optional proximal link length
    :param len2: optional distal link length
    :return: tuple (elbow, end) of two-element ndarrays with [x,y] locations
    """

    elbow = np.array((len1 * math.sin(q[0]), len1 * math.cos(q[0])))
    end   = elbow + np.array((len2 * math.sin(q[0]+q[1]), len2 * math.cos(q[0]+q[1])))
    return elbow, end

#================================================================
def two_link_inverse_kinematics(target, len1=497.0, len2=500.0):
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
    radiussq = np.dot(target, target) # x,y
    radius   = math.sqrt(radiussq) # r=sqrt(x**2+y**2)

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
    soln1 = np.array((theta - alpha, math.pi - elbow_supplement))
    soln2 = np.array((theta + alpha, elbow_supplement - math.pi))

    return soln1, soln2

################################################################
# When run as a script, try a sample problem:
if __name__ == "__main__":

    # choose a sample target position to test IK
    target = np.array((497.0, 500.0))
    ik = two_link_inverse_kinematics(target)
    print("The following solutions should reach endpoint position %s: %s" % (target, ik))

    # test the solutions:

    p1 = two_link_forward_kinematics(ik[0])
    p2 = two_link_forward_kinematics(ik[1])

    print("Endpoint position for first solution :", p1[1])
    print("Endpoint position for second solution:", p2[1])
