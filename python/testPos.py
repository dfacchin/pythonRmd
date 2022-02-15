import RMD
import can
import time
# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)


# ---------- RMD motor with ID 1 (Elbow) ----------
motor1 = RMD.RMD(0x142,bus,ratio = 13) # Elbow

motor1.info() # 'info' prints Pid and Acceleration 

motor1.Fn30() # read PID
motor1.Fn33() # read acceleration
motor1.info()
# Specify desired PID
motor1.PidPosKp  = 30 
motor1.PidPosKi  = 0
motor1.PidVelKp  = 30
motor1.PidVelKi  = 5
motor1.PidTrqKp  = 30
motor1.PidTrqKp  = 5
motor1.Fn31() # write PID to Ram
# Specify desired accelration
motor1.acceleration = 1000 
motor1.Fn34() # write acceleration to Ram

motor1.Fn30() # read PID
motor1.Fn33() # read acceleration
motor1.info()


# ---------- RMD motor with ID 2 (Shoulder) ----------
motor2 = RMD.RMD(0x141,bus,ratio = 13) # Shoulder

motor2.info()

motor2.Fn30() # read PID
motor2.Fn33() # read acceleration
motor2.info()
# Specify desired PID
motor2.PidPosKp  = 30
motor2.PidPosKi  = 0
motor2.PidVelKp  = 30
motor2.PidVelKi  = 5
motor2.PidTrqKp  = 30
motor2.PidTrqKp  = 5
motor2.Fn31() # write PID to Ram
# Specify desired accelration
motor2.acceleration = 1000 
motor2.Fn34() # write acceleration to Ram

motor2.Fn30() # read PID
motor2.Fn33() # read acceleration
motor2.info()


# ---------- Commands ----------

while True:
	angle1 = int(input("Elbow"))
	angle2 = int(input("Shoulder"))
	motor2.goG(angle2,1000)
	motor1.goG(angle1+angle2,1000) #gradi. velocità
	motor1.Fn92()	
	motor2.Fn92()
	motor1.print()	
	motor2.print()
	time.sleep(2)


