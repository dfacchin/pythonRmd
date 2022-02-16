import math

l1 = 497 # [mm]  Humerus
l2 = 500 # [mm]  Forearm
	
def DK(theta1,theta2):
	x = l1*math.cos(math.radians(theta1))+l2*math.cos(math.radians(theta1+theta2))
	y = l1*math.sin(math.radians(theta1))+l2*math.sin(math.radians(theta1+theta2))
	x = round(x,2) # round to 2 decimal numbers
	y = round(y,2)
	print('x:' + str(x), 'y:' + str(y))
	return x, y
	
direct = DK(0,90) # set desired values in degrees

print(direct)

