import math
import numpy as np
l1 = 497 # [mm]  Humerus
l2 = 500 # [mm]  Forearm
	

# Direct kinematics [DK] (transforms joint angles (theta1,theta2) in eef coordinates (x,y))
def DK(theta1,theta2):
	x = l1*math.cos(math.radians(theta1))+l2*math.cos(math.radians(theta1+theta2))
	y = l1*math.sin(math.radians(theta1))+l2*math.sin(math.radians(theta1+theta2))
	x = round(x,2) # round to 2 decimal numbers
	y = round(y,2)
	print('x:' + str(x), 'y:' + str(y))
	return x, y
	
# Inverse kinematics [IK] (transforms eef coordinates (x,y) in joint angles (theta1,theta2))
def IK(x,y,elbow=0):

	# elbow=0 (left-arm) towards the trees
	# elbow=1 (right-arm) towards the machine
		
	l = np.sqrt(x**2+y**2) # distance from shoulder joint to eef (Pitagora) [mm]
	if (l > (l1+l2)):
		l = (l1+l2)-0.001
		
	phi = np.arctan2(y,x) # phi = alpha + theta1
	alpha = np.arccos((l**2+l1**2-l2**2)/(2*l1*l)) # Theorem of the cosine
	
	if elbow==0:
		theta1 = phi-alpha
	else:
		theta1 = phi+alpha
		
	# Current frame (x_c,y_c)
	y_c = l*np.sin(alpha) # y_c = l2*sin(theta2)
	theta2 = np.arcsin((l*math.sin(alpha))/l2)
	
	
	if elbow==1:
		theta2 = -theta2
	
#	theta2 = theta2+theta1 # because we are using belts

	theta1 = math.degrees(theta1) # from rad to deg
	theta2 = math.degrees(theta2)
	
	gamma = np.arccos((l1**2+l2**2-l**2)/(2*l1*l2)) # Theorem of the cosine
	if elbow==0 and gamma < 90:
		theta2 = 180 - theta2
	elif elbow==1 and gamma < 90:
		theta2 = -180 - theta2

	theta1 = round(theta1,2) # round to 2 decimals
	theta2 = round(theta2,2)

	print("theta1: " + str(theta1))
	print("theta2: " + str(theta2))

	return theta1, theta2
	
'''
# Define points of a trajectory (until the robot receives the last_point=1 and then executes the trajectory) [max 50 points]

def trajectory(self,x=...,y=...,num_point=0,last_point=0,t=0,sync=True,verbose=False):
	theta1,theta2 = self.IK(x,y)
	if last_point==0: # Intermediate points do not have sync mode
		sync=False
	# if (verbose):
	#   print (">Traj XY:",x,y," IK:",theta1,theta2)
	# self.sendCommand(b'JJAT',int(A1*100),int(A2*100),int(z*100),ch4,ch5,elbow,num_point,last_point,t,sync)

traj_points= 40
move_range = 80
direct_move = True
without_traj = True

for k in range(1):
	for i in range(traj_points):
		myRobot.trajectory(-move_range+i*(move_range*2/traj_points),130,num_point=i)
	myRobot.trajectory(move_range,130,num_point=traj_points,last_point=1)
	for i in range(traj_points):
		myRobot.trajectory(move_range-i*(move_range*2/traj_points),130,num_point=i)
	myRobot.trajectory(-move_range,130,num_point=traj_points,last_point=1)
'''
