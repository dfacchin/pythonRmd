import RMD
import can
import time
# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

#RMD motor with ID 1
motor1 = RMD.RMD(0x142,bus,ratio = 9)

motor1.info()

motor1.Fn30()
motor1.Fn33()
motor1.info()
motor1.PidPosKp  = 30
motor1.PidPosKi  = 0
motor1.PidVelKp  = 30
motor1.PidVelKi  = 5
motor1.PidTrqKp  = 30
motor1.PidTrqKp  = 5
motor1.Fn31()
motor1.acceleration = 3000
motor1.Fn34()
motor1.Fn30()
motor1.Fn33()
motor1.info()

motor2 = RMD.RMD(0x141,bus,ratio = 9)

motor2.info()

motor2.Fn30()
motor2.Fn33()
motor2.info()

motor2.PidPosKp  = 30
motor2.PidPosKi  = 0
motor2.PidVelKp  = 30
motor2.PidVelKi  = 5
motor2.PidTrqKp  = 30
motor2.PidTrqKp  = 5
motor2.Fn31()
motor2.acceleration = 2000
motor2.Fn34()
motor2.Fn30()
motor2.Fn33()
motor2.info()

while True:
	
	motor2.goG(0,200)
	motor1.goG(100,4000)
	time.sleep(2)
	motor2.goG(0,200)
	motor1.goG(-100,4000)
	time.sleep(2)

