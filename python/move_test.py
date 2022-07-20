import numpy as np

# Variables
depth_offset = 0 # [mm]
apple_coords = [[700,0],[700,200],[800,300],[650,350]]
home = [300,0]
drop = [500,0]
pp = [home]
steps = 3
solt = []

#x1 = x_h # x_home
#x2 = x_a # x_apple
x1 = 301
x2 = 800.5
y1 = 0
y2 = 200.6
steps_x = np.linspace(x1, x2, steps, endpoint=True)  # (start, stop, steps)
steps_y = np.linspace(y1, y2, steps, endpoint=True)

# for xi in steps_x:
#     print(xi)

print(steps)
if x1 == x2:
    for y in steps_y:
        x = x1
        soln = [x, y]
        solt.append(soln)
elif y1 == y2:
    for x in steps_x:
        y = y1
        soln = [x, y]
        solt.append(soln)
else:
    for x in steps_x:
        y = (((x-x1)/(x2-x1))*(y2-y1))+y1
        soln = [x, y]
        solt.append(soln)
print(solt)