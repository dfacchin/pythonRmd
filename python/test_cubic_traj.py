import kinematics

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
v_S = [] # [deg/s]
v_E = [] # [deg/s]

shoulder = Joint(theta_S, theta_d_S, v_S)
elbow = Joint(theta_E, theta_d_E, v_E)

print(shoulder.velocity())
print(elbow.velocity())
print(shoulder.theta_d_pp())
print(elbow.theta_d_pp())
print(shoulder.trajectory())
print(elbow.trajectory())
