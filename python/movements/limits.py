import numpy as np


'''
Delimit the reachable workspace of the robot arm,
and notify if the eef wants to move out of bound.
'''

def workspace(r, theta_S, theta_E, x, y):
    # r (radius) = arm_length

    if theta_E == 0 and theta_S in range(-100,100): # if theta_E=0 the arm is completely extended.
        x_limit = r*np.cos(theta_S)
        y_limit = r*np.sin(theta_S)
        if x==x_limit and y==y_limit:
            print("Desired position not reachable!")
    else:
        pass