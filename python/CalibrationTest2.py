import RMD
import can
import time

# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# ---------- RMD motor with ID 1 (Elbow) ----------
motor_E = RMD.RMD(0x142,bus,ratio = 13) # Elbow

# ---------- RMD motor with ID 2 (Shoulder) ----------
motor_S = RMD.RMD(0x141,bus,ratio = 13) # Shoulder


motor_E.Fn90()
motor_S.Fn90()

motor_E.encoderInfo()
motor_S.encoderInfo()

while True:
	motor_E.Fn90()
	motor_S.Fn90()
	motor_E.Fn92()
	motor_S.Fn92()
	motor_E.Fn94()
	motor_S.Fn94()

	motor_E.print()
	motor_S.print()
	motor_E.print()
	motor_S.print()
	action = input("C_alibrate Z_ero")
	if (action == "C"):
		motor_E.Fn91(180)
		motor_S.Fn91(180)
	elif action == "Z":
		motor_E.Fn19()
		motor_S.Fn19()
