#
# Python sample code to control the Dynamixel motors:
# https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/sample_code/python_read_write_protocol_2_0/#python-protocol-20
#
# Dynamixel control table:
# https://emanual.robotis.com/docs/en/dxl/x/xc430-w240/
#
##################################################

import os
import struct

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

from dynamixel_sdk import *

class DyanamixelPort:
    '''
    Set Usb-port and Baudrate
    '''
    MY_DXL = 'X_SERIES'         # X430
    BAUDRATE                    = 57600
    PROTOCOL_VERSION            = 2.0
    DEVICENAME                  = '/dev/ttyUSB0'

    def __init__(self):
        # Initialize PortHandler instance
        self.portHandler = PortHandler(self.DEVICENAME)
        self.packetHandler = PacketHandler(self.PROTOCOL_VERSION)
        # Open port
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            quit()
            # Set port baudrate
        if self.portHandler.setBaudRate(self.BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()


class DynamixelControl:
    '''
    This python class is used to initialize and control the Dynamixel motors.
    '''

    TORQUE_ENABLE               = 1 # Value for enabling the torque
    # Addresses
    ADDR_TORQUE_ENABLE          = 64 # used to enabel torque
    ADDR_GOAL_POSITION          = 116 # used to set position
    ADDR_VELOCITY               = 112 # used to set velocity
    ADDR_DRIVE_MODE             = 10 # used to chande direction of rotation
    ADDR_OPERATING_MODE         = 11 # used to set multi or single turn
    ADDR_PRESENT_POSITION       = 132 # used to get current position


    def __init__(self, DXL_ID, dyanamixelPort):
        '''
        Init method used to set the motor ID and port
        '''
        self.DXL_ID = DXL_ID
        self.dyanamixelPort = dyanamixelPort


    def initDyn(self, direction):
        '''
        Method for initializing/connect the motor
        '''
        # Disable torque before applying changes
        dxl_comm_result, dxl_error = self.dyanamixelPort.packetHandler.write1ByteTxRx(self.dyanamixelPort.portHandler, self.DXL_ID, self.ADDR_TORQUE_ENABLE, 0)

        # Set direction of rotation
        if direction == "ccw": # ccw = counter-clockwise
            setBit = 1
        else:
            setBit = 0
        dxl_comm_result, dxl_error = self.dyanamixelPort.packetHandler.write1ByteTxRx(self.dyanamixelPort.portHandler, self.DXL_ID, self.ADDR_DRIVE_MODE, setBit)

        # Set operation mode to multi turn
        dxl_comm_result, dxl_error = self.dyanamixelPort.packetHandler.write1ByteTxRx(self.dyanamixelPort.portHandler, self.DXL_ID, self.ADDR_OPERATING_MODE, 4)

        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = self.dyanamixelPort.packetHandler.write1ByteTxRx(self.dyanamixelPort.portHandler, self.DXL_ID, self.ADDR_TORQUE_ENABLE, self.TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
           print("%s" % self.dyanamixelPort.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
           print("%s" % self.dyanamixelPort.getRxPacketError(dxl_error))
        else:
           print("Dynamixel has been successfully connected")


    def moveDyn(self, angle, velocity):
        '''
        Method to send desired position and velocity to the motor
        '''

        # Change velocity (velocity is in rev/min) - Max vel of X430-240: 70 rev/min
        velReq = int(velocity / 0.229)
        dxl_comm_result, dxl_error = self.dyanamixelPort.packetHandler.write4ByteTxRx(self.dyanamixelPort.portHandler, self.DXL_ID, self.ADDR_VELOCITY, velReq)
        
        # Change position (angle is in degrees)
        posReq = int((angle *4096) / 360) # 4096 = 360 DEGREES
        dxl_comm_result, dxl_error = self.dyanamixelPort.packetHandler.write4ByteTxRx(self.dyanamixelPort.portHandler, self.DXL_ID, self.ADDR_GOAL_POSITION, posReq)


    def getPose(self):
        '''
        Method to read the present position
        '''
        dxl_present_position = self.dyanamixelPort.packetHandler.read4ByteTxRx(self.dyanamixelPort.portHandler, self.DXL_ID, self.ADDR_PRESENT_POSITION)
        #print(dxl_present_position[0],hex(dxl_present_position[0]))
        valByte = struct.pack("I",dxl_present_position[0])
        valRet = struct.unpack("i",valByte)
        current_pose = (360.0/4096.0)*valRet[0]
        return current_pose
