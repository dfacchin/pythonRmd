import motor.RMD as RMD
import can

# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

#RMD motor with ID 1
motor1 = RMD.RMD(0x142,bus,ratio = 9)

"""
test = False
for a in range(100):
  motor1.Fn90()
  motor1.Fn92()
  motor1.Fn94()
  motor1.print()
  if test:
    test = False
    motor1.Fn80()
    motor1.Fn81()
  #time.sleep(0.2)

motor1.print()
motor1.info()
motor1.Fn90()
motor1.Fn90()
motor1.Fn92()
motor1.Fn94()
motor1.Fn30()
motor1.Fn33()
motor1.print()
motor1.info()
motor1.acceleration = 3000
motor1.Fn34()
motor1.acceleration = 0
motor1.print()
motor1.info()
"""
motor1.acceleration = 200
motor1.Fn34()
motor1.Fn90()
motor1.Fn90()
motor1.Fn92()
motor1.Fn94()
motor1.Fn30()
motor1.Fn33()
motor1.print()
motor1.info()

motor1.go(180*900,6000)
#motor1.go(0*900,6000)
