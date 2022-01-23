"""
First Test Python Command for RMD X Motor
Implementation based on DOC can bus protocol 1.6

Command line for can interface
sudo ip link set can0 type can bitrate 1000000
sudo ip link set up can0

Example
- this will show all RAW data on the CAN BUS
candumb can0 

- this will query the motor number 1
cansend can0 141#3000000000000000

-request made by the command on the candumb
  can0  141   [8]  30 00 00 00 00 00 00 00
-response on the candumb
  can0  141   [8]  30 00 1E 00 1E 05 1E 05

"""

#Python library to be intalled with ù
#requires python 3.9 >
#pip install python-can
import can


# Using specific buses works similar:
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)

#RMD motor with ID 1
CanId = 0x141
#Simple request
sendData = [0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

#prepare the message
msg = can.Message(arbitration_id=CanId,
                  data=sendData,
                  is_extended_id=False)

#try to send the message on the bus
try:
    bus.send(msg)
    print("Message sent on {}".format(bus.channel_info))
except can.CanError:
    print("Message NOT sent")
    
 #read the response, no timeout on this action without arguments in the recv function
msg = bus.recv()
#print it
print(msg)

