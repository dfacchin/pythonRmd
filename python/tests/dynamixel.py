'''
This python class is used to initialize and control the Dynamixel motors.
Python sample code to control the Dynamixel motors:
https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/sample_code/python_read_write_protocol_2_0/#python-protocol-20
Dynamixel control table:
https://emanual.robotis.com/docs/en/dxl/x/xc430-w240/
'''

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

from dynamixel_sdk import *


class DynamixelControl:

    # Definition of class varialbles (same values for each motor)
    # Dynamixel model definition
    MY_DXL = 'X_SERIES'         # X430
    BAUDRATE                    = 57600
    PROTOCOL_VERSION            = 2.0
    DEVICENAME                  = '/dev/ttyUSB0'
    TORQUE_ENABLE               = 1 # Value for enabling the torque
    # Addresses
    ADDR_TORQUE_ENABLE          = 64
    ADDR_GOAL_POSITION          = 116
    ADDR_VELOCITY               = 112
    # Initialize PortHandler instance
    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)


    # Init method used to set the motor ID
    def __init__(self, DXL_ID):
        self.DXL_ID = DXL_ID


    # Method for initializing the motor
    def initDyn(self):
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

        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_TORQUE_ENABLE, self.TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel has been successfully connected")


    def moveDyn(self, angle, velocity):
        #global packetHandler,portHandler,DXL_ID,ADDR_TORQUE_ENABLE,TORQUE_ENABLE
        
        # Change velocity (velocity is in rev/min)
        if 0 < velocity <= 70:
            velReq = int(velocity / 0.229)
        else:
            print("Wrong dynamixel velocity! Choose a value between 0 and 70 [rev/min]")
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_VELOCITY, velReq)
        
        # Change position (angle is in degrees)
        posReq = int((angle *4096) / 360) # 4096 = 360 DEGREES
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_GOAL_POSITION, posReq)


dyna1 = DynamixelControl(1)
dyna1.initDyn()
dyna1.moveDyn(90, 10) # (angle [deg], velocity [rev/min])
