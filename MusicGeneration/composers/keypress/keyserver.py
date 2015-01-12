"""This "in-process" socket server receives notifications of key
events and publishes them as events.

> s = start_server()
> t = TestClient()
> s.register_key(t)
> t.send("A")
'A'
"""

import sys
from collections import namedtuple
import socketserver
from .. import EventSender, EventReceiver
import threading
import socket

__thread = None
__server = None

def start_server(host="localhost", port=8888):
    global __thread, __server
    __server = KeystrokeServer((host, port), Handler)
    __thread = threading.Thread(target=__server.serve_forever)
    __thread.daemon = True
    __thread.start()
    return __server

def stop_server():
    global __thread, __server
    __server.shutdown()

@EventSender("key")
class KeystrokeServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        if data:
            self.server.send_key_event(data.decode("ASCII"))
@EventReceiver("key", "do_key")
class TestClient:
    def __init__(self, host="localhost", port=8888):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__host = host
        self.__port = port

    def do_key(self, key):
        print(key)

    def send(self, char):
        self.__sock.sendto(bytes(char, "ASCII"), (self.__host, self.__port))