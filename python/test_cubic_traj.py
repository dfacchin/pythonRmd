import kinematics
from traj_class import Joint

'''
time = [0, 1, 2] # [s]
theta_S = [0, 45, 0] # [deg]
theta_S_d = [0] # [deg/s]
theta_E = [0, 90, 0] # [deg]
theta_E_d = [0] # [deg/s]
'''

# Initial Conditions (i.c.):
# Define (pose,vel) for each path point
theta_S = [10, 20, 0, 30, 40] # [deg]
theta_d_S = [0] # [deg/s]
theta_E = [10, 20, 0, 30, 40] # [deg]
theta_d_E = [0] # [deg/s]
# Velocity in each segment
v_S = [] # [deg/s]
v_E = [] # [deg/s]
# Joint angles and velocities describing the trajectory (in time)
theta_S_t = [] # [deg]
theta_d_S_t = [] # [deg/s]
theta_E_t = [] # [deg]
theta_d_E_t = [] # [deg/s]

shoulder = Joint(theta_S, theta_d_S, v_S, theta_S_t, theta_d_S_t)
elbow = Joint(theta_E, theta_d_E, v_E, theta_E_t, theta_d_E_t)

print(shoulder.velocity())
print(elbow.velocity())
print(shoulder.theta_d_pp())
print(elbow.theta_d_pp())
print(shoulder.trajectory())
print(elbow.trajectory())
