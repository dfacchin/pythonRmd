'''
This script stores all the functions to make the gripper move
- motor1 = responsible for the finger open/close movement 
- motor2 = responsible for the finger twist movement
'''

###################################  VARIABLES  ######################################
gear_ratio = 2
twist = 200 # [deg]

# Velocities [rev/min]
vel_max = 15 #70
vel_2 = 15
vel_1 = vel_2 / gear_ratio

# Positions Open/Close [deg]
open_pose = -200 # -230
close_pose = -5 # 5deg of tolerance to avoid collision
######################################################################################


def open(motor1):
    '''
    Method used to open the gripper fingers,
    in order to release the apple.
    '''
    motor1.moveDyn(open_pose, vel_max) # (angle, velocity)


def close(motor1):
    '''
    Method used to close the gripper fingers,
    in order to grasp the apple.
    '''
    motor1.moveDyn(close_pose, vel_max) # (angle, velocity)


def twist_right(motor2, motor1):
    '''
    Method used to make the gripper fingers twist,
    in order to cut the stalk.
    '''
    # execute the twist
    motor2.moveDyn(motor2.getPose() - (twist*gear_ratio), vel_2) # (angle, velocity)
    # compensate the twist-rotation to avoid opening/closing fingers 
    motor1.moveDyn(motor1.getPose() + twist, vel_1) # (angle, velocity)


def twist_left(motor2, motor1):
    '''
    Method used to make the gripper fingers twist,
    in order to go back to their starting pose.
    '''
    # execute the twist
    motor2.moveDyn(motor2.getPose() + (twist*gear_ratio), vel_2) # (angle, velocity)
    # compensate the twist-rotation to avoid opening/closing fingers 
    motor1.moveDyn(motor1.getPose() - twist, vel_1) # (angle, velocity)
