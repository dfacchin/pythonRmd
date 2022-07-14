#Socket code from https://github.com/matthewwachter/py-tcp-threaded-server

from datetime import datetime
from json import loads, dumps
import socket
from threading import Thread

class TCPThreadedServer(Thread):
    def __init__(
            self,
            host,
            port,
            timeout=60,
            decode_json=True,
            on_connected_callback=None,
            on_receive_callback=None,
            on_disconnected_callback=None,
            debug=False,
            debug_data=False
            ):

        self.host = host
        self.port = port
        self.timeout = timeout
        self.decode_json = decode_json
        self.on_connected_callback = on_connected_callback
        self.on_receive_callback = on_receive_callback
        self.on_disconnected_callback = on_disconnected_callback
        self.debug = debug
        self.debug_data = debug_data
        self.clients = []
        Thread.__init__(self)
        #self.setDaemon(True) 

    # run by the Thread object
    def run(self):
        if self.debug:
            print(datetime.now(), 'SERVER Starting...', '\n')

        self.listen()

    def listen(self):
        # create an instance of socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to its host and port
        self.sock.bind((self.host, self.port))
        if self.debug:
            print(datetime.now(), 'SERVER Socket Bound', self.host, self.port, '\n')

        # start listening for a client
        self.sock.listen(5)
        if self.debug:
            print(datetime.now(), 'SERVER Listening...', '\n')
        
        while True:
            # get the client object and address
            client, address = self.sock.accept()

            # add client to list
            self.clients.append(client)

            # set a timeout
            client.settimeout(self.timeout)

            if self.debug:
                print(datetime.now(), 'CLIENT Connected', client, '\n')

            if self.on_connected_callback:
                self.on_connected_callback(client, address)

            # start a thread to listen to the client
            Thread(
                target=self.listen_to_client,
                args=(client, address, self.decode_json, self.on_receive_callback, self.on_disconnected_callback),
                daemon = True
            ).start()

    def listen_to_client(self, client, address, decode_json, on_receive_callback, on_disconnected_callback):
        # set a buffer size ( could be 2048 or 4096 / power of 2 )
        size = 1024*1024
        while True:
            try:
                d = client.recv(size)
                if d:
                    if self.debug:
                        print(datetime.now(), 'CLIENT Data Received', address)
                        print("length:",len(d))
                        print(d)

                    if on_receive_callback:
                        try:
                            on_receive_callback(client, address, d)
                        except Exception as e:
                            if self.debug:
                                print(datetime.now(), 'CLIENT Receive Callback Failed:', d, '\n', e, '\n')
                else:
                    raise ValueError('CLIENT Disconnected')
                    

            except Exception as e:
                if self.debug:
                    print(datetime.now(), e, client, '\n')

                client.close()
                client_index = self.clients.index(client)
                
                self.clients.pop(client_index)

                if on_disconnected_callback:
                    try:
                        on_disconnected_callback(client, address)
                    except Exception as e:
                        print('on_close_callback failed\n', e, '\n')
                return False
    
    def send_all(self, cmd, data):
        for client in self.clients:
            # send each client a message
            res = {
                'cmd': cmd,
                'data': data
            }
            response = dumps(res, default=str)
            # add new line chr for TD
            response += '\n'
            client.send(response.encode('utf-8'))


def example_on_receive_callback(client, address, data):
    res = data
    response = dumps(res, default=str)
    # add new line chr for TD
    response += '\n'
    #print(response)
    client.send(response.encode('utf-8'))
    return

def example_on_connected_callback(client, address):
    return

def example_on_disconnected_callback(client, address):
    return


if __name__ == "__main__":
    TCPThreadedServer(
        '127.0.0.1',
        8008,
        timeout=86400,
        decode_json=True,
        on_connected_callback=example_on_connected_callback,
        on_receive_callback=example_on_receive_callback,
        on_disconnected_callback=example_on_disconnected_callback,
        debug=True,
    ).start()