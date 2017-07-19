import sys
import socket

host = "35.176.144.147"
port = 54678

sock = socket.socket()

sock.connect((host, port))
sock.send("(4.4, -5.9, -6.8)(5.6, -2.1, -8.0)")
print "sent fake vector data!"
sock.close()
