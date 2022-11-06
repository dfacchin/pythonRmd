import movements.move_gripper as gripper
import movements.calibrate_gripper as calibrate
import motor.dynamixel as dyn
import time
import numpy as np

_dynPort = dyn.DyanamixelPort()
# Set ID and port
dyn1 = dyn.DynamixelControl(1,_dynPort)
dyn2 = dyn.DynamixelControl(2,_dynPort)

dyn1.initDyn("cw", homing_offset=0, reset_homePose=True) # initialize motor1 and reset the homing offset
dyn2.initDyn("cw", homing_offset=0, reset_homePose=True) # initialize motor2 and reset the homing offset



a = calibrate.calibrate_twist(dyn2, dyn1)
#dyn1.moveDyn(90, 50)
time.sleep(1)
current_pose_2 = dyn2.getPose()
print("a) current pose dyn2: ", current_pose_2)
current_pose_1 = dyn1.getPose()
print("a) current pose dyn1: ", current_pose_1)

time.sleep(5)

b = calibrate.calibrate_grasp(dyn1)
#dyn1.moveDyn(90, 50)
time.sleep(1)
current_pose_1 = dyn1.getPose()
print("b) current pose dyn1: ", current_pose_1)
current_pose_2 = dyn2.getPose()
print("b) current pose dyn2: ", current_pose_2)