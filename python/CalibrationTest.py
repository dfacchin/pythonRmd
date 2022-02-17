import RMD
import can
import time

# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# ---------- RMD motor with ID 1 (Elbow) ----------
motor_E = RMD.RMD(0x142,bus,ratio = 13.5) # Elbow

# ---------- RMD motor with ID 2 (Shoulder) ----------
motor_S = RMD.RMD(0x141,bus,ratio = 13.5) # Shoulder


motor_E.Fn90()
motor_S.Fn90()

motor_E.encoderInfo()
motor_S.encoderInfo()

while True:
	motor_E.Fn90()
	motor_S.Fn90()
	motor_E.Fn92()
	motor_S.Fn92()

	motor_E.print()
	motor_S.print()
	motor_E.print()
	motor_S.print()
	shulder = int(input("MT shulder"))
	elbow = int(input("MT elbow"))
	motor_E.goG(elbow,10)
	motor_S.goG(shulder,10)
	
'''
while True:

	# Straight
	angle_S = int(180/13)
	angle_E = int(180/13)
	motor_S.goG(angle_S,vel) # goG(Pos(degrees), velocity)
	motor_E.goG((angle_E+angle_S),vel)
	time.sleep(t)
	break
	

	# Right
	angle_S = -30
	angle_E = 30
	motor_S.goG(angle_S,vel)
	motor_E.goG((angle_E+angle_S),vel)
	time.sleep(t)
	
	# Left
	angle_S = 60
	angle_E = -40
	motor_S.goG(angle_S,vel)
	motor_E.goG((angle_E+angle_S),vel)
	time.sleep(t)


#	angle_E = int(input("Elbow's angle (degrees): "))
#	angle_S = int(input("Shoulder's angle (degrees): "))
#	motor_S.goG(angle_S,vel) # goG(Pos(degrees), velocity)
#	motor_E.goG((angle_E+angle_S),vel)
#	motor_E.Fn92()	# Read multi-turn angle (elbow)
#	motor_S.Fn92()  # Read multi-turn angle (shoulder)
#	motor_E.print()	
#	motor_S.print()
#	time.sleep(2)
'''
