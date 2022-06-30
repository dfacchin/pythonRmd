import numpy as np

time = [0, 2, 4, 8, 10] # [s]
fn = 10 # [Hz] frequency

for index, el_time in enumerate(time):
    if (index+1 < len(time)):
        dt = time[index+1] - time[index] # delta time
        steps = fn * dt
        print(steps)
        t = np.linspace(time[index], time[index+1], steps) # [s] Time
        print(t)