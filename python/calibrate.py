import RMD
import can

'''
Python script to calibrate the horizontal SCARA arm,
Gyems motors only (shoulder and elbow).
Before running this script place the arm manually perpendicular to the trees (completely extended).
After this calibration the motor angles will be set to 0 degrees.
'''

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

	motor_E.print()
	motor_S.print()
	motor_E.print()
	motor_S.print()
	input(print('Press "Enter" to complete the calibration.'))
	motor_E.Fn19()	
	motor_S.Fn19()
	