import movements.move_gripper as gripper
import motor.dynamixel as dyn

_dynPort = dyn.DyanamixelPort()
# Set ID and port
dyn1 = dyn.DynamixelControl(1,_dynPort)
dyn2 = dyn.DynamixelControl(2,_dynPort)

dyn1.initDyn("cw") # initialize motor1 and set direction
dyn2.initDyn("cw") # initialize motor2 and set direction

right = gripper.twist_right(dyn2,dyn1)
#open = gripper.open(dyn1)
#close = gripper.close(dyn1)