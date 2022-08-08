import dynamixel as dyn

'''
This script is used to make the gripper move
- motor1 = responsible for the finger open/close movement 
- motor2 = responsible for the finger twist movement
'''

def open(motor1):
    '''
    Method used to open the gripper fingers,
    in order to release the apple.
    '''
    motor1.moveDyn(0, 30) # (angle [deg], velocity [rev/min])


def close(motor1):
    '''
    Method used to close the gripper fingers,
    in order to grasp the apple.
    '''
    motor1.moveDyn(0, 30) # (angle [deg], velocity [rev/min])


def twist_right(motor2, motor1):
    '''
    Method used to make the gripper fingers twist,
    in order to cut the stalk.
    '''
    # execute the twist
    motor2.moveDyn(340, 30) # (angle [deg], velocity [rev/min])
    # compensate the twist-rotation to avoid opening/closing fingers 
    motor1.moveDyn(90, 50) # (angle [deg], velocity [rev/min])

def twist_left(motor2, motor1):
    '''
    Method used to make the gripper fingers twist,
    in order to go back to their starting pose.
    '''
    # execute the twist
    motor2.moveDyn(90, -30) # (angle [deg], velocity [rev/min])
    # compensate the twist-rotation to avoid opening/closing fingers 
    motor1.moveDyn(0, 30) # (angle [deg], velocity [rev/min])