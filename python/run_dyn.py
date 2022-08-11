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

# # Test homing:
# dyn1.moveDyn(-50, 60)
# time.sleep(7)

# current_pose = dyn1.getPose()
# print("current pose: ", current_pose)
# home_offset = - int((4096/360) * current_pose) # + 2048 (to get 180 deg)
# print("home offset: ", home_offset)
# dyn1.initDyn("cw", homing_offset=home_offset) # initialize motor1 and set direction
# # dyn1.setHomePose(home_offset)
# # read pose
# current_home_pose = dyn1.getPose()
# print("home pose: ", current_home_pose)

a = calibrate.calibrate_grasp(dyn1)

'''
###########################################################
vel = 10
goal_pose = 2000

dyn1.moveDyn(goal_pose, vel)
time.sleep(1) # wait to reach max pwm

# read PWM
current_pwm = abs(dyn1.readPWM())
print("current pwm: ", current_pwm)
# set limit pwm
limit_pwm = current_pwm + 12
print("limit_pwm: ", limit_pwm)

while True:
    # read current pose
    current_pose = dyn1.getPose()
    print("current pose: ", current_pose)
    print("goal_pose: ", goal_pose)

    # read PWM
    current_pwm = abs(dyn1.readPWM())
    print("current pwm: ", current_pwm)
    print("limit_pwm: ", limit_pwm)

    if current_pwm > limit_pwm:
        # stop moving
        current_pose = dyn1.getPose()
        dyn1.moveDyn(current_pose+2, 30)
        time.sleep(0.5)

        # set new home position
        current_pose = dyn1.getPose()
        print("current pose: ", current_pose)
        home_offset = - int((4096/360) * current_pose) # + 2048 (to get 180 deg)
        print("home offset: ", home_offset)
        dyn1.initDyn("cw", homing_offset=home_offset) # initialize motor1 and set direction
        # read pose
        current_home_pose = dyn1.getPose()
        print("home pose: ", current_home_pose)

        break

    time.sleep(1)

print("Calibration completed successfully!")
########################################################
'''