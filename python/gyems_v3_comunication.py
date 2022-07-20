import numpy as np
import can
import time

import RMD_V3
import kinematics
from trajectory_planner import Joint


# Specify the bus
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# Variables
ratio = 9 # Gear ratio
#v = 1000  # Motors velocity
a = 1000  # Motors acceleration



# ---------- RMD motor with ID 1 ----------
motor_E = RMD_V3.RMDV3(0x140, bus, 1)
#motor_E.Fn30()  # read PID
#motor_E.Fn33()  # read acceleration
# Specify desired PID
motor_E.PidPosKp = 30
motor_E.PidPosKi = 5
motor_E.PidVelKp = 30
motor_E.PidVelKi = 5
motor_E.PidTrqKp = 5
motor_E.PidTrqKi = 5
motor_E.Fn31()  # write PID to Ram
# Specify desired acceleration
motor_E.acceleration = a
motor_E.Fn34()  # write acceleration to Ram
motor_E.info()

for a in range(5):
	print("Start Moving")
	motor_E.goG(3600,200)
	timex = time.time()
	while(time.time()-timex)<10:
		print(motor_E.get_actual_angle())
		time.sleep(0.1)
	motor_E.goG(0,200)
	timex = time.time()
	while(time.time()-timex)<10:
		print(motor_E.get_actual_angle())
		time.sleep(0.1)

