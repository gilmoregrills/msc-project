import sys
import socket

host = "35.176.144.147"
port = 54678

sock = socket.socket()

sock.connect((host, port))
sock.send("(-0.6, 9.9, -0.9)(6.4, 4.2, 6.4)")
print "sent fake vector data!"
sock.close()
