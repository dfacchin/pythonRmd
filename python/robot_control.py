import numpy as np
import kinematics
from trajectory_planner import Joint

pp = [[1000,0],[500,-500],[1000,0]] # path points

# Initial Conditions (i.c.):
# Define (pose,vel) for each path point
theta_S = [] # [deg]
theta_d_S = [0] # [deg/s]
theta_E = [] # [deg]
theta_d_E = [0] # [deg/s]
# Velocity in each segment
v_S = [] # [deg/s]
v_E = [] # [deg/s]
# Joint angles and velocities describing the trajectory (in time)
theta_S_t = [] # [deg]
theta_d_S_t = [] # [deg/s]
theta_E_t = [] # [deg]
theta_d_E_t = [] # [deg/s]

for coord in pp:
    x = float(coord[0])
    y = float(coord[1])
    target = np.array((x,y))
    theta = kinematics.IK(target, elbow=1)
    theta_S.append(theta[0])
    theta_E.append(theta[1])

shoulder = Joint(theta_S, theta_d_S, v_S, theta_S_t, theta_d_S_t)
elbow = Joint(theta_E, theta_d_E, v_E, theta_E_t, theta_d_E_t)

shoulder.velocity()
elbow.velocity()
shoulder.theta_d_pp()
elbow.theta_d_pp()
print(shoulder.trajectory())
print(elbow.trajectory())