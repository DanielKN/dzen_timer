# Echo client program
import socket
import sys

HOST = 'localhost'
# TODO: Get port to pull from a setting file, shared with time_controller. 
PORT = 49152    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(bytes(sys.argv[1].encode('utf-8')))
    s.close()
