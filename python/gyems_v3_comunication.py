import numpy as np
import can
import time

import RMD
import kinematics
from trajectory_planner import Joint
import plots


# Specify the bus
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# Variables
ratio = 9 # Gear ratio
#v = 1000  # Motors velocity
a = 1000  # Motors acceleration



# ---------- RMD motor with ID 1 ----------
motor_E = RMD.RMD(0x140, bus, ratio)
#motor_E.Fn30()  # read PID
motor_E.Fn33()  # read acceleration
# Specify desired PID
# motor_E.PidPosKp = 30
# motor_E.PidPosKi = 5
# motor_E.PidVelKp = 30
# motor_E.PidVelKi = 30
# motor_E.PidTrqKp = 5
# motor_E.PidTrqKi = 5
# motor_E.Fn31()  # write PID to Ram
# Specify desired acceleration
#motor_E.acceleration = a
#motor_E.Fn34()  # write acceleration to Ram