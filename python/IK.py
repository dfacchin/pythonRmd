# Inverse kinematics [IK] (transforms eef coordinates (x,y) in joint angles (theta1,theta2))

import math

l1 = 497
l2 = 500

#x = 351
#y = 851

def IK(x,y,elbow=0):

	# elbow=0 (left-arm) towards the trees
	# elbow=1 (right-arm) towards the machine
#	if (elbow==1):
#		x = -x
		
	l = math.sqrt(x**2+y**2) # distance from shoulder joint to eef (Pitagora) [mm]
	if (l > (l1+l2)):
		l = (l1+l2)-0.001
		
	phi = math.atan2(y,x) # phi = alpha + theta1
	alpha = math.acos((l**2+l1**2-l2**2)/(2*l1*l)) # Theorem of the cosine
	theta1 = phi-alpha
	# Current frame (x_c,y_c)
	y_c = l*math.sin(alpha) # y_c = l2*sin(theta2)
	theta2 = math.asin((l*math.sin(alpha))/l2)
#	theta2 = theta2+theta1 # because we are using belts

	theta1 = math.degrees(theta1) # from rad to deg
	theta2 = math.degrees(theta2)
	
	if (elbow==1):
		theta1 = theta1 + 90
		theta2 = -theta2

	theta1 = round(theta1,2) # round to 2 decimals
	theta2 = round(theta2,2)

	print("theta1: " + str(theta1))
	print("theta2: " + str(theta2))

	return theta1, theta2

inverse = IK(705,2.12,elbow=1)
print(inverse)

'''
def IK(x,y):
	l = math.sqrt(x**2+y**2) # distance from shoulder joint to eef (Pitagora) [mm]
	phi = math.atan2(y,x) # phi = alpha + theta1
	alpha = math.acos((l**2+l1**2-l2**2)/(2*l1*l)) # Theorem of the cosine
	theta1 = phi-alpha
	# Current frame (x_c,y_c)
	y_c = l*math.sin(alpha) # y_c = l2*sin(theta2)
	theta2 = math.asin((l*math.sin(alpha))/l2)
	theta2 = theta2+theta1 # because we are using belts

	theta1 = math.degrees(theta1) # from rad to deg
	theta2 = math.degrees(theta2)

	theta1 = round(theta1,2) # round to 2 decimals
	theta2 = round(theta2,2)

	print("theta1: " + str(theta1))
	print("theta2: " + str(theta2))

	return theta1, theta2

inverse = IK(400,100)
print(inverse)
'''
