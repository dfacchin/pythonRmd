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
	
	
#	traj = kinematics.path(x1,y1,x2,y2)
#	print(traj)
#	x = traj[0]
#	y = traj[1]
	
#	motor_S.goG(ik[0], v)
#	motor_E.goG(ik[1]+ik[0], v)
#	time.sleep(t)

