import movements.move_gripper as gripper
import motor.dynamixel as dyn
import time

_dynPort = dyn.DyanamixelPort()
# Set ID and port
dyn1 = dyn.DynamixelControl(1,_dynPort)
dyn2 = dyn.DynamixelControl(2,_dynPort)

dyn1.initDyn("cw") # initialize motor1 and set direction
dyn2.initDyn("cw") # initialize motor2 and set direction


vel = 10
goal_pose = -500

# set low PWM
#dyn1.setPWM(100)

dyn1.moveDyn(goal_pose, vel)
time.sleep(1) # wait to reach max pwm 

# read PWM
current_pwm = abs(dyn1.readPWM())
print("current pwm: ", current_pwm)
# set limit pwm
limit_pwm = current_pwm + 20
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
        break

    time.sleep(1)
print("Finish!")



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



# Home
# dyn1.moveDyn(-90,40)
# dyn2.moveDyn(-90,40)
# time.sleep(5)
# print("Pose home dyn2; ", dyn2.getPose())
# print("Pose home dyn1; ", dyn1.getPose())

# right = gripper.twist_right(dyn2,dyn1)
# time.sleep(7)
# print("Pose cut dyn2; ", dyn2.getPose())
# print("Pose cut dyn1; ", dyn1.getPose())

# left = gripper.twist_left(dyn2,dyn1)
# time.sleep(7)
# print("Pose home dyn2; ", dyn2.getPose())
# print("Pose home dyn1; ", dyn1.getPose())

# right = gripper.twist_right(dyn2,dyn1)
# time.sleep(7)
# print("Pose cut dyn2; ", dyn2.getPose())
# print("Pose cut dyn1; ", dyn1.getPose())

# left = gripper.twist_left(dyn2,dyn1)
# time.sleep(7)
# print("Pose home dyn2; ", dyn2.getPose())
# print("Pose home dyn1; ", dyn1.getPose())
