import numpy as np
import kinematics

while True:
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
	

	# choose a target position to compute the joint angles (IK)
	# x is along the straight arm (extiting the machine)
	x2 = float(input("Desired x-coord [mm]: "))
	# y is perpendicular to the straight arm (positive is towards the wall)
	y2 = float(input("Desired y-coord [mm]: "))
	target = np.array((x2, y2))
	ik = kinematics.IK(target, elbow=1)
	print(ik[0]) # theta1
	print(ik[1]) # theta2
	
	traj = kinematics.path(x1,y1,x2,y2)
	x = traj[0]
	y = traj[1]
#	motor_S.goG(ik[0], v)
#	motor_E.goG(ik[1]+ik[0], v)
#	time.sleep(t)
	
	break
