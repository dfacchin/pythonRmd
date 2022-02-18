import math
import numpy as np

l1 = 497 # [mm]  Humerus
l2 = 500 # [mm]  Forearm


# Direct kinematics [DK] (transforms joint angles (theta1,theta2) in eef coordinates (x,y))
def DK(theta1,theta2):
	theta1 = np.deg2rad(theta1)
	theta2 = np.deg2rad(theta2)
	x = l1*np.cos(theta1) + l2*np.cos(theta1+theta2)
	y = l1*np.sin(theta1) + l2*np.sin(theta1+theta2)
	x = round(x,2) # round to 2 decimal numbers
	y = round(y,2)
	print("x: " + str(x), "y: " + str(y))
	return x, y

theta1 = float(input("MT shulder [deg]: "))
theta2 = float(input("MT elbow [deg]: "))

coord = DK(theta1,theta2)

# Inverse kinematics [IK] (transforms eef coordinates (x,y) in joint angles (theta1,theta2))
def IK(x,y,elbow=0):

	# elbow=0 (right-arm) elbow towards the wall
	# elbow=1 (left-arm) elbow towards coffee machine
	
	l = np.sqrt(x**2+y**2) # distance from shoulder joint to eef (Pitagora) [mm]
	phi = np.arctan2(y,x) # phi = alpha + theta1
	alpha = np.arccos((l**2+l1**2-l2**2)/(2*l1*l)) # Theorem of the cosine
	
	# alpha=90° causes arcsin to be unsolvable
	if alpha == 0.7853981633974484:
		alpha = alpha - 1e-10
	
	if elbow==0:
		theta1 = phi-alpha
	else:
		theta1 = phi+alpha
	
	# Current frame (x_c,y_c)
	y_c = l*np.sin(alpha) # and also: y_c = l2*sin(theta2)
	
	theta2 = np.arcsin(y_c/l2)
	
	if elbow==1:
		theta2 = -theta2
	
	gamma = np.arccos((l1**2+l2**2-l**2)/(2*l1*l2)) # Theorem of the cosine
	if elbow==0 and gamma < np.pi/2:
		theta2 = np.pi - theta2
	elif elbow==1 and gamma < np.pi/2:
		theta2 = -np.pi - theta2
	
#	# Because we use belts:
#	theta2 = theta2+theta1
	
	# From rad to deg
	theta1 = np.rad2deg(theta1)
	theta2 = np.rad2deg(theta2)
	
	# Round to 2 decimals
	theta1 = round(theta1,2) 
	theta2 = round(theta2,2)
	
	print("theta1: " + str(theta1), "theta2: " + str(theta2))
	return theta1, theta2

x = float(input("x-axis [mm]: ")) # x is along the straight arm
y = float(input("y-axis [mm]: ")) # y is perpendicular to the straight arm

angles = IK(x,y,elbow=0)

