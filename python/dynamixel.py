#
# Python sample code to control the Dynamixel motors:
# https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/sample_code/python_read_write_protocol_2_0/#python-protocol-20
#
# Dynamixel control table:
# https://emanual.robotis.com/docs/en/dxl/x/xc430-w240/
#
##################################################

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
    '''
    This python class is used to initialize and control the Dynamixel motors.
    '''

    # Dynamixel info/model definition (same values for each motor)
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


    def __init__(self, DXL_ID):
        '''
        Init method used to set the motor ID
        '''
        self.DXL_ID = DXL_ID


    def initDyn(self):
        '''
        Method for initializing/connect the motor
        '''
        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_TORQUE_ENABLE, self.TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel has been successfully connected")


    def moveDyn(self, angle, velocity):
        '''
        Method to send desired position and velocity to the motor
        '''

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
dyna2 = DynamixelControl(2)

dyna1.initDyn()
dyna1.moveDyn(90, 50) # (angle [deg], velocity [rev/min])

dyna2.initDyn()
dyna2.moveDyn(0, 50) # (angle [deg], velocity [rev/min])
