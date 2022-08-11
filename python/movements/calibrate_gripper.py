import time
import motor.dynamixel as dyn

'''
Python script to calibrate all the Dynamixel motors.
(Wrist motor and two gripper motors)
'''

###################################  VARIABLES  ######################################
goal_pose = -2000 # large enough value to reach the mechanical limit
vel = 10 # set slow velocity
######################################################################################


def calibrate_grasp(motor1):
    '''
    Calibrate motor1 responsible for opening/closing the fingers.
    Fingers completely open means motor1 at 0 degrees
    '''
    # rotate untill reaching the mechanical limit
    motor1.moveDyn(goal_pose, vel)
    time.sleep(1) # wait to reach max pwm

    # read PWM
    current_pwm = abs(motor1.readPWM())
    print("current pwm: ", current_pwm)
    # set limit pwm
    limit_pwm = current_pwm + 8
    print("limit_pwm: ", limit_pwm)

    while True:
        # read current pose
        current_pose = motor1.getPose()
        print("current pose: ", current_pose)
        print("goal_pose: ", goal_pose)

        # read PWM
        current_pwm = abs(motor1.readPWM())
        print("current pwm: ", current_pwm)
        print("limit_pwm: ", limit_pwm)

        if current_pwm > limit_pwm:
            # stop moving
            current_pose = motor1.getPose()
            motor1.moveDyn(current_pose+2, 30)
            time.sleep(0.5)

            # set new home position
            current_pose = motor1.getPose()
            print("current pose: ", current_pose)
            home_offset = - int((4096/360) * current_pose) # + 2048 (to get 180 deg)
            print("home offset: ", home_offset)
            motor1.initDyn("cw", homing_offset=home_offset)
            
            # read pose
            current_home_pose = motor1.getPose()
            print("home pose: ", current_home_pose)

            break

        time.sleep(1)

    print("Calibration completed successfully!")


def calibrate_twist(motor2):
    '''
    Calibrate motor2 responsible for twisting the fingers.
    After calibration motor2 will be set at 0 degrees
    '''

    pass


'''
    # Set maxPWM to a low value for calibration
    motor1.setPWM(PWM_calibrate)

    # Open until we reach the mechanical limit
    motor1.moveDyn(goal_pose, vel) # (angle, velocity)

    while True:
        i = 0
        # While rotating, keep reading PWM every 0.5s
        motor_pwm = abs(motor1.readPWM())

        # If PWM > 50 then stop rotating and calibrate
        if motor_pwm > PWM_calibrate:
            # stop moving
            current_pose = motor1.getPose()
            motor1.moveDyn(current_pose+1, vel)
            # set current positon to 0 degrees
            home_offset = motor1.getPose()
            motor1.setHomePose(-home_offset)
            # Set maxPWM back to its highest value
            motor1.setPWM(PWM_max)
            i = 1

        time.sleep(0.5) # read PWM twice every second

        if i==1:
            break

    print("Calibration motor1 complete!")
'''