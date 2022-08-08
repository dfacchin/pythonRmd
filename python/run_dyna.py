import dynamixel as dyn
import time
import movements.move_gripper as gripper

# Initialize the (gripper) dynamixel motors
dyna1 = dyn.DynamixelControl(1) # ID=1
dyna2 = dyn.DynamixelControl(2) # ID=2
dyna1.initDyn()
dyna2.initDyn()

gripper.twist_right(dyna2, dyna1)
time.sleep(3)
gripper.twist_left(dyna2, dyna1)



'''
dyna1.moveDyn(0, 50) # (angle [deg], velocity [rev/min])
dyna2.moveDyn(90, 50) # (angle [deg], velocity [rev/min])
time.sleep(3)
dyna1.moveDyn(90, 50) # (angle [deg], velocity [rev/min])
dyna2.moveDyn(0, 50) # (angle [deg], velocity [rev/min])
'''