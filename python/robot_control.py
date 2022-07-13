import numpy as np
import can
import time

import RMD
import kinematics
from trajectory_planner import Joint


# Specify the bus
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# Variables
v = 1000  # Motors velocity
a = 1000  # Motors acceleration


# ---------- RMD motor with ID 1 (Elbow) ----------
motor_E = RMD.RMD(0x142, bus, ratio=13.5)  # Elbow
motor_E.Fn30()  # read PID
motor_E.Fn33()  # read acceleration
# Specify desired PID
motor_E.PidPosKp = 100
motor_E.PidPosKi = 0
motor_E.PidVelKp = 100
motor_E.PidVelKi = 5
motor_E.PidTrqKp = 100
motor_E.PidTrqKp = 5
motor_E.Fn31()  # write PID to Ram
# Specify desired acceleration
motor_E.acceleration = a
motor_E.Fn34()  # write acceleration to Ram


# ---------- RMD motor with ID 2 (Shoulder) ----------
motor_S = RMD.RMD(0x141, bus, ratio=13.5)  # Shoulder
motor_S.Fn30()  # read PID
motor_S.Fn33()  # read acceleration
# Specify desired PID
motor_S.PidPosKp = 100
motor_S.PidPosKi = 0
motor_S.PidVelKp = 100
motor_S.PidVelKi = 5
motor_S.PidTrqKp = 100
motor_S.PidTrqKp = 5
motor_S.Fn31()  # write PID to Ram
# Specify desired accelration
motor_S.acceleration = a
motor_S.Fn34()  # write acceleration to Ram


# Initial Conditions (i.c.):
#pp = [[1000,0],[750,200],[300,350],[0,500],[300,350],[750,200],[1000,0]] # [mm] path points (x,y)
pp = [[1000,0],[400,0],[1000,0]]
t = np.array([0, 1, 2]) # [s]
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
    theta_S.append(theta[0])
    theta_E.append(theta[1])

shoulder = Joint(theta_S, theta_d_S, v_S, t, fn)
elbow = Joint(theta_E, theta_d_E, v_E, t, fn)

# Compute velocities
shoulder.velocity()
elbow.velocity()
shoulder.theta_d_pp()
elbow.theta_d_pp()

# Compute trajectory
angle_S = shoulder.trajectory()
angle_E = elbow.trajectory()
# Print "theta" and "theta_d" arrays
print(angle_S)
print(angle_E)

# Define actual angle arrays
# actual_angle_S = np.array([])
# actual_angle_E = np.array([])

actual_angle_S = []
actual_angle_E = []

#for i in range(3):
idx = 1
while idx < len(angle_S[0]):
	ik = [angle_S[0][idx],angle_E[0][idx]] # joint angles
	#v = [angle_S[1][idx],angle_E[1][idx]] # joint velocities
	idx += 1

	# Print desired pose
	print("Desired angle: ", ik)
	#print("Vel: ",v)

	# Read actual multiTurnGeared motor angle
	read_angle_S = motor_S.get_actual_angle()
	read_angle_E = motor_E.get_actual_angle()

	actual_angle_S.append(-read_angle_S)
	actual_angle_E.append(read_angle_E+read_angle_S)


	motor_S.goG(-ik[0], v) # - sign, since the motor is up-side-down
	motor_E.goG(ik[1]+ik[0], v) # sum of angles since we use belts
	time.sleep(1/fn)

	input("Hit 'Enter' and go to the next point")
	#time.sleep(2)
print("actual S: ", actual_angle_S)
print("actual E: ", actual_angle_E)
