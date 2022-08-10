import movements.move_gripper as gripper
import motor.dynamixel as dyn
import time

_dynPort = dyn.DyanamixelPort()
# Set ID and port
dyn1 = dyn.DynamixelControl(1,_dynPort)
dyn2 = dyn.DynamixelControl(2,_dynPort)

dyn1.initDyn("cw") # initialize motor1 and set direction
dyn2.initDyn("cw") # initialize motor2 and set direction



# Home
dyn1.moveDyn(90,40)
dyn2.moveDyn(-90,40)
time.sleep(5)
print("Pose home dyn2; ", dyn2.getPose())
print("Pose home dyn1; ", dyn1.getPose())

right = gripper.twist_right(dyn2,dyn1)
time.sleep(7)
print("Pose cut dyn2; ", dyn2.getPose())
print("Pose cut dyn1; ", dyn1.getPose())

left = gripper.twist_left(dyn2,dyn1)
time.sleep(7)
print("Pose home dyn2; ", dyn2.getPose())
print("Pose home dyn1; ", dyn1.getPose())

right = gripper.twist_right(dyn2,dyn1)
time.sleep(7)
print("Pose cut dyn2; ", dyn2.getPose())
print("Pose cut dyn1; ", dyn1.getPose())

left = gripper.twist_left(dyn2,dyn1)
time.sleep(7)
print("Pose home dyn2; ", dyn2.getPose())
print("Pose home dyn1; ", dyn1.getPose())
