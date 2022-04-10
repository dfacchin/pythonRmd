#INSTALL CAN
#pip install python-can
#INSTALL DYN SDK
#pip install dynamixel-sdk

import socketserver as SocketServer
import threading
import os
import struct
import time                      # to import module time


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



###########################################
###########################################
###########################################
###########################################
#          SERVER APPLICATION
###########################################
###########################################
###########################################
###########################################


# 0 = Rest
# 1 = Go
# 2 = Hold

state = "r"

actPosX = 1000
actPosY = 0
actPosZ = 0
actTempo = 2

desPosX = 1000
desPosY = 0
desPosZ = 0
desTempo = 2

ctrlTime1 = 0
ctrlPathIdx = 0
ctrlPathSize = 0

pathPlanned = []


def Go():
    global state
    #custom implement
    state = "g"
    pass

def moveMotors(positionXY,posZ):
    #move Dunker
    #DUNKER 1m = 869565
    moveDunker(int(869565*posZ))


    ik = kinematics.IK(positionXY, elbow=0)
    #print(x,y)
    print(ik)
    motor_S.goG(ik[0], v)
    motor_E.goG(ik[1]+ik[0], v)
    # dyn
    motor_W = -(ik[0] + ik[1])
    moveDyn(motor_W)

    #move Dynmixel
    #move RMD1
    #move RMD2
    print(positionXY,posZ)
    pass

def moveCtrl():
    global desPosX,desPosY,desPosZ,desTempo;
    global actPosX,actPosY,actPosZ,actTempo;
    global ctrlTime1,ctrlPathIdx,ctrlPathSize
    global pathPlanned
    global state
    #query current position
    if state == "g":
        #CALC PATH PLANNING
        #READ RMD position
        motor_S.Fn92()
        motor_E.Fn92()

        theta1 = motor_S.multiTurnG
        theta2 = motor_E.multiTurnG
        theta2 = theta2 - theta1
        print("Starting theta1 and theta2 values:")
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
        print("Starting x1 and y1 values:")
        print(x1)
        print(y1)

        #convert des pos to mm and int values
        x2 = int(desPosX*1000)
        y2 = int(desPosY*1000)
        print("Target position x2",desPosX,"y2",desPosY)

        #time is defined by steps of 100ms
        n = int(desTempo*10)
        pathPlanned = kinematics.path(x1,y1,x2,y2,steps=n)

        #qui funzione che genera il path X Y Z nel tempo
        ctrlPathSize = len(pathPlanned)
        #send command
        moveMotors(pathPlanned[0],desPosZ)
        ctrlPathIdx = 1
        #Update rate of 10Hz
        ctrlTime1 = time.time() + 0.1
        state = "G"
    elif state == "G":
        #enter every 100ms
        if (time.time() > ctrlTime1):
            ctrlTime1 = time.time() + 0.1
            moveMotors(pathPlanned[ctrlPathIdx],desPosZ)
            ctrlPathIdx += 1
        #if all path planning are complete, exit
        if (ctrlPathIdx >= ctrlPathSize):
            state = "H"


def decodeMessage(cmdMsg):
    global desPosX,desPosY,desPosZ,desTempo
    global state

    ret = "K"
    if (cmdMsg[0] == "Q"):
        #print("Query")
        pass
    #G:x,y,z,sec
     #x verso albero
     #y verso sinistra guardano la telecamera
     #z in su
    elif (cmdMsg[0] == "G"): #G:x:y:z:sec
        #split cmd into position and velocity
        # G:pos:vel
        # G:pos
        print("Go")
        values = cmdMsg.split(":")
        if len(values) == 5:
            desPosX = float(values[1])
            desPosY = float(values[2])
            desPosZ = float(values[3])
            desTempo = float(values[4])
        Go()
    else:
        print("Unknown")
        ret = "N"
    return ret

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global state
        data = self.request[0].strip()
        socket = self.request[1]
        for el in data:
            print(el)

        cmdMsg = data.decode("utf-8")
        ret = decodeMessage(cmdMsg)
        #print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        #old python
        #socket.sendto(ret + state + ":" + str(-position), self.client_address)
        socket.sendto(bytes(ret + state,"utf8"), self.client_address)


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8891

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        #print("Server started at {} port {}".format(HOST, PORT))
        while True:
            while 1:
                moveCtrl()
                time.sleep(0.01)


            # Close port
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()

        exit()
