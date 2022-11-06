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

t = 7

open = gripper.open(dyn1)
time.sleep(t)
close = gripper.close(dyn1)
time.sleep(t)
right = gripper.twist_right(dyn2, dyn1)
time.sleep(t)
left = gripper.twist_left(dyn2, dyn1)
time.sleep(t)
open = gripper.open(dyn1)
time.sleep(t)

current_pose_1 = dyn1.getPose()
print("c) current pose dyn1: ", current_pose_1)
current_pose_2 = dyn2.getPose()
print("c) current pose dyn2: ", current_pose_2)
