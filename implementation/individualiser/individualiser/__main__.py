import sys
import socket as socket
import select
import lmdb_interface as lmdb
import json

# Main individualiser process
# should be running before the frontend
# frontend should ping both ports on 
# awake/start to get a generalised HRTF
# and test the process

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    # should potentially open connection to lmdb here
    lmdb.open()# there should be a scenario under which this is closed, too
    print "Individualiser Running!"
    in_port = 8881
    out_port = 8080
    host = "127.0.0.1"# hardcoded to work on windows + linux
    print "the host is: ", host
    sock_in = socket.socket()
    sock_out = socket.socket()
    sock_in.bind((host, in_port))
    sock_out.bind((host, out_port))
    
    sock_out.listen(5)
    sock_in.listen(5)
    print "Sockets listening on their respective ports"
    
    sockets = [sock_out, sock_in]
    while True:
        ready_sockets,_,_ = select.select(sockets, [], [])
        for s in ready_sockets:
            conn, addr = s.accept()
            print "received connection from:", addr, "into", s.getsockname()
            if s.getsockname()[1] == 8881:
                data = conn.recv(4096)# the vector data I will feed the algo
                print "receiving localisation vector, triggering algorithm..."
                print "vector data: ", data
                conn.close()
                # read received data into memory then close the 
                # connection
                # trigger algo functions, somehow make it non-blocking?
                # spawn a new thread so requests like the one below can still
                # come in?
            elif s.getsockname()[1] == 8080:
                print "received a request for an hrtf, sending from lmdb..."
                # fetch latest custom HRTF from lmdb, it'll always be in the
                # same place as old ones get archived
                latest_hrtf = lmdb.fetch("custom_hrtf")
                print "transforming to json to send"
                latest_hrtf = latest_hrtf.tolist()
                output = json.dumps(latest_hrtf)
                print output
                print "json ready, size: ", sys.getsizeof(output), " sending..."
                conn.send(output)
                print "sent!"
                conn.close()
            else:
                print "error"
                conn.close()

    # should potentially close the connection to lmdb here

if __name__ == "__main__":
    main()
