import sys
import individualiser as ind
import socket as socket
import select
import lmdb_interface as lmdb
import pca_functions as pca
import utility_functions as util

def main(args=None):
    """Module's main routine:"""
    if args is None:
        args = sys.argv[1:]
    print "This routine should handle the general running of the individualiser"
    in_port = 8888
    out_port = 8080
    host = socket.gethostname()
    sock_in = socket.socket()
    sock_out = socket.socket()
    sock_in.bind((host, in_port))
    sock_out.bind((host, out_port))
    
    sock_out.listen(5)
    sock_in.listen(5)
    
    sockets = [sock_out, sock_in]
    while True:
        ready_sockets,_,_ = select.select(sockets, [], [])
        print ready_sockets
        for s in ready_sockets:
            conn, addr = s.accept()
            data = conn.recv(1024)
            print "received:", addr
            if s.getsockname()[1] == 8888:
                print "receiving localisation vector, triggering algorithm..."
                print "port number: ", s.getsockname()[1]
            elif s.getsockname()[1] == 8080:
                print "received a request for an hrtf, sending from lmdb..."
                print "port number: ", s.getsockname()[1]
            else:
                print "error"

if __name__ == "__main__":
    main()
