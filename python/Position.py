import RMD
import can
import time

# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# Variables:
acc = 1000 # Motors acceleration
vel = 1000 # Motors velocity

# ---------- RMD motor with ID 1 (Elbow) ----------
motor_E = RMD.RMD(0x142,bus,ratio = 13) # Elbow

motor_E.info() # 'info' prints Pid and Acceleration 

motor_E.Fn30() # read PID
motor_E.Fn33() # read acceleration
motor_E.info()
# Specify desired PID
motor_E.PidPosKp  = 30 
motor_E.PidPosKi  = 0
motor_E.PidVelKp  = 30
motor_E.PidVelKi  = 5
motor_E.PidTrqKp  = 30
motor_E.PidTrqKp  = 5
motor_E.Fn31() # write PID to Ram
# Specify desired accelration
motor_E.acceleration = acc
motor_E.Fn34() # write acceleration to Ram

motor_E.Fn30() # read PID
motor_E.Fn33() # read acceleration
motor_E.info()


# ---------- RMD motor with ID 2 (Shoulder) ----------
motor_S = RMD.RMD(0x141,bus,ratio = 13) # Shoulder

motor_S.info()

motor_S.Fn30() # read PID
motor_S.Fn33() # read acceleration
motor_S.info()
# Specify desired PID
motor_S.PidPosKp  = 30
motor_S.PidPosKi  = 0
motor_S.PidVelKp  = 30
motor_S.PidVelKi  = 5
motor_S.PidTrqKp  = 30
motor_S.PidTrqKp  = 5
motor_S.Fn31() # write PID to Ram
# Specify desired accelration
motor_S.acceleration = acc
motor_S.Fn34() # write acceleration to Ram

motor_S.Fn30() # read PID
motor_S.Fn33() # read acceleration
motor_S.info()


# ---------- Commands ----------

while True:
	angle_E = int(input("Elbow's angle (degrees): "))
	angle_S = int(input("Shoulder's angle (degrees): "))
	motor_S.goG(angle_S,vel) # goG(Pos(degrees), velocity)
	motor_E.goG(angle_E+angle_S,vel)
	motor_E.Fn92()	
	motor_S.Fn92()
	motor_E.print()	
	motor_S.print()
	time.sleep(2)

