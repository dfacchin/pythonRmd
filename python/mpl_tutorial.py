import numpy as np
import matplotlib.pyplot as plt

t = [0, 2, 4, 8, 10]
theta = [10, 20, 0, 30, 40]
theta_d = [0, -10, 20, 3, 0]
theta_dd = [0, -35, 40, -3, -10]

plt.style.use('seaborn-dark') # 'Solarize_Light2'

# Position Plot
plt.subplot(1,3,1) # (row, column, plot)
plt.title("Position")
plt.xlabel("time [s]")
plt.ylabel("theta [deg]")
plt.plot(t, theta, marker='.')
plt.grid(True)

# Velocity Plot
plt.subplot(1,3,2) # (row, column, plot)
plt.title("Velocity")
plt.xlabel("time [s]")
plt.ylabel("theta_d [deg/s]")
plt.plot(t, theta_d, color='y', marker='.')
plt.grid(True)

# Acceleration Plot
plt.subplot(1,3,3) # (row, column, plot)
plt.title("Acceleration")
plt.xlabel("time [s]")
plt.ylabel("theta_dd [deg/s^2]")
plt.plot(t,theta_dd, color='r', marker='.')
plt.grid(True)

plt.tight_layout() # avoid text overlapping
plt.show()