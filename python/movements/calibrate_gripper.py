import time
import motor.dynamixel as dyn

'''
Python script to calibrate all the Dynamixel motors.
(Wrist motor and two gripper motors)
'''

###################################  VARIABLES  ######################################
gear_ratio = 2
pwm_overshoot = 8
goal_pose_2 = 3000 # large enough value to reach the mechanical limit
vel_2 = 10 # set slow velocity
goal_pose_1 = 3000 # large enough value to reach the mechanical limit
vel_1 = vel_2 / gear_ratio
######################################################################################


def calibrate_grasp(motor1):
    '''
    Calibrate motor1 responsible for opening/closing the fingers.
    Fingers completely closed means motor1 at 0 degrees
    '''
    # rotate until reaching the mechanical limit
    motor1.moveDyn(goal_pose_1, vel_2)
    time.sleep(1) # wait to reach max pwm

    # read PWM
    current_pwm = abs(motor1.readPWM())
    print("current pwm: ", current_pwm)
    # set limit pwm
    limit_pwm = current_pwm + pwm_overshoot
    print("limit_pwm: ", limit_pwm)

    while True:
        # read current pose
        current_pose = motor1.getPose()
        print("current pose: ", current_pose)
        print("goal_pose: ", goal_pose_1)

        # read PWM
        current_pwm = abs(motor1.readPWM())
        print("current pwm: ", current_pwm)
        print("limit_pwm: ", limit_pwm)

        if current_pwm > limit_pwm:
            # stop moving
            current_pose = motor1.getPose()
            motor1.moveDyn(current_pose-2, 30)
            time.sleep(2)

            # set new home position
            current_pose = motor1.getPose()
            print("current pose: ", current_pose)
            home_offset = - int((4096/360) * current_pose) # + 2048 (to get 180 deg)
            print("home offset: ", home_offset)
            motor1.initDyn("cw", homing_offset=home_offset, reset_homePose=True)

            # read pose
            current_home_pose = motor1.getPose()
            print("home pose: ", current_home_pose)

            break

        #time.sleep(0.5)

    print("Calibration (Grasp) completed successfully!")


def calibrate_twist(motor2, motor1):
    '''
    Calibrate motor2 responsible for twisting the fingers.
    After calibration motor2 will be set at 0 degrees
    '''
    print("current pose dyn2: ", motor2.getPose())

    # rotate until reaching the mechanical limit
    motor2.moveDyn(goal_pose_2, vel_2)
    motor1.moveDyn(-goal_pose_2, vel_1)
    time.sleep(1) # wait to reach max pwm

    # read PWM
    current_pwm = abs(motor2.readPWM())
    print("current pwm dyn2: ", current_pwm)
    # set limit pwm
    limit_pwm = current_pwm + pwm_overshoot
    print("limit_pwm: ", limit_pwm)

    while True:
        # read current pose
        current_pose = motor2.getPose()
        print("current pose dyn2: ", current_pose)
        print("goal_pose dyn2: ", goal_pose_2)

        # read PWM
        current_pwm = abs(motor2.readPWM())
        print("current pwm dyn2: ", current_pwm)
        print("limit_pwm: ", limit_pwm)

        if current_pwm > limit_pwm:
            # stop moving
            current_pose_2 = motor2.getPose()
            current_pose_1 = motor1.getPose()
            motor2.moveDyn(current_pose_2-2, 30)
            motor1.moveDyn(current_pose_1+2, 30)
            time.sleep(2)

            # set new home position
            current_pose_2 = motor2.getPose()
            print("current pose: ", current_pose_2)
            home_offset = - int((4096/360) * current_pose_2) # + 2048 (to get 180 deg)
            print("home offset: ", home_offset)
            motor2.initDyn("cw", homing_offset=home_offset, reset_homePose=True)

            # read pose
            current_home_pose = motor2.getPose()
            print("home pose dyn2: ", current_home_pose)

            break

        #time.sleep(0.5)

    print("Calibration (Twist) completed successfully!")