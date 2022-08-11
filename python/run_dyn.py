import movements.move_gripper as gripper
import movements.calibrate_gripper as calibrate
import motor.dynamixel as dyn
import time
import numpy as np

_dynPort = dyn.DyanamixelPort()
# Set ID and port
dyn1 = dyn.DynamixelControl(1,_dynPort)
dyn2 = dyn.DynamixelControl(2,_dynPort)

dyn1.initDyn("cw") # initialize motor1 and set direction
dyn2.initDyn("cw") # initialize motor2 and set direction


# a = calibrate.calibrate_grasp(dyn1)
# dyn1.moveDyn(90, 50)
# time.sleep(2)
# current_pose = dyn1.getPose()
# print("current pose: ", current_pose)

b = calibrate.calibrate_twist(dyn2, dyn1)
#dyn1.moveDyn(90, 50)
time.sleep(2)
current_pose_2 = dyn2.getPose()
print("current pose dyn2: ", current_pose_2)
current_pose_1 = dyn1.getPose()
print("current pose dyn1: ", current_pose_1)
