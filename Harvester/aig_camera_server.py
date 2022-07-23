# Camera Server
# Open TCP socket on IP 20000
# Allows 5 Max connections
# Real sense starts with 
# RGB 1920*1080
# Depth 1280*720 -> aligned to RGB it can be a 1920*1080 picture

# When a request is made it's a serialized dictionart request
# command: RgbAndAlignDepth
# mode: real/demo (demo has fake numpy array of the size of the RGB and Depth to test bandwidth not detection)
# debug: 0-9 debug levels, 0 is none
# we take a "picture" and responde with it 
# receiving thread should allocate enough "incoming" packet size to get the images

import aig_tcp_server
import pickle
import numpy

serverPort = 20000

ImageWidth = 1920
ImageHeight = 500

def example_on_receive_callback(client, address, data):    

    #Get the request and unpack it
    datain = pickle.loads(data)

    if datain["command"] == "RgbAndAlignDepth":
        if datain["mode"] == "real":
            if datain.get("debug",0):
                print("Real mode not yet implemented, Switch to Demo")
            datain["mode"] == "demo" 

        if datain["mode"] == "demo":
            response = {"response":"RgbAndAlignDepthOK"}
            response["rgb"] = numpy.array([[[0.0]*ImageWidth]*ImageHeight])
            response["depth"] = numpy.array([[[0.1]*ImageWidth]*ImageHeight])
            response["width"] = ImageWidth
            response["height"] = ImageHeight
            data = pickle.dumps(response)
            client.send(data)
    return

def example_on_connected_callback(client, address):
    return

def example_on_disconnected_callback(client, address):
    return

if __name__ == "__main__":

    #Start Realsense Camera
    
    print("Start server")

    aig_tcp_server.TCPThreadedServer(
        '127.0.0.1',
        serverPort,
        timeout=86400,
        decode_json=True,
        #on_connected_callback=example_on_connected_callback,
        on_receive_callback=example_on_receive_callback,
        #on_disconnected_callback=example_on_disconnected_callback,
        debug=True,
        debug_data=True
    ).start()    

