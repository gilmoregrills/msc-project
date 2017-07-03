import sys
import socket

host = socket.gethostname()
port = 8888

sock = socket.socket()

sock.connect((host, port))
sock.send("[example vector data from the client]")
sock.close()
