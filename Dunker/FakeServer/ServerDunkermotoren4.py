import socketserver as SocketServer
import threading
import os
import struct
import time                      # to import module time


# 0 = Rest
# 1 = Go
# 2 = Hold

state = "r"
position = 0
velocity = 0
desiredPosition = 0
desiredTime = 0
defaultVelocity = 20
stepX = 0
moving = 0


def Go(pos,vel):
    global state
    #custom implement
    state = "g"
    pass

def Hold():
    global state
    #custom implement
    #keep actual position with "force"
    state = "h"
    pass

def Rest():
    global state
    #custom implement
    #let the motor be move by hand

    state = "r"
    pass

def Calibrate(value):
    global state
    #custom implement
    #clear encoder value and go back to rest position
    state = "c"
    pass

def moveCtrl():
    global state
    global desiredPosition
    global position
    global velocity
    global moving
    global stepX
    #query current position
    if state == "g":
        #cmd motor to go
        # run to position
        # Write goal position
        time.sleep(0.1)
        stepX = int((desiredPosition - position) / 1000)
        print(stepX)
        state = "G"
    elif state == "G":
        #wait until postion is reached then go to hold

        #if position is < 2deg from des position
        #and if velocity is near 0 target reached

        position += stepX
        print(position)
        if abs(desiredPosition-position)<2000:
            Hold()
    elif state == "c":
        #cmd motor to calibrate
        position = 0
        Rest()
    elif state == "r":
        #dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, 0)
        state = "R"
    elif state == "h":
        #dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, 1)
        state = "H"
    pass




def decodeMessage(cmdMsg):
    global desiredPosition
    global desiredTime
    global defaultVelocity
    global state

    ret = "K"
    if (cmdMsg[0] == "Q"):
        #print("Query")
        pass
    elif (cmdMsg[0] == "R"):
        if (state == "H"):
            print("Rest")
            #cmd motor to rest
            Rest()
            print(state, desiredPosition, desiredTime)
        else:
            ret = "N"
    elif (cmdMsg[0] == "G"): #G:pos:vel
        #split cmd into position and velocity
        # G:pos:vel
        # G:pos
        if (state == "H") or (state == "R") or (state == "G"):
            print("Go")
            values = cmdMsg.split(":")
            if len(values) == 2:
                desiredPosition = -int(values[1])
                desiredTime = defaultVelocity
            if len(values) == 3:
                desiredPosition = -int(values[1])
                desiredTime = int(values[2])
            Go(desiredPosition, desiredTime)
            print(state, desiredPosition, desiredTime)
        else:
            ret = "N"
    elif (cmdMsg[0] == "H"):
        if (state == "R"):
            Hold()
            print(state, desiredPosition, desiredTime)
            print("Hold")
        else:
            ret = "N"
    elif (cmdMsg[0] == "C"):
        if (state == "R"):
            values = cmdMsg.split(":")
            if len(values) == 2:
                Calibrate(int(values[1]))
            else:
                Calibrate(0)
            print("Calibrate")
        else:
            ret = "N"
    else:
        print("Unknown")
        ret = "N"
    return ret

def refreshMotor():
    global position, velocity, moving,state
    # Update position
    #dataIn, dxl_comm_result, dxl_error = packetHandler.readTxRx(portHandler, DXL_ID,122,14)

    velocity = 0
    moving = 0

    #print(position, velocity,state,moving)
    # print("[ID:%03d] PresPos:%03d" % (DXL_ID, dxl_present_position))


class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global desiredPosition
        global position
        global state
        data = self.request[0].strip()
        socket = self.request[1]
        for el in data:
            print(el)

        cmdMsg = data.decode("utf-8")
        ret = decodeMessage(cmdMsg)
        #print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        #old python
        #socket.sendto(ret + state + ":" + str(-position), self.client_address)
        socket.sendto(bytes(ret + state + ":" + str(position),"utf8"), self.client_address)


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8891

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        #print("Server started at {} port {}".format(HOST, PORT))
        while True:
            while 1:
                refreshMotor()
                moveCtrl()
                time.sleep(0.01)


            # Close port
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()

        exit()
