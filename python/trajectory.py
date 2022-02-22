import numpy as np

'''
Current pose is obtained from DK:
Read joint angles(theta1,theta2)-->Compute DK(x1,y1)
'''
x1 = 800.0
y1 = 800.0
'''
New pose is specified by us: (x2,y2)
'''
x2 = 300.0
y2 = 800.0

# Definition of the path points:
steps_x = np.linspace(x1, x2, 20, endpoint=True) # np.linspace(start, stop, num)
steps_y = np.linspace(y1, y2, 20, endpoint=True)

if x1==x2:
	for y in steps_y:
		x = x1
		x = round(x,2)
		y = round(y,2)
		print(x,y)
elif y1==y2:
	for x in steps_x:
		y = y1
		x = round(x,2)
		y = round(y,2)
		print(x,y)
else:
	for x in steps_x:
		y = (((x-x1)/(x2-x1))*(y2-y1))+y1
		x = round(x,2)
		y = round(y,2)
		print(x,y)

