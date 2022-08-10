import time
import motor.dynamixel as dyn

'''
Python script to calibrate all the Dynamixel motors.
(Wrist motor and two gripper motors)
'''

###################################  VARIABLES  ######################################
# set slow velocity
vel = 15
# set maxPWM to a low value, e.g. 50
PWM_max = 885
PWM_calibrate = 50
# go to 1000deg (rotate until you hit the calibration mechanical part)
# check present PWM:
#  -  if PWM > maxPWM --> stop and calibrate
# set maxPWM back to a high value
######################################################################################

def calibrate_grasp(motor1):
    '''
    Calibrate motor1 responsible for opening/closing the fingers.
    Fingers completely open means motor1 at 0 degrees
    '''
    # Set maxPWM to a low value for calibration
    motor1.setPWM(PWM_calibrate)
    # Open until we reach the mechanical limit
    motor_pwm = motor1.readPWM()
    while True:
        if motor_pwm < PWM_calibrate:
            motor_pwm = motor1.readPWM()
            time.sleep(0.5)
        motor1.moveDyn(-1000, vel) # (angle, velocity)
    #set pose

        
    pass


def calibrate_twist(motor2):
    '''
    Calibrate motor2 responsible for twisting the fingers.
    After calibration motor2 will be set at 0 degrees
    '''

    pass