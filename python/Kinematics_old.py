import math
import numpy as np

# Direct kinematics [DK] (transforms joint angles (theta1,theta2) in eef coordinates (x,y))

# Link lengths:
l1 = 510.0 # [mm] Humerus
l2 = 479.5 # [mm] Forearm
# Joint angles:
#theta1 =  ... # S-Motor [deg]
#theta2 = ... + theta1 # E-Motor [deg]

def DK(theta1,theta2):
	x = l1*math.cos(math.degrees(theta1))+l2*math.cos(math.degrees(theta1))*math.cos(math.degrees(theta2))
	y = l1*math.sin(math.degrees(theta1))+l2*math.sin(math.degrees(theta1))*math.sin(math.degrees(theta2))
	print('x:' + str(x), 'y:' + str(y))

# Inverse kinematics [IK] (transforms eef coordinates (x,y) in joint angles (theta1,theta2))

def IK(x,y):
	l = math.sqrt(x**2+y**2) # distance from shoulder joint to eef (Pitagora) [mm]
	phi = math.atan2(y,x) # phi = alpha + theta1
	alpha = math.acos((l**2+l1**2-l2**2)/(2*l1*l)) # Theorem of the cosine
	theta1 = math.degrees(phi-alpha)
	# Current frame (x_c,y_c)
	y_c = l*math.sin(math.degrees(alpha)) # y_c = l2*sin(theta2)
	theta2 = math.asin((l*math.sin(alpha))/l2)
	theta2 = math.degrees(theta2+theta1) # because we are using belts
	print('theta1:' + str(theta1))


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
