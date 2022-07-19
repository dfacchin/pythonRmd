import numpy as np
import can
import time

import RMD
import RMD_V3
import kinematics
from trajectory_planner import Joint
import plots


# Specify the bus
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# Variables
ratio = 13.5 # Gear ratio
#v = 1000  # Motors velocity
a = 4000  # Motors acceleration

# Initial Conditions (i.c.):
#pp = [[1000,0],[750,200],[300,350],[0,500],[300,350],[750,200],[1000,0]] # [mm] path points (x,y)
pp = [[1000,0],[700,300],[400,0],[700,300],[1000,0]]
t = np.array([0, 1, 2, 3, 4]) # [s]
fn = 15 #25 # [Hz]

# pid
#_pp = 200
#_pi = 5
#_vp = 200
#_vi = 5
#_tp = 5
#_ti = 5

#_pps = 200
#_pis = 5
#_vps = 200
#_vis = 5
#_tps = 10
#_tis = 5

# ---------- RMD motor with ID 1 (Elbow) ----------
motor_E = RMD_V3.RMDV3(0x140, bus, 9)  # Elbow
motor_E.Fn30()  # read PID
motor_E.Fn33()  # read acceleration
# Specify desired PID
motor_E.PidPosKp = 100
motor_E.PidPosKi = 5
motor_E.PidVelKp = 100
motor_E.PidVelKi = 5
motor_E.PidTrqKp = 5
motor_E.PidTrqKi = 5
motor_E.Fn31()  # write PID to Ram
# Specify desired acceleration
motor_E.acceleration = a
motor_E.Fn34()  # write acceleration to Ram

# ---------- RMD motor with ID 2 (Shoulder) ----------
motor_S = RMD.RMD(0x141, bus, ratio)  # Shoulder
motor_S.Fn30()  # read PID
motor_S.Fn33()  # read acceleration
# Specify desired PID
motor_S.PidPosKp = 100
motor_S.PidPosKi = 5
motor_S.PidVelKp = 100
motor_S.PidVelKi = 5
motor_S.PidTrqKp = 10
motor_S.PidTrqKi = 5
motor_S.Fn31()  # write PID to Ram
# Specify desired accelration
motor_S.acceleration = a
motor_S.Fn34()  # write acceleration to Ram


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

# Define lists of actual joint angles
actual_angle_S = []
actual_angle_E = []

# Define lists of actual joint velocities
actual_vel_S = []
actual_vel_E = []

#for i in range(3):
idx = 1
while idx < len(angle_S[0]):
	timestamp = time.time()
	ik = [angle_S[0][idx],angle_E[0][idx]] # joint angles
	v = [angle_S[1][idx],angle_E[1][idx]] # joint velocities
	idx += 1

	# Print desired pose
	print("Desired angle: ", ik)
	print("Desired vel: ",v)

	# Read actual multiTurnGeared motor angle
	read_angle_S = motor_S.get_actual_angle()
	read_angle_E = motor_E.get_actual_angle()

	actual_angle_S.append(-read_angle_S)
	actual_angle_E.append(read_angle_E+read_angle_S)

	#motor_S.goG(-ik[0], 2500) # - sign, since the motor is up-side-down
	#motor_S.goG(-ik[0], 4*abs(v[0])) # - sign, since the motor is up-side-down
	#motor_E.goG(ik[1]+ik[0], 2500) # sum of angles since we use belts
	motor_E.goG(ik[1]+ik[0], 4*abs(v[1]+v[0])) # sum of angles since we use belts

	actual_vel_S.append(-motor_S.actualVelocity/ratio)
	actual_vel_E.append(motor_E.actualVelocity/ratio + motor_S.actualVelocity/ratio)

	#compensate delay of functions
	deltaTime = time.time() - timestamp
	desiredTime = 1/fn
	#if elapsed time is too long we go straight to next point
	#else we subtract the evaluation time from the desired time
	if deltaTime < desiredTime:
		time.sleep(desiredTime-deltaTime)


	#input("Hit 'Enter' and go to the next point")
	#time.sleep(2)

#print("act_vel: ", act_vel)

read_angle_S = motor_S.get_actual_angle()
read_angle_E = motor_E.get_actual_angle()

actual_angle_S.append(-read_angle_S)
actual_angle_E.append(read_angle_E+read_angle_S)

actual_vel_S.append(-motor_S.actualVelocity/ratio)
actual_vel_E.append(motor_E.actualVelocity/ratio)

print("Actual angle S: ", actual_angle_S)
print("Actual angle E: ", actual_angle_E)
print("Actual vel S: ", actual_vel_S)
print("Actual vel E: ", actual_vel_E)


# Plot
plot_S = shoulder.plot("shoulder", angle_S[0], angle_S[1], angle_S[2], actual_angle_S, actual_vel_S)
plot_E = elbow.plot("elbow", angle_E[0], angle_E[1], angle_E[2], actual_angle_E, actual_vel_E)
print(plot_S)
print(plot_E)
traj_points = plots.path_plot(angle_S[0], angle_E[0], pp, actual_angle_S, actual_angle_E)
print(traj_points)
