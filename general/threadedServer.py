# -*- coding: utf-8 -*-
import SocketServer as Ss
import threading

class ThreadedTCPRequestHandler(Ss.BaseRequestHandler):
    def handle(self):
        pass

class ThreadedUDPRequestHandler(Ss.BaseRequestHandler):
    def handle(self):
        pass

class ThreadedTCPServer(Ss.ThreadingMixIn, Ss.TCPServer):
    pass

class ThreadedUDPServer(Ss.ThreadingMixIn, Ss.UDPServer):
    pass

if __name__ == '__main__':
    HOST, PORT = 'localhost', 8989
    udpsv = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    tcpsv = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    udp_thread = threading.Thread(target=udpsv.serve_forever)
    tcp_thread = threading.Thread(target=tcpsv.serve_forever)
    udp_thread.start()
    tcp_thread.start()
    print "udp server run in thread:", udp_thread.getName()
    print "tcp server run in thread:", tcp_thread.getName()
