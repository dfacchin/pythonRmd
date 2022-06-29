import kinematics


# Initial Conditions (i.c.):
# Define (time,pose,vel) for each path point
time = [0, 2, 4, 8, 10] # [s]
theta = [10, 20, 0, 30, 40] # [deg]
theta_d = [0] # [deg/s]

traj = kinematics.cubic_trajectory(time, theta, theta_d)