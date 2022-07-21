import RMD
import can
import time

# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

#RMD motor with ID 1
motor1 = RMD.RMD(0x142,bus,ratio = 9)
motor1.acceleration = 10000000
motor1.Fn34()
motor1.Fn90()
motor1.Fn90()
motor1.Fn92()
motor1.Fn94()
motor1.Fn30()
motor1.Fn33()
motor1.print()
motor1.info()


pos = 0
direction = 1
while True:
    #motor1.go(180*900,6000)
    motor1.goG(pos,6000)
    pos += direction
    if pos == 180:
        direction = -1
    elif pos == -180:
        direction = 1
    print(pos)
    time.sleep(0.01)
    
    
    


    

