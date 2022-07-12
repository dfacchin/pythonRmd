import numpy as np

from trajectory_planner_plot import Joint


# Initial Conditions (i.c.):
time = np.array([0, 2, 4, 8, 10]) # [s]
fn = 5 # [Hz]
# Define (pose,vel) for each path point
theta_S = [10, 20, 0, 30, 40] # [deg]
theta_d_S = [0] # [deg/s]
theta_E = [10, 20, 0, 30, 40] # [deg]
theta_d_E = [0] # [deg/s]
# Velocity in each segment
v_S = [] # [deg/s]
v_E = [] # [deg/s]


shoulder = Joint(theta_S, theta_d_S, v_S, time, fn)
elbow = Joint(theta_E, theta_d_E, v_E, time, fn)

# Compute velocities
shoulder.velocity()
elbow.velocity()
shoulder.theta_d_pp()
elbow.theta_d_pp()

# Make sure to speciy the joint_name: shoulder and elbow
angle_S = shoulder.trajectory()
angle_E = elbow.trajectory()
# Print "theta" and "theta_d" arrays
print(angle_S)
print(angle_E)

# Plot
plot_S = shoulder.plot("shoulder", angle_S[0], angle_S[1], angle_S[2])
plot_E = elbow.plot("elbow", angle_E[0], angle_E[1], angle_E[2])
print(plot_S)
print(plot_E)