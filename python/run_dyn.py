import movements.move_gripper as gripper
import motor.dynamixel as dyn
import time
import numpy as np

_dynPort = dyn.DyanamixelPort()
# Set ID and port
dyn1 = dyn.DynamixelControl(1,_dynPort)
dyn2 = dyn.DynamixelControl(2,_dynPort)

dyn1.initDyn("cw") # initialize motor1 and set direction
dyn2.initDyn("cw") # initialize motor2 and set direction

# Test homing:
dyn1.moveDyn(90, 30)
current_pose = dyn1.getPose()
home_offset = - int((4096/360) * current_pose)
print("home offset: ", home_offset)
dyn1.setHomePose(home_offset)
# read pose
current_home_pose = dyn1.getPose()
print("home pose: ", current_home_pose)



# vel = 10
# goal_pose = -2000

# dyn1.moveDyn(goal_pose, vel)
# time.sleep(1) # wait to reach max pwm 

# # read PWM
# current_pwm = abs(dyn1.readPWM())
# print("current pwm: ", current_pwm)
# # set limit pwm
# limit_pwm = current_pwm + 20
# print("limit_pwm: ", limit_pwm)

# while True:
#     # read current pose
#     current_pose = dyn1.getPose()
#     print("current pose: ", current_pose)
#     print("goal_pose: ", goal_pose)

#     # read PWM
#     current_pwm = abs(dyn1.readPWM())
#     print("current pwm: ", current_pwm)
#     print("limit_pwm: ", limit_pwm)

#     if current_pwm > limit_pwm:
#         # stop moving
#         current_pose = dyn1.getPose()
#         dyn1.moveDyn(current_pose+2, 30)

#         # set new home position
#         current_pose = dyn1.getPose()
#         if np.sign(dyn1.getPose()) == 1: # positive value
#             home_offset = - int((4096/360) * current_pose)
#             print("home offset: ", home_offset)
#             dyn1.setHomePose(home_offset)
#         elif np.sign(dyn1.getPose()) == -1: # negetive value
#             home_offset = int((4096/360) * current_pose)
#             print("home offset: ", home_offset)
#             dyn1.setHomePose(home_offset)        

#         # read pose
#         current_home_pose = dyn1.getPose()
#         print("home pose: ", current_home_pose)

#         break

#     time.sleep(1)
# print("Finish!")



'''
vel = 10
goal_pose = 5000

dyn1.moveDyn(goal_pose, vel)

while True:

    # read PWM
    print("current pwm: ", abs(dyn1.readPWM()))
    time.sleep(1)

    # read current pose
    current_pose = dyn1.getPose()

    print("current pose: ", current_pose)
    print("goal_pose: ", goal_pose)

    if (goal_pose-1) <= current_pose <= (goal_pose+1):
        break
print("Finish!")
'''