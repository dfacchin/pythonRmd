import RMD
import can
import time
import Kinematics

# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# ---------- RMD motor with ID 1 (Elbow) ----------
motor_E = RMD.RMD(0x142,bus,ratio = 13.5) # Elbow

# ---------- RMD motor with ID 2 (Shoulder) ----------
motor_S = RMD.RMD(0x141,bus,ratio = 13.5) # Shoulder

# Read internal encoder position and off set
motor_E.Fn90()
motor_S.Fn90()

motor_E.encoderInfo()
motor_S.encoderInfo()


# Variables:
a = 550 # Motors acceleration
v = 220 # Motors velocity
t = 5 # Waiting time

motor_E.acceleration = a
motor_E.Fn34() # write acceleration to Ram

motor_S.acceleration = a
motor_S.Fn34() # write acceleration to Ram

while True:
	motor_E.Fn90()
	motor_S.Fn90()
	motor_E.Fn92()
	motor_S.Fn92()

	motor_E.print()
	motor_S.print()
	motor_E.print()
	motor_S.print()
#	shoulder = int(input("MT shoulder [deg]: "))
#	elbow = int(input("MT elbow [deg]: "))
	shoulder = 45
	elbow = -90
	motor_E.goG(elbow+shoulder,v)
	motor_S.goG(shoulder,v)
	coord = Kinematics.DK(shoulder,elbow+shoulder)
	print(coord)
	time.sleep(3)
	
	shoulder = -45
	elbow = 90
	motor_E.goG(elbow+shoulder,v)
	motor_S.goG(shoulder,v)
	time.sleep(3)
	coord = Kinematics.DK(shoulder,elbow+shoulder)
	print(coord)

