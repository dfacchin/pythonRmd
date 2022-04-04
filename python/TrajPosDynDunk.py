import RMD
import can
import time
import numpy as np
import kinematics

############## DUNKER ##################
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "10.170.43.203"
port = 8891
def moveDunker(pos):
	global sock
	request = "G:" + str(pos) + ":2000"
	# send the message
	data = bytes(str(request).encode("utf8"))
	sock.sendto(data, (host, port))

	# empty buffer
	sock.recv(1024)
############## DUNKER ##################

############## DYNAMIXEL ##################
import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import * # Uses Dynamixel SDK library

#********* DYNAMIXEL Model definition *********
#***** (Use only one definition at a time) *****
MY_DXL = 'X_SERIES'       # X330 (5.0 V recommended), X430, X540, 2X430
# MY_DXL = 'MX_SERIES'    # MX series with 2.0 firmware update.
# MY_DXL = 'PRO_SERIES'   # H54, H42, M54, M42, L54, L42
# MY_DXL = 'PRO_A_SERIES' # PRO series with (A) firmware update.
# MY_DXL = 'P_SERIES'     # PH54, PH42, PM54
# MY_DXL = 'XL320'        # [WARNING] Operating Voltage : 7.4V


ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_POSITION       = 132
DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
BAUDRATE                    = 57600

# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Factory default ID of all DYNAMIXEL is 1
DXL_ID                      = 1
# Use the actual port assigned to the U2D2.
# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = '/dev/ttyUSB0'

TORQUE_ENABLE               = 1     # Value for enabling the torque
TORQUE_DISABLE              = 0     # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         # Goal position


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")

#Change velocity of dyn
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, 112, 30)


def moveDyn(angle):
	global packetHandler,portHandler,DXL_ID,ADDR_TORQUE_ENABLE,TORQUE_ENABLE
	#ANGLE IS IN DEGREES
	#4096 = 360 DEGREES
	posReq = int((angle *4096 ) / 360)
	dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, posReq)
############## DYNAMIXEL ##################


############## GYEMS ##################
# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# Variables:
a = 500  # Motors acceleration
v = 500  # Motors velocity
t = 3  # Waiting time

# ---------- RMD motor with ID 1 (Elbow) ----------
motor_E = RMD.RMD(0x142, bus, ratio=13.5)  # Elbow

#motor_E.info() # 'info' prints Pid and Acceleration

motor_E.Fn30()  # read PID

motor_E.Fn33()  # read acceleration
#motor_E.info()
# Specify desired PID
motor_E.PidPosKp = 30
motor_E.PidPosKi = 0
motor_E.PidVelKp = 30
motor_E.PidVelKi = 5
motor_E.PidTrqKp = 30
motor_E.PidTrqKp = 5
motor_E.Fn31()  # write PID to Ram
# Specify desired accelration
motor_E.acceleration = a
motor_E.Fn34()  # write acceleration to Ram


# ---------- RMD motor with ID 2 (Shoulder) ----------
motor_S = RMD.RMD(0x141, bus, ratio=13.5)  # Shoulder

#motor_S.info()

motor_S.Fn30()  # read PID
motor_S.Fn33()  # read acceleration
#motor_S.info()
# Specify desired PID
motor_S.PidPosKp = 30
motor_S.PidPosKi = 0
motor_S.PidVelKp = 30
motor_S.PidVelKi = 5
motor_S.PidTrqKp = 30
motor_S.PidTrqKp = 5
motor_S.Fn31()  # write PID to Ram
# Specify desired accelration
motor_S.acceleration = a
motor_S.Fn34()  # write acceleration to Ram
############## GYEMS ##################


############## MOVEMENT ##################
while True:

	theta1 = motor_S.multiTurnG
	theta2 = motor_E.multiTurnG
	theta2 = theta2 - theta1
	print("Starting theta1 and theta2:")
	print(theta1,theta2)
	'''
	Read motor multi-turn angles
	and define them as two variables: theta1 and theta2
	'''

	# Compute the actual coordinates:
	target = [theta1, theta2]
	dk = kinematics.DK(target)
	x1 = dk[0]
	y1 = dk[1]
	print("Starting x1 and y1:")
	print(x1)
	print(y1)

	'''
	Choose a target position to compute the joint angles (IK)
	x is along the straight arm (extiting the machine)
	y is perpendicular to the straight arm (positive is towards the wall)
	'''
	x2 = float(input("x-axis [mm]: "))
	y2 = float(input("y-axis [mm]: "))
	# z is up and down of the veritcal rail
	z = float(input("z-axis [mm]: "))

	steps_x = np.linspace(x1, x2, 50, endpoint=True) #  (start, stop, steps)
	steps_y = np.linspace(y1, y2, 50, endpoint=True)

	if x1==x2:
		for y in steps_y:
			x = x1
			x = round(x,2)
			y = round(y,2)
			target = np.array((x, y))
			ik = kinematics.IK(target, elbow=0)
			#print(x,y)
			print(ik)
			motor_S.goG(ik[0], v)
			motor_E.goG(ik[1]+ik[0], v)
			#time.sleep(t)
	elif y1==y2:
		for x in steps_x:
			y = y1
			x = round(x,2)
			y = round(y,2)
			target = np.array((x, y))
			ik = kinematics.IK(target, elbow=0)
			#print(x,y)
			print(ik)
			motor_S.goG(ik[0], v)
			motor_E.goG(ik[1]+ik[0], v)
			#time.sleep(t)
	else:
		for x in steps_x:
			y = (((x-x1)/(x2-x1))*(y2-y1))+y1
			x = round(x,2)
			y = round(y,2)
			target = np.array((x, y))
			ik = kinematics.IK(target, elbow=0)
			print(ik)
			motor_S.goG(ik[0], v)
			motor_E.goG(ik[1]+ik[0], v)
			#time.sleep(t)

	motor_W = -(ik[0] + ik[1])

	print("Shouder angle: ", ik[0])
	print("Elbow angle: ", ik[1])
	print("Wrist angle: ", motor_W)
	#dyn
	moveDyn(motor_W)
	#Dunker goes from 0 to 1000000 in position
	moveDunker(int(z))


	time.sleep(t)
