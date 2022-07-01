import numpy as np
import matplotlib.pyplot as plt

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

# Print "theta" and "theta_d" arrays
angle_S = shoulder.trajectory()
angle_E = elbow.trajectory()

print(angle_S)
print(angle_E)


# # Plots

# plt.style.use('seaborn-dark')

# # Position Plot
# plt.subplot(1,2,1) # (row, column, plot)
# plt.title("Position")
# plt.xlabel("time [s]")
# plt.ylabel("theta [deg]")
# plt.plot(time, angle_S[0], marker='.')
# plt.grid(True)

# # Velocity Plot
# plt.subplot(1,2,2) # (row, column, plot)
# plt.title("Velocity")
# plt.xlabel("time [s]")
# plt.ylabel("theta_d [deg/s]")
# plt.plot(time, angle_S[1], color='y', marker='.')
# plt.grid(True)


# plt.tight_layout() # avoid text overlapping
# plt.show()