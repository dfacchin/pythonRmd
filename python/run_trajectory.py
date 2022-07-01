import numpy as np

from trajectory_planner import Joint


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
angle_S = shoulder.trajectory(joint_name="shoulder")
angle_E = elbow.trajectory(joint_name="elbow")
# Print "theta" and "theta_d" arrays
print(angle_S)
print(angle_E)
