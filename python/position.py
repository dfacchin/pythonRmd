import RMD
import can
import time
import numpy as np
import kinematics

# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# Variables:
a = 1000  # Motors acceleration
v = 1000  # Motors velocity
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


while True:
	# choose a target position to compute the joint angles (IK)
	# x is along the straight arm (extiting the machine)
	x = float(input("x-axis [mm]: "))
	# y is perpendicular to the straight arm (positive is towards the coffee machine)
	y = float(input("y-axis [mm]: "))
	target = np.array((x, y))
	ik = kinematics.IK(target, elbow=1)
	print("The following solutions should reach endpoint position %s: %s" % (target, ik))

	#print(ik[0]) #theta_shoulder
	#print(ik[1]) #theta_elbow

	motor_S.goG(-ik[0], v)
	motor_E.goG(ik[1]+ik[0], v)
	time.sleep(t)


while False:
	# choose desired joint angles to compute x,y coordinates (DK)
	theta1 = float(input("Shoulder angle [deg]: "))
	theta2 = float(input("Elbow angle [deg]: "))
	target = np.array((theta1, theta2))
	dk = kinematics.DK(target)
	print("The following angles %s, correspond to x,y coord: %s" % target % dk)

	motor_S.goG(dk[0], v)
	motor_E.goG(dk[1]+dk[0], v)
	time.sleep(t)

'''
while True:

	motor_E.Fn90()
	motor_S.Fn90()
	motor_E.Fn92()
	motor_S.Fn92()

	motor_E.print()
	motor_S.print()

	shoulder = int(input("MT shoulder [deg]: "))
	elbow = int(input("MT elbow [deg]: "))
	motor_E.goG(elbow+shoulder,v)
	motor_S.goG(shoulder,v)
	time.sleep(t)
'''
