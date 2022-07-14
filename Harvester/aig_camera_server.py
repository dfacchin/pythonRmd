import aig_tcp_server
import pickle

def example_on_receive_callback(client, address, data):
    resp = {"response":"RgbDepth"}
    resp["Rgb"] = [0]*1024*1024*2
    resp["Depth"]= [0]*1024*1024*2
    data = pickle.dumps(resp)
    print(len(data))
    client.send(data)
    return

def example_on_connected_callback(client, address):
    return

def example_on_disconnected_callback(client, address):
    return

if __name__ == "__main__":
    
    print("Start server")
    for a in range(10):
        print(a)

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
    print("end")