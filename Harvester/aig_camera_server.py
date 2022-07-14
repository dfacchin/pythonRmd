import aig_tcp_server
import pickle

name = "lele"

def example_on_receive_callback(client, address, data):    
    global name

    #Get realsense camera frame
    #Align camera frame
    #deep copy frames

    resp = {"response":"RgbDepth"}
    resp["name"] = name
    resp["Rgb"] = "RGB DATA"
    resp["Depth"] = 1280
    resp["Height"] = 1024

    data = pickle.dumps(resp)
    print(len(data))
    client.send(data)
    return

def example_on_connected_callback(client, address):
    return

def example_on_disconnected_callback(client, address):
    return

if __name__ == "__main__":

    #Start Realsense Camera
    
    print("Start server")
    for a in range(10):
        print(a)

    name = name +" 2"
    aig_tcp_server.TCPThreadedServer(
        '127.0.0.1',
        8009,
        timeout=86400,
        decode_json=True,
        #on_connected_callback=example_on_connected_callback,
        on_receive_callback=example_on_receive_callback,
        #on_disconnected_callback=example_on_disconnected_callback,
        debug=True,
        debug_data=True
    ).start()    
    name = name +" 3"
    print("end")

