import RMD
import can
import time
import numpy as np
import kinematics



############## GYEMS ##################
# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# Variables:
a = 1000  # Motors acceleration
v = 2000  # Motors velocity
t = 3  # Waiting time

# ---------- RMD motor with ID 1 (Elbow) ----------
motor_E = RMD.RMD(0x142, bus, ratio=13.5)  # Elbow

#motor_E.info() # 'info' prints Pid and Acceleration

motor_E.Fn30()  # read PID

motor_E.Fn33()  # read acceleration
#motor_E.info()
# Specify desired PID
motor_E.PidPosKp = 30
motor_E.PidPosKi = 0
motor_E.PidVelKp = 30
motor_E.PidVelKi = 5
motor_E.PidTrqKp = 30
motor_E.PidTrqKp = 5
motor_E.Fn31()  # write PID to Ram
# Specify desired accelration
motor_E.acceleration = a
motor_E.Fn34()  # write acceleration to Ram


# ---------- RMD motor with ID 2 (Shoulder) ----------
motor_S = RMD.RMD(0x141, bus, ratio=13.5)  # Shoulder

#motor_S.info()

motor_S.Fn30()  # read PID
motor_S.Fn33()  # read acceleration
#motor_S.info()
# Specify desired PID
motor_S.PidPosKp = 30
motor_S.PidPosKi = 0
motor_S.PidVelKp = 30
motor_S.PidVelKi = 5
motor_S.PidTrqKp = 30
motor_S.PidTrqKp = 5
motor_S.Fn31()  # write PID to Ram
# Specify desired accelration
motor_S.acceleration = a
motor_S.Fn34()  # write acceleration to Ram
############## GYEMS ##################


############## MOVEMENT ##################
while True:

	theta1 = motor_S.multiTurnG
	theta2 = motor_E.multiTurnG
	theta2 = theta2 - theta1
	print("Starting theta1 and theta2 values:")
	print(theta1,theta2)

	'''
	Read motor multi-turn angles
	and define them as two variables: theta1 and theta2
	'''

	# Compute the actual coordinates:
	target = [theta1, theta2]
	dk = kinematics.DK(target)
	x1 = dk[0]
	y1 = dk[1]
	print("Starting x1 and y1 values:")
	print(x1)
	print(y1)

	'''
	Choose a target position to compute the joint angles (IK)
	x is along the straight arm (extiting the machine)
	y is perpendicular to the straight arm (positive is towards the wall)
	'''

	x2 = float(input("x-axis [mm]: "))
	y2 = float(input("y-axis [mm]: "))
	# z is up and down of the veritcal rail
	z = float(input("z-axis [mm]: "))

	#Dunker goes from 0 to 1000000 in position
	#moveDunker(int(z))

	n = 5 # amount of steps
	traj_target = kinematics.path(x1,y1,x2,y2,steps=n)
	print(traj_target)
	for i in range(n):
		print(traj_target[i])

		ik = kinematics.IK(traj_target[i], elbow=0)
		#print(x,y)
		print(ik)
		motor_S.goG(ik[0], v)
		motor_E.goG(ik[1]+ik[0], v)
		time.sleep(0.1)

		# dyn
		motor_W = -(ik[0] + ik[1])
		#moveDyn(motor_W)

	print("Shouder angle: ", ik[0])
	print("Elbow angle: ", ik[1])
	print("Wrist angle: ", motor_W)

	time.sleep(t)
