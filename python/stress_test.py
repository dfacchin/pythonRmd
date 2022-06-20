import numpy as np
import time
import can

import kinematics
import RMD

# Connect via CanBus:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# Variables:
a = 2000  # Motors acceleration
v = 2000  # Motors velocity
t = 5     # Waiting time

# ---------- RMD motor ID 1 (Elbow) ----------
motor_E = RMD.RMD(0x142, bus, ratio=13.5)  # Elbow

motor_E.Fn30()  # read PID
motor_E.Fn33()  # read acceleration
# Specify desired PID
motor_E.PidPosKp = 50
motor_E.PidPosKi = 0
motor_E.PidVelKp = 50
motor_E.PidVelKi = 5
motor_E.PidTrqKp = 50
motor_E.PidTrqKp = 5
motor_E.Fn31()  # write PID to Ram
# Specify desired accelration
motor_E.acceleration = a
motor_E.Fn34()  # write acceleration to Ram

# ---------- RMD motor ID 2 (Shoulder) ----------
motor_S = RMD.RMD(0x141, bus, ratio=13.5)  # Shoulder

motor_E.Fn30()  # read PID
motor_E.Fn33()  # read acceleration
# Specify desired PID
motor_S.PidPosKp = 50
motor_S.PidPosKi = 0
motor_S.PidVelKp = 50
motor_S.PidVelKi = 5
motor_S.PidTrqKp = 50
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
coords = [[1000,0],[800,0],[700,200],[700,-200],[800,0],[500,0],[1000,0]]

for coord in coords:
	x = float(coord[0])
	y = float(coord[1])
	target = np.array((x, y))
	ik = kinematics.IK(target, elbow=1)

	motor_S.goG(-ik[0], v) # We use -theta since we put the pulley up-side-down
	motor_E.goG(ik[1]+ik[0], v)

	print("Shouder angle: ", ik[0])
	print("Elbow angle: ", ik[1])

	time.sleep(t)