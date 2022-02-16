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

'''
Procedure:
-  Read current motor angles "multi-turn" (theta1_c, theta2_c) [deg]
-  Calculate DK theta1_c,theta2_c --> x,y
-  Set desired goal position (x_new,y_new)
-  Calculate IK x_new,y_new --> theta1,theta2
-  Use goG function to move the motors
-  Implement a straight and smooth trajectory
'''

theta1_c = motor_S.Fn92() # Read current multi-turn angle (shoulder)
theta2_c = motor_E.Fn92()	# Read current multi-turn angle (elbow)

coord = DK(theta1_c,theta2_c) # get current x,y coordinates 
print(coord)

x_new = int(input("Enter desired x-coordinate: "))
y_new = int(input("Enter desired y-coordinate: "))

angles = IK(x_new, y_new, elbow=0) # get new joint angles
print(angles)

# now that we obtained theta1 and theta2 from the IK
# we can move the motors:

angle_S = theta1
angle_E = theta2
motor_S.goG(angle_S,vel) # goG(Pos(degrees), velocity)
motor_E.goG((angle_E+angle_S),vel)
time.sleep(t)



'''
while True:

	# Straight
	angle_S = 15
	angle_E = -5
	motor_S.goG(angle_S,vel) # goG(Pos(degrees), velocity)
	motor_E.goG((angle_E+angle_S),vel)
	time.sleep(t)

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

