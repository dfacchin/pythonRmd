import numpy as np
import time
import can

import kinematics
import RMD

# Variables:
a = 500  # Motors acceleration
v = 500  # Motors velocity
t = 2    # Waiting time

# Connect via CanBus:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# ---------- RMD motor ID 1 (Elbow) ----------
motor_E = RMD.RMD(0x142, bus, ratio=13.5)  # Elbow

# Specify desired PID
motor_E.PidPosKp = 30
motor_E.PidPosKi = 0
motor_E.PidVelKp = 30
motor_E.PidVelKi = 5
motor_E.PidTrqKp = 30
motor_E.PidTrqKp = 5
motor_E.Fn31()  # write PID to Ram
# Specify desired accelration
motor_E.acceleration = a
motor_E.Fn34()  # write acceleration to Ram

# ---------- RMD motor ID 2 (Shoulder) ----------
motor_S = RMD.RMD(0x141, bus, ratio=13.5)  # Shoulder

# Specify desired PID
motor_S.PidPosKp = 30
motor_S.PidPosKi = 0
motor_S.PidVelKp = 30
motor_S.PidVelKi = 5
motor_S.PidTrqKp = 30
motor_S.PidTrqKp = 5
motor_S.Fn31()  # write PID to Ram
# Specify desired accelration
motor_S.acceleration = a
motor_S.Fn34()  # write acceleration to Ram

# Define desired eef positions [x,y]
'''
x = straight along the exended arm (positive is towards the trees) [mm]
    Maximum value of x is 1000mm (completely extended)

y = perpendicular to the straight arm (positive is on the right) [mm] 
'''
coords = [[1000,0],[800,0],[700,200],[700,-200],[800,0],[500,0]]

for coord in coords:
	x = float(coord[0])
	y = float(coord[1])
	target = np.array((x, y))
	theta = kinematics.IK(target, elbow=0)

	motor_S.goG(theta[0], v)
	motor_E.goG(theta[1]+theta[0], v)

	print("Shouder angle: ", theta[0])
	print("Elbow angle: ", theta[1])

	time.sleep(t)