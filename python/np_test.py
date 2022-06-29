import numpy as np

time = [0, 2, 4, 8, 10]
theta = np.array([[10, 0], [20, 0], [0, 0], [30, 0], [40, 0]]) # [deg]
theta_d = np.zeros((5,2)) # (r, c)
print(theta)
print(theta_d)


v = np.zeros() # create an empty list
for index, (el_time,el_theta) in enumerate(zip(time,theta)):
    if (index+1 < len(time)): # compute only until the second to last value
        v = (theta[index+1]-theta[index])/(time[index+1]-time[index])
        np.append()
        #v.append((theta[index+1]-theta[index])/(time[index+1]-time[index]))
print("v: " + str(v))
