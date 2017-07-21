import sys
import socket as socket
import select
import lmdb_interface as lmdb
import simplejson as json
import individualiser
import time
import os

# Main individualiser process
# should be running before the frontend
# frontend should ping both ports on 
# awake/start to get a generalised HRTF
# and test the process

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    logdir = "logs/"+time.strftime("%d-%m-%Y")+"/"
    if not os.path.exists(logdir):
        print "creating log directory"
        os.makedirs(logdir)
    logfname = logdir+"log.json"
    if not os.path.exists(logfname):
        print "creating log file"
        logfile = open(logfname, "w")
        logfile.write(json.dumps({'logs':[]}, indent=4, sort_keys=True))
        logfile.close()
    lmdb.open()# there should be a scenario under which this is closed, too
    print "Individualiser Running!"
    in_port = 54678
    out_port = 54679
    if "DESKTOP" not in socket.gethostname():
        host = "ec2-35-176-144-147.eu-west-2.compute.amazonaws.com"
    else:
        host = "127.0.0.1"
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
            if s.getsockname()[1] == in_port:
                data = conn.recv(4096)# the vector data I will feed the algo
                # read received data into memory then close the 
                # connection
                #print "vector data: ", data
                conn.close()
                individualiser.individualiser(data)
                # trigger algo function, somehow make it non-blocking?
                # spawn a new thread so requests like the one below can still
                # come in?
            elif s.getsockname()[1] == out_port:
                print "received a request for an hrtf, sending from lmdb..."
                # fetch latest custom HRTF from lmdb, it'll always be in the
                # same place as old ones get archived elsewhere
                latest_hrir = lmdb.fetch("custom_hrir")
                print "transforming to json to send"
                latest_hrir = latest_hrir.tolist()
                print "hrtf fetched, shape: ", 
                print len(latest_hrir), len(latest_hrir[0]), len(latest_hrir[0][0]), len(latest_hrir[0][0][0])
                output = json.dumps(latest_hrir)
                size = sys.getsizeof(output)
                print "size of size value: ", sys.getsizeof(size)
                print "json ready, size: ", size, " sending..."
                conn.send(str(size))
                conn.sendall(output)
                conn.close()
                print "sent!"
            else:
                print "error"
                conn.close()

    lmdb.close()

if __name__ == "__main__":
    main()
