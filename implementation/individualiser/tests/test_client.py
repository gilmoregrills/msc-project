import sys
import socket

host = socket.gethostname()
send_port = 8888
req_port = 8080

send_sock = socket.socket()
req_sock = socket.socket()

send_sock.connect((host, send_port))
send_sock.close()

req_sock.connect((host, req_port))
req_sock.close()
