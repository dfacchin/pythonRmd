
import Kinematics

# ---------- Commands ----------
# DK
theta1 = float(input("MT shulder [deg]: "))
theta2 = float(input("MT elbow [deg]: "))

coord = Kinematics.DK(theta1,theta2)

# IK
x = float(input("x-axis [mm]: ")) # x is along the straight arm
y = float(input("y-axis [mm]: ")) # y is perpendicular to the straight arm

angles = Kinematics.IK(x,y,elbow=1)

'''
Procedure:
-  Read current motor angles "multi-turn" (theta1_c, theta2_c) [deg]
-  Calculate DK theta1_c,theta2_c --> x,y
-  Set desired goal position (x_new,y_new)
-  Calculate IK x_new,y_new --> theta1,theta2
-  Use goG function to move the motors
-  Implement a straight and smooth trajectory


# Variables:
v = 20 # velocity
a = 20 # acceleration
t = 3 # time [sec]

theta1 = int(input("MT shulder [deg]: "))
theta2 = int(input("MT elbow [deg]: "))

motor_S.goG(theta1, v)
motor_E.goG(theta2, v)






theta1_c = motor_S.Fn92() # Read current multi-turn angle (shoulder)
theta2_c = motor_E.Fn92()	# Read current multi-turn angle (elbow)

coord = DK(theta1_c,theta2_c) # get current x,y coordinates 
print(coord)

x_new = int(input("Enter desired x-coordinate: "))
y_new = int(input("Enter desired y-coordinate: "))

angles = IK(x_new, y_new, elbow=0) # get new joint angles
print(angles)

# now that we obtained theta1 and theta2 from the IK
# we can move the motors:

angle_S = theta1
angle_E = theta2
motor_S.goG(angle_S,vel) # goG(Pos(degrees), velocity)
motor_E.goG((angle_E+angle_S),vel)
time.sleep(t)
'''

