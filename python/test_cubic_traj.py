import kinematics


# Initial Conditions (i.c.):
# Define (time,pose,vel) for each path point

time = [0, 2, 4, 8, 10] # [s]
theta_S = [10, 20, 0, 30, 40] # [deg]
theta_S_d = [0] # [deg/s]
theta_E = [10, 20, 0, 30, 40] # [deg]
theta_E_d = [0] # [deg/s]
'''
time = [0, 1, 2] # [s]
theta_S = [0, 45, 0] # [deg]
theta_S_d = [0] # [deg/s]
theta_E = [0, 90, 0] # [deg]
theta_E_d = [0] # [deg/s]
'''

traj = kinematics.cubic_trajectory_print(time, theta_S, theta_S_d, theta_E, theta_E_d)
