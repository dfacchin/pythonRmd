import motor.RMD as RMD
import can
import time
import numpy as np
import robot.kinematics as kinematics

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
MY_DXL = 'X_SERIES'       # X330 (5.0 V recommended), X430, X540, 2X430

ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_POSITION       = 132
DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
BAUDRATE                    = 57600

# DYNAMIXEL Protocol Version (1.0 / 2.0)
PROTOCOL_VERSION            = 2.0

# Factory default ID of all DYNAMIXEL is 1
DXL_ID                      = 1
# Use the actual port assigned to the U2D2.
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
t = 2  # Waiting time

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
while False:
	# choose a target position to compute the joint angles (IK)
	# x is along the straight arm (extiting the machine)
	x = float(input("x-axis [mm]: "))
	# y is perpendicular to the straight arm (positive is towards the coffee machine)
	y = float(input("y-axis [mm]: "))
	# z is up and down of the veritcal rail
	z = float(input("z-axis [mm]: "))

	target = np.array((x, y))
	ik = kinematics.IK(target, elbow=0)
	print("The following solutions should reach endpoint position %s: %s" % (target, ik))
	#print(ik[0]) #theta_shoulder
	#print(ik[1]) #theta_elbow
	motor_S.goG(ik[0], v)
	motor_E.goG(ik[1]+ik[0], v)
	#Dynamixel
	motor_W = -(ik[0] + ik[1])

	print("Shouder angle: ", ik[0])
	print("Elbow angle: ", ik[1])
	print("Wrist angle: ", motor_W)
	#dyn
	moveDyn(motor_W)
	#Dunker goes from 0 to 1000000 in position
	moveDunker(int(z))


arrayEl = [[800,0,0],[700,-200,100000],[900,100,10000],[500,0,100000],[1000,0,0]] # [x, y, z]
demoArray = [[700,0,500000],[700,80,260000],[750,-100,450000],[850,-250,300000],[200,0,0]] # [x, y, z]
new = [[700,0,480000],[700,-200,350000],[880,-350, 300000],[850,-180,520000],[850,-180,730000],[150,0,200000]] # [x, y, z]

for el in new:
	# choose a target position to compute the joint angles (IK)
	x = float(el[0]) # x is along the straight arm (extiting the machine)
	y = float(el[1]) # y is perpendicular to the straight arm
	z = int(el[2])
	target = np.array((x, y))
	ik = kinematics.IK(target, elbow=0)

	motor_S.goG(ik[0], v)
	motor_E.goG(ik[1]+ik[0], v)

	motor_W = -(ik[0] + ik[1])

	print("Shouder angle: ", ik[0])
	print("Elbow angle: ", ik[1])
	print("Wrist angle: ", motor_W)
	#dyn
	moveDyn(motor_W)
	#Dunker goes from 0 to 1000000 in position
	moveDunker(z)

	time.sleep(t)
