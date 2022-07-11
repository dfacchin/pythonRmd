import numpy as np
import can
import time

import RMD
import kinematics
from trajectory_planner import Joint


# Specify the bus
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

# Variables
v = 400  # Motors velocity
a = 800  # Motors acceleration


# ---------- RMD motor with ID 1 (Elbow) ----------
motor_E = RMD.RMD(0x142, bus, ratio=13.5)  # Elbow
motor_E.Fn30()  # read PID
motor_E.Fn33()  # read acceleration
# Specify desired PID
motor_E.PidPosKp = 100
motor_E.PidPosKi = 0
motor_E.PidVelKp = 100
motor_E.PidVelKi = 5
motor_E.PidTrqKp = 100
motor_E.PidTrqKp = 5
motor_E.Fn31()  # write PID to Ram
# Specify desired acceleration
motor_E.acceleration = a
motor_E.Fn34()  # write acceleration to Ram


# ---------- RMD motor with ID 2 (Shoulder) ----------
motor_S = RMD.RMD(0x141, bus, ratio=13.5)  # Shoulder
motor_S.Fn30()  # read PID
motor_S.Fn33()  # read acceleration
# Specify desired PID
motor_S.PidPosKp = 100
motor_S.PidPosKi = 0
motor_S.PidVelKp = 100
motor_S.PidVelKi = 5
motor_S.PidTrqKp = 100
motor_S.PidTrqKp = 5
motor_S.Fn31()  # write PID to Ram
# Specify desired accelration
motor_S.acceleration = a
motor_S.Fn34()  # write acceleration to Ram


# Initial Conditions (i.c.):
pp = [[1000,0],[750,200],[300,350],[0,500],[300,350],[750,200],[1000,0]] # [mm] path points (x,y)
t = np.array([0, 1, 2, 3, 4, 5, 6]) # [s]
fn = 10 # [Hz]

# Define (pose,vel) for each path point
theta_S = [] # [deg]
theta_d_S = [0] # [deg/s]
theta_E = [] # [deg]
theta_d_E = [0] # [deg/s]
# Velocity in each segment
v_S = [] # [deg/s]
v_E = [] # [deg/s]

for coord in pp:
    x = float(coord[0])
    y = float(coord[1])
    target = np.array((x,y))
    theta = kinematics.IK(target, elbow=1)
    theta_S.append(theta[0])
    theta_E.append(theta[1])

shoulder = Joint(theta_S, theta_d_S, v_S, t, fn)
elbow = Joint(theta_E, theta_d_E, v_E, t, fn)

# Compute velocities
shoulder.velocity()
elbow.velocity()
shoulder.theta_d_pp()
elbow.theta_d_pp()

# Make sure to speciy the joint_name: shoulder and elbow
angle_S = shoulder.trajectory(joint_name="shoulder")
angle_E = elbow.trajectory(joint_name="elbow")
# Print "theta" and "theta_d" arrays
print(angle_S)
print(angle_E)


idx = 1

while idx < len(angle_S[0]):
    ik = [angle_S[0][idx],angle_E[0][idx]]
    idx += 1
    print("Pos:",ik)
    motor_S.goG(-ik[0], v) # - sign, since the motor is up-side-down
    motor_E.goG(ik[1]+ik[0], v) # sum of angles since we use belts
    time.sleep(1/fn)
   # input("Hit 'Enter' and go to the next point")
