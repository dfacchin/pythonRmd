import numpy as np

# Variables

# time
dt = 0.1 # [s] time step
tEnd = 4 # [s] time in which we want the motion to be executed
t = np.linspace(0, dt, tEnd) # [s]

# position

# velocity

# acceleration

# Delta values
delta_theta = theta_f - theta_i
theta_d_sum = theta_d_f + theta_d_i

# c-coefficients
c0 = theta_i
c1 = theta_d_i
c2 = ((3*delta_theta)/tEnd**2) - ((2*theta_d_i)/tEnd) - (theta_d_f/tEnd)
c3 = (-(2*delta_theta)/tEnd**3) + (theta_d_sum/tEnd**2)

# Cubic Polinomial [Trajectory of angular displacement]

theta = c0 + (c1*t) +(c2*t**2) + (c3*t**3)

# Cubic Polinomial [Trajectory of angular velocity]

theta_d = c1 + (2*c2*t) +(3*c3*t**2)
