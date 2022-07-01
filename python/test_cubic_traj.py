import matplotlib.pyplot as plt
from trajectory_planner import Joint


# Initial Conditions (i.c.):
# Define (pose,vel) for each path point
theta_S = [10, 20, 0, 30, 40] # [deg]
theta_d_S = [0] # [deg/s]
theta_E = [10, 20, 0, 30, 40] # [deg]
theta_d_E = [0] # [deg/s]
# Velocity in each segment
v_S = [] # [deg/s]
v_E = [] # [deg/s]


shoulder = Joint(theta_S, theta_d_S, v_S)
elbow = Joint(theta_E, theta_d_E, v_E)

# Compute velocities
shoulder.velocity()
elbow.velocity()
shoulder.theta_d_pp()
elbow.theta_d_pp()

# Print "theta" and "theta_d" arrays
print(shoulder.trajectory())
print(elbow.trajectory())
