import RMD
import can
import time
import numpy as np
import kinematics

# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# Variables:
a = 200  # Motors acceleration
v = 200  # Motors velocity
t = 3  # Waiting time

# ---------- RMD motor with ID 1 (Elbow) ----------
motor_E = RMD.RMD(0x142, bus, ratio=13.5)  # Elbow

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
	motor_E.Fn92()
	motor_S.Fn92()
	motor_E.print()
	motor_S.print()
	break

while False:
	# choose a target position to compute the joint angles (IK)
	# x is along the straight arm (extiting the machine)
	x = float(input("x-axis [mm]: "))
	# y is perpendicular to the straight arm (positive is towards the wall)
	y = float(input("y-axis [mm]: "))
	target = np.array((x, y))
	ik = kinematics.IK(target, elbow=1)
	print("The following solutions should reach endpoint position %s: %s" % (target, ik))

	motor_S.goG(ik[0], v)
	motor_E.goG(ik[1]+ik[0], v)
	time.sleep(t)


while False:
	'''
	Read motor multi-turn angles
	and define them as two variables: theta1 and theta2
	'''
	theta1 = 0
	theta2 = 90
	# Compute the actual coordinates:
	target = [theta1, theta2]
	dk = kinematics.DK(target)
	x1 = dk[0]
	y1 = dk[1]
	print(x1)
	print(y1)
	
	'''
	# choose a target position to compute the joint angles (IK)
	# x is along the straight arm (extiting the machine)
	x2 = float(input("Desired x-coord [mm]: "))
	# y is perpendicular to the straight arm (positive is towards the wall)
	y2 = float(input("Desired y-coord [mm]: "))
	'''
	x2 = 700
	y2 = 10
#	target = np.array((x2, y2))
#	ik = kinematics.IK(target, elbow=1)
#	print(ik[0]) # theta1
#	print(ik[1]) # theta2
	
	
	steps_x = np.linspace(x1, x2, 20, endpoint=True) #  (start, stop, steps)
	steps_y = np.linspace(y1, y2, 20, endpoint=True)
	
	if x1==x2:
		for y in steps_y:
			x = x1
			x = round(x,2)
			y = round(y,2)
			target = np.array((x, y))
			ik = kinematics.IK(target, elbow=1)
			#print(x,y)
			print(ik)
			motor_S.goG(ik[0], v)
			motor_E.goG(ik[1]+ik[0], v)
			time.sleep(t)
	elif y1==y2:
		for x in steps_x:
			y = y1
			x = round(x,2)
			y = round(y,2)
			target = np.array((x, y))
			ik = kinematics.IK(target, elbow=1)
			#print(x,y)
			print(ik)
			motor_S.goG(ik[0], v)
			motor_E.goG(ik[1]+ik[0], v)
			time.sleep(t)
	else:
		for x in steps_x:
			y = (((x-x1)/(x2-x1))*(y2-y1))+y1
			x = round(x,2)
			y = round(y,2)
			target = np.array((x, y))
			ik = kinematics.IK(target, elbow=1)
			print(ik)
			motor_S.goG(ik[0], v)
			motor_E.goG(ik[1]+ik[0], v)
			time.sleep(t)
	break


