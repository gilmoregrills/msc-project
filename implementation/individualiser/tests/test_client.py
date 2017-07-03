import sys
import socket

host = socket.gethostname()
port = 8080

sock = socket.socket()

sock.connect((host, port))
sock.send("hrtf pls")
returned = sock.recv(4096)
print returned
sock.close()
