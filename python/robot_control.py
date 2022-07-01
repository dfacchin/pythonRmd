import numpy as np
import kinematics
from trajectory_planner import Joint

# Initial Conditions (i.c.):
pp = [[1000,0],[500,-500],[1000,0]] # [mm] path points (x,y)
time = np.array([0, 1, 2]) # [s]
fn = 5 # [Hz]

# Define (pose,vel) for each path point
theta_S = [] # [deg]
theta_d_S = [0] # [deg/s]
theta_E = [] # [deg]
theta_d_E = [0] # [deg/s]
# Velocity in each segment
v_S = [] # [deg/s]
v_E = [] # [deg/s]

for coord in pp:
    x = float(coord[0])
    y = float(coord[1])
    target = np.array((x,y))
    theta = kinematics.IK(target, elbow=1)
    theta_S.append(-theta[0]) # - sign, since the motor is up-side-down
    theta_E.append(theta[1]+theta[0]) # sum of angles since we use belts

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