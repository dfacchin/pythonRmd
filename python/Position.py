import RMD
import can
import time

# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# Variables:
acc = 2000 # Motors acceleration
vel = 3000 # Motors velocity
t = 4 # Waiting time

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

# Home:
# S: 15
# E: -5


while True:

	# Straight
	angle_S = 15
	angle_E = -5
	motor_S.goG(angle_S,vel) # goG(Pos(degrees), velocity)
	motor_E.goG((angle_E+angle_S),vel)
	time.sleep(t)
	
'''
l1 = 500
l2 = 500
angle_S = theta1
angle_E = theta2
	
def DK(theta1,theta2):
	x = l1*math.cos(math.degrees(theta1))+l2*math.cos(math.degrees(theta1))*math.cos(math.degrees(theta2))
	y = l1*math.sin(math.degrees(theta1))+l2*math.sin(math.degrees(theta1))*math.sin(math.degrees(theta2))
	print('x:' + str(x), 'y:' + str(y))




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

