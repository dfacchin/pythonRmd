import numpy as np

x1 = 200
y1 = 200

x2 = 800
y2 = 800

# define starting point
start = []
# define end point
end = []

np.append(x1)
np.append(y1)

np.append(x2, end)
np.append(y2, end)

#start[0] = x1
#start[1] = y1

x = x1

while True:
	y = (((x-x1)/(x2-x1))*(y2-y1))+y1
	print(x, y)
	x = x + 50
	if x > x2:
		break
		
while False:
	y = (((x-start[0])/(end[0]-start[0]))*(end[1]-start[1]))+start[1]
	print(x, y)
	x = x + 50
	if x > end[1]:
		break
